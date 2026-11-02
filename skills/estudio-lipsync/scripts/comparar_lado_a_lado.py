#!/usr/bin/env python3
"""Monta um vídeo com o original e os resultados lado a lado, para olhar a boca com som.

Os painéis aparecem da esquerda para a direita na ordem dada: original, resultado 1, resultado 2...
O script imprime essa ordem. Não escreve texto no vídeo (evita depender de fontes).

Exemplo:
  python comparar_lado_a_lado.py --original teste/original_trecho.mp4 \
      --resultado saida_modeloA.mp4 saida_modeloB.mp4 --saida comparacao.mp4
"""
import argparse
import os
import shutil
import subprocess
import sys


def main() -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Compara original e resultados de lip sync lado a lado.")
    ap.add_argument("--original", required=True, help="trecho original")
    ap.add_argument("--resultado", nargs="+", required=True, help="um ou mais vídeos gerados, na ordem desejada")
    ap.add_argument("--saida", required=True, help="arquivo .mp4 de saída")
    ap.add_argument("--altura", type=int, default=540, help="altura de cada painel (padrão 540)")
    ap.add_argument("--fps", type=int, default=25, help="fps do vídeo comparado (padrão 25)")
    ap.add_argument("--audio-de", type=int, default=1,
                    help="painel cujo áudio será usado: 0 = original, 1 = primeiro resultado (padrão 1)")
    args = ap.parse_args()

    entradas = [args.original] + args.resultado
    for caminho in entradas:
        if not os.path.isfile(caminho):
            print(f"ERRO: arquivo não existe: {caminho}", file=sys.stderr)
            return 1
    if shutil.which("ffmpeg") is None:
        print("ERRO: ffmpeg não encontrado no PATH.", file=sys.stderr)
        return 3
    if not 0 <= args.audio_de < len(entradas):
        print(f"ERRO: --audio-de deve ficar entre 0 e {len(entradas) - 1}.", file=sys.stderr)
        return 1

    comando = ["ffmpeg", "-y", "-v", "error"]
    for caminho in entradas:
        comando += ["-i", caminho]
    partes = [f"[{i}:v]fps={args.fps},scale=-2:{args.altura},setsar=1[v{i}]"
              for i in range(len(entradas))]
    rotulos = "".join(f"[v{i}]" for i in range(len(entradas)))
    filtro = ";".join(partes) + f";{rotulos}hstack=inputs={len(entradas)}:shortest=1[v]"
    comando += ["-filter_complex", filtro, "-map", "[v]", "-map", f"{args.audio_de}:a?",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-shortest", args.saida]
    saida = subprocess.run(comando, capture_output=True, encoding="utf-8", errors="replace", check=False)
    if saida.returncode != 0:
        print("ERRO do ffmpeg:\n" + "\n".join(saida.stderr.strip().splitlines()[-8:]), file=sys.stderr)
        return 1

    print(f"Criado: {args.saida}")
    print("Painéis, da esquerda para a direita:")
    for i, caminho in enumerate(entradas):
        marca = " (áudio deste painel)" if i == args.audio_de else ""
        print(f"  {i}: {'original' if i == 0 else 'resultado'} -> {caminho}{marca}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
