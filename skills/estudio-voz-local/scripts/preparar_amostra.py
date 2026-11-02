#!/usr/bin/env python3
"""Prepara a amostra de referencia para clonagem de voz.

Recebe audio ou video, mede o loudness, recorta o trecho indicado (ou o melhor
trecho, sem silencio longo), gera WAV mono, normaliza para cerca de -18 LUFS e
relata duracao, pico e silencio. Usa so a biblioteca padrao do Python, o ffmpeg
e o ffprobe.
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

FOLGA_ANTES = 0.10
FOLGA_DEPOIS = 0.15
QUEDA_SILENCIO_DB = 22.0
FFMPEG = FFPROBE = None


class Erro(Exception):
    pass


def rodar(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def tempo(texto):
    try:
        partes = [float(p.replace(",", ".")) for p in str(texto).strip().split(":")]
    except ValueError:
        partes = []
    if not 1 <= len(partes) <= 3 or any(p < 0 for p in partes):
        raise argparse.ArgumentTypeError(f"tempo invalido: {texto!r} (use segundos, mm:ss ou hh:mm:ss)")
    total = 0.0
    for p in partes:
        total = total * 60 + p
    return total


def num(x, casas=1):
    if x is None or not math.isfinite(x):
        return "n/d"
    return f"{x:.{casas}f}".replace(".", ",")


def sondar(arquivo):
    cod, saida, erro = rodar([FFPROBE, "-v", "error", "-print_format", "json",
                              "-show_format", "-show_streams", str(arquivo)])
    if cod != 0:
        raise Erro(f"o ffprobe nao leu '{arquivo}': {erro.strip()[:200]}")
    info = json.loads(saida or "{}")
    faixas = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    if not faixas:
        raise Erro("o arquivo nao tem faixa de audio")
    duracao = None
    for fonte in (info.get("format", {}), faixas[0]):
        try:
            duracao = float(fonte["duration"])
            break
        except (KeyError, TypeError, ValueError):
            continue
    if not duracao or duracao <= 0:
        raise Erro("nao consegui descobrir a duracao do arquivo")
    return duracao, int(faixas[0].get("sample_rate") or 0)


def janela(ini, dur):
    return [] if ini is None else ["-ss", f"{ini:.3f}", "-t", f"{dur:.3f}"]


def ffmpeg_audio(arquivo, ini, dur, filtro, saida_args):
    cmd = [FFMPEG, "-hide_banner", "-nostdin", "-nostats", *janela(ini, dur),
           "-i", str(arquivo), "-map", "0:a:0", "-af", filtro, *saida_args]
    return rodar(cmd)


def medir(arquivo, ini, dur, alvo, pico):
    filtro = f"aformat=channel_layouts=mono,loudnorm=I={alvo}:TP={pico}:LRA=11:print_format=json"
    cod, _, erro = ffmpeg_audio(arquivo, ini, dur, filtro, ["-f", "null", "-"])
    achado = re.search(r'\{[^{}]*"input_i"[^{}]*\}', erro, re.S)
    if cod != 0 or not achado:
        raise Erro("o ffmpeg nao conseguiu medir o loudness: " + erro.strip()[-300:])
    bruto = json.loads(achado.group(0))
    return {k: float(v) for k, v in bruto.items() if k.startswith("input_") or k == "target_offset"}


def detectar_silencios(arquivo, ini, dur, limiar_db, minimo):
    filtro = f"aformat=channel_layouts=mono,silencedetect=noise={limiar_db:.1f}dB:d={minimo}"
    cod, _, erro = ffmpeg_audio(arquivo, ini, dur, filtro, ["-f", "null", "-"])
    if cod != 0:
        raise Erro("o ffmpeg nao conseguiu detectar silencios: " + erro.strip()[-300:])
    numero = r"(-?\d+(?:\.\d+)?(?:e[-+]?\d+)?)"
    inicios = [max(0.0, float(x)) for x in re.findall(r"silence_start:\s*" + numero, erro)]
    fins = [float(x) for x in re.findall(r"silence_end:\s*" + numero, erro)]
    pares = []
    for k, s in enumerate(inicios):
        e = fins[k] if k < len(fins) else dur
        pares.append((s, min(max(e, s), dur)))
    return pares


def trechos_de_fala(total, silencios):
    falas, cursor = [], 0.0
    for s, e in sorted(silencios):
        if s - cursor > 0.05:
            falas.append((cursor, s))
        cursor = max(cursor, e)
    if total - cursor > 0.05:
        falas.append((cursor, total))
    return falas


def silencio_em(silencios, ini, fim):
    soma = maior = 0.0
    quantidade = 0
    for s, e in silencios:
        parte = min(e, fim) - max(s, ini)
        if parte > 1e-3:
            soma += parte
            maior = max(maior, parte)
            quantidade += 1
    return soma, maior, quantidade


def escolher_trecho(total, silencios, alvo, tolerancia, maximo):
    avisos = []
    if total <= alvo + tolerancia:
        avisos.append(f"o arquivo tem so {num(total)} s; usei o arquivo inteiro")
        return 0.0, total, "arquivo inteiro", avisos

    falas = trechos_de_fala(total, silencios)
    curto, longo = alvo - tolerancia, alvo + tolerancia
    melhor = None
    for i in range(len(falas)):
        for j in range(i, len(falas)):
            comprimento = falas[j][1] - falas[i][0]
            if comprimento > longo:
                break
            if comprimento < curto:
                continue
            lacunas = [falas[k + 1][0] - falas[k][1] for k in range(i, j)]
            if max(lacunas, default=0.0) > maximo:
                continue
            chave = (sum(lacunas), abs(comprimento - alvo), falas[i][0])
            if melhor is None or chave < melhor[0]:
                melhor = (chave, falas[i][0], falas[j][1])
    if melhor:
        _, a, b = melhor
        return max(0.0, a - FOLGA_ANTES), min(total, b + FOLGA_DEPOIS), "entre pausas", avisos

    inicios = {0.0} | {round(a, 3) for a, _ in falas}
    t = 0.0
    while t + alvo <= total + 1e-6:
        inicios.add(round(t, 3))
        t += 0.5
    pontuados = []
    for t in sorted(inicios):
        if t + alvo > total + 1e-6:
            continue
        soma, maior, _ = silencio_em(silencios, t, t + alvo)
        excedeu = maior > maximo
        pontuados.append(((excedeu, maior if excedeu else 0.0, soma, t), t))
    (excedeu, _, _, _), t = min(pontuados)
    avisos.append(f"nao achei pausas que fechem um trecho de cerca de {num(alvo, 0)} s: o corte pode cair "
                  "no meio de uma palavra, confira o texto contra o audio")
    if excedeu:
        avisos.append(f"todo trecho tem pausa maior que {num(maximo)} s; usei o menos ruim")
    return max(0.0, t - FOLGA_ANTES), min(total, t + alvo), "corte fixo", avisos


def limpo(x):
    return round(x, 3) if x is not None and math.isfinite(x) else None


def executar(args):
    global FFMPEG, FFPROBE
    for nome in ("ffmpeg", "ffprobe"):
        if not shutil.which(nome):
            raise Erro(f"'{nome}' nao esta no PATH. Instale o ffmpeg (o ffprobe vem junto).")
    FFMPEG, FFPROBE = shutil.which("ffmpeg"), shutil.which("ffprobe")

    entrada, saida = Path(args.entrada), Path(args.saida)
    if not entrada.is_file():
        raise Erro(f"arquivo nao encontrado: {entrada}")
    if saida.resolve() == entrada.resolve():
        raise Erro("a saida nao pode ser o proprio arquivo de entrada")
    if saida.exists() and not args.sobrescrever:
        raise Erro(f"'{saida}' ja existe; use --sobrescrever")
    saida.parent.mkdir(parents=True, exist_ok=True)

    total, taxa_entrada = sondar(entrada)
    avisos = []
    inteiro = None

    if args.inicio is not None or args.fim is not None:
        ini = args.inicio if args.inicio is not None else max(0.0, args.fim - args.duracao)
        fim = min(args.fim if args.fim is not None else ini + args.duracao, total)
        if ini >= total:
            raise Erro(f"o inicio ({num(ini)} s) esta alem do fim do arquivo ({num(total)} s)")
        if fim - ini < 1.0:
            raise Erro("o trecho indicado tem menos de 1 s")
        modo = "indicado"
        referencia = medir(entrada, ini, fim - ini, args.lufs, args.pico)["input_i"]
        if not math.isfinite(referencia):
            raise Erro("o trecho indicado nao tem sinal audivel")
        limiar = args.limiar_db if args.limiar_db is not None else referencia - QUEDA_SILENCIO_DB
    else:
        inteiro = medir(entrada, None, None, args.lufs, args.pico)
        referencia = inteiro["input_i"]
        if not math.isfinite(referencia):
            raise Erro("o arquivo nao tem sinal audivel")
        limiar = args.limiar_db if args.limiar_db is not None else referencia - QUEDA_SILENCIO_DB
        silencios = detectar_silencios(entrada, None, total, limiar, args.silencio_min)
        ini, fim, modo, avisos = escolher_trecho(total, silencios, args.duracao, args.tolerancia,
                                                 args.silencio_max)

    dur_trecho = fim - ini
    antes = medir(entrada, ini, dur_trecho, args.lufs, args.pico)
    if not math.isfinite(antes["input_i"]):
        raise Erro("o trecho escolhido nao tem sinal audivel")

    filtro = (f"aformat=channel_layouts=mono,loudnorm=I={args.lufs}:TP={args.pico}:LRA=11:"
              f"measured_I={antes['input_i']}:measured_TP={antes['input_tp']}:"
              f"measured_LRA={antes['input_lra']}:measured_thresh={antes['input_thresh']}:"
              f"offset={antes['target_offset']}:linear=true,aresample={args.taxa}")
    cod, _, erro = ffmpeg_audio(entrada, ini, dur_trecho, filtro,
                                ["-ar", str(args.taxa), "-ac", "1", "-c:a", "pcm_s16le", "-y", str(saida)])
    if cod != 0 or not saida.is_file():
        saida.unlink(missing_ok=True)
        raise Erro("o ffmpeg falhou ao gerar o WAV: " + erro.strip()[-300:])

    depois = medir(saida, None, None, args.lufs, args.pico)
    dur_final, _ = sondar(saida)
    queda = referencia - limiar
    silencios_saida = detectar_silencios(saida, None, dur_final, depois["input_i"] - queda,
                                         args.silencio_min)
    soma, maior, quantidade = silencio_em(silencios_saida, 0.0, dur_final)
    limiar_saida = depois["input_i"] - queda

    if dur_final < 3:
        avisos.append("trecho com menos de 3 s: pouca informacao de voz")
    if dur_final > 20:
        avisos.append("trecho com mais de 20 s: alguns modelos recusam a amostra ou ignoram o texto "
                      "dela (o OmniVoice faz isso quando ha transcricao); confira o seu modelo")
    if maior > args.silencio_max:
        avisos.append(f"ha uma pausa de {num(maior)} s dentro do trecho")
    if abs(depois["input_i"] - args.lufs) > 1.0:
        avisos.append(f"ficou em {num(depois['input_i'])} LUFS, longe do alvo de {num(args.lufs)}: "
                      "o limite de pico segurou o ganho; tente --pico -1")
    if depois["input_tp"] > -1.0:
        avisos.append("pico verdadeiro acima de -1 dBTP: risco de distorcer ao converter")
    if taxa_entrada and taxa_entrada < args.taxa:
        avisos.append(f"a entrada tem {taxa_entrada} Hz; subir para {args.taxa} Hz nao recupera "
                      "graves nem agudos que nao foram gravados")

    texto_irmao = saida.with_suffix(".txt")
    dados = {
        "entrada": str(entrada),
        "duracao_entrada_s": limpo(total),
        "loudness_entrada_inteira": None if inteiro is None else {
            "lufs": limpo(inteiro["input_i"]), "pico_dbtp": limpo(inteiro["input_tp"]),
            "lra": limpo(inteiro["input_lra"])},
        "trecho": {"inicio_s": limpo(ini), "fim_s": limpo(fim), "duracao_s": limpo(dur_trecho),
                   "modo": modo},
        "loudness_trecho_antes": {"lufs": limpo(antes["input_i"]), "pico_dbtp": limpo(antes["input_tp"]),
                                  "lra": limpo(antes["input_lra"])},
        "saida": {"arquivo": str(saida), "formato": "WAV PCM 16 bits", "taxa_hz": args.taxa,
                  "canais": 1, "duracao_s": limpo(dur_final),
                  "lufs": limpo(depois["input_i"]), "pico_dbtp": limpo(depois["input_tp"]),
                  "lra": limpo(depois["input_lra"])},
        "silencio": {"limiar_db": limpo(limiar_saida), "minimo_s": args.silencio_min,
                     "total_s": limpo(soma), "maior_s": limpo(maior), "quantidade": quantidade,
                     "fracao_fala": limpo(1 - soma / dur_final if dur_final else 0.0)},
        "avisos": avisos,
        "proximo_passo": f"transcreva o trecho, revise palavra por palavra e salve em {texto_irmao.name}",
    }

    if args.json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        return 0

    s = dados["saida"]
    print(f"Entrada          : {entrada.name} ({num(total)} s)")
    if inteiro is not None:
        print(f"Loudness inteiro : {num(inteiro['input_i'])} LUFS | pico {num(inteiro['input_tp'])} dBTP "
              f"| LRA {num(inteiro['input_lra'])} LU")
    print(f"Trecho           : {num(ini, 2)} s a {num(fim, 2)} s ({num(dur_trecho, 2)} s) | modo: {modo}")
    print(f"Trecho antes     : {num(antes['input_i'])} LUFS | pico {num(antes['input_tp'])} dBTP")
    print(f"Saida            : {saida} | WAV PCM 16 bits | {args.taxa} Hz | mono | {num(dur_final, 2)} s")
    print(f"Loudness saida   : {num(s['lufs'])} LUFS | pico {num(s['pico_dbtp'])} dBTP | "
          f"LRA {num(s['lra'])} LU")
    print(f"Silencio         : limiar {num(limiar_saida)} dB | total {num(soma)} s | maior pausa "
          f"{num(maior)} s | {quantidade} pausa(s) | fala {num(100 * dados['silencio']['fracao_fala'], 0)} %")
    if avisos:
        print("Avisos:")
        for aviso in avisos:
            print(f" - {aviso}")
    print(f"Proximo passo    : {dados['proximo_passo']}")
    return 0


def main():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(
        description="Prepara a amostra de referencia para clonagem de voz: recorta, converte para WAV "
                    "mono, normaliza para cerca de -18 LUFS e relata duracao, pico e silencio.")
    ap.add_argument("entrada", help="arquivo de audio ou video")
    ap.add_argument("-o", "--saida", default="amostra.wav", help="WAV de saida (padrao: amostra.wav)")
    ap.add_argument("--inicio", type=tempo, help="inicio do trecho: segundos, mm:ss ou hh:mm:ss")
    ap.add_argument("--fim", type=tempo, help="fim do trecho (use com --inicio ou sozinho)")
    ap.add_argument("--duracao", type=float, default=16.0,
                    help="duracao alvo em segundos (padrao 16); no modo automatico e o centro da faixa")
    ap.add_argument("--tolerancia", type=float, default=2.0,
                    help="quanto a duracao pode variar para cortar entre pausas (padrao 2 s)")
    ap.add_argument("--taxa", type=int, default=24000, help="taxa do WAV em Hz (padrao 24000)")
    ap.add_argument("--lufs", type=float, default=-18.0, help="loudness alvo (padrao -18)")
    ap.add_argument("--pico", type=float, default=-1.5, help="teto de pico verdadeiro em dBTP (padrao -1.5)")
    ap.add_argument("--silencio-max", type=float, default=0.7,
                    help="maior pausa aceita dentro do trecho, em s (padrao 0.7)")
    ap.add_argument("--silencio-min", type=float, default=0.3,
                    help="pausa minima que conta como silencio, em s (padrao 0.3)")
    ap.add_argument("--limiar-db", type=float,
                    help="nivel em dB abaixo do qual e silencio (padrao: loudness do audio menos 22 dB)")
    ap.add_argument("--sobrescrever", action="store_true", help="aceita sobrescrever a saida")
    ap.add_argument("--json", action="store_true", help="imprime o relatorio em JSON")
    args = ap.parse_args()

    if args.duracao <= 0 or args.tolerancia < 0:
        ap.error("--duracao deve ser maior que zero e --tolerancia nao pode ser negativa")
    if not 8000 <= args.taxa <= 96000:
        ap.error("--taxa deve ficar entre 8000 e 96000 Hz")
    if not -40 <= args.lufs <= -5:
        ap.error("--lufs deve ficar entre -40 e -5")
    if args.pico > 0:
        ap.error("--pico deve ser 0 ou negativo")
    if args.inicio is not None and args.fim is not None and args.fim <= args.inicio:
        ap.error("--fim precisa ser maior que --inicio")

    try:
        return executar(args)
    except Erro as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
