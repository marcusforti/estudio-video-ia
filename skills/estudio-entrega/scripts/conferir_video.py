#!/usr/bin/env python3
"""Confere um vídeo final antes da entrega e gera relatório + folha de contato.

Mede: resolução, fps fixo, codec, pix_fmt, cor (bt709 ou HDR), faststart, erros de decodificação,
duração de vídeo x áudio, loudness integrado, pico real, quadros pretos e silêncio longo.
Com --roteiro (e --transcricao) compara a fala do vídeo com o roteiro.

Exemplos:
    python conferir_video.py video_v1.mp4
    python conferir_video.py video_v1.mp4 --roteiro ROTEIRO.md --transcricao transcricao_final.txt
    python conferir_video.py video_v1_whats.mp4 --resolucao 720x1280 --tamanho-max 30

Requer Python 3.10+, ffmpeg e ffprobe no PATH.
Código de saída: 0 aprovado, 1 reprovado, 2 erro de uso ou de ambiente.
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import re
import shutil
import struct
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

TOL_LUFS = 0.5   # tolerância de medição do loudness integrado, em LU
TOL_PICO = 0.2   # tolerância de medição do pico real, em dB
TRANSFERENCIAS_HDR = {"smpte2084", "arib-std-b67"}
SEM_FALA = ("sem voz", "take real", "silencio", "sem fala", "so musica")


# ---------------------------------------------------------------- utilidades

def rodar(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def numero(valor, padrao: float = 0.0) -> float:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao


def razao(valor) -> float:
    texto = str(valor or "")
    if "/" in texto:
        a, _, b = texto.partition("/")
        return numero(a) / numero(b, 1.0) if numero(b) else 0.0
    return numero(texto)


def fmt_tempo(t: float) -> str:
    t = round(t, 1)
    minutos, segundos = divmod(t, 60)
    texto = f"{int(minutos)}:{segundos:04.1f}".replace(".", ",")
    return texto[:-2] if texto.endswith(",0") else texto


def virgula(x: float, casas: int = 1) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def sem_acento(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------- medições

def sondar(ffprobe: str, video: Path):
    cod, saida, erro = rodar([ffprobe, "-v", "error", "-print_format", "json",
                              "-show_format", "-show_streams", str(video)])
    if cod != 0:
        return None, (erro.strip() or "ffprobe não conseguiu ler o arquivo")
    try:
        return json.loads(saida), ""
    except json.JSONDecodeError:
        return None, "saída do ffprobe ilegível"


def quadros_irregulares(ffprobe: str, video: Path) -> tuple[int, int]:
    """Conta intervalos entre quadros que fogem da mediana em mais de 25%. Devolve (irregulares, quadros)."""
    _, saida, _ = rodar([ffprobe, "-v", "error", "-select_streams", "v:0",
                         "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(video)])
    tempos = []
    for linha in saida.splitlines():
        try:
            tempos.append(float(linha.split(",")[0]))
        except ValueError:
            continue
    tempos.sort()
    if len(tempos) < 3:
        return 0, len(tempos)
    deltas = [b - a for a, b in zip(tempos, tempos[1:])]
    mediana = sorted(deltas)[len(deltas) // 2]
    if mediana <= 0:
        return len(deltas), len(tempos)
    return sum(1 for d in deltas if abs(d - mediana) > 0.25 * mediana), len(tempos)


def faststart(video: Path) -> bool | None:
    """True se o átomo 'moov' vem antes do 'mdat'. None se não for possível dizer."""
    ordem = []
    try:
        with open(video, "rb") as f:
            tamanho_arquivo = f.seek(0, 2)
            pos = 0
            while pos < tamanho_arquivo and len(ordem) < 64:
                f.seek(pos)
                cab = f.read(8)
                if len(cab) < 8:
                    break
                tam, tipo = struct.unpack(">I4s", cab)
                if tam == 1:
                    ext = f.read(8)
                    if len(ext) < 8:
                        break
                    tam = struct.unpack(">Q", ext)[0]
                elif tam == 0:
                    tam = tamanho_arquivo - pos
                if tam < 8:
                    break
                ordem.append(tipo.decode("latin-1"))
                pos += tam
    except OSError:
        return None
    if "moov" not in ordem or "mdat" not in ordem:
        return None
    return ordem.index("moov") < ordem.index("mdat")


def erros_de_decodificacao(ffmpeg: str, video: Path) -> tuple[int, list[str]]:
    cod, _, erro = rodar([ffmpeg, "-v", "error", "-nostdin", "-i", str(video), "-f", "null", "-"])
    return cod, [linha.strip() for linha in erro.splitlines() if linha.strip()]


def passada_de_deteccao(ffmpeg: str, video: Path, tem_video: bool, tem_audio: bool, args):
    """Uma passada só: quadros pretos, silêncio e loudness/pico (loudnorm em modo análise)."""
    cmd = [ffmpeg, "-hide_banner", "-nostats", "-nostdin", "-i", str(video)]
    if tem_video:
        cmd += ["-vf", f"blackdetect=d={args.preto_dur}:pic_th=0.98:pix_th=0.10"]
    if tem_audio:
        cmd += ["-af", f"silencedetect=noise={args.silencio_db}dB:d={args.silencio_dur},"
                       "loudnorm=I=-14:TP=-1:LRA=11:print_format=json"]
    cmd += ["-f", "null", "-"]
    return rodar(cmd)


def ler_pretos(log: str) -> list[tuple[float, float, float]]:
    achados = []
    for m in re.finditer(r"black_start:(\S+)\s+black_end:(\S+)\s+black_duration:(\S+)", log):
        achados.append((numero(m.group(1)), numero(m.group(2)), numero(m.group(3))))
    return achados


def ler_silencios(log: str, duracao: float) -> list[tuple[float, float, float]]:
    inicios: list[float] = []
    achados = []
    for linha in log.splitlines():
        m = re.search(r"silence_start:\s*(-?\d+(?:\.\d+)?)", linha)
        if m:
            inicios.append(max(0.0, float(m.group(1))))
            continue
        m = re.search(r"silence_end:\s*(-?\d+(?:\.\d+)?)\s*\|\s*silence_duration:\s*(\d+(?:\.\d+)?)", linha)
        if m and inicios:
            achados.append((inicios.pop(), float(m.group(1)), float(m.group(2))))
    for ini in inicios:  # silêncio que vai até o fim do arquivo
        achados.append((ini, duracao, max(0.0, duracao - ini)))
    return sorted(achados)


def ler_loudness(log: str):
    m = re.search(r'\{\s*"input_i"\s*:.*?\}', log, re.S)
    if not m:
        return None
    try:
        dados = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    return (numero(dados.get("input_i"), -99.0), numero(dados.get("input_tp"), -99.0),
            numero(dados.get("input_lra"), 0.0))


# ---------------------------------------------------------------- folha de contato

def folha_de_contato(ffmpeg: str, video: Path, pasta: Path, duracao: float, args) -> list[Path]:
    por_folha = args.colunas * args.linhas
    n_quadros = int(duracao // args.intervalo) + 1
    n_folhas = math.ceil(n_quadros / por_folha)
    criadas = []
    for k in range(n_folhas):
        inicio = k * por_folha * args.intervalo
        alvo = pasta / f"folha_{k + 1:02d}.jpg"
        cmd = [ffmpeg, "-hide_banner", "-v", "error", "-nostdin", "-y",
               "-ss", f"{inicio:.3f}", "-t", f"{por_folha * args.intervalo:.3f}", "-i", str(video),
               "-an", "-vf", f"fps=1/{args.intervalo},scale={args.largura_quadro}:-2,"
                             f"tile={args.colunas}x{args.linhas}:margin=3:padding=3:color=0x404040",
               "-frames:v", "1", "-update", "1", str(alvo)]
        rodar(cmd)
        if alvo.is_file() and alvo.stat().st_size > 0:
            criadas.append(alvo)
    ultimo = pasta / "ultimo_quadro.jpg"
    rodar([ffmpeg, "-hide_banner", "-v", "error", "-nostdin", "-y", "-sseof", "-0.3", "-i", str(video),
           "-an", "-vf", f"scale={args.largura_quadro * 2}:-2", "-frames:v", "1", "-update", "1", str(ultimo)])
    if ultimo.is_file() and ultimo.stat().st_size > 0:
        criadas.append(ultimo)
    return criadas


# ---------------------------------------------------------------- roteiro e transcrição

def dividir_linha_tabela(linha: str) -> list[str]:
    s = linha.strip().strip("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def fala_do_roteiro(texto: str) -> str:
    """Se o arquivo tiver uma tabela com coluna Fala (STORYBOARD.md), usa só ela; senão usa o texto corrido."""
    linhas = texto.splitlines()
    for i in range(len(linhas) - 1):
        if linhas[i].lstrip().startswith("|") and re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$",
                                                           linhas[i + 1].strip()):
            cab = [sem_acento(c).lower() for c in dividir_linha_tabela(linhas[i])]
            if "fala" in cab:
                idx = cab.index("fala")
                falas = []
                j = i + 2
                while j < len(linhas) and linhas[j].lstrip().startswith("|"):
                    celulas = dividir_linha_tabela(linhas[j])
                    if idx < len(celulas):
                        cel = celulas[idx]
                        limpa = re.sub(r"[^\w\s]", " ", sem_acento(cel).lower())
                        if cel.strip() and not " ".join(limpa.split()).startswith(SEM_FALA):
                            falas.append(cel)
                    j += 1
                return "\n".join(falas)
    limpo = re.sub(r"<!--.*?-->", " ", texto, flags=re.S)
    limpo = re.sub(r"```.*?```", " ", limpo, flags=re.S)
    limpo = re.sub(r"^\s*#.*$", " ", limpo, flags=re.M)
    limpo = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", limpo)
    return re.sub(r"[*_`>|]", " ", limpo)


def limpar_transcricao(texto: str) -> str:
    texto = re.sub(r"^\d+\s*$", " ", texto, flags=re.M)
    texto = re.sub(r"\d\d:\d\d:\d\d[,.]\d+\s*-->\s*\d\d:\d\d:\d\d[,.]\d+", " ", texto)
    return re.sub(r"^WEBVTT.*$", " ", texto, flags=re.M)


def tokens(texto: str) -> list[str]:
    return re.sub(r"[^\w\s]", " ", sem_acento(texto).lower()).split()


def palavras_de_risco(texto: str) -> dict[str, str]:
    achadas: dict[str, str] = {}
    for sentenca in re.split(r"(?<=[.!?:])\s+|\n", texto):
        palavras = re.findall(r"[A-Za-zÀ-ÿ0-9$%]+(?:[.,][0-9]+)?", sentenca)
        for i, p in enumerate(palavras):
            if re.search(r"\d", p):
                tipo = "número"
            elif len(p) >= 2 and p.isupper():
                tipo = "sigla"
            elif re.search(r"[a-zà-ÿ][A-ZÀ-Ý]", p):
                tipo = "marca"
            elif i > 0 and p[0].isupper() and len(p) > 2:
                tipo = "nome próprio"
            else:
                continue
            achadas.setdefault(p, tipo)
    return achadas


# ---------------------------------------------------------------- relatório

def montar_relatorio(video: Path, resumo: dict, itens: list, detalhes: list, arquivos: list[Path],
                     pasta: Path, intervalo: float, colunas: int) -> tuple[str, int, int]:
    falhas = sum(1 for n, *_ in itens if n == "FALHA")
    avisos = sum(1 for n, *_ in itens if n == "AVISO")
    veredito = "REPROVADO" if falhas else "APROVADO"
    L = [f"# Conferência: {video.name}", "",
         f"- Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
         f"- Arquivo: {video}",
         f"- Duração: {resumo['duracao']} · Tamanho: {resumo['tamanho']} · Container: {resumo['container']}", "",
         f"## Resultado: {veredito} ({falhas} falha(s), {avisos} aviso(s))", "",
         "| Status | Verificação | Medido | Esperado |", "|---|---|---|---|"]
    for nivel, nome, medido, esperado in itens:
        L.append(f"| {nivel} | {nome} | {medido} | {esperado} |")
    for titulo, linhas in detalhes:
        L += ["", f"## {titulo}", ""] + [f"- {x}" for x in linhas]
    if arquivos:
        L += ["", "## Folha de contato", "",
              f"Um quadro a cada {virgula(intervalo, 0 if intervalo == int(intervalo) else 1)} s, "
              f"da esquerda para a direita e de cima para baixo ({colunas} por linha). "
              "O primeiro quadro de cada folha é o instante inicial dela; "
              "`ultimo_quadro.jpg` é o quadro a ~0,3 s do fim.", ""]
        L += [f"- `{a.name}`" for a in arquivos]
    L += ["", f"Relatório salvo em `{pasta / 'relatorio.md'}`."]
    return "\n".join(L) + "\n", falhas, avisos


# ---------------------------------------------------------------- principal

def criar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Confere um vídeo final (arquivo, cor, áudio, quadros pretos, silêncio) e gera relatório "
                    "e folha de contato. Código de saída 0 = aprovado, 1 = reprovado, 2 = erro de uso.")
    ap.add_argument("video", help="caminho do MP4 (coloque antes das opções)")
    ap.add_argument("--roteiro", help="roteiro em texto ou STORYBOARD.md; lista palavras de risco")
    ap.add_argument("--transcricao", help="transcrição do vídeo FINAL (txt, srt ou vtt); exige --roteiro")
    ap.add_argument("--saida", help="pasta do relatório e das folhas (padrão: <pasta do vídeo>/qa/<nome>)")
    ap.add_argument("--intervalo", type=float, default=10.0, help="segundos entre quadros da folha (padrão 10)")
    ap.add_argument("--colunas", type=int, default=6, help="quadros por linha na folha (padrão 6)")
    ap.add_argument("--linhas", type=int, default=5, help="linhas por folha (padrão 5)")
    ap.add_argument("--largura-quadro", type=int, default=240, help="largura de cada quadro em px (padrão 240)")
    ap.add_argument("--sem-folha", action="store_true", help="não gera a folha de contato")
    ap.add_argument("--resolucao", nargs="+", default=["1080x1920", "1920x1080"], metavar="LxA",
                    help="resolução(ões) aceita(s) (padrão 1080x1920 1920x1080)")
    ap.add_argument("--fps", type=float, default=30.0, help="fps esperado (padrão 30)")
    ap.add_argument("--codec-video", default="h264", help="codec de vídeo esperado (padrão h264)")
    ap.add_argument("--codec-audio", default="aac", help="codec de áudio esperado (padrão aac)")
    ap.add_argument("--taxa-audio", type=int, default=48000, help="taxa de amostragem esperada em Hz (padrão 48000)")
    ap.add_argument("--lufs-min", type=float, default=-16.0, help="loudness integrado mínimo (padrão -16)")
    ap.add_argument("--lufs-max", type=float, default=-14.0, help="loudness integrado máximo (padrão -14)")
    ap.add_argument("--pico-max", type=float, default=-1.0, help="pico real máximo em dBTP (padrão -1)")
    ap.add_argument("--preto-dur", type=float, default=0.1, help="quadro preto a partir de N s (padrão 0,1)")
    ap.add_argument("--silencio-dur", type=float, default=2.0, help="silêncio longo a partir de N s (padrão 2)")
    ap.add_argument("--silencio-db", type=float, default=-40.0, help="nível abaixo do qual é silêncio (padrão -40)")
    ap.add_argument("--tamanho-max", type=float, help="tamanho máximo em MB (1 MB = 1.000.000 bytes)")
    ap.add_argument("--similaridade-min", type=float, default=0.95,
                    help="semelhança mínima entre transcrição e roteiro, de 0 a 1 (padrão 0,95)")
    return ap


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = criar_parser()
    args = ap.parse_args(argv)
    if args.transcricao and not args.roteiro:
        ap.error("--transcricao precisa de --roteiro")
    for r in args.resolucao:
        if not re.fullmatch(r"\d+[xX]\d+", r):
            ap.error(f"resolução inválida: {r} (use LARGURAxALTURA, ex.: 1080x1920)")
    if args.intervalo <= 0 or args.colunas < 1 or args.linhas < 1:
        ap.error("--intervalo, --colunas e --linhas precisam ser positivos")

    video = Path(args.video)
    if not video.is_file():
        print(f"erro: arquivo não encontrado: {video}", file=sys.stderr)
        return 2
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        print("erro: ffmpeg e ffprobe precisam estar no PATH", file=sys.stderr)
        return 2

    pasta = Path(args.saida) if args.saida else video.parent / "qa" / video.stem
    pasta.mkdir(parents=True, exist_ok=True)
    itens: list[tuple[str, str, str, str]] = []
    detalhes: list[tuple[str, list[str]]] = []

    def ver(nivel: str, nome: str, medido: str, esperado: str = "") -> None:
        itens.append((nivel, nome, medido, esperado))

    def progresso(msg: str) -> None:
        print(f"... {msg}", file=sys.stderr)

    progresso("lendo o arquivo")
    dados, erro = sondar(ffprobe, video)
    resumo = {"duracao": "?", "tamanho": "?", "container": "?"}
    arquivos: list[Path] = []
    duracao = 0.0
    if dados is None:
        ver("FALHA", "Leitura do arquivo", erro.splitlines()[-1] if erro else "ilegível", "arquivo legível")
    else:
        fmt = dados.get("format", {})
        streams = dados.get("streams", [])
        v = next((s for s in streams if s.get("codec_type") == "video"), None)
        a = next((s for s in streams if s.get("codec_type") == "audio"), None)
        duracao = numero(fmt.get("duration"))
        tamanho_mb = numero(fmt.get("size"), video.stat().st_size) / 1_000_000
        resumo = {"duracao": fmt_tempo(duracao), "tamanho": f"{virgula(tamanho_mb)} MB",
                  "container": fmt.get("format_name", "?")}

        if v is None:
            ver("FALHA", "Trilha de vídeo", "ausente", "uma trilha de vídeo")
        if a is None:
            ver("FALHA", "Trilha de áudio", "ausente", "uma trilha de áudio")

        if v is not None:
            largura, altura = int(v.get("width", 0)), int(v.get("height", 0))
            rotacao = 0
            for dado in v.get("side_data_list", []) or []:
                if "rotation" in dado:
                    rotacao = abs(int(numero(dado["rotation"]))) % 360
            if rotacao in (90, 270):
                largura, altura = altura, largura
                ver("AVISO", "Rotação", f"metadado de rotação {rotacao} graus", "sem rotação (grave a rotação no vídeo)")
            aceitas = [r.lower() for r in args.resolucao]
            medida = f"{largura}x{altura}"
            ver("OK" if medida in aceitas else "FALHA", "Resolução", medida, " ou ".join(aceitas))

            r_fps, media_fps = razao(v.get("r_frame_rate")), razao(v.get("avg_frame_rate"))
            irregulares, n_quadros = quadros_irregulares(ffprobe, video)
            fixo = irregulares == 0 and r_fps > 0 and abs(media_fps - r_fps) <= 0.005 * r_fps
            fps_ok = fixo and abs(r_fps - args.fps) <= 0.01
            ver("OK" if fps_ok else "FALHA", "FPS fixo",
                f"{virgula(r_fps, 3)} fps, {irregulares} intervalo(s) irregular(es) em {n_quadros} quadros",
                f"{virgula(args.fps, 0 if args.fps == int(args.fps) else 2)} fps constante")

            codec = v.get("codec_name", "?")
            ver("OK" if codec == args.codec_video else "FALHA", "Codec de vídeo", codec, args.codec_video)
            pix = v.get("pix_fmt", "?")
            ver("OK" if pix == "yuv420p" else "FALHA", "pix_fmt", pix, "yuv420p")

            espaco = v.get("color_space", "unknown")
            primarias = v.get("color_primaries", "unknown")
            transf = v.get("color_transfer", "unknown")
            if transf in TRANSFERENCIAS_HDR:
                ver("FALHA", "Cor", f"HDR (transferência {transf})", "SDR bt709")
            elif espaco == primarias == transf == "bt709":
                ver("OK", "Cor", "bt709 (espaço, primárias e transferência)", "bt709")
            else:
                ver("FALHA", "Cor", f"tags incompletas: espaço={espaco}, primárias={primarias}, transferência={transf}",
                    "bt709 nos três campos")

        if a is not None:
            codec_a = a.get("codec_name", "?")
            ver("OK" if codec_a == args.codec_audio else "FALHA", "Codec de áudio", codec_a, args.codec_audio)
            taxa = int(numero(a.get("sample_rate")))
            ver("OK" if taxa == args.taxa_audio else "FALHA", "Taxa de amostragem", f"{taxa} Hz", f"{args.taxa_audio} Hz")

        if v is not None and a is not None:
            dur_v, dur_a = numero(v.get("duration"), duracao), numero(a.get("duration"), duracao)
            dif = abs(dur_v - dur_a)
            ver("OK" if dif <= 0.2 else "FALHA", "Duração vídeo x áudio",
                f"vídeo {virgula(dur_v, 2)} s, áudio {virgula(dur_a, 2)} s (diferença {virgula(dif, 2)} s)",
                "diferença até 0,2 s")

        formato = str(fmt.get("format_name", ""))
        if "mp4" in formato or "mov" in formato:
            fs = faststart(video)
            if fs is None:
                ver("FALHA", "Faststart", "estrutura MP4 ilegível", "moov antes do mdat")
            else:
                ver("OK" if fs else "FALHA", "Faststart", "moov antes do mdat" if fs else "moov depois do mdat",
                    "moov antes do mdat")
        else:
            ver("AVISO", "Faststart", f"não se aplica ({formato})", "MP4 ou MOV")

        if args.tamanho_max is not None:
            ver("OK" if tamanho_mb <= args.tamanho_max else "FALHA", "Tamanho",
                f"{virgula(tamanho_mb)} MB", f"até {virgula(args.tamanho_max)} MB")
        else:
            ver("INFO", "Tamanho", f"{virgula(tamanho_mb)} MB", "")
        ver("INFO", "Duração", fmt_tempo(duracao), "")

        progresso("procurando erros de decodificação")
        cod, linhas_erro = erros_de_decodificacao(ffmpeg, video)
        if cod != 0 or linhas_erro:
            ver("FALHA", "Erros de decodificação", f"{len(linhas_erro)} linha(s) de erro", "nenhum erro")
            detalhes.append(("Erros de decodificação (primeiras 8 linhas)", linhas_erro[:8] or ["ffmpeg saiu com erro"]))
        else:
            ver("OK", "Erros de decodificação", "nenhum", "nenhum erro")

        progresso("medindo loudness, quadros pretos e silêncio")
        _, _, log = passada_de_deteccao(ffmpeg, video, v is not None, a is not None, args)
        if v is not None:
            pretos = [p for p in ler_pretos(log) if p[2] >= args.preto_dur - 1e-9]
            if pretos:
                ver("FALHA", "Quadros pretos", f"{len(pretos)} trecho(s)", f"nenhum trecho de {virgula(args.preto_dur)} s ou mais")
                detalhes.append(("Quadros pretos", [f"{fmt_tempo(i)} a {fmt_tempo(f)} ({virgula(d, 2)} s)" for i, f, d in pretos]))
            else:
                ver("OK", "Quadros pretos", "nenhum", f"nenhum trecho de {virgula(args.preto_dur)} s ou mais")
        if a is not None:
            silencios = [s for s in ler_silencios(log, duracao) if s[2] >= args.silencio_dur - 1e-9]
            esperado_sil = f"nenhum silêncio de {virgula(args.silencio_dur)} s ou mais (abaixo de {virgula(args.silencio_db, 0)} dB)"
            if silencios:
                ver("FALHA", "Silêncio longo", f"{len(silencios)} trecho(s)", esperado_sil)
                detalhes.append(("Silêncio longo", [f"{fmt_tempo(i)} a {fmt_tempo(f)} ({virgula(d, 1)} s)" for i, f, d in silencios]))
            else:
                ver("OK", "Silêncio longo", "nenhum", esperado_sil)
            medido = ler_loudness(log)
            if medido is None:
                ver("FALHA", "Loudness integrado", "não consegui medir", f"{virgula(args.lufs_min, 0)} a {virgula(args.lufs_max, 0)} LUFS")
                ver("FALHA", "Pico real", "não consegui medir", f"até {virgula(args.pico_max)} dBTP")
            else:
                lufs, pico, lra = medido
                faixa = f"{virgula(args.lufs_min, 1)} a {virgula(args.lufs_max, 1)} LUFS (±{virgula(TOL_LUFS)} de medição)"
                ok_l = args.lufs_min - TOL_LUFS <= lufs <= args.lufs_max + TOL_LUFS
                ver("OK" if ok_l else "FALHA", "Loudness integrado", f"{virgula(lufs, 1)} LUFS (LRA {virgula(lra, 1)})", faixa)
                ok_p = pico <= args.pico_max + TOL_PICO
                ver("OK" if ok_p else "FALHA", "Pico real", f"{virgula(pico, 1)} dBTP",
                    f"até {virgula(args.pico_max, 1)} dBTP (±{virgula(TOL_PICO)} de medição)")

    # roteiro e transcrição
    if args.roteiro:
        try:
            bruto = Path(args.roteiro).read_text(encoding="utf-8-sig")
        except OSError as e:
            print(f"erro: não consegui ler o roteiro: {e}", file=sys.stderr)
            return 2
        fala = fala_do_roteiro(bruto)
        risco = palavras_de_risco(fala)
        a_tok = tokens(fala)
        if not args.transcricao:
            ver("INFO", "Roteiro", f"{len(a_tok)} palavras", "")
            if risco:
                detalhes.append(("Palavras de risco para conferir na transcrição do final",
                                 [f"{p} ({t})" for p, t in sorted(risco.items())[:60]]))
        else:
            try:
                trans = limpar_transcricao(Path(args.transcricao).read_text(encoding="utf-8-sig"))
            except OSError as e:
                print(f"erro: não consegui ler a transcrição: {e}", file=sys.stderr)
                return 2
            b_tok = tokens(trans)
            if not a_tok or not b_tok:
                ver("FALHA", "Fala x roteiro", "texto vazio no roteiro ou na transcrição", "")
            else:
                sm = difflib.SequenceMatcher(None, a_tok, b_tok, autojunk=False)
                sim = sm.ratio()
                ver("OK" if sim >= args.similaridade_min else "FALHA", "Fala x roteiro",
                    f"{virgula(sim * 100, 1)}% de semelhança ({len(a_tok)} palavras no roteiro, {len(b_tok)} na transcrição)",
                    f"{virgula(args.similaridade_min * 100, 0)}% ou mais")
                difs = []
                for tag, i1, i2, j1, j2 in sm.get_opcodes():
                    if tag != "equal" and len(difs) < 12:
                        difs.append(f"roteiro: \"{' '.join(a_tok[i1:i2][:8])}\" | transcrição: \"{' '.join(b_tok[j1:j2][:8])}\"")
                if difs:
                    detalhes.append(("Diferenças entre roteiro e transcrição (até 12)", difs))
                conj = set(b_tok)
                ausentes = [p for p in sorted(risco) if (tokens(p) or [""])[0] not in conj]
                if ausentes:
                    ver("AVISO", "Palavras de risco", f"{len(ausentes)} ausente(s) na transcrição", "todas presentes")
                    detalhes.append(("Palavras de risco ausentes na transcrição", [f"{p} ({risco[p]})" for p in ausentes[:40]]))
                else:
                    ver("OK", "Palavras de risco", f"{len(risco)} presente(s) na transcrição", "todas presentes")

    # folha de contato
    if dados is not None and duracao > 0 and not args.sem_folha and any(
            s.get("codec_type") == "video" for s in dados.get("streams", [])):
        progresso("gerando a folha de contato")
        arquivos = folha_de_contato(ffmpeg, video, pasta, duracao, args)
        if not arquivos:
            ver("AVISO", "Folha de contato", "não foi possível gerar", "folha gerada")

    texto, falhas, _ = montar_relatorio(video, resumo, itens, detalhes, arquivos, pasta,
                                        args.intervalo, args.colunas)
    (pasta / "relatorio.md").write_text(texto, encoding="utf-8")
    print(texto, end="")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
