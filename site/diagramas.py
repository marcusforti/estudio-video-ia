"""Desenhos do site, gerados em SVG. Cores vêm das variáveis CSS."""
from html import escape

ETAPAS = [
    (0, "Captar o pedido", "áudio, takes, fotos", "/workflow/", "talking reel vsl aula"),
    (1, "Transcrever e catalogar", "por palavra", "/workflow/", "talking reel explicativo vsl aula"),
    (2, "Folha de rosto", "o mapa do projeto", "/folha-de-rosto/", "talking reel explicativo vsl aula"),
    (3, "Referência de estilo", "/estudio-escolher-motion", "/escolhermotion/", "reel explicativo vsl"),
    (4, "Roteiro por blocos", "texto exato da voz", "/workflow/", "reel explicativo vsl aula"),
    (5, "Voz", "real, clone ou gerada", "/voz-local/", "reel explicativo vsl"),
    (6, "Storyboard e imagens", "cena a cena", "/storyboard/", "talking reel explicativo vsl"),
    (7, "Linha do tempo e motion", "composição", "/motion/", "talking reel explicativo vsl aula"),
    (8, "Mix de áudio", "voz, trilha, SFX", "/edicao/", "reel explicativo vsl aula"),
    (9, "Render", "local ou GPU alugada", "/gpu/", "talking reel explicativo vsl aula"),
    (10, "Finalização", "legenda e loudness", "/edicao/", "talking reel explicativo vsl aula"),
    (11, "Conferência", "transcreve o final", "/conferencia/", "talking reel explicativo vsl aula"),
    (12, "Entrega ao dono", "só para ele", "/conferencia/", "talking reel explicativo vsl aula"),
    (13, "Iteração", "versão N+1", "/workflow/", "talking reel explicativo vsl aula"),
    (14, "Postagem", "com o ok", "/conferencia/", "talking reel explicativo vsl aula"),
    (15, "Isca e automação", "comentário vira DM", "/workflow/", "reel"),
    (16, "Registro", "retomada e destruir VM", "/workflow/", "talking reel explicativo vsl aula"),
]

# etapa depois da qual o portão fica
PORTOES = {
    2: ("Decisões", "reel vsl talking explicativo aula"),
    4: ("Roteiro", "vsl"),
    6: ("Quadros e fala", "reel explicativo vsl talking"),
    7: ("Prévia", "vsl"),
    12: ("Entrega", "talking reel explicativo vsl aula"),
    13: ("Publicar", "talking reel explicativo vsl aula"),
}

# travas de segurança: o agente para sozinho nesta etapa
TRAVAS = {
    5: ("Consentimento", "reel explicativo vsl"),
    9: ("Gasto", "talking reel explicativo vsl aula"),
    11: ("Conferência", "talking reel explicativo vsl aula"),
}


def _quebrar(texto, limite):
    linhas, atual = [], ""
    for palavra in texto.split():
        candidato = f"{atual} {palavra}".strip()
        if len(candidato) > limite and atual:
            linhas.append(atual)
            atual = palavra
        else:
            atual = candidato
    if atual:
        linhas.append(atual)
    return linhas


def _texto(x, y, linhas, classe, ancora="middle", altura=20):
    partes = []
    for i, linha in enumerate(linhas):
        partes.append(
            f'<text x="{x}" y="{y + i * altura}" text-anchor="{ancora}" class="{classe}">{escape(linha)}</text>'
        )
    return "".join(partes)


def _carimbo(x, y, texto, tipos, classe="portao"):
    largura = max(86, 10 * len(texto) + 30)
    return (
        f'<g class="{classe}" data-tipos="{tipos}" transform="translate({x} {y}) rotate(-5)">'
        f'<rect x="{-largura / 2}" y="-16" width="{largura}" height="32" class="portao-caixa"/>'
        f'<text x="0" y="6" text-anchor="middle" class="portao-texto">{escape(texto)}</text></g>'
    )


def _estacao(cx, cy, n, nome, sub, href, tipos, largura=190):
    linhas = _quebrar(nome, 18)
    y_nome = cy + 42
    return (
        f'<a href="{href}" class="estacao" data-tipos="{tipos}" data-etapa="{n}">'
        f"<title>{escape(nome)}: {escape(sub)}</title>"
        f'<rect x="{cx - largura / 2}" y="{cy - 28}" width="{largura}" height="128" class="estacao-alvo"/>'
        f'<circle cx="{cx}" cy="{cy}" r="17" class="estacao-ponto"/>'
        f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" class="estacao-num">{n}</text>'
        + _texto(cx, y_nome, linhas, "estacao-nome")
        + _texto(cx, y_nome + 20 * len(linhas) + 2, _quebrar(sub, 24), "estacao-sub", altura=18)
        + "</a>"
    )


def workflow_largo():
    colunas, passo_x, passo_y, margem_x, margem_y = 6, 214, 212, 164, 66
    largura = margem_x * 2 + passo_x * (colunas - 1)
    linhas_grade = (len(ETAPAS) + colunas - 1) // colunas
    altura = margem_y + passo_y * linhas_grade - 30

    def posicao(i):
        linha = i // colunas
        coluna = i % colunas
        if linha % 2:
            coluna = colunas - 1 - coluna
        return margem_x + coluna * passo_x, margem_y + linha * passo_y

    pontos = [posicao(i) for i in range(len(ETAPAS))]
    caminho = f"M{pontos[0][0]} {pontos[0][1]}"
    for i in range(1, len(pontos)):
        x0, y0 = pontos[i - 1]
        x1, y1 = pontos[i]
        if y0 != y1:
            lado = 128 if x0 > largura / 2 else -128
            caminho += f" C{x0 + lado} {y0} {x1 + lado} {y1} {x1} {y1}"
        else:
            caminho += f" L{x1} {y1}"

    corpo = [f'<path d="{caminho}" class="linha-trilho"/>']
    x13, y13 = pontos[13]
    _, y10 = pontos[10]
    corpo.append(f'<path d="M{x13} {y13 - 22} L{x13} {y10 + 100}" class="linha-volta"/>')
    corpo.append(_texto(x13 + 12, y10 + 128, ["reprovou: volta", "e ajusta"], "volta-texto", "start", 17))
    for (n, nome, sub, href, tipos), (x, y) in zip(ETAPAS, pontos):
        corpo.append(_estacao(x, y, n, nome, sub, href, tipos))
    for n, (texto, tipos) in PORTOES.items():
        x0, y0 = pontos[n]
        x1, y1 = pontos[n + 1]
        if y0 == y1:
            corpo.append(_carimbo((x0 + x1) / 2, y0 - 34, texto, tipos))
        else:
            corpo.append(_carimbo(x0 + (90 if x0 > largura / 2 else -60), (y0 + y1) / 2 - 8, texto, tipos))
    for n, (texto, tipos) in TRAVAS.items():
        x0, y0 = pontos[n]
        corpo.append(_carimbo(x0 + 26, y0 - 44, texto, tipos, "portao trava"))
    x5, y5 = pontos[5]
    corpo.append(
        f'<a href="/lip-sync/" class="ramal"><title>Lip sync: quando a boca precisa acompanhar a voz nova</title>'
        f'<path d="M{x5} {y5 + 100} L{x5} {y5 + 122}" class="linha-volta"/>'
        f'<rect x="{x5 - 72}" y="{y5 + 122}" width="144" height="34" class="ramal-caixa"/>'
        f'<text x="{x5}" y="{y5 + 144}" text-anchor="middle" class="ramal-texto">Lip sync, se precisar</text></a>'
    )
    return (
        f'<svg class="mapa mapa-largo" viewBox="0 0 {largura} {altura}" role="img" '
        f'aria-label="Mapa das 17 etapas do workflow, com portões de aprovação e links para cada etapa">'
        + "".join(corpo)
        + "</svg>"
    )


def workflow_estreito():
    largura, passo, margem, x = 360, 104, 36, 40
    corpo, n_total = [], len(ETAPAS)
    altura = margem * 2 + passo * n_total
    corpo.append(f'<path d="M{x} {margem} L{x} {margem + passo * (n_total - 1)}" class="linha-trilho"/>')
    for i, (n, nome, sub, href, tipos) in enumerate(ETAPAS):
        y = margem + i * passo
        corpo.append(
            f'<a href="{href}" class="estacao" data-tipos="{tipos}" data-etapa="{n}">'
            f'<rect x="0" y="{y - 26}" width="{largura}" height="{passo - 8}" class="estacao-alvo"/>'
            f'<circle cx="{x}" cy="{y}" r="17" class="estacao-ponto"/>'
            f'<text x="{x}" y="{y + 6}" text-anchor="middle" class="estacao-num">{n}</text>'
            + _texto(x + 32, y + 2, [nome], "estacao-nome", "start")
            + _texto(x + 32, y + 22, [sub], "estacao-sub", "start")
            + "</a>"
        )
        if n in PORTOES:
            texto, tipos_p = PORTOES[n]
            corpo.append(_carimbo(x + 104, y + 50, texto, tipos_p))
        if n in TRAVAS:
            texto, tipos_t = TRAVAS[n]
            corpo.append(_carimbo(x + 250, y + 50, texto, tipos_t, "portao trava"))
    return (
        f'<svg class="mapa mapa-estreito" viewBox="0 0 {largura} {altura}" role="img" '
        f'aria-label="Mapa vertical das 17 etapas do workflow">' + "".join(corpo) + "</svg>"
    )


def workflow():
    return f'<figure class="diagrama diagrama-mapa">{workflow_largo()}{workflow_estreito()}</figure>'


def _sequencia(titulo, passos, colunas=4, alerta=None, fecha=False):
    largura_no, altura_no, gap_x, gap_y, margem = 218, 118, 44, 56, 16
    n_linhas = (len(passos) + colunas - 1) // colunas
    largura = margem * 2 + colunas * largura_no + (colunas - 1) * gap_x
    altura = margem * 2 + n_linhas * altura_no + (n_linhas - 1) * gap_y + (54 if alerta else 0)
    corpo = []

    def caixa(i):
        linha = i // colunas
        coluna = i % colunas
        if linha % 2:
            coluna = colunas - 1 - coluna
        return margem + coluna * (largura_no + gap_x), margem + linha * (altura_no + gap_y)

    for i, passo in enumerate(passos):
        nome, sub, destaque = (list(passo) + [False])[:3]
        x, y = caixa(i)
        classe = "no no-alerta" if destaque else "no"
        corpo.append(f'<rect x="{x}" y="{y}" width="{largura_no}" height="{altura_no}" class="{classe}"/>')
        corpo.append(_texto(x + 16, y + 34, _quebrar(nome, 20), "no-nome", "start", 22))
        corpo.append(_texto(x + 16, y + 34 + 22 * len(_quebrar(nome, 20)) + 2, _quebrar(sub, 25), "no-sub", "start", 19))
        if i + 1 < len(passos):
            xa, ya = caixa(i + 1)
            if ya == y:
                de, para = (x + largura_no, xa) if xa > x else (x, xa + largura_no)
                corpo.append(f'<path d="M{de} {y + altura_no / 2} L{para} {y + altura_no / 2}" class="seta"/>')
            else:
                corpo.append(f'<path d="M{x + largura_no / 2} {y + altura_no} L{xa + largura_no / 2} {ya}" class="seta"/>')
    if alerta:
        corpo.append(_texto(margem, altura - 22, _quebrar(alerta, 92), "no-alerta-texto", "start"))
    return (
        f'<figure class="diagrama"><div class="rolagem"><svg class="seq" viewBox="0 0 {largura} {altura}" '
        f'role="img" aria-label="{escape(titulo)}" style="min-width:{min(largura, 760)}px">'
        + "".join(corpo)
        + f"</svg></div><figcaption>{escape(titulo)}</figcaption></figure>"
    )


def folhas():
    return _sequencia(
        "Do pedido solto ao vídeo aprovado: uma folha para cada decisão",
        [
            ("Folha de rosto", "o que é, para quem, com que voz, o que é proibido"),
            ("Folha de storyboard", "cena a cena: fala, imagem, texto, som, origem"),
            ("Folha de contato", "material, imagens geradas e quadros finais", True),
            ("Checklist de entrega", "medido com número, antes de mostrar"),
        ],
    )


def gpu_ciclo():
    return _sequencia(
        "Ciclo de vida da máquina alugada: só termina com a lista vazia",
        [
            ("Confirmar o gasto", "preço por hora e teto"),
            ("Escolher e criar", "GPU, disco, imagem"),
            ("Entrar por SSH", "chave, porta, sem senha"),
            ("Subir o projeto", "código, dados, modelos"),
            ("Rodar sem depender do SSH", "setsid, nohup ou tmux"),
            ("Baixar o resultado", "para o seu disco"),
            ("Conferir md5", "duração e tamanho"),
            ("Destruir a instância", "parar ainda cobra disco", True),
        ],
        alerta="Fim real do ciclo: listar instâncias e ver a lista vazia.",
    )


def escolhermotion_fluxo():
    return _sequencia(
        "O caminho da referência ao vídeo",
        [
            ("Entender o pedido", "uso, formato, duração, marca"),
            ("Buscar referências", "termos em inglês"),
            ("Mostrar 3 a 5 opções", "uma linha e o link"),
            ("Adaptar o prompt", "mecânica fica, conteúdo muda"),
            ("Produzir", "código vira MP4"),
            ("Conferir quadros", "folha de contato"),
            ("Dar crédito", "autor e post original"),
            ("Entregar ao dono", "antes de publicar", True),
        ],
    )


def arvore(titulo, raiz):
    """raiz = (texto, [(resposta, filho), ...]); folha = (texto, [])."""
    largura_no, altura_no, gap_x, gap_y, margem = 214, 96, 22, 74, 16

    def folhas_de(no):
        return max(1, sum(folhas_de(f) for _, f in no[1]))

    def profundidade(no):
        return 1 + max((profundidade(f) for _, f in no[1]), default=0)

    total = folhas_de(raiz)
    prof = profundidade(raiz)
    largura = margem * 2 + total * largura_no + (total - 1) * gap_x
    altura = margem * 2 + prof * altura_no + (prof - 1) * gap_y
    corpo = []

    def desenha(no, x_ini, nivel):
        fatia = folhas_de(no) * (largura_no + gap_x) - gap_x
        x = x_ini + (fatia - largura_no) / 2
        y = margem + nivel * (altura_no + gap_y)
        folha = not no[1]
        classe = "no no-fim" if folha else "no"
        corpo.append(f'<rect x="{x}" y="{y}" width="{largura_no}" height="{altura_no}" class="{classe}"/>')
        limite = 24
        linhas = _quebrar(no[0], limite)
        y_txt = y + altura_no / 2 - (len(linhas) - 1) * 10 + 5
        corpo.append(_texto(x + largura_no / 2, y_txt, linhas, "no-fim-texto" if folha else "no-nome", altura=20))
        cursor = x_ini
        for resposta, filho in no[1]:
            fatia_f = folhas_de(filho) * (largura_no + gap_x) - gap_x
            cx_f = cursor + fatia_f / 2
            y_f = y + altura_no + gap_y
            cx = x + largura_no / 2
            corpo.append(
                f'<path d="M{cx} {y + altura_no} C{cx} {y + altura_no + 40} {cx_f} {y_f - 40} {cx_f} {y_f}" class="seta"/>'
            )
            corpo.append(
                _texto((cx + cx_f) / 2, y + altura_no + gap_y / 2 + 4, [resposta], "resposta")
            )
            desenha(filho, cursor, nivel + 1)
            cursor += fatia_f + gap_x

    desenha(raiz, margem, 0)
    return (
        f'<figure class="diagrama"><div class="rolagem"><svg class="arvore" viewBox="0 0 {largura} {altura}" '
        f'role="img" aria-label="{escape(titulo)}" style="min-width:{min(largura, 860)}px">'
        + "".join(corpo)
        + f"</svg></div><figcaption>{escape(titulo)}</figcaption></figure>"
    )


def escada(titulo, degraus):
    """degraus = [(pergunta, [(resposta, destino, href ou None), ...], rótulo de seguir ou None)]."""
    linhas = [f'<figure class="diagrama"><ol class="escada" aria-label="{escape(titulo)}">']
    for pergunta, respostas, seguir in degraus:
        itens = []
        for resposta, destino, href in respostas:
            alvo = f'<a href="{href}">{escape(destino)}</a>' if href else f"<strong>{escape(destino)}</strong>"
            itens.append(f"<li><span>{escape(resposta)}</span>{alvo}</li>")
        desce = f'<p class="escada-desce">{escape(seguir)}</p>' if seguir else ""
        linhas.append(
            f'<li class="degrau"><p class="escada-pergunta">{escape(pergunta)}</p>'
            f'<ul class="escada-respostas">{"".join(itens)}</ul>{desce}</li>'
        )
    linhas.append(f"</ol><figcaption>{escape(titulo)}</figcaption></figure>")
    return "".join(linhas)


def motion_decisao():
    return escada(
        "Que técnica usar: comece pela primeira pergunta e desça",
        [
            ("Há pessoa falando para a câmera?", [
                ("Motion ocupa metade da tela o tempo todo", "Tela dividida vertical", "#receita-2-tela-dividida-vertical-motion-em-cima"),
                ("Profundidade atrás dela, em trechos curtos", "3D atrás da pessoa", "#receita-1-3d-atras-da-pessoa"),
                ("Só reforça a selfie com elementos por cima", "Overlay com transparência", None),
                ("Mostra um sistema funcionando sobre os takes", "Reel com detecção real", "#receita-6-reel-com-deteccao-real"),
            ], "Não há pessoa"),
            ("Há produto ou site para virar filme?", [
                ("Sim", "Skill product-launch-video, do HyperFrames", None),
            ], "Não"),
            ("Peça curta, sem locução, em que o motion é a mensagem?", [
                ("Sim, até cerca de 30 s", "Skill motion-graphics: tipografia cinética, número, gráfico, logo ou mapa", None),
            ], "Não"),
            ("Precisa explicar algo sem filmar ninguém?", [
                ("Com ilustrações geradas e voz", "Explicativo ilustrado", None),
                ("Com look desenhado em canvas", "ANIMATE (cth9191, MIT)", "https://github.com/cth9191/animate"),
            ], "Não"),
            ("É série com estética própria, em que o conceito faz parte do produto?", [
                ("Sim", "Dossiê ou conceito próprio com storyboard por cena", "#receita-3-dossie-mesa-de-investigacao"),
                ("Não", "Skill general-video: filme narrado multi-cena", None),
            ], "Depois de escolher"),
            ("Onde renderizar?", [
                ("Até 1 a 2 min de vídeo", "No PC, em pedaços", "#render-em-pedacos-memoria-e-vm"),
                ("Mais longo, muita camada ou alfa longo", "Em VM alugada, em pedaços", "/gpu/"),
            ], None),
        ],
    )


def voz_decisao():
    return escada(
        "Qual caminho de voz seguir: comece pela primeira pergunta e desça",
        [
            ("A voz é sua, ou o dono autorizou por escrito?", [
                ("Não", "Pare. Use voz de catálogo, sem clone", None),
            ], "Sim"),
            ("A peça vai a público ou é paga por cliente?", [
                ("Não, é rascunho ou uso interno", "Pule para a pergunta da fala gravada", None),
            ], "Sim"),
            ("Precisa soar igual à pessoa real?", [
                ("Sim", "Clonagem profissional paga, com 30 min ou mais de áudio limpo", None),
            ], "Não"),
            ("Quer rodar modelo aberto, por custo ou privacidade?", [
                ("Não", "Clone instantâneo pago, com 1 a 3 min de áudio", None),
            ], "Sim, com pesos permissivos e prova cega"),
            ("Já existe fala humana gravada e só falta trocar o timbre?", [
                ("Sim", "Conversão de voz (RVC), com 10 min ou mais de áudio limpo", None),
            ], "Não: TTS com clonagem"),
            ("Tem GPU NVIDIA com 8 GB ou mais?", [
                ("Sim", "Rode nela", None),
                ("Não, frase curta", "CPU resolve", None),
                ("Não, texto longo", "GPU alugada", "/gpu/"),
            ], "Depois"),
            ("O texto passa de 20 s de fala?", [
                ("Sim", "Gere em blocos, com retomada", None),
                ("Não", "Gere direto", None),
            ], None),
        ],
    )


def lipsync_decisao():
    teste = "#o-teste-de-10-a-15-s-no-seu-pior-plano"
    return escada(
        "Qual caminho de lip sync seguir: comece pela primeira pergunta e desça",
        [
            ("Você tem consentimento por escrito de quem aparece e de quem fala?", [
                ("Não", "Pare. Sem consentimento não se mexe em boca nem em rosto", None),
            ], "Sim"),
            ("O que você tem em mãos?", [
                ("Foto de pessoa real e áudio", "Evite: o rosto gerado por IA que testamos foi reprovado. Filme um take", None),
                ("Personagem ou ilustração e áudio", "InfiniteTalk 480p (rodou aqui, sem veredito de qualidade) ou LongCat 1.5 (não testado)", None),
                ("Nem filmagem nem foto", "Filme um take fixo, de frente, e recomece", None),
            ], "Filmagem da pessoa e áudio novo"),
            ("O plano é fácil? De frente, boca livre, uma pessoa, boa luz", [
                ("Não, e aceito alugar GPU", "Teste de 10 a 15 s com TBDub e X-Dub", teste),
                ("Não, e não quero alugar", "Teste com sync-3 ou HeyGen Precision", teste),
            ], "Sim"),
            ("Quanto você aceita montar e gastar?", [
                ("Rascunho barato, placa de 4 GB ou mais", "MuseTalk 1.5", None),
                ("Qualidade de entrega, GPU alugada de 24 a 80 GB", "TBDub Student, com LatentSync 1.6 de reserva", None),
            ], "Não quero montar nada"),
            ("Precisa traduzir ou dublar junto?", [
                ("Sim", "Pacote de dublagem: HeyGen Translate ou sync.so Dubbing", None),
                ("Não", "LatentSync ou VEED na fal, lipsync-2-pro, sync-3, nessa ordem. Pare no primeiro que passar no teste", teste),
            ], None),
        ],
    )


DIAGRAMAS = {
    "workflow": workflow,
    "folhas": folhas,
    "gpu-ciclo": gpu_ciclo,
    "escolhermotion-fluxo": escolhermotion_fluxo,
    "motion-decisao": motion_decisao,
    "voz-decisao": voz_decisao,
    "lipsync-decisao": lipsync_decisao,
}
