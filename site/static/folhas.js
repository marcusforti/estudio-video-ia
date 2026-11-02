(function (raiz) {
  var ROSTO = [
    ["A. Identificação", [
      ["slug", "Slug, série e episódio", 2, "REEL-TEMA-AAAA-MM-DD; série e número"],
      ["dono", "Dono do vídeo e destino da saída", 1, "Quem é o dono e em que pasta a saída fica"],
      ["pedido", "Pedido original", 0, "Canal, data e o que chegou: áudio, vídeos, fotos"],
      ["tipo", "Tipo de projeto e fluxo", 1, "Talking head, Reel com motion, explicativo gerado, VSL ou aula longa"],
      ["versoes", "Versão vigente e tabela de versões", 0, "Cada versão com status e motivo"]
    ]],
    ["B. Intenção", [
      ["objetivo", "Objetivo e \"sai pensando\"", 1, "O que a pessoa sente ou faz no fim e a frase que ela diria ao sair"],
      ["publico", "Público: quem é e quem NÃO é", 1, "Para quem se fala e para quem não se fala"],
      ["arco", "Arco com tempos", 1, "Gancho, desenvolvimento, prova, oferta, CTA, com faixas de tempo"],
      ["cta", "CTA e mecânica de captura", 0, "Palavra do comentário, destino, isca, automação"],
      ["oferta", "Oferta e preço", 0, "Valores, prazos, vagas e quem confirmou"]
    ]],
    ["C. Entrada", [
      ["material", "Inventário de material", 1, "Arquivo, o que tem, uso. Inclua descartados e duplicados"],
      ["referencias", "Referências de estilo e créditos", 0, "Vídeo de referência, o que se aproveita, o que não se copia"],
      ["fatos", "Fatos a provar", 0, "Dado, fonte, estado: confirmado, estimativa ou simulação"]
    ]],
    ["D. Voz e som", [
      ["voz", "Quem fala, com que voz", 1, "Real, clone, gerada ou de terceiro; modelo; nome da variável, nunca o valor"],
      ["pronuncia", "Dicionário de pronúncia", 0, "Palavra e grafia fonética"],
      ["som", "Trilha, SFX e loudness", 0, "Origem, nível em relação à voz, alvo de LUFS"]
    ]],
    ["E. Formato e linguagem visual", [
      ["formato", "Formato, duração, teto e derivados", 1, "Resolução, fps, duração-alvo, teto, versões derivadas"],
      ["linguagem", "Linguagem visual", 1, "Referência, paleta em hex, tipografia, o que é proibido"],
      ["imagem", "Regra de imagem: real x gerada", 0, "O que pode ser real, gerado ou simulado; selo; rostos; marca"],
      ["area", "Área segura e zona de rosto", 0, "Régua aplicada e onde fica o rosto"]
    ]],
    ["F. Vetos e conformidade", [
      ["vetos", "Vetos do cliente", 1, "Lista curta de \"nunca\""],
      ["autorizacoes", "Autorizações e privacidade", 0, "Imagem e voz de terceiros, dados internos, por escrito"]
    ]],
    ["G. Produção e custo", [
      ["custo", "Onde roda e quanto pode gastar", 0, "Local ou máquina alugada, teto, quem destrói a instância"],
      ["responsaveis", "Responsáveis e destinatários", 0, "Quem produz, quem aprova, quem recebe"],
      ["caminhos", "Caminhos e comando de retomada", 0, "Pastas, scripts na ordem e o comando para continuar"]
    ]],
    ["H. Portões e estado", [
      ["portoes", "Portões", 1, "Roteiro, quadros e fala, prévia, entrega, publicar: estado, data, quem aprovou"],
      ["perguntas", "Perguntas abertas e padrão adotado", 0, "Pergunta, proposta, o que foi adotado sem resposta"],
      ["riscos", "Riscos e atenção", 0, "O que pode dar errado e o plano B"]
    ]],
    ["I. Pós-publicação", [
      ["publicacao", "Publicação", 0, "Link do post, data, collab, arquivo da legenda"],
      ["automacao", "Automação e isca", 0, "Palavra, campanha, URL da página"],
      ["resultado", "Resultado e feedback", 0, "O que o dono disse e o que mudou"]
    ]]
  ];

  var EXEMPLO_ROSTO = {
    slug: "REEL-LAVANDERIA-2026-11-02 · série de exemplo, ep. 03",
    dono: "Criador do perfil de exemplo. Saída na pasta do criador",
    pedido: "Áudio de 1:50, 7 vídeos e 3 fotos recebidos no chat",
    tipo: "Reel com motion · storyboard: sim",
    objetivo: "Quem assiste entende onde procurar a primeira venda e sai querendo visitar um negócio do bairro. Sai pensando: \"dá pra eu fazer isso na lavanderia perto de casa\"",
    publico: "Quem quer vender implantação de IA para negócio local. NÃO é o dono da lavanderia",
    arco: "Gancho 0:00-0:06 · o cliente 0:06-0:22 · diagnóstico por câmera 0:22-0:58 · 3 soluções 0:58-1:45 · o que precisa 1:45-2:00 · preço de referência 2:00-2:15 · CTA 2:15-2:30",
    cta: "Comenta LAVANDERIA → DM com o link do material",
    material: "v01 fachada à noite: gancho\nv02 corredor das máquinas: diagnóstico\nv03 balcão: painel do atendente\nv04 e v05 cópias de v02: descartar",
    voz: "Clone do próprio criador, com autorização dele. Variável: VOZ_ID",
    formato: "1080x1920, 30 fps, 2:30, teto 3:00. Derivados: leve para mensagem e versão para postar",
    linguagem: "Paleta #0F1B2D, #F4EFE6, #E07B39 · Anton + Inter · proibido: cards genéricos, logo real",
    vetos: "Sem logo nem nome de marca · sem promessa de resultado · sem nome de cliente real",
    caminhos: "_bruto/ _materiais/ hf/ saida/ · retomar: python timeline.py && python gen.py && python mix.py",
    portoes: "Roteiro: aprovado 02/11 · Quadros e fala: pendente · Entrega: pendente · Pode postar: pendente"
  };

  var CABECA_STORY = [
    ["nome", "Nome e versão", "Storyboard 1 · nome · duração"],
    ["objetivo", "Objetivo", "Na voz de quem recebe"],
    ["sai", "Sai pensando", "A frase que a pessoa diria ao sair"],
    ["sentimento", "Sentimento", "Uma palavra"],
    ["ideia", "Ideia", "2 ou 3 linhas do arco"],
    ["linguagem", "Linguagem visual", "Paleta, tipografia, movimento, tratamento do material real"],
    ["regua", "Régua de tempo", "Estimada com 2,33 palavras/s + 0,35 s entre falas; depois medida"],
    ["trilha", "Trilha e SFX", "Estilo, nível, silêncios"],
    ["custo", "Custo de geração", "Imagens x custo unitário"],
    ["curta", "Versão curta", "Mesma ideia, metade das cenas"]
  ];

  var COLUNAS = [
    ["id", "#", 0], ["bloco", "Bloco", 0], ["tempo", "Tempo", 0], ["fala", "Fala", 1], ["gatilho", "Gatilho", 0],
    ["tipo", "Tipo", 0], ["visual", "Visual", 1], ["camera", "Câmera / transição", 0], ["texto", "Texto em tela", 1],
    ["som", "Som", 0], ["origem", "Origem do asset", 1], ["checagens", "Checagens", 0], ["status", "Status", 0], ["nota", "Nota do portão", 0]
  ];
  var STATUS = ["outline", "imagem aprovada", "construído", "animado", "conferido"];

  function limpa(v) {
    return String(v || "").replace(/\|/g, "/").replace(/\s*\n\s*/g, " · ").trim();
  }

  function gerarRosto(d) {
    var saida = ["# ROSTO · " + (d.slug || "PROJETO"), ""];
    ROSTO.forEach(function (g) {
      var linhas = g[1].filter(function (c) { return String(d[c[0]] || "").trim(); });
      if (!linhas.length) return;
      saida.push("## " + g[0]);
      linhas.forEach(function (c) { saida.push("- **" + c[1] + ":** " + limpa(d[c[0]])); });
      saida.push("");
    });
    return saida.join("\n");
  }

  function contar(cenas) {
    var mapa = {};
    cenas.forEach(function (c) {
      var t = limpa(c.tipo) || "?";
      mapa[t] = (mapa[t] || 0) + 1;
    });
    return Object.keys(mapa).map(function (k) { return k + " " + mapa[k]; }).join(", ");
  }

  function gerarStoryboard(d) {
    var saida = ["# STORYBOARD · " + (d.cabeca.nome || "PROJETO"), ""];
    CABECA_STORY.forEach(function (c) {
      if (String(d.cabeca[c[0]] || "").trim()) saida.push("- **" + c[1] + ":** " + limpa(d.cabeca[c[0]]));
    });
    saida.push("- **Códigos de tipo:** R real · IA imagem gerada · B banco · M motion · T tela real · S simulação (S leva o selo \"exemplo\")");
    saida.push("");
    saida.push("| " + COLUNAS.map(function (c) { return c[1]; }).join(" | ") + " |");
    saida.push("|" + COLUNAS.map(function () { return "---"; }).join("|") + "|");
    d.cenas.forEach(function (cena) {
      saida.push("| " + COLUNAS.map(function (c) { return limpa(cena[c[0]]); }).join(" | ") + " |");
    });
    saida.push("");
    saida.push("**Contagem:** " + d.cenas.length + " cenas = " + contar(d.cenas));
    saida.push("");
    return saida.join("\n");
  }

  function baixar(nome, texto) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([texto], { type: "text/markdown;charset=utf-8" }));
    a.download = nome;
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  }

  function nomeArquivo(base, slug) {
    var s = String(slug || "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^\w-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
    return base + (s ? "-" + s : "") + ".md";
  }

  function montarRosto(alvo) {
    var chave = "estudio.rosto";
    var dados = JSON.parse(localStorage.getItem(chave) || "{}");
    ROSTO.forEach(function (g) {
      var bloco = document.createElement("section");
      bloco.className = "grupo";
      bloco.innerHTML = "<h2></h2><div class=\"campos\"></div>";
      bloco.querySelector("h2").textContent = g[0];
      g[1].forEach(function (c) {
        var campo = document.createElement("div");
        campo.className = "campo largo" + (c[2] ? " campo-nucleo" : "");
        var id = "r-" + c[0];
        campo.innerHTML = "<label for=\"" + id + "\"></label><small></small><textarea id=\"" + id + "\" rows=\"2\"></textarea>";
        campo.querySelector("label").innerHTML = (c[2] === 1 ? "<span class=\"nucleo\">Núcleo · </span>" : c[2] === 2 ? "<span class=\"nucleo\">Título · </span>" : "") + c[1];
        campo.querySelector("small").textContent = c[3];
        var t = campo.querySelector("textarea");
        t.value = dados[c[0]] || "";
        t.addEventListener("input", function () {
          dados[c[0]] = t.value;
          localStorage.setItem(chave, JSON.stringify(dados));
        });
        bloco.querySelector(".campos").appendChild(campo);
      });
      alvo.appendChild(bloco);
    });
    var preencher = function (novo) {
      dados = novo;
      localStorage.setItem(chave, JSON.stringify(dados));
      ROSTO.forEach(function (g) {
        g[1].forEach(function (c) { document.getElementById("r-" + c[0]).value = dados[c[0]] || ""; });
      });
    };
    document.getElementById("exemplo").onclick = function () { preencher(Object.assign({}, EXEMPLO_ROSTO)); };
    document.getElementById("limpar").onclick = function () { if (confirm("Apagar o que está na folha?")) preencher({}); };
    document.getElementById("imprimir").onclick = function () { print(); };
    document.getElementById("baixar").onclick = function () { baixar(nomeArquivo("ROSTO", dados.slug), gerarRosto(dados)); };
    var nucleo = document.getElementById("nucleo");
    nucleo.onclick = function () {
      var ligado = nucleo.getAttribute("aria-pressed") !== "true";
      nucleo.setAttribute("aria-pressed", String(ligado));
      alvo.classList.toggle("so-nucleo", ligado);
    };
  }

  function montarStoryboard(alvo) {
    var chave = "estudio.storyboard";
    var cenaVazia = function (n) {
      return { id: "c" + String(n).padStart(2, "0"), status: "outline" };
    };
    var dados = JSON.parse(localStorage.getItem(chave) || "null") || { cabeca: {}, cenas: [cenaVazia(1), cenaVazia(2), cenaVazia(3)] };
    var salvar = function () { localStorage.setItem(chave, JSON.stringify(dados)); };

    var topo = document.createElement("section");
    topo.className = "grupo";
    topo.innerHTML = "<h2>Cabeçalho</h2><div class=\"campos\"></div>";
    CABECA_STORY.forEach(function (c) {
      var campo = document.createElement("div");
      campo.className = "campo";
      var id = "s-" + c[0];
      campo.innerHTML = "<label for=\"" + id + "\"></label><small></small><textarea id=\"" + id + "\" rows=\"2\"></textarea>";
      campo.querySelector("label").textContent = c[1];
      campo.querySelector("small").textContent = c[2];
      var t = campo.querySelector("textarea");
      t.value = dados.cabeca[c[0]] || "";
      t.addEventListener("input", function () { dados.cabeca[c[0]] = t.value; salvar(); });
      topo.querySelector(".campos").appendChild(campo);
    });
    alvo.appendChild(topo);

    var grade = document.createElement("section");
    grade.className = "grupo";
    grade.innerHTML = "<h2>Cenas</h2><div class=\"grade-cenas\" tabindex=\"0\"><table><thead><tr></tr></thead><tbody></tbody></table></div>";
    alvo.appendChild(grade);
    var cab = grade.querySelector("thead tr");
    COLUNAS.forEach(function (c) {
      var th = document.createElement("th");
      th.textContent = c[1];
      cab.appendChild(th);
    });
    cab.appendChild(document.createElement("th"));
    var corpo = grade.querySelector("tbody");

    var desenhar = function () {
      corpo.innerHTML = "";
      dados.cenas.forEach(function (cena, i) {
        var tr = document.createElement("tr");
        COLUNAS.forEach(function (c) {
          var td = document.createElement("td");
          if (c[2]) td.className = "largo";
          var el;
          if (c[0] === "status") {
            el = document.createElement("select");
            STATUS.forEach(function (s) {
              var o = document.createElement("option");
              o.textContent = s;
              el.appendChild(o);
            });
          } else {
            el = document.createElement(c[2] ? "textarea" : "input");
          }
          el.setAttribute("aria-label", c[1] + " da cena " + (i + 1));
          el.value = cena[c[0]] || (c[0] === "status" ? "outline" : "");
          el.addEventListener("input", function () { cena[c[0]] = el.value; salvar(); });
          td.appendChild(el);
          tr.appendChild(td);
        });
        var acao = document.createElement("td");
        var tirar = document.createElement("button");
        tirar.type = "button";
        tirar.textContent = "Tirar";
        tirar.onclick = function () { dados.cenas.splice(i, 1); salvar(); desenhar(); };
        acao.appendChild(tirar);
        tr.appendChild(acao);
        corpo.appendChild(tr);
      });
    };
    desenhar();

    document.getElementById("adicionar").onclick = function () {
      dados.cenas.push(cenaVazia(dados.cenas.length + 1));
      salvar();
      desenhar();
    };
    document.getElementById("limpar").onclick = function () {
      if (!confirm("Apagar o storyboard?")) return;
      dados = { cabeca: {}, cenas: [cenaVazia(1), cenaVazia(2), cenaVazia(3)] };
      salvar();
      location.reload();
    };
    document.getElementById("imprimir").onclick = function () { print(); };
    document.getElementById("baixar").onclick = function () {
      baixar(nomeArquivo("STORYBOARD", dados.cabeca.nome), gerarStoryboard(dados));
    };
  }

  raiz.EstudioFolhas = { gerarRosto: gerarRosto, gerarStoryboard: gerarStoryboard, ROSTO: ROSTO, COLUNAS: COLUNAS };

  if (typeof document !== "undefined") {
    var a = document.getElementById("folha-rosto");
    var b = document.getElementById("folha-storyboard");
    if (a) montarRosto(a);
    if (b) montarStoryboard(b);
  }
})(typeof window !== "undefined" ? window : globalThis);
