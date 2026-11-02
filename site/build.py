#!/usr/bin/env python3
"""Gera o site estático em site/dist a partir de conhecimento/, modelos/ e skills/.

Uso: python site/build.py
Depende de: pip install markdown
"""
import json
import re
import shutil
import sys
import zipfile
from html import escape
from pathlib import Path

import markdown

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
from diagramas import DIAGRAMAS  # noqa: E402

DIST = AQUI / "dist"
REPO = "https://github.com/marcusforti/estudio-video-ia"
SITE = "https://estudio-video-ia.marcusforti2.workers.dev"

PAGINAS = [
    ("comece-aqui", "00-comece-aqui.md", "Comece aqui"),
    ("workflow", "01-workflow-completo.md", "Workflow completo"),
    ("folha-de-rosto", "02-folha-de-rosto.md", "Folha de rosto"),
    ("storyboard", "03-folha-de-storyboard.md", "Folha de storyboard"),
    ("edicao", "04-edicao-e-corte.md", "Edição e corte"),
    ("voz-local", "05-voz-local.md", "Voz local"),
    ("gpu", "06-gpu-como-local.md", "GPU como local"),
    ("lip-sync", "07-lip-sync.md", "Lip sync"),
    ("motion", "08-motion.md", "Motion"),
    ("escolhermotion", "09-escolhermotion.md", "/escolhermotion"),
    ("conferencia", "10-conferencia-e-entrega.md", "Conferência e entrega"),
    ("licencas", "11-licencas-e-consentimento.md", "Licenças e consentimento"),
    ("pesquisa", "12-pesquisa-estado-da-arte.md", "Pesquisa completa"),
    ("grafo", "13-grafo.md", "Análise do grafo"),
]
SLUG_POR_ARQUIVO = {arq: slug for slug, arq, _ in PAGINAS}

SELOS = {
    "testado": "testado aqui",
    "oficial": "fonte oficial",
    "fornecedor": "o fornecedor diz",
    "independente": "medição independente",
    "praticante": "opinião de quem faz",
    "sem medição": "sem medição",
}

IMAGEM_SKILL = {
    "estudio-workflow": ("claquete.jpg", "60% 40%"),
    "estudio-folha-de-rosto": ("mesa-moviola.jpg", "50% 20%"),
    "estudio-storyboard": ("storyboard-desenhado.jpg", "20% 20%"),
    "estudio-corte": ("mesa-de-luz.jpg", "30% 30%"),
    "estudio-voz-local": ("projetor-poster.jpg", "50% 50%"),
    "estudio-gpu": ("arquivo-de-filmes.jpg", "20% 60%"),
    "estudio-lipsync": ("mesa-moviola.jpg", "60% 80%"),
    "estudio-motion": ("storyboard-desenhado.jpg", "80% 60%"),
    "estudio-escolher-motion": ("mesa-de-luz.jpg", "50% 85%"),
    "estudio-entrega": ("arquivo-de-filmes.jpg", "70% 50%"),
}


def ler_frontmatter(caminho):
    texto = caminho.read_text(encoding="utf-8")
    achado = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    dados = {}
    if achado:
        chave = None
        for linha in achado.group(1).splitlines():
            par = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", linha)
            if par:
                chave = par.group(1)
                dados[chave] = par.group(2).strip().strip("\"'")
            elif chave and linha.startswith(" "):
                dados[chave] = (dados[chave] + " " + linha.strip()).strip()
    return dados


def carregar_skills():
    skills = []
    for pasta in sorted((RAIZ / "skills").glob("*/")):
        arquivo = pasta / "SKILL.md"
        if not arquivo.exists():
            continue
        dados = ler_frontmatter(arquivo)
        scripts = sorted(p.name for p in (pasta / "scripts").glob("*.py")) if (pasta / "scripts").exists() else []
        skills.append(
            {
                "nome": dados.get("name", pasta.name),
                "pasta": pasta.name,
                "descricao": dados.get("description", ""),
                "arquivos": sum(1 for p in pasta.rglob("*") if p.is_file() and "__pycache__" not in p.parts),
                "scripts": scripts,
            }
        )
    return skills


def compactar(destino, itens):
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for origem, prefixo in itens:
            if origem.is_file():
                z.write(origem, f"{prefixo}/{origem.name}")
                continue
            for arq in sorted(origem.rglob("*")):
                if arq.is_file() and "__pycache__" not in arq.parts:
                    z.write(arq, f"{prefixo}/{arq.relative_to(origem).as_posix()}")


def gerar_downloads(skills):
    pasta = DIST / "baixar"
    pasta.mkdir(parents=True)
    for s in skills:
        destino = pasta / f"{s['pasta']}.zip"
        compactar(destino, [(RAIZ / "skills" / s["pasta"], s["pasta"])])
        s["kb"] = round(destino.stat().st_size / 1024)
    compactar(
        pasta / "estudio-video-ia-skills.zip",
        [(RAIZ / "skills" / s["pasta"], s["pasta"]) for s in skills],
    )
    compactar(pasta / "modelos.zip", [(RAIZ / "modelos", "modelos")])


def trocar_fora_de_codigo(html_texto, funcao):
    partes = re.split(r"(<pre>.*?</pre>|<code>.*?</code>)", html_texto, flags=re.S)
    return "".join(p if i % 2 else funcao(p) for i, p in enumerate(partes))


def selos(texto):
    def um(m):
        chave = m.group(1)
        classe = "sem-medicao" if chave == "sem medição" else chave
        return f'<span class="selo selo-{classe}">{SELOS[chave]}</span>'

    return re.sub(r"\[(" + "|".join(SELOS) + r")\]", um, texto)


def ajustar_links(html_texto):
    def href(m):
        alvo = m.group(1)
        if alvo.startswith(("http://", "https://")):
            return f'href="{alvo}" target="_blank" rel="noopener"'
        interno = re.match(r"^(?:\./)?(\d\d-[\w-]+\.md)(#.*)?$", alvo)
        if interno and interno.group(1) in SLUG_POR_ARQUIVO:
            return f'href="/{SLUG_POR_ARQUIVO[interno.group(1)]}/{interno.group(2) or ""}"'
        relativo = re.match(r"^(?:\.\./)+((?:modelos|skills)/[^#\"]*)$", alvo)
        if relativo:
            tipo = "tree" if relativo.group(1).endswith("/") else "blob"
            return f'href="{REPO}/{tipo}/main/{relativo.group(1)}" target="_blank" rel="noopener"'
        return f'href="{alvo}"'

    return re.sub(r'href="([^"]+)"', href, html_texto)


def renderizar_md(caminho):
    texto = caminho.read_text(encoding="utf-8")
    texto = re.sub(r"^---\s*\n.*?\n---\s*\n", "", texto, flags=re.S)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
        extension_configs={"toc": {"toc_depth": "2-2"}},
    )
    corpo = md.convert(texto)
    corpo = trocar_fora_de_codigo(corpo, selos)
    corpo = ajustar_links(corpo)
    corpo = re.sub(r"<table>", '<div class="tabela" tabindex="0"><table>', corpo)
    corpo = corpo.replace("</table>", "</table></div>")

    def diagrama(m):
        nome = m.group(1)
        if nome not in DIAGRAMAS:
            raise SystemExit(f"Diagrama sem desenho: {nome} em {caminho.name}")
        return DIAGRAMAS[nome]()

    corpo = re.sub(r"<!--\s*diagrama:([\w-]+)\s*-->", diagrama, corpo)
    titulo = re.search(r"<h1[^>]*>(.*?)</h1>", corpo, re.S)
    titulo_txt = re.sub(r"<[^>]+>", "", titulo.group(1)) if titulo else caminho.stem
    corpo = re.sub(r"<h1[^>]*>.*?</h1>", "", corpo, count=1, flags=re.S)
    entrada = md.toc_tokens
    return titulo_txt, corpo, entrada


def resumo_de(corpo):
    primeiro = re.search(r"<p>(.*?)</p>", corpo, re.S)
    texto = re.sub(r"<[^>]+>", "", primeiro.group(1)) if primeiro else ""
    return (texto[:157] + "...") if len(texto) > 160 else texto


def abas(ativa, sumario=None):
    linhas = []
    for slug, _, nome in PAGINAS:
        marcada = ' aria-current="page"' if slug == ativa else ""
        linhas.append(f'<li><a href="/{slug}/"{marcada}>{escape(nome)}</a>')
        if slug == ativa and sumario:
            linhas.append('<ul class="sumario">')
            for item in sumario:
                nome_item = re.sub(r"<[^>]+>", "", item["name"])
                linhas.append(f'<li><a href="#{item["id"]}">{nome_item}</a></li>')
            linhas.append("</ul>")
        linhas.append("</li>")
    extra = ' aria-current="page"' if ativa == "skills" else ""
    linhas.append(f'<li><a class="aba-baixar" href="/skills/"{extra}>Baixar as skills</a></li>')
    return "\n".join(linhas)


def pagina_doc(modelo, titulo, corpo, ativa, sumario=None, descricao="", rodape_nav="", classe=""):
    html_final = modelo
    trocas = {
        "{{titulo}}": escape(titulo),
        "{{descricao}}": escape(descricao or titulo, quote=True),
        "{{abas}}": abas(ativa, sumario),
        "{{corpo}}": corpo,
        "{{rodape_nav}}": rodape_nav,
        "{{classe}}": classe,
        "{{url}}": f"{SITE}/{ativa}/",
    }
    for chave, valor in trocas.items():
        html_final = html_final.replace(chave, valor)
    return html_final


def gravar(rota, conteudo):
    destino = DIST / rota / "index.html" if rota else DIST / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def tiles_skills(skills):
    pares = ["par-a", "par-b", "par-c", "par-d"]
    saida = []
    for i, s in enumerate(skills):
        img, foco = IMAGEM_SKILL.get(s["pasta"], ("claquete.jpg", "50% 50%"))
        curta = s["nome"].removeprefix("estudio-").replace("-", " ")
        saida.append(
            f'<li class="tile"><div class="tile-foto"><img src="/static/img/{img}" alt="" loading="lazy" '
            f'width="600" height="750" style="object-position:{foco}"></div>'
            f'<div class="tile-etiqueta {pares[i % 4]}"><strong>{escape(curta)}</strong>'
            f'<span class="tile-linha"><a href="/baixar/{s["pasta"]}.zip">Baixar zip</a>'
            f'<a href="/skills/#{s["pasta"]}">O que faz</a></span>'
            f'<span class="tile-linha"><span>{s["arquivos"]} arquivos</span><span>{s["kb"]} KB</span></span>'
            f"</div></li>"
        )
    return "\n".join(saida)


def gavetas():
    grupos = [
        ("Planejar", "Como organizo um projeto antes de abrir a linha do tempo?",
         "As folhas decidem o vídeo antes do render: público, voz, vetos, cena por cena.",
         ["workflow", "folha-de-rosto", "storyboard"]),
        ("Cortar", "Como transformo um bruto em Reel legendado?",
         "Corte por palavra, gancho, legenda dentro da área segura e loudness medido.",
         ["edicao"]),
        ("Voz", "Dá para clonar voz sem depender de serviço pago?",
         "Dá, com autorização por escrito. A amostra decide quase tudo e a licença do modelo decide o uso.",
         ["voz-local"]),
        ("Máquina", "Como uso uma GPU alugada como se fosse meu PC?",
         "Alugar, entrar, rodar sem depender do SSH, baixar, conferir e destruir.",
         ["gpu"]),
        ("Boca", "Lip sync: local ou pago?",
         "Modelos abertos testados em GPU alugada, serviços pagos com preço por minuto e o teste do pior plano.",
         ["lip-sync"]),
        ("Motion", "Como fazer motion em código que não parece template?",
         "Conceito antes de efeito, ritmo, área segura, receitas e 703 prompts de referência.",
         ["motion", "escolhermotion"]),
        ("Entregar", "O que confiro antes de mostrar?",
         "Transcrição do arquivo final, rosto livre, loudness, versões derivadas, licenças e autorizações.",
         ["conferencia", "licencas"]),
        ("Evidência", "De onde vem tudo isso?",
         "Pesquisa com mais de 400 links e o grafo que mostra como os assuntos se ligam.",
         ["pesquisa", "grafo"]),
    ]
    nomes = {slug: nome for slug, _, nome in PAGINAS}
    saida = []
    for i, (aba, pergunta, resposta, rotas) in enumerate(grupos):
        links = "".join(f'<a href="/{r}/">{escape(nomes[r])}</a>' for r in rotas)
        aberto = " open" if i == 0 else ""
        saida.append(
            f'<details class="gaveta gaveta-{i % 3}" name="gavetas" style="--passo:{i}"{aberto}>'
            f'<summary><span class="gaveta-aba">{aba}</span><span class="gaveta-pergunta">{pergunta}</span></summary>'
            f'<div class="gaveta-corpo"><p>{resposta}</p><p class="gaveta-links">{links}</p></div></details>'
        )
    return "\n".join(saida)


def pagina_skills(skills):
    linhas = [
        '<p class="abertura-doc">São skills para Claude Code e Codex. Cada uma é uma pasta com instruções e, '
        "quando faz sentido, scripts. Você instala uma vez e chama pelo nome, como <code>/estudio-workflow</code>.</p>",
        '<h2 id="instalar">Instalar tudo de uma vez</h2>',
        "<p>No Windows, abra o PowerShell e cole:</p>",
        "<pre><code>irm https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.ps1 | iex</code></pre>",
        "<p>No Linux ou macOS:</p>",
        "<pre><code>curl -fsSL https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.sh | bash</code></pre>",
        "<p>O instalador copia as pastas para <code>~/.claude/skills</code> e <code>~/.codex/skills</code>. "
        "Abra uma sessão nova depois de instalar. Skill com o mesmo nome é substituída, a versão antiga vai para <code>~/.estudio-video-ia-backup</code>, e nenhuma outra é tocada.</p>",
        '<h2 id="manual">Baixar manualmente</h2>',
        '<p class="botoes"><a class="botao" href="/baixar/estudio-video-ia-skills.zip">Todas as skills em zip</a> '
        '<a class="botao botao-2" href="/baixar/modelos.zip">Só as folhas em branco</a> '
        f'<a class="botao botao-2" href="{REPO}" target="_blank" rel="noopener">Repositório no GitHub</a></p>',
        "<p>Para instalar um zip à mão, descompacte em <code>~/.claude/skills/</code>. A pasta final deve ser "
        "<code>~/.claude/skills/estudio-workflow/SKILL.md</code>.</p>",
        '<h2 id="lista">As skills, uma a uma</h2>',
    ]
    for s in skills:
        scripts = ""
        if s["scripts"]:
            nomes = ", ".join(f"<code>{escape(n)}</code>" for n in s["scripts"])
            scripts = f"<p><strong>Scripts:</strong> {nomes}</p>"
        linhas.append(
            f'<section class="ficha-skill" id="{s["pasta"]}"><h3>{escape(s["nome"])}</h3>'
            f"<p>{escape(s['descricao'])}</p>{scripts}"
            f'<p class="botoes"><a class="botao" href="/baixar/{s["pasta"]}.zip">Baixar zip ({s["kb"]} KB)</a> '
            f'<a class="botao botao-2" href="{REPO}/tree/main/skills/{s["pasta"]}" target="_blank" rel="noopener">Ver no GitHub</a></p></section>'
        )
    return "\n".join(linhas)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(AQUI / "static", DIST / "static")

    skills = carregar_skills()
    ordem = list(IMAGEM_SKILL)
    skills.sort(key=lambda s: ordem.index(s["pasta"]) if s["pasta"] in ordem else len(ordem))
    gerar_downloads(skills)
    modelo = (AQUI / "modelo.html").read_text(encoding="utf-8")

    existentes = [(s, a, n) for s, a, n in PAGINAS if (RAIZ / "conhecimento" / a).exists()]
    for i, (slug, arquivo, nome) in enumerate(existentes):
        titulo, corpo, sumario = renderizar_md(RAIZ / "conhecimento" / arquivo)
        if titulo.strip() != nome:
            subtitulo = titulo.strip()
            if subtitulo.lower().startswith(nome.lower() + ":"):
                resto = subtitulo[len(nome) + 1:].strip()
                subtitulo = resto[:1].upper() + resto[1:]
            corpo = f'<p class="subtitulo">{escape(subtitulo)}</p>' + corpo
        navegacao = []
        if i > 0:
            navegacao.append(f'<a href="/{existentes[i - 1][0]}/">Folha anterior: {escape(existentes[i - 1][2])}</a>')
        if i + 1 < len(existentes):
            navegacao.append(f'<a href="/{existentes[i + 1][0]}/">Próxima folha: {escape(existentes[i + 1][2])}</a>')
        destaque = ""
        if slug == "folha-de-rosto":
            destaque = '<p class="botoes"><a class="botao" href="/folha-de-rosto/preencher/">Preencher a folha aqui</a></p>'
        if slug == "storyboard":
            destaque = '<p class="botoes"><a class="botao" href="/storyboard/preencher/">Preencher o storyboard aqui</a></p>'
        descricao = resumo_de(re.sub(r'<p class="subtitulo">.*?</p>', "", corpo, count=1, flags=re.S))
        gravar(slug, pagina_doc(modelo, nome, destaque + corpo, slug, sumario, descricao, "".join(navegacao)))

    gravar("skills", pagina_doc(modelo, "Baixar as skills", pagina_skills(skills), "skills", None,
                                "Skills de edição de vídeo com IA para Claude Code e Codex, com instalação em uma linha."))

    for rota, arquivo, titulo, ativa in [
        ("folha-de-rosto/preencher", "preencher-rosto.html", "Preencher a folha de rosto", "folha-de-rosto"),
        ("storyboard/preencher", "preencher-storyboard.html", "Preencher o storyboard", "storyboard"),
    ]:
        corpo = (AQUI / arquivo).read_text(encoding="utf-8")
        gravar(rota, pagina_doc(modelo, titulo, corpo, ativa, None, titulo, "", "ferramenta"))

    home = (AQUI / "home.html").read_text(encoding="utf-8")
    home = home.replace("{{mapa}}", DIAGRAMAS["workflow"]())
    home = home.replace("{{tiles}}", tiles_skills(skills))
    home = home.replace("{{gavetas}}", gavetas())
    home = home.replace("{{n_skills}}", str(len(skills)))
    grafo = RAIZ / "site" / "grafo-resumo.html"
    home = home.replace("{{grafo}}", grafo.read_text(encoding="utf-8") if grafo.exists() else "")
    gravar("", home)

    pagina_404 = pagina_doc(
        modelo, "Folha não encontrada",
        '<p>Essa folha não está na pasta. <a href="/">Volte ao começo</a> ou abra <a href="/skills/">as skills</a>.</p>',
        "", None, "Folha não encontrada",
    )
    (DIST / "404.html").write_text(pagina_404, encoding="utf-8")

    urls = [""] + [s for s, _, _ in existentes] + ["skills", "folha-de-rosto/preencher", "storyboard/preencher"]
    mapa = "".join(f"<url><loc>{SITE}/{u}{'/' if u else ''}</loc></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{mapa}</urlset>',
        encoding="utf-8",
    )
    (DIST / "skills.json").write_text(json.dumps(skills, ensure_ascii=False, indent=2), encoding="utf-8")
    faltando = [a for _, a, _ in PAGINAS if not (RAIZ / "conhecimento" / a).exists()]
    print(f"{len(existentes)} capítulos, {len(skills)} skills, saída em {DIST}")
    if faltando:
        print("Sem arquivo ainda:", ", ".join(faltando))


if __name__ == "__main__":
    main()
