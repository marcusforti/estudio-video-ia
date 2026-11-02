#!/usr/bin/env python3
"""Busca referências de motion na coleção awesome-opus5-5-videos.

A coleção é um repositório público (MIT) com prompts e links de vídeos feitos
com Claude Opus 5.5. Cada vídeo e cada prompt pertence ao criador: use como
referência, credite o autor e não republique o prompt.

Exemplos:
  python buscar.py "dashboard numbers" --cat motion --com-video --n 5
  python buscar.py --ver SLUG
  python buscar.py --resumo

Onde fica a coleção: --base PASTA ou a variável de ambiente MOTION_REFS_DIR.
Só biblioteca padrão. Nunca altera a pasta da coleção.
"""
import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO = "https://github.com/yihui-dev/awesome-opus5-5-videos"
CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def limpar(texto):
    """Tira caracteres de controle (inclusive ESC) de texto de terceiros."""
    return CONTROLE.sub("", str(texto if texto is not None else ""))


def ensinar_clone(motivo):
    print(motivo, file=sys.stderr)
    print(
        "\nBaixe uma cópia da coleção (precisa do git):\n"
        f"  git clone {REPO}\n"
        "Depois aponte para a pasta clonada, de um destes jeitos:\n"
        "  python buscar.py --base CAMINHO/awesome-opus5-5-videos \"termos\"\n"
        "  PowerShell:    $env:MOTION_REFS_DIR = \"CAMINHO\\awesome-opus5-5-videos\"\n"
        "  macOS/Linux:   export MOTION_REFS_DIR=CAMINHO/awesome-opus5-5-videos\n"
        "Cada vídeo e cada prompt pertence ao criador: a cópia é só para você consultar.",
        file=sys.stderr,
    )
    sys.exit(2)


def carregar(base_arg):
    texto = base_arg or os.environ.get("MOTION_REFS_DIR")
    if not texto:
        ensinar_clone("Não sei onde está a coleção: use --base ou defina MOTION_REFS_DIR.")
    base = Path(texto).expanduser()
    if not (base / "data" / "videos.json").is_file() and (base / "awesome-opus5-5-videos" / "data" / "videos.json").is_file():
        base = base / "awesome-opus5-5-videos"
    arquivo = base / "data" / "videos.json"
    if not arquivo.is_file():
        ensinar_clone(f"Não achei data/videos.json dentro de: {base}")
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
        if not isinstance(dados, list):
            raise ValueError("o arquivo não é uma lista")
        dados = [v for v in dados if isinstance(v, dict) and v.get("slug")]
    except (OSError, ValueError) as erro:
        print(f"Não consegui ler {arquivo}: {erro}", file=sys.stderr)
        sys.exit(2)
    return base, dados


def tem_video(v):
    return bool(v.get("has_remake") or v.get("skillry_url"))


def titulo(base, v):
    """Primeira linha '# ' do prompts/<slug>.md; se faltar, o próprio slug."""
    slug = str(v["slug"])
    if not re.fullmatch(r"[\w][\w.-]*", slug) or ".." in slug:
        return limpar(slug)
    arquivo = base / "prompts" / f"{slug}.md"
    try:
        with arquivo.open(encoding="utf-8", errors="replace") as f:
            primeira = f.readline()
    except OSError:
        return limpar(slug)
    m = re.match(r"#\s+(.+)", primeira)
    return limpar(m.group(1).strip()) if m else limpar(slug)


def autor(v):
    a = limpar(v.get("author")).strip()
    return ("@" + a.lstrip("@")) if a else ""


def linhas_credito(v):
    saida = []
    a, post = autor(v), limpar(v.get("post_url")).strip()
    if a or post:
        saida.append("autor: " + (a or "(não informado)") + ("  post: " + post if post else ""))
    elif v.get("author_url"):
        saida.append("perfil: " + limpar(v["author_url"]))
    return saida


def selo(v):
    return "[vídeo]" if tem_video(v) else "[só post]"


def tags(v):
    t = v.get("tech_tags")
    return ", ".join(limpar(x) for x in t) if isinstance(t, list) else ""


def resumo(dados):
    cats = Counter(v.get("category", "?") for v in dados)
    com = Counter(v.get("category", "?") for v in dados if tem_video(v))
    n_video = sum(1 for v in dados if tem_video(v))
    print(f"Prompts: {len(dados)}")
    print(f"  com página de vídeo no Skillry (original e remake): {n_video}")
    print(f"  só com o link do post no X: {len(dados) - n_video}")
    print(f"  prompts parciais (o criador publicou só parte): {sum(1 for v in dados if v.get('prompt_partial'))}")
    print("Por categoria (total, com vídeo, só post):")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {limpar(c)}: {n}, {com[c]}, {n - com[c]}")


def ver(base, dados, slug):
    por_slug = {str(v["slug"]): v for v in dados}
    v = por_slug.get(slug) or next((x for k, x in por_slug.items() if k.lower() == slug.lower()), None)
    if v is None:
        print(f"Não existe o slug: {limpar(slug)}", file=sys.stderr)
        parecidos = difflib.get_close_matches(slug, list(por_slug), n=5, cutoff=0.5)
        if parecidos:
            print("Parecidos: " + ", ".join(limpar(p) for p in parecidos), file=sys.stderr)
        print("Para achar o slug, busque primeiro: python buscar.py \"termos\"", file=sys.stderr)
        sys.exit(1)
    print(f"{titulo(base, v)}  {selo(v)}")
    print(f"categoria: {limpar(v.get('category'))} | tags: {tags(v) or '-'}")
    for linha in linhas_credito(v) or ["autor e post: não constam na coleção; procure antes de creditar"]:
        print(linha)
    print("vídeo: " + (limpar(v.get("skillry_url")) if v.get("skillry_url") else "sem página no Skillry; veja o post"))
    if v.get("prompt_partial"):
        print("aviso: prompt parcial, o criador publicou só parte dele ou descreveu o resultado no post")
    print("\nPROMPT (cópia local; pertence ao criador, não republique):\n")
    print(limpar(v.get("prompt") or "(sem prompt)"))


def buscar(base, dados, termos, cat, so_video, n):
    termos = [palavra for t in termos for palavra in t.lower().split()]
    achados = []
    for v in dados:
        if cat and str(v.get("category")).lower() != cat.lower():
            continue
        if so_video and not tem_video(v):
            continue
        t = titulo(base, v)
        texto = " ".join([t, str(v.get("prompt") or ""), tags(v)]).lower()
        pontos = sum(texto.count(x) * (3 if x in t.lower() else 1) for x in termos) if termos else 1
        if pontos:
            achados.append((pontos + (0.5 if tem_video(v) else 0), t, v))
    achados.sort(key=lambda r: (-r[0], str(r[2]["slug"])))
    if not achados:
        print("Nenhum resultado. Tente termos em inglês (os prompts são em inglês), "
              "menos termos, ou tire --cat e --com-video.")
        return
    for i, (_, t, v) in enumerate(achados[:n], 1):
        print(f"{i}. {selo(v)} {t}")
        print(f"   {limpar(v.get('category'))} | {tags(v) or '-'} | slug={limpar(v['slug'])}"
              + ("  (prompt parcial)" if v.get("prompt_partial") else ""))
        for linha in linhas_credito(v):
            print("   " + linha)
        if v.get("skillry_url"):
            print("   vídeo: " + limpar(v["skillry_url"]))
        inicio = limpar(str(v.get("prompt") or "")[:200]).replace("\n", " ").strip()
        print(f"   prompt: {inicio}...\n")
    print(f"Mostrando {min(n, len(achados))} de {len(achados)}. Prompt completo: python buscar.py --ver SLUG")
    print("Credite o autor e o link do post; não republique o prompt.")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Busca referências de motion na coleção awesome-opus5-5-videos.")
    ap.add_argument("termos", nargs="*", help="palavras da busca (em inglês funciona melhor)")
    ap.add_argument("--base", help="pasta da coleção clonada (ou use MOTION_REFS_DIR)")
    ap.add_argument("--cat", help="filtra por categoria (motion, 3d, explainer, interactive)")
    ap.add_argument("--com-video", action="store_true", help="só entradas com página de vídeo")
    ap.add_argument("--n", type=int, default=8, help="quantos resultados mostrar (padrão 8)")
    ap.add_argument("--ver", metavar="SLUG", help="mostra o prompt completo de um slug")
    ap.add_argument("--resumo", action="store_true", help="conta a coleção por categoria")
    a = ap.parse_intermixed_args()
    base, dados = carregar(a.base)
    if a.resumo:
        return resumo(dados)
    if a.ver:
        return ver(base, dados, a.ver)
    categorias = sorted({str(v.get("category")).lower() for v in dados})
    if a.cat and a.cat.lower() not in categorias:
        print(f"Categoria desconhecida: {limpar(a.cat)}. Existem: {', '.join(limpar(c) for c in categorias)}", file=sys.stderr)
        sys.exit(1)
    buscar(base, dados, a.termos, a.cat, a.com_video, max(a.n, 1))


if __name__ == "__main__":
    main()
