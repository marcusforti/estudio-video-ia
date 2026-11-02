#!/usr/bin/env python3
"""Confere um arquivo baixado da máquina alugada antes de destruí-la.

Uso:
  python conferir_download.py final.mp4 --md5 "HASH_CALCULADO_NA_VM" --duracao 150 --midia
Na VM:      md5sum /caminho/final.mp4
No seu PC:  este script calcula o md5 e compara.
Código de saída: 0 = tudo passou, 1 = alguma checagem falhou, 3 = ferramenta ausente.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys


def md5_do_arquivo(caminho: str) -> str:
    h = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def sondar(caminho: str):
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
         "-of", "json", caminho],
        capture_output=True, encoding="utf-8", errors="replace", check=False)
    if saida.returncode != 0:
        return None
    dados = json.loads(saida.stdout or "{}")
    tipos = {s.get("codec_type") for s in dados.get("streams", [])}
    duracao = float(dados.get("format", {}).get("duration", 0) or 0)
    return duracao, tipos


def main() -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Confere tamanho, md5 e duração de um download.")
    ap.add_argument("arquivo")
    ap.add_argument("--md5", help="md5 calculado na máquina remota (aceita a saída inteira do md5sum)")
    ap.add_argument("--duracao", type=float, help="duração esperada, em segundos")
    ap.add_argument("--tolerancia", type=float, default=0.5, help="tolerância da duração, em s (padrão 0.5)")
    ap.add_argument("--min-bytes", type=int, default=1, help="tamanho mínimo aceito (padrão 1)")
    ap.add_argument("--midia", action="store_true", help="exige que o ffprobe leia vídeo ou áudio")
    args = ap.parse_args()

    falhas = 0

    def resultado(ok: bool, texto: str) -> None:
        nonlocal falhas
        print(("PASSOU  " if ok else "FALHOU  ") + texto)
        falhas += 0 if ok else 1

    if not os.path.isfile(args.arquivo):
        print(f"FALHOU  arquivo não existe: {args.arquivo}")
        return 1
    tamanho = os.path.getsize(args.arquivo)
    resultado(tamanho >= args.min_bytes, f"tamanho {tamanho} bytes (mínimo {args.min_bytes})")

    calculado = md5_do_arquivo(args.arquivo)
    if args.md5:
        esperado = args.md5.strip().split()[0].lower()
        resultado(calculado == esperado, f"md5 local {calculado} / remoto {esperado}")
    else:
        print(f"INFO    md5 local {calculado} (compare com `md5sum` na máquina)")

    if args.midia or args.duracao is not None:
        if shutil.which("ffprobe") is None:
            print("ERRO: ffprobe não encontrado no PATH.", file=sys.stderr)
            return 3
        lido = sondar(args.arquivo)
        if lido is None:
            resultado(False, "o ffprobe não conseguiu ler o arquivo (download truncado?)")
        else:
            duracao, tipos = lido
            resultado(bool(tipos & {"video", "audio"}), f"fluxos encontrados: {sorted(t for t in tipos if t)}")
            if args.duracao is not None:
                resultado(abs(duracao - args.duracao) <= args.tolerancia,
                          f"duração {duracao:.2f} s (esperada {args.duracao:g} s, tolerância {args.tolerancia:g} s)")
            else:
                print(f"INFO    duração {duracao:.2f} s")

    if falhas:
        print(f"{falhas} checagem(ns) falharam: NÃO destrua a máquina ainda. Baixe de novo ou retome o envio.")
        return 1
    if not args.md5:
        print("AVISO: sem --md5 não há comparação com a máquina. NÃO destrua ainda; rode de novo com --md5.")
        return 1
    print("Tudo conferido. Pode destruir a máquina.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
