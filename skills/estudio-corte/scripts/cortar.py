#!/usr/bin/env python3
"""cortar.py - corta um vídeo de uma pessoa falando em um Reel vertical legendado.

Por padrão só mostra o PLANO (gancho, trechos mantidos, pausas removidas, avisos)
e não renderiza nada. O plano termina com um código. Mostre o plano ao dono do
vídeo e, depois que ele aprovar, rode o MESMO comando com --aprovado CODIGO. Se
qualquer parâmetro mudar depois da aprovação, o código muda e o render recusa.

Entrada: vídeo + transcrição JSON com tempo por palavra (veja transcrever.py e
references/formato-transcricao.md).
Saída: MP4 1080x1920, 30 fps, H.264 + AAC 48 kHz, áudio em -14 LUFS (2 passadas).

Regras de corte: fronteira sempre no limite de uma palavra; pausa de 0,6 s ou mais
é cortada; folga de 0,05 s antes e 0,18 s depois de cada trecho; fade de 30 ms em
cada emenda; loudnorm medido no áudio já cortado.

Dependências: Python 3.10+ (só biblioteca padrão) e ffmpeg/ffprobe no PATH.
Origem: escrito do zero para o Estúdio de Vídeo com IA. A ideia do fade de 30 ms
e a do corte sempre no limite da palavra aparecem na documentação do video-use
(MIT, Browser Use, https://github.com/browser-use/video-use).
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

LARGURA_REF, ALTURA_REF = 1080, 1920
BASE_PADRAO = 1200                 # linha de base da legenda em 1920 de altura
BASE_MIN, BASE_MAX = 1150, 1300    # faixa da régua de área segura
MARGEM_LATERAL = 140               # px de cada lado, em 1080 de largura
LARGURA_CHAR = 0.55                # largura média de um caractere, em fração do corpo da fonte (Arial negrito mede ~0,45 a 0,55)
MAX_TRECHOS = 100                  # uma entrada do ffmpeg por trecho
TRC_HDR = ("arib-std-b67", "smpte2084")
HDR_PARA_SDR = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
                "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def erro(msg, codigo=2):
    sys.stdout.flush()
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(codigo)


# ----------------------------------------------------------------- utilidades

def para_segundos(txt):
    total = 0.0
    for parte in txt.strip().split(":"):
        total = total * 60 + float(parte)
    return total


def ler_intervalos(txt, nome):
    saida = []
    for item in (txt or "").split(","):
        item = item.strip()
        if not item:
            continue
        try:
            a, b = item.split("-")
            a, b = para_segundos(a), para_segundos(b)
        except ValueError:
            erro(f"{nome}: '{item}' não é um intervalo válido. Use inicio-fim em segundos, ex.: 12.5-18")
        if b <= a:
            erro(f"{nome}: em '{item}' o fim precisa ser maior que o início.")
        saida.append((a, b))
    return saida


def mmss(t):
    t = max(0.0, t)
    return f"{int(t // 60)}:{t % 60:04.1f}"


def tempo_ass(t):
    cs = max(0, int(round(t * 100)))
    h, resto = divmod(cs, 360000)
    m, resto = divmod(resto, 6000)
    s, c = divmod(resto, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def meio(w):
    return (w["s"] + w["e"]) / 2


def subtrair(intervalo, remocoes):
    """Tira de (a, b) os intervalos de remocoes e devolve os pedaços que sobram."""
    pedacos = [intervalo]
    for c, d in remocoes:
        novos = []
        for x, y in pedacos:
            if d <= x or c >= y:
                novos.append((x, y))
                continue
            if x < c:
                novos.append((x, c))
            if d < y:
                novos.append((d, y))
        pedacos = novos
    return pedacos


# ----------------------------------------------------------------- transcrição

def _primeiro(d, chaves):
    for k in chaves:
        if d.get(k) is not None:
            return d[k]
    return None


def carregar_palavras(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError) as e:
        erro(f"não consegui ler a transcrição '{caminho}': {e}")
    if isinstance(dados, list):
        brutas = dados
    elif isinstance(dados, dict) and isinstance(dados.get("words"), list):
        brutas = dados["words"]
    elif isinstance(dados, dict) and isinstance(dados.get("segments"), list):
        brutas = [p for seg in dados["segments"] if isinstance(seg, dict)
                  for p in (seg.get("words") or [])]
    else:
        brutas = []
    palavras = []
    for p in brutas:
        if not isinstance(p, dict) or p.get("type") not in (None, "word"):
            continue
        texto = _primeiro(p, ("w", "word", "text", "palavra"))
        texto = str(texto).strip() if texto is not None else ""
        try:
            ini = float(_primeiro(p, ("s", "start", "inicio")))
            fim = float(_primeiro(p, ("e", "end", "fim")))
        except (TypeError, ValueError):
            continue
        if not texto or not math.isfinite(ini) or not math.isfinite(fim) or ini < 0:
            continue
        prob = p.get("p", p.get("probability"))
        palavras.append({"w": texto, "s": ini, "e": max(fim, ini),
                         "p": prob if isinstance(prob, (int, float)) else None})
    if not palavras:
        erro("a transcrição não tem palavras com tempo (início e fim de cada palavra). "
             "Gere com transcrever.py ou veja references/formato-transcricao.md.")
    palavras.sort(key=lambda w: (w["s"], w["e"]))
    dur = dados.get("duration") if isinstance(dados, dict) else None
    return palavras, (float(dur) if isinstance(dur, (int, float)) else None)


def frases(palavras, pausa):
    atual, saida = [], []
    for w in palavras:
        if atual and (w["s"] - atual[-1]["e"] >= pausa or len(atual) >= 16
                      or re.search(r"[.?!…]$", atual[-1]["w"])):
            saida.append(atual)
            atual = []
        atual.append(w)
    if atual:
        saida.append(atual)
    return saida


def imprimir_texto(palavras, pausa):
    for fr in frases(palavras, pausa):
        print(f"[{fr[0]['s']:8.2f} - {fr[-1]['e']:8.2f}] " + " ".join(w["w"] for w in fr))


# ----------------------------------------------------------------- sondagem

def fracao(txt):
    try:
        a, b = str(txt).split("/")
        return float(a) / float(b) if float(b) else 0.0
    except (ValueError, ZeroDivisionError):
        return 0.0


def sondar(video):
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        erro("ffmpeg/ffprobe não encontrados no PATH.")
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json",
                        "-show_format", "-show_streams", video],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        erro("o ffprobe não conseguiu ler o vídeo: " + r.stderr.strip()[-300:])
    d = json.loads(r.stdout)
    fluxos = d.get("streams", [])
    v = next((s for s in fluxos if s.get("codec_type") == "video"), None)
    a = next((s for s in fluxos if s.get("codec_type") == "audio"), None)
    if not v:
        erro("o arquivo não tem vídeo.")
    if not a:
        erro("o arquivo não tem áudio; sem áudio não há fala para cortar.")
    rot = 0
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd:
            rot = int(round(float(sd["rotation"])))
    if not rot and (v.get("tags") or {}).get("rotate"):
        rot = int(float(v["tags"]["rotate"]))
    larg, alt = int(v["width"]), int(v["height"])
    if abs(rot) % 180 == 90:
        larg, alt = alt, larg
    r_fps, m_fps = fracao(v.get("r_frame_rate")), fracao(v.get("avg_frame_rate"))
    dur = d.get("format", {}).get("duration") or v.get("duration")
    return {
        "larg": larg, "alt": alt, "rot": rot,
        "fps": m_fps or r_fps,
        "vfr": bool(r_fps and m_fps and abs(r_fps - m_fps) / m_fps > 0.01),
        "trc": v.get("color_transfer") or "",
        "hdr": (v.get("color_transfer") or "") in TRC_HDR,
        "duracao": float(dur) if dur else None,
        "taxa_audio": a.get("sample_rate"),
    }


# ----------------------------------------------------------------- plano de corte

def ajustar_a_palavras(intervalo, palavras):
    """Estende uma remoção para cobrir inteiras as palavras cujo meio cai dentro dela."""
    c, d = intervalo
    ws = [w for w in palavras if c <= meio(w) <= d]
    return (min(c, ws[0]["s"]), max(d, max(w["e"] for w in ws))) if ws else intervalo


def fazer_trecho(ws, args, dur, remover=()):
    cs, ce = min(w["s"] for w in ws), max(w["e"] for w in ws)
    a, b = max(0.0, cs - args.folga_antes), min(dur, ce + args.folga_depois)
    for c, d in remover:
        if cs >= d - 1e-6:
            a = max(a, d)
        elif ce <= c + 1e-6:
            b = min(b, c)
    return {"cs": cs, "ce": ce, "a": a, "b": b, "words": list(ws)}


def juntar_sobrepostos(trechos, tolerancia):
    """Une trechos vizinhos cujas folgas se tocam, para nunca repetir áudio nem cortar palavra."""
    saida = []
    for t in trechos:
        if saida and t["a"] <= saida[-1]["b"] + tolerancia and t["a"] >= saida[-1]["a"]:
            ant = saida[-1]
            ant["b"] = max(ant["b"], t["b"])
            ant["ce"] = max(ant["ce"], t["ce"])
            ant["words"] += t["words"]
        else:
            saida.append(t)
    return saida


def montar_plano(args, palavras, dur):
    fim_corpo = args.fim_corpo if args.fim_corpo is not None else dur
    remover = [ajustar_a_palavras(r, palavras) for r in ler_intervalos(args.remover, "--remover")]

    gancho = []
    for x, y in ler_intervalos(args.gancho, "--gancho"):
        ws = [w for w in palavras if w["e"] > x and w["s"] < y]
        if not ws:
            erro(f"--gancho {x}-{y}: não há palavras da transcrição nesse intervalo.")
        gancho.append(fazer_trecho(ws, args, dur))
    gancho = juntar_sobrepostos(gancho, 0.0)

    uteis = [w for w in palavras
             if w["s"] >= args.inicio_corpo - 1e-6 and w["e"] <= fim_corpo + 1e-6
             and not any(c <= meio(w) <= d for c, d in remover)]
    corridas = []
    for w in uteis:
        if corridas and w["s"] - max(x["e"] for x in corridas[-1]) < args.pausa - 1e-6:
            corridas[-1].append(w)
        else:
            corridas.append([w])
    corpo = []
    for run in corridas:
        for x, y in subtrair((run[0]["s"], max(w["e"] for w in run)), remover):
            ws = [w for w in run if x - 1e-6 <= meio(w) <= y + 1e-6]
            if ws:
                corpo.append(fazer_trecho(ws, args, dur, remover))
    corpo.sort(key=lambda t: t["cs"])
    corpo = [t for t in juntar_sobrepostos(corpo, 0.02) if t["b"] - t["a"] >= 0.1]
    if not corpo and not gancho:
        erro("nada para exportar: nenhum trecho com fala dentro do intervalo escolhido.")

    todos = gancho + corpo
    desloc = 0.0
    for t in todos:
        t["off"] = desloc
        t["dur"] = t["b"] - t["a"]
        desloc += t["dur"]
    return gancho, corpo, desloc


# ----------------------------------------------------------------- legenda

def limpar_token(txt):
    return re.sub(r"[{}\\]", "", txt).strip()


def quebrar(tokens, maximo):
    """Texto em 1 linha se couber, senão em 2 linhas equilibradas. Devolve (texto, largura_max)."""
    um = " ".join(tokens)
    if len(um) <= maximo or len(tokens) == 1:
        return um, len(um)
    melhor = min(range(1, len(tokens)),
                 key=lambda k: max(len(" ".join(tokens[:k])), len(" ".join(tokens[k:]))))
    l1, l2 = " ".join(tokens[:melhor]), " ".join(tokens[melhor:])
    return l1 + r"\N" + l2, max(len(l1), len(l2))


def agrupar(ws, max_palavras, max_chars):
    """Blocos de legenda: até max_palavras em até 2 linhas de max_chars. Colapsa palavra repetida."""
    limpas = []
    for w in ws:
        t = limpar_token(w["w"])
        if not t:
            continue
        chave = re.sub(r"\W+", "", t.lower())
        if limpas and chave and chave == re.sub(r"\W+", "", limpas[-1]["t"].lower()):
            limpas[-1]["e"] = max(limpas[-1]["e"], w["e"])
            continue
        limpas.append({"t": t, "s": w["s"], "e": w["e"]})
    blocos, i = [], 0
    while i < len(limpas):
        n = min(max_palavras, len(limpas) - i)
        while n > 1 and quebrar([x["t"] for x in limpas[i:i + n]], max_chars)[1] > max_chars:
            n -= 1
        blocos.append(limpas[i:i + n])
        i += n
    return blocos


def eventos_legenda(trechos, args, max_chars):
    eventos = []
    for t in trechos:
        blocos = agrupar(t["words"], args.palavras_por_legenda, max_chars)
        for k, bl in enumerate(blocos):
            ini = t["off"] + max(0.0, bl[0]["s"] - t["a"])
            fim = t["off"] + min(t["dur"], bl[-1]["e"] - t["a"])
            prox = (t["off"] + max(0.0, blocos[k + 1][0]["s"] - t["a"])
                    if k + 1 < len(blocos) else t["off"] + t["dur"])
            fim = prox if prox - fim <= 0.5 else min(prox, fim + 0.15)
            if fim - ini >= 0.05:
                texto = quebrar([x["t"] for x in bl], max_chars)[0]
                eventos.append((ini, fim, texto))
    return eventos


def cor_ass(hex_rgb):
    h = hex_rgb.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        erro("--cor-legenda precisa ser RRGGBB em hexadecimal, ex.: FFFF00 (amarelo).")
    return ("&H00" + h[4:6] + h[2:4] + h[0:2]).upper()


def escrever_ass(caminho, eventos, p):
    cab = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {p['larg']}\nPlayResY: {p['alt']}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
        "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Cap,{p['fonte']},{p['tamanho']},{p['cor']},&H000000FF,&H00000000,&H90000000,"
        f"1,0,0,0,100,100,0,0,1,{p['contorno']},{p['sombra']},2,{p['margem_lat']},{p['margem_lat']},"
        f"{p['margem_v']},1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(cab)
        for ini, fim, texto in eventos:
            f.write(f"Dialogue: 0,{tempo_ass(ini)},{tempo_ass(fim)},Cap,,0,0,0,,{texto}\n")


def estilo_legenda(args):
    esc_h, esc_l = args.altura / ALTURA_REF, args.largura / LARGURA_REF
    tamanho = args.tamanho_fonte or max(10, round(64 * esc_h))
    base = args.linha_base if args.linha_base is not None else round(BASE_PADRAO * esc_h)
    margem_lat = round(MARGEM_LATERAL * esc_l)
    max_chars = max(8, int((args.largura - 2 * margem_lat) / (LARGURA_CHAR * tamanho)))
    return {"larg": args.largura, "alt": args.altura, "fonte": args.fonte, "tamanho": tamanho,
            "cor": cor_ass(args.cor_legenda), "contorno": max(1, round(3 * esc_h)),
            "sombra": max(1, round(3 * esc_h)), "margem_lat": margem_lat,
            "margem_v": max(0, args.altura - base), "base": base, "max_chars": max_chars}


# ----------------------------------------------------------------- avisos

def achar_loops(palavras):
    chaves = [re.sub(r"\W+", "", w["w"].lower()) for w in palavras]
    achados = []
    for n in (1, 2, 3, 4):
        reps = 4 if n == 1 else 3
        i = 0
        while i + n * reps <= len(chaves):
            bloco = chaves[i:i + n]
            if all(bloco) and all(chaves[i + k * n:i + (k + 1) * n] == bloco for k in range(reps)):
                achados.append(palavras[i]["s"])
                i += n * reps
            else:
                i += 1
    return sorted(set(achados))


def palavras_suspeitas(trechos):
    sus = []
    for t in trechos:
        for w in t["words"]:
            letras = len(re.sub(r"\W+", "", w["w"]))
            curta = letras >= 4 and (w["e"] - w["s"]) < 0.1
            baixa = w["p"] is not None and w["p"] < 0.3
            if curta or baixa:
                sus.append(w)
    return sus


def reunir_avisos(args, info, palavras, gancho, corpo, usar_hdr, estilo, total):
    av = []
    if info["larg"] * 16 > info["alt"] * 9 * 1.05:
        mantido = (args.largura / (info["larg"] * max(args.largura / info["larg"], args.altura / info["alt"])))
        av.append(f"A fonte não é vertical ({info['larg']}x{info['alt']}). O script recorta o centro "
                  f"(--recorte-x {args.recorte_x:g}) e mantém só {mantido * 100:.0f}% da largura: "
                  "confira em um quadro se a pessoa fica inteira.")
    ampliacao = max(args.largura / info["larg"], args.altura / info["alt"])
    if ampliacao > 1.5:
        av.append(f"A fonte será ampliada {ampliacao:.1f}x para encher o quadro; a imagem vai perder "
                  "nitidez. Use o arquivo original, se existir.")
    if info["hdr"] and not usar_hdr:
        av.append("A fonte é HDR e a conversão para SDR está desligada: a cor pode sair lavada depois "
                  "que a rede reprocessar o vídeo.")
    if info["vfr"]:
        av.append("Taxa de quadros variável na fonte. A saída é fixada em "
                  f"{args.fps} fps; confira a sincronia nas emendas.")
    if args.gancho and corpo:
        ini_corpo = corpo[0]["cs"]
        for g in gancho:
            if g["ce"] > ini_corpo + 0.05 and g["cs"] < ini_corpo + 10:
                av.append(f"O gancho ({g['cs']:.1f}-{g['ce']:.1f} s) cai nos primeiros 10 s do corpo: a "
                          f"frase vai tocar duas vezes seguidas. Use --inicio-corpo {g['ce']:.1f} ou "
                          "escolha o gancho em outro ponto.")
                break
    if not gancho:
        av.append("Sem gancho (--gancho). O vídeo começa direto no corpo.")
    sus = palavras_suspeitas(gancho + corpo)
    if sus:
        ex = ", ".join(f"'{w['w']}' em {w['s']:.1f} s" for w in sus[:4])
        av.append(f"{len(sus)} palavra(s) com tempo ou confiança suspeitos ({ex}). Confira na "
                  "transcrição antes de queimar a legenda.")
    loops = achar_loops(palavras)
    if loops:
        av.append("Trechos repetidos em sequência (possível alucinação do Whisper em áudio ruim) perto de "
                  + ", ".join(f"{t:.1f} s" for t in loops[:4]) + ". Se for o caso, descarte o vídeo.")
    longas = sorted({limpar_token(w["w"]) for t in gancho + corpo for w in t["words"]
                     if len(limpar_token(w["w"])) > estilo["max_chars"]})
    if longas and not args.sem_legenda:
        av.append(f"Palavra(s) mais larga(s) que a legenda ({', '.join(longas[:3])}): vão passar da margem "
                  "lateral. Reduza --tamanho-fonte ou confira o quadro.")
    if not args.sem_legenda and not (BASE_MIN * args.altura / ALTURA_REF - 0.5
                                     <= estilo["base"] <= BASE_MAX * args.altura / ALTURA_REF + 0.5):
        av.append(f"A linha de base da legenda (y {estilo['base']}) fica fora da régua "
                  f"(y {BASE_MIN} a {BASE_MAX} em 1920 de altura).")
    if len(gancho) + len(corpo) > 60:
        av.append(f"{len(gancho) + len(corpo)} trechos: o ffmpeg abre uma entrada por trecho. Se faltar "
                  "memória, divida o bruto em partes ou aumente --pausa.")
    if total > 180:
        av.append("O corte passa de 3 minutos. Reels longos podem ter distribuição diferente; confira "
                  "a regra vigente da plataforma antes de postar.")
    return av


# ----------------------------------------------------------------- plano na tela

def resumo_texto(ws, inicio=7, fim=3):
    t = [w["w"] for w in ws]
    return " ".join(t) if len(t) <= inicio + fim + 2 else " ".join(t[:inicio]) + " ... " + " ".join(t[-fim:])


def codigo_plano(args, trechos, usar_hdr):
    """Hash do plano exato: trechos e todos os parâmetros que mudam o resultado."""
    ignorar = {"saida", "sobrescrever", "aprovado", "texto"}
    base = {k: v for k, v in sorted(vars(args).items()) if k not in ignorar}
    base["trechos"] = [[round(t["a"], 3), round(t["b"], 3), len(t["words"])] for t in trechos]
    base["hdr_usado"] = usar_hdr
    return hashlib.sha1(json.dumps(base, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:8]


def imprimir_plano(args, info, palavras, gancho, corpo, total, eventos, estilo, usar_hdr, avisos, dur, codigo):
    print("PLANO DE CORTE (nada foi renderizado)")
    print(f"Fonte: {os.path.basename(args.entrada)} | {info['larg']}x{info['alt']} | "
          f"{info['fps']:.2f} fps | {mmss(dur)} | HDR: {'sim' if info['hdr'] else 'não'}")
    print(f"Saída: {args.largura}x{args.altura} | {args.fps} fps | áudio {args.lufs:g} LUFS, "
          f"pico verdadeiro até {args.pico_verdadeiro:g} dB | conversão HDR: {'sim' if usar_hdr else 'não'}")
    print(f"Transcrição: {len(palavras)} palavras\n")

    print("GANCHO (vai para o topo do vídeo)")
    if gancho:
        for i, g in enumerate(gancho, 1):
            print(f"  {i}. {g['cs']:.2f}-{g['ce']:.2f} s ({g['dur']:.1f} s)  \"{resumo_texto(g['words'], 14, 4)}\"")
        print(f"  Total do gancho: {sum(g['dur'] for g in gancho):.1f} s")
    else:
        print("  nenhum")

    print("\nCORPO (trechos mantidos, em tempo do vídeo original)")
    print("   #   início     fim     dur  texto")
    for i, t in enumerate(corpo, 1):
        print(f"  {i:2d}  {t['a']:7.2f}  {t['b']:7.2f}  {t['dur']:6.2f}  \"{resumo_texto(t['words'])}\"")

    if corpo:
        print("\nREMOVIDO")
        if corpo[0]["a"] > 0.5:
            print(f"  começo: 0.00 -> {corpo[0]['a']:.2f} s ({corpo[0]['a']:.1f} s)")
        cortes = [(ant["b"], nxt["a"]) for ant, nxt in zip(corpo, corpo[1:]) if nxt["a"] - ant["b"] > 0.05]
        if len(cortes) > 12:
            maiores = sorted(sorted(cortes, key=lambda c: c[0] - c[1])[:8])
            for x, y in maiores:
                print(f"  corte:  {x:.2f} -> {y:.2f} s ({y - x:.2f} s)")
            resto = [c for c in cortes if c not in maiores]
            print(f"  e mais {len(resto)} cortes menores, {sum(y - x for x, y in resto):.1f} s no total")
        else:
            for x, y in cortes:
                print(f"  corte:  {x:.2f} -> {y:.2f} s ({y - x:.2f} s)")
        if dur - corpo[-1]["b"] > 0.5:
            print(f"  final:  {corpo[-1]['b']:.2f} -> {dur:.2f} s ({dur - corpo[-1]['b']:.1f} s)")

    gdur = sum(g["dur"] for g in gancho)
    print(f"\nRESUMO\n  original {mmss(dur)} -> corte {mmss(total)} "
          f"(gancho {gdur:.1f} s + corpo {total - gdur:.1f} s)")
    if args.sem_legenda:
        print("  legenda: desligada")
    else:
        maior = max((max(len(l) for l in e[2].split(r'\N')) for e in eventos), default=0)
        print(f"  legenda: {len(eventos)} blocos, linha de base em y {estilo['base']} de {args.altura}, "
              f"maior linha com {maior} caracteres (limite {estilo['max_chars']})")
        for ini, fim, texto in eventos[:3]:
            print(f"    {ini:6.2f}-{fim:6.2f} s  {texto.replace(chr(92) + 'N', ' / ')}")
    if avisos:
        print("\nAVISOS")
        for a in avisos:
            print("  - " + a)
    print(f"\nCódigo do plano: {codigo}")
    if args.aprovado is None:
        print("Mostre o gancho e os cortes ao dono do vídeo. Depois que ele aprovar, rode o mesmo "
              f"comando acrescentando --aprovado {codigo}")


# ----------------------------------------------------------------- render

def executar(rotulo, cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        erro(f"o ffmpeg falhou na etapa '{rotulo}':\n" + r.stderr[-2000:], 1)
    return r


def medir_loudness(entradas, grafo, mapa):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", *entradas, "-filter_complex", grafo,
           "-map", mapa, "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        blocos = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)
        return json.loads(blocos[-1])
    except (IndexError, ValueError):
        return None


def renderizar(args, trechos, estilo, eventos, usar_hdr):
    tmp = tempfile.mkdtemp(prefix="corte_")
    try:
        entradas, partes_av, partes_a = [], [], []
        for i, t in enumerate(trechos):
            f = min(args.fade, t["dur"] / 2)
            entradas += ["-ss", f"{t['a']:.3f}", "-t", f"{t['dur']:.3f}", "-i", args.entrada]
            fade = (f"asetpts=PTS-STARTPTS,afade=t=in:st=0:d={f:.3f},"
                    f"afade=t=out:st={t['dur'] - f:.3f}:d={f:.3f}")
            partes_av.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}];[{i}:a]{fade}[a{i}];")
            partes_a.append(f"[{i}:a]{fade}[m{i}];")
        n = len(trechos)
        if os.name == "nt" and sum(len(x) + 1 for x in entradas) + sum(len(x) for x in partes_av) > 30000:
            erro("trechos demais para um único comando no Windows. Aumente --pausa ou divida o bruto.")

        ln = f"loudnorm=I={args.lufs:g}:TP={args.pico_verdadeiro:g}:LRA=11"
        concat_a = "".join(f"[m{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[mc];"
        med = medir_loudness(entradas, "".join(partes_a) + concat_a + f"[mc]{ln}:print_format=json[mo]", "[mo]")
        if med:
            ln += (f":measured_I={med['input_i']}:measured_LRA={med['input_lra']}"
                   f":measured_TP={med['input_tp']}:measured_thresh={med['input_thresh']}"
                   f":offset={med['target_offset']}:linear=true")
            print(f"loudnorm 2 passadas: medido I={med['input_i']} LUFS, TP={med['input_tp']} dB")
        else:
            print("AVISO: a medição de loudness falhou; usando 1 passada (ganho dinâmico).")

        cadeia = []
        if usar_hdr:
            cadeia.append(HDR_PARA_SDR)
        cadeia += [f"scale={args.largura}:{args.altura}:force_original_aspect_ratio=increase",
                   f"crop={args.largura}:{args.altura}:(iw-ow)*{args.recorte_x:g}:(ih-oh)/2", "setsar=1"]
        if not args.sem_legenda:
            ass = os.path.join(tmp, "cap.ass")
            escrever_ass(ass, eventos, estilo)
            cadeia.append("subtitles=cap.ass")
        atraso = ""
        if args.silencio_inicial > 0:
            # atrasa áudio e imagem juntos (depois da legenda), para não criar defasagem
            atraso = f",adelay={int(round(args.silencio_inicial * 1000))}:all=1"
            cadeia.append(f"tpad=start_mode=clone:start_duration={args.silencio_inicial:g}")
        grafo = ("".join(partes_av)
                 + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
                 + f"[cv]{','.join(cadeia)}[vout];"
                 + f"[ca]{ln},aresample=48000{atraso}[ax]")
        tags = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"] if usar_hdr else []
        print("Renderizando (pode levar alguns minutos)...")
        executar("render", ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *entradas,
                            "-filter_complex", grafo, "-map", "[vout]", "-map", "[ax]",
                            "-c:v", "libx264", "-preset", "fast", "-crf", str(args.crf),
                            "-pix_fmt", "yuv420p", *tags, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                            "-movflags", "+faststart", "-r", str(args.fps), args.saida], cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def conferir_saida(args):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format",
                        "-show_streams", args.saida], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = next(s for s in d["streams"] if s["codec_type"] == "audio")
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", args.saida, "-vn", "-af",
           f"loudnorm=I={args.lufs:g}:TP={args.pico_verdadeiro:g}:LRA=11:print_format=json", "-f", "null", "-"]
    m = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        med = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", m.stderr)[-1])
        loud = f"{med['input_i']} LUFS, pico verdadeiro {med['input_tp']} dB"
    except (IndexError, ValueError):
        loud = "não medido"
    tam = os.path.getsize(args.saida) / 1e6
    print(f"\nPRONTO: {args.saida}")
    print(f"  {v['width']}x{v['height']} | {v.get('r_frame_rate')} | {v.get('pix_fmt')} | "
          f"cor: {v.get('color_transfer', 'sem marcação')} | duração {float(d['format']['duration']):.1f} s | "
          f"{tam:.1f} MB")
    print(f"  áudio {a.get('codec_name')} {a.get('sample_rate')} Hz | medido no arquivo final: {loud}")
    print("  Confira os quadros e as emendas e envie só ao dono do vídeo; não publique antes do OK dele.")


# ----------------------------------------------------------------- linha de comando

def montar_parser():
    ap = argparse.ArgumentParser(
        prog="cortar.py",
        description="Corta um vídeo de uma pessoa falando em um Reel vertical legendado. "
                    "Sem --aprovado, só mostra o plano de corte.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""exemplos (a ordem importa):
  1) ler a fala com os tempos:
     python cortar.py --transcricao palavras.json --texto
  2) mostrar o plano e esperar o OK do dono do vídeo (o plano termina com um código):
     python cortar.py --entrada bruto.mp4 --transcricao palavras.json --gancho 42.5-48.0 --inicio-corpo 12
  3) renderizar exatamente esse plano, depois do OK:
     python cortar.py --entrada bruto.mp4 --transcricao palavras.json --gancho 42.5-48.0 --inicio-corpo 12 --aprovado CODIGO""")
    g = ap.add_argument_group("arquivos e modo")
    g.add_argument("--entrada", help="vídeo de origem")
    g.add_argument("--transcricao", required=True, help="JSON com tempo por palavra")
    g.add_argument("--saida", help="MP4 de saída (padrão: <entrada>_corte.mp4 ao lado do vídeo)")
    g.add_argument("--texto", action="store_true", help="só imprime a fala com os tempos e sai")
    g.add_argument("--aprovado", metavar="CODIGO",
                   help="renderiza. Use o código impresso no fim do plano, só depois que o dono do "
                        "vídeo aprovar esse plano")
    g.add_argument("--sobrescrever", action="store_true", help="permite substituir o arquivo de saída")
    c = ap.add_argument_group("corte")
    c.add_argument("--gancho", default="", help="trechos do gancho em segundos, ex.: 42.5-48.0,50.2-51.6")
    c.add_argument("--inicio-corpo", type=float, default=0.0, help="onde o corpo começa (s)")
    c.add_argument("--fim-corpo", type=float, default=None, help="onde o corpo termina (s)")
    c.add_argument("--remover", default="", help="intervalos a tirar do meio da fala (vícios), ex.: 16.2-16.4")
    c.add_argument("--pausa", type=float, default=0.6, help="pausa a partir da qual há corte (s). Padrão 0.6")
    c.add_argument("--folga-antes", type=float, default=0.05, help="folga antes de cada trecho (s). Padrão 0.05")
    c.add_argument("--folga-depois", type=float, default=0.18,
                   help="folga depois de cada trecho (s). Padrão 0.18; suba para 0.22 se cortar fim de palavra")
    c.add_argument("--fade", type=float, default=0.03, help="fade de áudio em cada emenda (s). Padrão 0.03")
    l = ap.add_argument_group("legenda")
    l.add_argument("--sem-legenda", action="store_true", help="corta mas não queima legenda")
    l.add_argument("--palavras-por-legenda", type=int, default=5, help="máximo de palavras por bloco")
    l.add_argument("--fonte", default="Arial", help="nome da fonte (Arial em negrito)")
    l.add_argument("--tamanho-fonte", type=int, default=None, help="padrão 64 em 1920 de altura")
    l.add_argument("--cor-legenda", default="FFFF00", help="RRGGBB em hexadecimal. Padrão FFFF00 (amarelo)")
    l.add_argument("--linha-base", type=int, default=None,
                   help="y da linha de base da legenda. Padrão 1200 em 1920 (régua: 1150 a 1300)")
    s = ap.add_argument_group("saída")
    s.add_argument("--largura", type=int, default=1080)
    s.add_argument("--altura", type=int, default=1920)
    s.add_argument("--fps", type=int, default=30)
    s.add_argument("--crf", type=int, default=20, help="qualidade do x264 (menor = melhor). Padrão 20")
    s.add_argument("--recorte-x", type=float, default=0.5,
                   help="se a fonte não for vertical: 0 = recorta pela esquerda, 1 = pela direita. Padrão 0.5")
    s.add_argument("--hdr", choices=["auto", "sim", "nao"], default="auto",
                   help="converte HDR para SDR bt709. auto = só se a fonte for HDR")
    s.add_argument("--lufs", type=float, default=-14.0, help="loudness integrado alvo. Padrão -14")
    s.add_argument("--pico-verdadeiro", type=float, default=-1.5, help="teto de true peak em dB. Padrão -1.5")
    s.add_argument("--silencio-inicial", type=float, default=0.0,
                   help="segundos de silêncio (e de primeiro quadro parado) no início. 0.08 evita chiado "
                        "quando um agendador re-codifica o áudio. Padrão 0")
    return ap


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    args = montar_parser().parse_args()
    palavras, dur_json = carregar_palavras(args.transcricao)
    if args.texto:
        imprimir_texto(palavras, args.pausa)
        return
    if not args.entrada:
        erro("informe --entrada (ou use --texto só para ler a transcrição).")
    if not os.path.isfile(args.entrada):
        erro(f"vídeo não encontrado: {args.entrada}")
    args.entrada = os.path.abspath(args.entrada)
    if args.saida is None:
        base, _ = os.path.splitext(args.entrada)
        args.saida = base + "_corte.mp4"
    args.saida = os.path.abspath(args.saida)
    if args.palavras_por_legenda < 1:
        erro("--palavras-por-legenda precisa ser 1 ou mais.")
    if args.aprovado is not None:
        if os.path.exists(args.saida) and not args.sobrescrever:
            erro(f"'{args.saida}' já existe. Use --sobrescrever ou escolha outro --saida.")
        if not os.path.isdir(os.path.dirname(args.saida)):
            erro(f"a pasta de saída não existe: {os.path.dirname(args.saida)}")

    info = sondar(args.entrada)
    dur = info["duracao"] or dur_json or (palavras[-1]["e"] + 1.0)
    usar_hdr = args.hdr == "sim" or (args.hdr == "auto" and info["hdr"])
    gancho, corpo, total = montar_plano(args, palavras, dur)
    if len(gancho) + len(corpo) > MAX_TRECHOS:
        erro(f"{len(gancho) + len(corpo)} trechos: mais que o limite de {MAX_TRECHOS} por passada. "
             "Aumente --pausa ou divida o bruto em partes.")
    estilo = estilo_legenda(args)
    eventos = [] if args.sem_legenda else eventos_legenda(gancho + corpo, args, estilo["max_chars"])
    avisos = reunir_avisos(args, info, palavras, gancho, corpo, usar_hdr, estilo, total)
    codigo = codigo_plano(args, gancho + corpo, usar_hdr)
    imprimir_plano(args, info, palavras, gancho, corpo, total, eventos, estilo, usar_hdr, avisos, dur, codigo)
    if args.aprovado is None:
        return
    if args.aprovado != codigo:
        erro(f"o plano mudou desde a aprovação (código atual {codigo}, informado {args.aprovado}). "
             "Mostre o plano acima ao dono do vídeo e use o código novo depois do OK.")
    renderizar(args, gancho + corpo, estilo, eventos, usar_hdr)
    conferir_saida(args)


if __name__ == "__main__":
    main()
