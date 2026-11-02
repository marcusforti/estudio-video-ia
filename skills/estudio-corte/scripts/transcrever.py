#!/usr/bin/env python3
"""transcrever.py - transcreve um vídeo ou áudio por palavra, local, com faster-whisper.

Dependência OPCIONAL: faster-whisper (MIT, SYSTRAN). Só instale se for transcrever aqui:
    pip install faster-whisper
Na primeira vez o modelo é baixado (large-v3-turbo tem cerca de 1,5 GB). Se você já tem
uma transcrição com tempo por palavra de outra ferramenta, pule este script e passe o
JSON direto ao cortar.py (veja references/formato-transcricao.md).

Uso:
    python transcrever.py VIDEO SAIDA.json [--idioma pt] [--modelo large-v3-turbo] [--threads 2]

Saída: {"language": "pt", "duration": 184.2, "words": [{"w": "Olá,", "s": 0.5, "e": 0.9, "p": 0.98}]}
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def converter(segmentos, info):
    """Converte a saída do faster-whisper no JSON por palavra lido pelo cortar.py."""
    palavras = []
    for seg in segmentos:
        for w in (seg.words or []):
            texto = (w.word or "").strip()
            if texto:
                palavras.append({"w": texto, "s": round(w.start, 3), "e": round(w.end, 3),
                                 "p": round(w.probability, 3)})
    return {"language": getattr(info, "language", None),
            "duration": getattr(info, "duration", None), "words": palavras}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description="Transcreve por palavra com faster-whisper (local).")
    ap.add_argument("entrada", help="vídeo ou áudio")
    ap.add_argument("saida", help="JSON de saída")
    ap.add_argument("--idioma", default="pt", help="código do idioma. Padrão pt")
    ap.add_argument("--modelo", default="large-v3-turbo",
                    help="nome do modelo do faster-whisper. Em PC fraco use small. Padrão large-v3-turbo")
    ap.add_argument("--threads", type=int, default=2, help="threads de CPU. Padrão 2")
    ap.add_argument("--dispositivo", choices=["cpu", "cuda"], default="cpu")
    a = ap.parse_args()

    if not os.path.isfile(a.entrada):
        sys.exit(f"ERRO: arquivo não encontrado: {a.entrada}")
    if not shutil.which("ffmpeg"):
        sys.exit("ERRO: ffmpeg não encontrado no PATH.")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("ERRO: o faster-whisper não está instalado. Confirme com o dono do vídeo e rode: "
                 "pip install faster-whisper\nOu gere a transcrição por palavra em outra ferramenta "
                 "(references/formato-transcricao.md).")

    with tempfile.TemporaryDirectory(prefix="transc_") as tmp:
        wav = os.path.join(tmp, "audio.wav")
        r = subprocess.run(["ffmpeg", "-y", "-i", a.entrada, "-vn", "-ac", "1", "-ar", "16000",
                            "-c:a", "pcm_s16le", wav], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            sys.exit("ERRO: o ffmpeg não conseguiu extrair o áudio:\n" + r.stderr[-800:])
        tipo = "float16" if a.dispositivo == "cuda" else "int8"
        print(f"Modelo {a.modelo} ({a.dispositivo}/{tipo}); a primeira execução baixa o modelo...", flush=True)
        modelo = WhisperModel(a.modelo, device=a.dispositivo, compute_type=tipo, cpu_threads=a.threads)
        segmentos, info = modelo.transcribe(
            wav, language=a.idioma, word_timestamps=True, beam_size=5,
            vad_filter=True, vad_parameters={"min_silence_duration_ms": 300})
        resultado = converter(segmentos, info)  # o gerador só roda aqui, dentro do with

    with open(a.saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    print(f"OK: {len(resultado['words'])} palavras em {a.saida}")
    print("Próximo passo: python cortar.py --transcricao " + a.saida + " --texto")


if __name__ == "__main__":
    main()
