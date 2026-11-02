#!/usr/bin/env python3
"""Desenha a área segura vertical sobre um quadro, uma folha de quadros ou um vídeo.

Zona proibida em vermelho: topo 250, base 480, esquerda 80 e direita 140, medidas
para 1080x1920 e aplicadas por proporção em outros tamanhos 9:16. Linhas amarelas:
faixa da linha de base da legenda (y 1150 a 1300). Com --anuncio, linhas ciano
mostram o limite recomendado pela Meta para anúncios (y 269 e y 1248).

Exemplos:
  python area_segura.py video.mp4 --t 3.5
  python area_segura.py video.mp4 --folha --cada 2 --colunas 6
  python area_segura.py video.mp4 --video --anuncio

Precisa de ffmpeg e ffprobe no PATH. Só biblioteca padrão.
"""
import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path


def sair(msg, codigo=1):
    print(msg, file=sys.stderr)
    sys.exit(codigo)


def sonda(video, *args):
    r = subprocess.run(["ffprobe", "-v", "error", *args, "-of", "csv=p=0", str(video)],
                       capture_output=True, text=True)
    if r.returncode or not r.stdout.strip():
        sair(f"Não consegui ler o vídeo {video}: {r.stderr.strip() or 'sem trilha de vídeo'}", 2)
    return r.stdout.strip().split(",")


def filtro(anuncio):
    caixas = [
        "x=0:y=0:w=iw:h=ih*250/1920:color=red@0.35:t=fill",
        "x=0:y=ih*1440/1920:w=iw:h=ih*480/1920:color=red@0.35:t=fill",
        "x=0:y=0:w=iw*80/1080:h=ih:color=red@0.35:t=fill",
        "x=iw*940/1080:y=0:w=iw*140/1080:h=ih:color=red@0.35:t=fill",
        "x=0:y=ih*1150/1920:w=iw:h=3:color=yellow@0.9:t=fill",
        "x=0:y=ih*1300/1920:w=iw:h=3:color=yellow@0.9:t=fill",
    ]
    if anuncio:
        caixas += ["x=0:y=ih*269/1920:w=iw:h=3:color=cyan@0.9:t=fill",
                   "x=0:y=ih*1248/1920:w=iw:h=3:color=cyan@0.9:t=fill"]
    return ",".join("drawbox=" + c for c in caixas)


def main():
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Desenha a área segura vertical sobre um quadro, folha ou vídeo.")
    ap.add_argument("video", help="vídeo vertical 9:16")
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--folha", action="store_true", help="folha de quadros com a área desenhada")
    modo.add_argument("--video", action="store_true", dest="como_video", help="vídeo inteiro com a área (sem áudio)")
    ap.add_argument("--t", type=float, default=0.0, help="instante do quadro, em segundos (padrão 0)")
    ap.add_argument("--cada", type=float, default=2.0, help="folha: um quadro a cada N segundos (padrão 2)")
    ap.add_argument("--colunas", type=int, default=6, help="folha: colunas (padrão 6)")
    ap.add_argument("--largura", type=int, default=180, help="folha: largura de cada quadro (padrão 180)")
    ap.add_argument("--anuncio", action="store_true", help="marca também o limite recomendado pela Meta")
    ap.add_argument("--saida", help="arquivo de saída (padrão: ao lado do vídeo)")
    ap.add_argument("--sobrescrever", action="store_true", help="permite sobrescrever a saída")
    a = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sair("ffmpeg e ffprobe não estão no PATH. Instale o FFmpeg (https://ffmpeg.org/download.html) e tente de novo.", 2)
    video = Path(a.video)
    if not video.is_file():
        sair(f"Não achei o vídeo: {video}", 2)
    w, h = (int(x) for x in sonda(video, "-select_streams", "v:0", "-show_entries", "stream=width,height")[:2])
    if abs(w / h - 9 / 16) > 0.03:
        sair(f"O vídeo tem {w}x{h}. A régua é para vertical 9:16. Para horizontal use margem de 5% para o motion e 10% para o texto.")
    if a.cada <= 0 or a.colunas < 1 or a.largura < 16:
        sair("Valores inválidos em --cada, --colunas ou --largura.")

    sufixo = ".mp4" if a.como_video else ".png"
    nome = "_area" if not a.folha else "_folha"
    saida = Path(a.saida) if a.saida else video.with_name(video.stem + nome + sufixo)
    if saida.exists() and not a.sobrescrever:
        sair(f"{saida} já existe. Use --saida outro.png ou --sobrescrever.")

    vf = filtro(a.anuncio)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if a.como_video:
        cmd += ["-i", str(video), "-vf", vf, "-an", "-pix_fmt", "yuv420p"]
    elif a.folha:
        try:
            duracao = float(sonda(video, "-show_entries", "format=duration")[0])
        except ValueError:
            sair("Não consegui medir a duração do vídeo.", 2)
        quadros = max(1, math.ceil(duracao / a.cada))
        linhas = min(10, max(1, math.ceil(quadros / a.colunas)))
        cmd += ["-i", str(video), "-vf", f"{vf},fps=1/{a.cada},scale={a.largura}:-1,tile={a.colunas}x{linhas}", "-frames:v", "1"]
    else:
        cmd += ["-ss", str(a.t), "-i", str(video), "-frames:v", "1", "-vf", vf]
    cmd.append(str(saida))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not saida.is_file():
        sair(f"O ffmpeg falhou: {r.stderr.strip()}", 2)
    print(f"Gerado: {saida}")


if __name__ == "__main__":
    main()
