#!/usr/bin/env python3
"""Valida a folha de storyboard (STORYBOARD.md) do Estúdio de Vídeo com IA.

Confere: colunas obrigatórias, ids únicos, tempo crescente e sem buraco, cena acima do teto,
gatilho presente na fala, tipo válido, simulação com selo "exemplo", texto em tela de até
2 linhas (separadas por <br> ou " · "), status válido e rodapé de contagem.

Exemplos:
    python checar_storyboard.py STORYBOARD.md
    python checar_storyboard.py STORYBOARD.md --teto 3     # VSL: nenhuma cena acima de 3 s

Código de saída: 0 aprovado, 1 reprovado, 2 arquivo ilegível.
Usa só a biblioteca padrão (Python 3.10+).
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

OBRIGATORIAS = {
    "id": "#",
    "tempo": "Tempo",
    "fala": "Fala",
    "gatilho": "Gatilho",
    "tipo": "Tipo",
    "visual": "Visual",
    "texto": "Texto em tela",
    "origem": "Origem do asset",
    "status": "Status",
}

# (chave, apelido normalizado): do mais específico para o mais geral
APELIDOS = [
    ("texto", "texto em tela"), ("origem", "origem do asset"), ("nota", "nota do portao"),
    ("camera", "camera / transicao"), ("camera", "camera e transicao"),
    ("camera", "camera"), ("camera", "transicao"),
    ("id", "#"), ("id", "id"), ("id", "cena"),
    ("bloco", "bloco"), ("tempo", "tempo"), ("fala", "fala"), ("gatilho", "gatilho"),
    ("tipo", "tipo"), ("visual", "visual"), ("som", "som"), ("checagens", "checagens"),
    ("status", "status"), ("texto", "texto"), ("origem", "origem"), ("nota", "nota"),
]

TIPOS_VALIDOS = {"R", "IA", "B", "M", "T", "S"}
STATUS_VALIDOS = ("outline", "imagem aprovada", "construido", "animado", "conferido")
VAZIOS = {"", "-", "–", "—", "nenhum", "(nenhum)", "n/a", "sem texto"}
SEM_FALA = ("sem voz", "take real", "silencio", "sem fala", "so musica")
SEPARADOR = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$")


def sem_acento(txt: str) -> str:
    decomposto = unicodedata.normalize("NFD", txt)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def basico(txt: str) -> str:
    """Minúsculas, sem acento, sem marcas de markdown, espaços colapsados."""
    t = sem_acento(txt).lower().replace("*", "").replace("`", "")
    return " ".join(t.split())


def so_palavras(txt: str) -> str:
    t = basico(re.sub(r"<br\s*/?>", " ", txt, flags=re.I))
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(t.split())


def cena_muda(fala: str) -> bool:
    """True quando a coluna Fala descreve uma cena sem voz (silêncio, take real, só música)."""
    return not fala.strip() or so_palavras(fala).startswith(SEM_FALA)


def dividir(linha: str) -> list[str]:
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.replace("\\|", "|").strip() for c in re.split(r"(?<!\\)\|", s)]


def chave_coluna(cabecalho: str) -> str | None:
    n = basico(cabecalho)
    for chave, apelido in APELIDOS:
        if n == apelido or n.startswith(apelido + " ") or n.startswith(apelido + "("):
            return chave
    return None


def instante(txt: str) -> float | None:
    t = txt.strip().replace(",", ".")
    if not re.fullmatch(r"\d+(:\d{1,2}){0,2}(\.\d+)?", t):
        return None
    total = 0.0
    for parte in t.split(":"):
        total = total * 60 + float(parte)
    return total


def intervalo(celula: str) -> tuple[float, float] | None:
    m = re.match(r"^\s*~?\s*(\S+?)\s*[-–—]\s*(\S+?)\s*s?\s*$", celula)
    if not m:
        return None
    ini, fim = instante(m.group(1)), instante(m.group(2))
    if ini is None or fim is None:
        return None
    return ini, fim


def fmt(t: float) -> str:
    t = round(t, 1)
    minutos, segundos = divmod(t, 60)
    texto = f"{int(minutos)}:{segundos:04.1f}".replace(".", ",")
    return texto[:-2] if texto.endswith(",0") else texto


def fmt_s(t: float) -> str:
    return f"{t:.1f}".replace(".", ",")


def ler_tabela(linhas: list[str]):
    for i in range(len(linhas) - 1):
        if not linhas[i].lstrip().startswith("|"):
            continue
        if not SEPARADOR.match(linhas[i + 1].strip()):
            continue
        cabecalho = dividir(linhas[i])
        chaves = [chave_coluna(c) for c in cabecalho]
        if "tempo" in chaves and "fala" in chaves:
            corpo = []
            j = i + 2
            while j < len(linhas) and linhas[j].lstrip().startswith("|"):
                corpo.append((j + 1, dividir(linhas[j])))
                j += 1
            return cabecalho, chaves, corpo
    return None


def tipo_normalizado(txt: str) -> tuple[str, ...]:
    return tuple(p.strip().upper() for p in txt.split("+"))


def ler_rodape(linhas: list[str]):
    achado = None
    for linha in linhas:
        if linha.lstrip().startswith("|"):
            continue
        limpa = linha.replace("*", "").replace("`", "")
        m = re.search(r"(?i)contagem\s*:\s*(\d+)\s*cenas?\s*[=:]?\s*(.*)$", limpa)
        if m:
            achado = m
    if achado is None:
        return None
    total = int(achado.group(1))
    contagem: Counter = Counter()
    for tipo, qtd in re.findall(r"([A-Za-z]+(?:\s*\+\s*[A-Za-z]+)*)\s+(\d+)", achado.group(2)):
        chave = "+".join(sorted(tipo_normalizado(tipo)))
        contagem[chave] += int(qtd)
    return total, contagem


def validar(texto: str, teto: float, tolerancia: float):
    """Devolve (resumo, verificações, avisos). Cada verificação é (nome, [detalhes])."""
    linhas = texto.splitlines()
    achada = ler_tabela(linhas)
    if achada is None:
        return "", [("Tabela de cenas", [
            "nenhuma tabela com as colunas Tempo e Fala foi encontrada"])], []
    cabecalho, chaves, corpo = achada

    avisos = []
    desconhecidas = [c for c, k in zip(cabecalho, chaves) if k is None]
    if desconhecidas:
        avisos.append("colunas que não reconheço (ignoradas): " + ", ".join(desconhecidas))

    faltando = [nome for chave, nome in OBRIGATORIAS.items() if chave not in chaves]
    if faltando:
        return "", [("Colunas obrigatórias", ["faltam: " + ", ".join(faltando)])], avisos

    cenas = []
    estrutura = []
    for num, celulas in corpo:
        if not any(c.strip() for c in celulas):
            continue
        if len(celulas) > len(cabecalho):
            estrutura.append(f"linha {num}: {len(celulas)} células para {len(cabecalho)} colunas "
                             "(um | solto no texto? escape com \\|)")
        celulas = celulas + [""] * (len(cabecalho) - len(celulas))
        reg = {"_linha": num}
        for chave, valor in zip(chaves, celulas):
            if chave and chave not in reg:
                reg[chave] = valor
        cenas.append(reg)

    verificacoes: list[tuple[str, list[str]]] = [("Colunas obrigatórias", [])]
    if not cenas:
        verificacoes.append(("Cenas preenchidas", ["nenhuma cena preenchida na tabela"]))
        return "", verificacoes, avisos
    verificacoes.append(("Estrutura da tabela", estrutura))

    def nome_cena(reg) -> str:
        return f"{reg.get('id') or '?'} (linha {reg['_linha']})"

    # células obrigatórias
    vazias = []
    for reg in cenas:
        for chave, nome in OBRIGATORIAS.items():
            valor = reg.get(chave, "").strip()
            if valor:
                continue
            if chave == "gatilho" and cena_muda(reg.get("fala", "")):
                continue
            vazias.append(f"{nome_cena(reg)}: coluna {nome} vazia")
    verificacoes.append(("Células obrigatórias preenchidas", vazias))

    # ids únicos
    vistos: dict[str, int] = {}
    repetidos = []
    for reg in cenas:
        cid = reg.get("id", "").strip()
        if not cid:
            continue
        if cid in vistos:
            repetidos.append(f"id {cid} repetido (linhas {vistos[cid]} e {reg['_linha']})")
        else:
            vistos[cid] = reg["_linha"]
    verificacoes.append(("Ids únicos", repetidos))

    # tempo e teto
    erros_tempo, erros_teto = [], []
    anterior_fim = None
    primeiro = True
    inicio_total = fim_total = None
    for reg in cenas:
        par = intervalo(reg.get("tempo", ""))
        if par is None:
            erros_tempo.append(f"{nome_cena(reg)}: tempo '{reg.get('tempo', '')}' fora do formato "
                               "início-fim (ex.: 0:03,8-0:08)")
            anterior_fim = None
            primeiro = False
            continue
        ini, fim = par
        if fim <= ini:
            erros_tempo.append(f"{nome_cena(reg)}: o fim ({fmt(fim)}) não é maior que o início ({fmt(ini)})")
        if primeiro and abs(ini) > tolerancia:
            erros_tempo.append(f"{nome_cena(reg)}: a primeira cena começa em {fmt(ini)}, não em 0:00")
        if anterior_fim is not None:
            folga = ini - anterior_fim
            if folga > tolerancia:
                erros_tempo.append(f"{nome_cena(reg)}: buraco de {fmt_s(folga)} s depois da cena anterior")
            elif folga < -tolerancia:
                erros_tempo.append(f"{nome_cena(reg)}: começa {fmt_s(-folga)} s antes do fim da cena anterior "
                                   "(tempo não crescente)")
        duracao = fim - ini
        if duracao - teto > 0.001:
            erros_teto.append(f"{nome_cena(reg)}: dura {fmt_s(duracao)} s")
        if inicio_total is None:
            inicio_total = ini
        fim_total = fim
        anterior_fim = fim
        primeiro = False
    verificacoes.append(("Tempo crescente e sem buraco", erros_tempo))
    verificacoes.append((f"Cena acima do teto de {fmt_s(teto)} s", erros_teto))

    # gatilho
    erros_gatilho = []
    for reg in cenas:
        fala = reg.get("fala", "")
        gatilho = reg.get("gatilho", "").strip()
        if cena_muda(fala):
            continue
        if basico(gatilho) in VAZIOS:
            erros_gatilho.append(f"{nome_cena(reg)}: gatilho vazio (a cena tem fala)")
        elif f" {so_palavras(gatilho)} " not in f" {so_palavras(fala)} ":
            erros_gatilho.append(f"{nome_cena(reg)}: o gatilho '{gatilho}' não aparece na fala")
    verificacoes.append(("Gatilho presente na fala", erros_gatilho))

    # tipo
    erros_tipo = []
    for reg in cenas:
        tipo = reg.get("tipo", "").strip()
        if not tipo:
            continue
        invalidos = [p for p in tipo_normalizado(tipo) if p not in TIPOS_VALIDOS]
        if invalidos:
            erros_tipo.append(f"{nome_cena(reg)}: tipo '{tipo}' inválido "
                              "(use R, IA, B, M, T, S, ou combine com +)")
    verificacoes.append(("Tipo válido", erros_tipo))

    # simulação com selo
    erros_selo = []
    for reg in cenas:
        if "S" in tipo_normalizado(reg.get("tipo", "")) and "exemplo" not in basico(reg.get("texto", "")):
            erros_selo.append(f"{nome_cena(reg)}: simulação (S) sem o selo \"exemplo\" no texto em tela")
    verificacoes.append(("Simulação com selo exemplo", erros_selo))

    # texto em tela
    erros_texto = []
    for reg in cenas:
        texto_tela = reg.get("texto", "").strip()
        if basico(texto_tela) in VAZIOS:
            continue
        partes = [p for p in re.split(r"<br\s*/?>|\\n|\s\u00b7\s", texto_tela, flags=re.I) if p.strip()]
        if len(partes) > 2:
            erros_texto.append(f"{nome_cena(reg)}: texto em tela com {len(partes)} linhas (máximo 2)")
    verificacoes.append(("Texto em tela de até 2 linhas", erros_texto))

    # status
    erros_status = []
    for reg in cenas:
        status = reg.get("status", "").strip()
        if status and basico(status) not in STATUS_VALIDOS:
            erros_status.append(f"{nome_cena(reg)}: status '{status}' inválido "
                                "(outline, imagem aprovada, construído, animado, conferido)")
    verificacoes.append(("Status válido", erros_status))

    # rodapé
    erros_rodape = []
    rodape = ler_rodape(linhas)
    if rodape is None:
        erros_rodape.append("rodapé ausente. Escreva, depois da tabela, uma linha como: "
                            "**Contagem:** 10 cenas = R 3, M 7")
    else:
        total, contagem = rodape
        real: Counter = Counter()
        for reg in cenas:
            tipo = reg.get("tipo", "").strip()
            if tipo:
                real["+".join(sorted(tipo_normalizado(tipo)))] += 1
        if total != len(cenas):
            erros_rodape.append(f"o rodapé diz {total} cenas, a tabela tem {len(cenas)}")
        if not contagem:
            erros_rodape.append("o rodapé não traz a contagem por tipo (ex.: R 3, M 7)")
        elif contagem != real:
            for tipo in sorted(set(contagem) | set(real)):
                if contagem.get(tipo, 0) != real.get(tipo, 0):
                    erros_rodape.append(f"tipo {tipo}: o rodapé diz {contagem.get(tipo, 0)}, "
                                        f"a tabela tem {real.get(tipo, 0)}")
    verificacoes.append(("Rodapé de contagem", erros_rodape))

    resumo = f"{len(cenas)} cenas"
    if inicio_total is not None and fim_total is not None:
        resumo += f", {fmt(inicio_total)} a {fmt(fim_total)}"
    return resumo, verificacoes, avisos


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(
        description="Valida a folha de storyboard (STORYBOARD.md). Código de saída 0 = aprovado, 1 = reprovado.")
    ap.add_argument("arquivo", help="caminho do STORYBOARD.md")
    ap.add_argument("--teto", type=float, default=5.0,
                    help="duração máxima de uma cena, em segundos (padrão 5; use 3 em VSL)")
    ap.add_argument("--tolerancia", type=float, default=0.05,
                    help="folga, em segundos, entre o fim de uma cena e o início da seguinte (padrão 0,05)")
    args = ap.parse_args(argv)

    try:
        texto = Path(args.arquivo).read_text(encoding="utf-8-sig")
    except OSError as erro:
        print(f"erro: não consegui ler {args.arquivo}: {erro}", file=sys.stderr)
        return 2

    resumo, verificacoes, avisos = validar(texto, args.teto, args.tolerancia)
    print(f"checar_storyboard: {args.arquivo}" + (f" ({resumo})" if resumo else ""))
    reprovadas = 0
    for nome, detalhes in verificacoes:
        print(f"[{'FALHA' if detalhes else 'OK   '}] {nome}")
        for detalhe in detalhes:
            print(f"        {detalhe}")
        reprovadas += 1 if detalhes else 0
    for aviso in avisos:
        print(f"[AVISO] {aviso}")
    if reprovadas:
        print(f"RESULTADO: REPROVADO ({reprovadas} verificação(ões) com falha)")
        return 1
    print("RESULTADO: APROVADO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
