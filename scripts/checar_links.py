#!/usr/bin/env python3
"""Confere os links do site gerado em site/dist.

Uso: python scripts/checar_links.py [--externos]
Internos: arquivo e âncora precisam existir. Externos: faz requisição HTTP e lista o que falhou.
"""
import argparse
import concurrent.futures as cf
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "site" / "dist"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def paginas():
    return sorted(DIST.rglob("*.html"))


def alvo_interno(pagina, href):
    caminho, _, ancora = href.partition("#")
    if not caminho:
        destino = pagina
    elif caminho.startswith("/"):
        destino = DIST / caminho.lstrip("/")
    else:
        destino = pagina.parent / caminho
    if destino.is_dir():
        destino = destino / "index.html"
    return destino, ancora


def checar_internos():
    ids = {}
    erros = []
    for pagina in paginas():
        texto = pagina.read_text(encoding="utf-8")
        for href in re.findall(r'(?:href|src)="([^"]+)"', texto):
            if re.match(r"^(https?:|mailto:|data:|#$)", href):
                continue
            destino, ancora = alvo_interno(pagina, href)
            if not destino.exists():
                erros.append(f"{pagina.relative_to(DIST)} -> {href}: arquivo não existe")
                continue
            if ancora and destino.suffix == ".html":
                if destino not in ids:
                    ids[destino] = set(re.findall(r'\bid="([^"]+)"', destino.read_text(encoding="utf-8")))
                if ancora not in ids[destino]:
                    erros.append(f"{pagina.relative_to(DIST)} -> {href}: âncora não existe")
    return erros


def testar(url):
    for metodo in ("HEAD", "GET"):
        try:
            pedido = urllib.request.Request(url, method=metodo, headers=HEADERS)
            with urllib.request.urlopen(pedido, timeout=25) as resposta:
                return url, resposta.status
        except urllib.error.HTTPError as erro:
            codigo = erro.code
            if metodo == "GET":
                return url, codigo
        except Exception as erro:
            if metodo == "GET":
                return url, f"{type(erro).__name__}"
    return url, "sem resposta"


def checar_externos():
    urls = set()
    for pagina in paginas():
        if pagina.name == "grafo-interativo.html":
            continue
        urls.update(re.findall(r'href="(https?://[^"]+)"', pagina.read_text(encoding="utf-8")))
    urls = sorted(u.replace("&amp;", "&") for u in urls if "//estudio-video-ia." not in u)
    print(f"{len(urls)} links externos")
    falhas = []
    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        for url, estado in executor.map(testar, urls):
            if estado != 200:
                falhas.append((estado, url))
    return sorted(falhas, key=lambda f: str(f[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--externos", action="store_true")
    args = parser.parse_args()
    erros = checar_internos()
    for erro in erros:
        print(erro)
    print(f"{len(erros)} links internos quebrados")
    if args.externos:
        falhas = checar_externos()
        for estado, url in falhas:
            print(f"{estado}  {url}")
        print(f"{len(falhas)} links externos sem 200")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
