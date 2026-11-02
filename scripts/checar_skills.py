#!/usr/bin/env python3
"""Confere as skills do repositório: frontmatter, arquivos citados e dependências.

Uso: python scripts/checar_skills.py
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = sorted(p for p in (RAIZ / "skills").iterdir() if (p / "SKILL.md").exists())
NOMES = {p.name for p in SKILLS}


def main():
    erros = []
    for pasta in SKILLS:
        texto = (pasta / "SKILL.md").read_text(encoding="utf-8")
        cabeca = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
        if not cabeca:
            erros.append(f"{pasta.name}: sem frontmatter")
            continue
        chaves = re.findall(r"^([a-z_-]+):", cabeca.group(1), re.M)
        if chaves[:2] != ["name", "description"] or len(chaves) != 2:
            erros.append(f"{pasta.name}: frontmatter com chaves {chaves}")
        nome = re.search(r"^name:\s*(.+)$", cabeca.group(1), re.M).group(1).strip()
        if nome != pasta.name:
            erros.append(f"{pasta.name}: name diferente da pasta ({nome})")
        descricao = re.search(r"^description:\s*(.+)$", cabeca.group(1), re.M).group(1)
        if len(descricao) > 1024:
            erros.append(f"{pasta.name}: descrição com {len(descricao)} caracteres")
        linhas = texto.count("\n")
        if linhas > 200:
            erros.append(f"{pasta.name}: SKILL.md com {linhas} linhas")
        for arquivo in pasta.rglob("*.md"):
            conteudo = arquivo.read_text(encoding="utf-8")
            relativo = arquivo.relative_to(pasta)
            for citado in set(re.findall(r"(?<![\w/-])((?:references|scripts)/[\w./-]+\.\w+)", conteudo)):
                if not (pasta / citado).exists():
                    erros.append(f"{pasta.name}/{relativo}: cita {citado}, que não existe")
            for outra in set(re.findall(r"\bestudio-[a-z-]+[a-z]\b", conteudo)):
                if outra not in NOMES and outra != "estudio-video-ia":
                    erros.append(f"{pasta.name}/{relativo}: cita skill {outra}, que não existe")
        for script in pasta.rglob("*.py"):
            saida = subprocess.run(
                [sys.executable, str(script), "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
            )
            if saida.returncode != 0:
                erros.append(f"{script.relative_to(RAIZ)}: --help saiu com {saida.returncode}")
    for erro in erros:
        print(erro)
    print(f"{len(SKILLS)} skills, {len(erros)} problemas")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
