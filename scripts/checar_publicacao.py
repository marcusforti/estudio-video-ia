#!/usr/bin/env python3
"""Procura dado que não pode ir a público nos arquivos do repositório e do site.

Uso: python scripts/checar_publicacao.py [--termos ARQUIVO] [PASTAS...]
O arquivo de termos é uma lista privada, um regex por linha, fora do git.
Sai com código 1 quando acha algo.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEXTO = {".md", ".py", ".html", ".css", ".js", ".json", ".ps1", ".sh", ".txt", ".jsonc", ".svg", ".yaml", ".yml"}

PADROES = {
    "caminho Windows": r"(?i)(?<![\w/\\])[a-z]:(?:\\{1,2}|/)[\w$.\- ]",
    "caminho de usuário": r"(?i)(?:[a-z]:(?:\\{1,2}|/)|/mnt/[a-z]/|/[a-z]/|/)(?:Users|home)(?:\\{1,2}|/)(?!(?:user|usuario|seu|voce|you|name|ubuntu|runner|root)\b)[\w.-]+",
    "e-mail": r"[\w.+-]+@(?:[\w-]+\.)+[A-Za-z]{2,}\b",
    "telefone BR": r"(?<!\d)(?:\+?55[\s.-]?)?\(?\d{2}\)?[\s.-]?9[\s.-]?\d{4}[\s.-]?\d{4}(?!\d)",
    "JID WhatsApp": r"\b\d{8,}(?:-\d+)?@(?:s\.whatsapp\.net|c\.us|g\.us|lid)\b|\b120363\d{9,}\b",
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "chave": r"\b(?:sk-[A-Za-z0-9_-]{16,}|sk_[A-Za-z0-9]{20,}|gh[oprsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|hf_[A-Za-z0-9]{20,}|r8_[A-Za-z0-9]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,})\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bBearer\s+[A-Za-z0-9._~+/-]{20,}",
    "segredo atribuído": r"""(?i)[\w.-]*(?<![a-z])(?:api[_-]?key|token|secret|senha|password|passwd)(?![a-z])[\w.-]*["']?\s*[:=]\s*["']?[A-Za-z0-9_\-/+=.]{20,}""",
    "ssh/scp com host": r"(?i)\b(?:ssh|scp|sftp|rsync)\b[^\n]*\b[\w.-]+@(?:ssh\d*\.vast\.ai|proxy\d*\.vast\.ai|(?:\d{1,3}\.){3}\d{1,3})\b",
    "host vast": r"(?i)\b(?:ssh|proxy)\d*\.vast\.ai\b",
    "hex de 64": r"\b[0-9a-f]{64}\b",
    "variável do cofre": r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*__[A-Z0-9]+(?:_[A-Z0-9]+)*\b",
}
PERMITIDOS = {
    "e-mail": re.compile(r"^(?:usuario|voce|seu|exemplo|nome|email)@|@example\.(?:com|org)$|^noreply@anthropic\.com$"),
    "IP": re.compile(r"^(?:127\.0\.0\.1|0\.0\.0\.0|\d\.\d\.\d\.\d)$"),
}
NOMES_TEXTO = {".gitignore", ".gitattributes", ".graphifyignore", "LICENSE"}

def arquivos(pastas):
    r = subprocess.run(
        ["git", "ls-files", "-z", "-co", "--exclude-standard", *pastas],
        cwd=RAIZ, capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        sys.exit("ERRO do git: " + r.stderr.strip())
    itens = [i for i in r.stdout.split("\0") if i]
    return [RAIZ / i for i in itens if Path(i).suffix.lower() in TEXTO or Path(i).name in NOMES_TEXTO]


def arquivos_de_pasta(pasta):
    return [p for p in pasta.rglob("*") if p.is_file() and (p.suffix.lower() in TEXTO or p.name in NOMES_TEXTO)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--termos", type=Path, default=RAIZ / ".deny.txt")
    parser.add_argument("--dist", action="store_true", help="confere o site gerado em vez dos arquivos do git")
    parser.add_argument("pastas", nargs="*", default=[])
    args = parser.parse_args()

    regras = [(nome, re.compile(p)) for nome, p in PADROES.items()]
    if not args.termos.exists():
        sys.exit(f"ERRO: lista de termos privados ausente ({args.termos}). Sem ela a checagem de nomes não roda.")
    for linha in args.termos.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            regras.append((f"termo privado: {linha}", re.compile(linha, re.I)))
    lista = arquivos_de_pasta(RAIZ / "site" / "dist") if args.dist else arquivos(args.pastas)

    achados = 0
    for caminho in lista:
        if caminho.name == "checar_publicacao.py":
            continue
        try:
            linhas = caminho.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            print(f"AVISO: não decodifiquei {caminho.relative_to(RAIZ)}; confira à mão")
            achados += 1
            continue
        for numero, linha in enumerate(linhas, 1):
            for nome, regra in regras:
                for achado in regra.finditer(linha):
                    if PERMITIDOS.get(nome) and PERMITIDOS[nome].search(achado.group(0)):
                        continue
                    achados += 1
                    trecho = linha[max(0, achado.start() - 40): achado.end() + 40].strip()
                    print(f"{caminho.relative_to(RAIZ)}:{numero} [{nome}] {trecho}")
    print(f"{achados} ocorrências" if achados else "Nada a remover.")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main())
