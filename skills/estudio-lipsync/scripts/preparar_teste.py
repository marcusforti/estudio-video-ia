#!/usr/bin/env python3
"""Prepara o teste de lip sync de 10 a 15 s no seu pior plano.

Cria, numa pasta de saída:
  original_trecho.mp4   o trecho original, com áudio, para comparar depois
  base_25fps.mp4        o mesmo trecho em 25 fps constantes, SEM áudio, com a folga no fim
                        (é o vídeo-base que você entrega aos modelos)
  voz_16k_mono.wav      o áudio do teste em 16 kHz mono, com silêncio no fim

Sem --audio, usa o áudio do próprio trecho (serve para ver se o modelo reproduz a boca).
Com --audio, usa o seu áudio novo a partir de --inicio-audio.

Exemplo:
  python preparar_teste.py --video bruto.mp4 --inicio 83 --duracao 12 --audio voz_nova.wav --saida teste
"""
import argparse
import json
import os
import shutil
import subprocess
import sys


def rodar(comando: list[str]) -> None:
    saida = subprocess.run(comando, capture_output=True, encoding="utf-8", errors="replace", check=False)
    if saida.returncode != 0:
        cauda = "\n".join(saida.stderr.strip().splitlines()[-8:])
        raise SystemExit(f"ERRO ao rodar {comando[0]}:\n{cauda}")


def resumo(caminho: str) -> str:
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", caminho],
        capture_output=True, encoding="utf-8", errors="replace", check=False)
    dados = json.loads(saida.stdout or "{}")
    duracao = float(dados.get("format", {}).get("duration", 0) or 0)
    partes = [f"{duracao:.2f} s"]
    for fluxo in dados.get("streams", []):
        if fluxo.get("codec_type") == "video":
            num, _, den = str(fluxo.get("r_frame_rate", "0/1")).partition("/")
            fps = float(num) / float(den or 1) if float(den or 1) else 0.0
            partes.append(f"{fluxo.get('width')}x{fluxo.get('height')} a {fps:g} fps")
        elif fluxo.get("codec_type") == "audio":
            partes.append("com áudio")
    return ", ".join(partes)


def main() -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Prepara o trecho de teste de lip sync.")
    ap.add_argument("--video", required=True, help="vídeo bruto que contém o seu pior plano")
    ap.add_argument("--inicio", default="0", help="início do trecho: segundos (83) ou HH:MM:SS (00:01:23)")
    ap.add_argument("--duracao", type=float, default=12.0, help="duração da fala em segundos (padrão 12)")
    ap.add_argument("--audio", help="áudio novo para o teste (opcional)")
    ap.add_argument("--inicio-audio", default="0", help="início dentro do áudio novo (padrão 0)")
    ap.add_argument("--folga", type=float, default=0.5, help="segundos extras de vídeo e de silêncio no fim (padrão 0.5)")
    ap.add_argument("--fps", type=int, default=25, help="fps constante do vídeo-base (padrão 25)")
    ap.add_argument("--saida", required=True, help="pasta de saída (criada se não existir)")
    args = ap.parse_args()

    for ferramenta in ("ffmpeg", "ffprobe"):
        if shutil.which(ferramenta) is None:
            print(f"ERRO: {ferramenta} não encontrado no PATH.", file=sys.stderr)
            return 3
    for caminho in filter(None, (args.video, args.audio)):
        if not os.path.isfile(caminho):
            print(f"ERRO: arquivo não existe: {caminho}", file=sys.stderr)
            return 1
    if not 3 <= args.duracao <= 20:
        print("Aviso: o teste foi pensado para 10 a 15 s; fora de 3 a 20 s ele perde o sentido.")

    os.makedirs(args.saida, exist_ok=True)
    original = os.path.join(args.saida, "original_trecho.mp4")
    base = os.path.join(args.saida, f"base_{args.fps}fps.mp4")
    voz = os.path.join(args.saida, "voz_16k_mono.wav")
    longa = f"{args.duracao + args.folga:g}"
    curta = f"{args.duracao:g}"

    rodar(["ffmpeg", "-y", "-v", "error", "-ss", args.inicio, "-t", curta, "-i", args.video,
           "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", original])
    rodar(["ffmpeg", "-y", "-v", "error", "-ss", args.inicio, "-t", longa, "-i", args.video,
           "-an", "-vf", f"fps={args.fps}", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
           "-pix_fmt", "yuv420p", base])
    origem_audio = (args.audio, args.inicio_audio) if args.audio else (args.video, args.inicio)
    rodar(["ffmpeg", "-y", "-v", "error", "-ss", origem_audio[1], "-t", curta, "-i", origem_audio[0],
           "-vn", "-ac", "1", "-ar", "16000", "-af", f"apad=pad_dur={args.folga:g}", voz])

    print("Pronto. Arquivos criados:")
    for caminho in (original, base, voz):
        print(f"  {caminho}: {resumo(caminho)}")
    print("Entregue base + voz ao modelo ou ao serviço. Depois compare com comparar_lado_a_lado.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
