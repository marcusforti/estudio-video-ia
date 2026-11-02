(function () {
  var doc = document.documentElement;
  doc.classList.add("js");
  var calmo = matchMedia("(prefers-reduced-motion: reduce)").matches && location.search.indexOf("animar") < 0;
  doc.classList.add(calmo ? "calmo" : "anima");

  var alvos = document.querySelectorAll(
    ".cabeca>*,.passa,.gaveta,.tile,.livro-coluna,.folhas-texto,.prato,.secao-indice>h2,.passantes-titulo,.seletor,.seletor-texto,.diagrama-mapa"
  );
  if ("IntersectionObserver" in window && !calmo) {
    var obs = new IntersectionObserver(
      function (itens) {
        itens.forEach(function (i) {
          if (i.isIntersecting) {
            i.target.classList.add("visto");
            obs.unobserve(i.target);
          }
        });
      },
      { rootMargin: "0px 0px 8% 0px" }
    );
    alvos.forEach(function (el, n) {
      el.classList.add("surge");
      el.style.setProperty("--atraso", (n % 4) * 70 + "ms");
      obs.observe(el);
    });
  }

  var cartao = document.getElementById("cartao");
  var sala = document.getElementById("sala");
  var canhoto = document.getElementById("canhoto");
  if (cartao && !calmo) {
    var pendente = false;
    var atualizar = function () {
      pendente = false;
      var vh = innerHeight;
      var p = Math.min(1, Math.max(0, scrollY / (vh * 0.85)));
      var q = p * p * (3 - 2 * p);
      var escala = innerWidth < 640 ? 0.24 : 0.2;
      var caixa = cartao.getBoundingClientRect();
      var largura = caixa.width / (cartao.__escala || 1);
      var altura = caixa.height / (cartao.__escala || 1);
      var folgaX = (innerWidth - largura) / 2 - 16;
      var folgaY = (vh - altura) / 2 - 16;
      var s = 1 - (1 - escala) * q;
      cartao.__escala = s;
      cartao.style.transform =
        "translate(" + -folgaX * q + "px," + folgaY * q + "px) scale(" + s + ")";
      if (sala) sala.style.opacity = String(1 - q * 0.75);
      var parede = document.querySelector(".passantes");
      var fim = parede ? parede.getBoundingClientRect().bottom : 0;
      var mostrar = p >= 1 && fim > vh * 0.55;
      var some = innerWidth < 640 ? p >= 1 : fim <= vh * 0.55;
      cartao.style.opacity = some ? "0" : "1";
      cartao.style.visibility = some ? "hidden" : "visible";
      if (canhoto) canhoto.classList.toggle("visivel", mostrar);
      cartao.classList.toggle("encolhido", p >= 0.9);
    };
    addEventListener(
      "scroll",
      function () {
        if (!pendente) {
          pendente = true;
          requestAnimationFrame(atualizar);
        }
      },
      { passive: true }
    );
    addEventListener("resize", atualizar);
    atualizar();
  }

  var textos = {
    reel: "Entram de 9 a 18 takes e um áudio de briefing. Mapa primeiro, voz com tempo por palavra, takes na velocidade real, telas de sistema de verdade e render em máquina alugada.",
    talking: "Entra um bruto por corte e a voz é a real, sem clone. Você aprova gancho, cortes e frases dos cartões antes do render, e o render local resolve.",
    explicativo: "Sem filmagem: roteiro, voz e imagens geradas. Quadros e roteiro são aprovados antes do render, que roda em pedaços de 60 s.",
    vsl: "Briefing com fontes, piloto antes da versão longa e portões extras: roteiro, storyboard do piloto e prévia longa. Lista de ressalvas antes de publicar.",
    aula: "Gravação longa de reunião ou live. Transcrição com falante, layout remontado e render em dezenas de pedaços. A voz é a real de quem fala; clone só com termo escrito dele."
  };
  var botoes = document.querySelectorAll(".seletor button");
  var aplicar = function (tipo) {
    document.querySelectorAll("[data-tipos]").forEach(function (el) {
      el.classList.toggle("apagado", el.getAttribute("data-tipos").split(" ").indexOf(tipo) < 0);
    });
    botoes.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.tipo === tipo));
    });
    var alvo = document.getElementById("seletor-texto");
    if (alvo) alvo.textContent = textos[tipo];
  };
  botoes.forEach(function (b) {
    b.addEventListener("click", function () {
      aplicar(b.dataset.tipo);
    });
  });
  if (botoes.length) aplicar("reel");

  var abas = document.querySelectorAll(".abas-folha button");
  abas.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.folha;
      abas.forEach(function (x) {
        x.setAttribute("aria-pressed", String(x === b));
      });
      document.querySelectorAll(".folha-info").forEach(function (i) {
        i.hidden = i.dataset.info !== f;
      });
      document.querySelectorAll(".prato-item").forEach(function (i) {
        i.classList.toggle("ativo", i.dataset.prato === f);
      });
    });
  });

  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var alvo = document.getElementById(b.dataset.copiar);
      navigator.clipboard.writeText(alvo.textContent).then(function () {
        var antes = b.textContent;
        b.textContent = "Copiado";
        setTimeout(function () {
          b.textContent = antes;
        }, 1800);
      });
    });
  });
})();
