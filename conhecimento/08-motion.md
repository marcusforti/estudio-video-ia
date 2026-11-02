# Motion por código: técnica certa, ritmo, área segura e render

Este capítulo reúne o que sabemos para criar motion escrito em código (HTML, GSAP, Three.js): a técnica certa para cada peça, ritmo, tipografia, cor, som, área segura de 1080x1920, o contrato do HyperFrames, render em pedaços e em VM, e seis receitas. É para quem edita com agente de código (Claude Code, Codex).

## Resumo em 30 segundos

- Pergunte primeiro se há pessoa falando. Com pessoa: tela dividida ou 3D atrás dela. Sem pessoa: `motion-graphics` (curta) ou `general-video` (longa ou narrada).
- Escreva a SPEC (roteiro técnico) antes do código e mostre quadros e fala ao dono antes de renderizar: é o que a skill [estudio-motion](../skills/estudio-motion/SKILL.md) conduz.
- Em 1080x1920, texto e motion ficam em x 80 a 940 e y 250 a 1440; a legenda tem linha de base entre y 1150 e 1300. Em anúncio, até y 1248.
- Renderize em pedaços (50 a 60 s no PC, 10 a 30 s numa VM alugada). Confirme o gasto e destrua a máquina ao terminar.
- Duas escolas funcionam: contenção (marca, vinheta) e impacto (vídeo falado, série com conceito).

## Mapa de decisão

Responda na ordem. Se você já tem uma referência de outro criador, passe antes pelo [capítulo 09](09-escolhermotion.md).

<!-- diagrama:motion-decisao -->


As quatro skills citadas são do pacote HyperFrames (Apache-2.0, HeyGen) [oficial]; as rotas são a nossa leitura das descrições delas [testado]. Técnica por tipo: palavras de impacto, tipografia cinética presa à fala; número, contador com dado verdadeiro; vinheta, uma ideia por cena; texto atrás da pessoa, matting (recorte de vídeo); mundo 3D, Three.js por relógio de tween; look desenhado, canvas com ruído semeado.

### Storyboard antes da animação (método geral)

Para marca e vinheta, não anime na primeira passada. O fluxo do HyperFrames já prevê mostrar um storyboard antes de construir [oficial]. Na prática: gere um quadro parado por cena, com a marca e as imagens reais, e mostre à pessoa. Anime a cena só depois do OK dela, uma de cada vez, e refaça apenas a cena que ela pedir para mudar [praticante]. O modelo está na skill estudio-motion; num projeto completo, a tabela de cenas é a [folha de storyboard](03-folha-de-storyboard.md) do [workflow](01-workflow-completo.md).

## Gancho nos 2 primeiros segundos

- Gancho visual e de fala nos 2 primeiros segundos, com som no golpe [testado]. Exemplo nosso: um valor grande estoura aos 0,9 s e um carimbo cai aos 2,36 s.
- O quadro 0 é a miniatura: rosto, resultado ou linha forte; nunca preto nem só logo [fornecedor].
- TikTok pede a proposta de conteúdo nos 3 primeiros segundos e o gancho até os 6 [oficial].
- Risco: o Instagram disse em 2023 que reels mudos, com bordas ou com maioria de texto ficam menos visíveis (sem revisão achada em 2026); TikTok e YouTube tratam material repetido de molde como risco de elegibilidade ou monetização [oficial]. Leve algo próprio: voz, dado ou imagem.

## Ritmo e duração de beat

Beat é a batida visual: o instante em que algo muda na tela.

- Cena nova presa na fala a cada 2 a 4 s, com fundo 3D contínuo: 75 cenas em 4:01, cerca de 3,2 s cada. Nenhum card parado por mais de 5 a 6 s [testado].
- Vertical: planos de 1 a 2 s. Hold de leitura: 0,5 s mais 0,3 s por palavra [fornecedor].
- Talking heads de TikTok de alto desempenho cortam em média a cada 2,7 s; em experimento, ritmo mais alto reduziu o engajamento sustentado (242 estudantes, tema único) [independente], fraco.

## Easing e física

Easing é a curva de aceleração de um movimento.

- Entrada com cauda longa (`expo.out`, `power4.out`), saída `power3.in`, câmera `power2.inOut`. O mesmo `power2.out` de 0,5 s em tudo dá "cara de gerado" [fornecedor].
- Material 3: entrada `cubic-bezier(0.05, 0.7, 0.1, 1.0)` em 400 ms, saída `cubic-bezier(0.3, 0.0, 0.8, 0.15)` em 200 ms (sair pede menos atenção). É para interface, não para vídeo linear [oficial].
- Nosso motor: cena entra em 0,55 s `expo.out` e sai em 0,26 s `power2.in` (47% da entrada); pop `back.out(1.8)`; letras `rotateX −100 → 0` com `back.out(1.6)` e 0,03 s entre letras; deriva `scale 1 → 1,06` [testado].
- Mola: amortecimento 1,0 nunca quica; 0,7 a 0,85 premium; 0,4 a 0,6 brincalhão. Posição e tamanho podem passar do alvo; opacidade e cor nunca [fornecedor].

## Tipografia e legibilidade

- O HyperFrames embute 18 fontes; as demais pedem `@font-face` em `assets/fonts/` [oficial]. Não verificamos a licença das fontes que usamos (Google Fonts): confira antes de embutir e não distribua fontes da Microsoft.
- Feed vertical: título a partir de 90 px, corpo a partir de 32 px, nada para ler abaixo de 28 px, até 5 palavras por linha [fornecedor].
- Legenda é apoio, não manchete: 58 px em 1080x1920 (era 74), contorno 4, sombra 2, só a palavra ativa muda de cor, até 4 palavras por bloco. Uma legenda grande, que pulava de posição, roubava o olhar do card; por isso reduzimos o tamanho. Palavra por palavra aprovada: desfoque 6 px → 0, sobe 14 px, 0,32 s `power2.out` [testado].
- Leitura: BBC, 160 a 180 palavras por minuto e pelo menos 0,3 s por palavra; Netflix, até 20 caracteres por segundo [oficial]. O TikTok sugere 5 a 10 palavras por segundo em texto de anúncio, 2 a 3 vezes o padrão de legenda: não use como meta [oficial]. Um estudo pequeno (15 pessoas por velocidade) achou 90 palavras por minuto a mais atraente em tipografia cinética [independente], fraco.

Flashes (WCAG 2.2, critério 2.3.1, norma de acessibilidade) [oficial]: nada pode piscar mais de 3 vezes por segundo, a menos que fique abaixo dos limiares de flash geral e de flash vermelho. Flash geral é um par de mudanças opostas de luminância de 10% ou mais, com a imagem escura abaixo de 0,80, numa área acima de 341x256 pixels CSS, e um celular em tela cheia passa disso. Batida a 180 BPM com flash completo em cada batida está no limite. Nosso flash de virada do gancho é único, de 120 ms [testado]. O `check` do HyperFrames cobre contraste e layout, não flashes (pelas nossas notas).

## Cor, contraste e hierarquia

- Um acento de cor, um significado, até 8% dos pixels [praticante].
- Gradiente linear de tela cheia em fundo escuro cria faixas no H.264: use radial ou sólido. Acento a 5% de opacidade some na compressão: use 15 a 25% [fornecedor].
- `backdrop-filter` (vidro) não funcionou em render com transparência: use `rgba`. Diverge da recomendação do HyperFrames [testado].
- Preto com dourado virou clichê no nosso gosto: preferimos conceito (papel, carimbo, fio vermelho) [praticante]. Foto leve em tela cheia, dissolvendo no fundo claro, foi aprovada [testado].
- Hierarquia: rosto, depois legenda (apoio), depois motion (protagonista). Cada fala ganha um evento visual preso à palavra. Mostre o sistema ou produto real, não card genérico; contador só com número verdadeiro [testado].

## Som e volume

- Som só onde há causa visível: clique, whoosh no corte ou card grande, tic em texto letra a letra, pop em selo ou número, riser com impacto uma vez por filme. Pico do som um quadro depois da imagem; golpes 3 a 6 dB acima da trilha [fornecedor].
- Geramos os efeitos por texto (API de efeitos da ElevenLabs); no mix, trilha em .10 e golpes até .55 [testado].
- Áudio final: `highpass=f=70` e `loudnorm=I=-14:TP=-1.5:LRA=11` [testado]. Nenhuma plataforma de vídeo publica alvo de LUFS (medida de volume) nas páginas que abrimos. Praticantes usam −14 LUFS com pico até −1 dBTP [praticante]; a EBU fixa −23 LUFS para TV e −20 a −16 para streaming [oficial].
- Música alta cobre a voz. Mantenha a trilha bem abaixo da voz, com ducking forte, e evite limitador que levante a trilha nos respiros [testado].

## Área segura

Área segura é a parte do quadro que a interface do app não cobre. Medidas em 1080x1920:

| Régua | Topo | Base | Esquerda | Direita | Selo |
|---|---|---|---|---|---|
| Casa | 250 | 480 | 80 | 140 | [testado] |
| Meta, anúncios de Reels (14%, 35%, 6%, 6%) | 269 | 672 | 65 | 65 | [oficial] |

A casa deixa x 80 a 940 e y 250 a 1440 para texto e motion. A legenda falada tem linha de base entre y 1150 e 1300 (60 a 68% da altura) e nunca abaixo de y 1400. Contra a Meta, a nossa régua reserva mais nas laterais (80 e 140 contra 65) e menos no topo e embaixo (250 e 480 contra 269 e 672). A Meta recomenda, só para anúncios: área útil em x 65 a 1015 e y 269 a 1248. Em anúncio, use a interseção: x 80 a 940 e y 269 a 1248, com a legenda até y 1240. Com aviso legal, a Meta pede 40% da base livre (768 px) [oficial].

A régua nasceu depois que uma legenda foi cortada pela interface e o motion encostou nas laterais [testado]. Não medimos a interface de cada app. A mesma régua, com o estilo da legenda, está no [capítulo 04](04-edicao-e-corte.md). O TikTok publica a zona só em arquivos de template; para YouTube Shorts e Reels orgânico não achamos números oficiais.

Rotina: desenhe a caixa antes de animar e tire depois; confira por snapshot no começo, no meio, no fim e nos picos da animação (escala, zoom, entrada lateral) com a caixa por cima. O feed 4:5 corta 285 px em cima e embaixo, e a capa 3:4, 240 px [testado].

## Especificações por plataforma

Tudo abaixo é [oficial], lido em 01/11/2026.

| Item | Instagram Reels | TikTok | YouTube Shorts |
|---|---|---|---|
| Proporção | 1,91:1 a 9:16 | 9:16 recomendado | quadrado ou vertical |
| Resolução | mínimo 720 px; anúncio 1440x2560 | anúncio a partir de 540x960 | máximo 1080p |
| Quadros por segundo | mínimo 30 | 23 a 60 (API) | o da gravação |
| Vídeo e áudio | anúncio: H.264, AAC estéreo 128 kbps ou mais | H.264 recomendado | H.264 High, AAC-LC 48 kHz, 384 kbps; 8 Mbps em 1080p (ajuste geral do YouTube) |
| Duração | grava até 20 min; recomendado a não seguidores até 3 min | 3 min para todos; 5 ou 10 para alguns | até 3 min |

Nossa conclusão: um MP4 1080x1920, H.264 com AAC, 30 fps ou mais e até 3 min serve aos três destinos (em 24 fps o Instagram fica abaixo do mínimo declarado). A Meta cita 20, 15 e 3 minutos em páginas diferentes; o teto prático é 3. O programa de recompensas do TikTok pede mais de 1 min e 1080p ou mais: faça uma versão por destino. Deixe o `moov` no início (`-movflags +faststart`).

## Contrato do HyperFrames

O HyperFrames (HeyGen, Apache-2.0) transforma HTML em vídeo: abre a página no Chrome, avança uma timeline pausada quadro a quadro e codifica com FFmpeg, com mesma entrada e mesmos pixels. Pede Node 22 ou superior e FFmpeg; está na série 0.8 (a mais nova que vimos em 01/11/2026 era a 0.8.228) [oficial]. Fixe a versão: `npx --yes hyperframes@0.8.105 render ...` [testado].

- Todo elemento temporizado leva `class="clip"`, `data-start` e `data-duration` (segundos). A duração do vídeo é o `data-duration` da raiz.
- Cada composição monta uma timeline GSAP pausada e a registra no fim: `window.__timelines["<id>"] = tl`, com o mesmo id de `data-composition-id`.
- Proibidos `Date.now()`, `Math.random()` sem semente, rede, timers e `repeat: -1`. Sem `transform` de CSS no elemento que o GSAP move; use `fromTo`.
- Todo `<audio>` e `<video>` leva `id`: sem `id`, o áudio fica fora do mix e o render sai mudo. Nunca chame `play()`, `pause()` ou seek em mídia.
- Caminhos de asset são relativos à raiz (`assets/...`).
- Three.js, canvas e Lottie desenham a partir do tempo do evento `hf-seek`. Nosso padrão: um tween de relógio com `draw(t)` função pura do tempo [testado].

Laço de trabalho [oficial]: `npx hyperframes init <pasta> --non-interactive --example=blank`, escreva o HTML, rode `npx hyperframes check --json` (lint, layout, contraste) e `npx hyperframes snapshot --review` (folhas de quadros), veja com `npx hyperframes preview --background` e só então `npx hyperframes render --quality draft|looks|delivery --output saida.mp4`. Para transparência use `--format mov` (ProRes 4444, formato com canal alfa); `webm` em qualidade draft saiu sem alfa [testado].

## Render em pedaços, memória e VM

Uma timeline mestra toca só o trecho de T0 a T1 da timeline original. Um script reescreve o HTML de cada pedaço: ajusta o `data-duration` da raiz, desloca e apara cada `<video>` e tira do DOM o vídeo fora da janela. No fim entra o registro novo [testado]:

```js
const __m = gsap.timeline({ paused: true });
__m.add(tl.tweenFromTo(T0, T1, { ease: "none", duration: T1 - T0 }), 0);
window.__timelines["main"] = __m;
```

Renderize cada pedaço com `npx hyperframes render -c chunk_N.html --workers 2 --output chunks/N.mp4` e junte com `ffmpeg -f concat -safe 0 -i lista.txt -c copy saida.mp4`. O que medimos [testado]: 4 min de vídeo falado em pedaços de 50 s no PC (~2,5 min cada); um vídeo de cerca de 14 min em pedaços de 60 s (4 a 8 min cada); 3:57 em 8 pedaços de 30 s na VM, em paralelo (~5 min no total). Relato, sem script reconferido: vídeo longo com alfa, em dezenas de pedaços de 30 s, ~20 min.

No PC [testado]:

- Cada worker abre um Chrome (~256 MB). No máximo 2 coisas pesadas por vez; não encerre o navegador do usuário sem pedir.
- Um pedaço por chamada: o agente encerra processos em segundo plano quando falta RAM, e os pedaços prontos ficam. Montagem final acima de 10 min também é encerrada: monte em partes de 80 s e junte com `concat -c copy`.
- Com o navegador aberto, o commit de memória do Windows chegou a ~1,7 GB: rode `loudnorm` em passo separado e o ProRes 4444 com `-threads 1`.
- Multi-worker sem stream pede ~70 GB no disco do sistema: use `HF_CAPTURE_PARALLEL_STREAM=true` e `TEMP` e `TMP` em outro disco.
- Alfa de mais de 30 min passa de 30 GB: componha com `-f concat`, sem emendar. PNG de 3 MB derruba o `snapshot` (use JPG até 1080 px). B-roll com keyframe a cada 10 s congela no seek: recodifique com `-g 30`.

Na VM (o HyperFrames renderiza em CPU) [testado]. Aluguel, SSH, custo e destruição da máquina estão no [capítulo 06](06-gpu-como-local.md); aqui ficam os pontos do HyperFrames:

1. Ofertas de 64 núcleos custaram US$ 0,27 a 0,54 por hora (alugadas em outubro de 2026). Confirme o gasto com o dono antes de alugar.
2. Imagem de PyTorch traz ffmpeg do conda sem `libx264` (`export PATH=/usr/bin:$PATH`). Instale `unzip` antes de `hyperframes browser ensure`, as bibliotecas do Chrome e `fonts-noto-color-emoji` (sem ela o emoji vira quadrado).
3. Veja o limite de processos do contêiner (`pids.max`): numa oferta era 1792 e só 3 pedaços (~450 threads cada) cabiam; em outras rodamos 8 e 9. Um processo com 24 ou mais workers empaca.
4. Nunca escreva `pkill -f "texto"` dentro do comando ssh: ele casa com o próprio comando e derruba a sessão. Ao terminar, baixe, confira o md5 e destrua a máquina (não só pare).

## Receitas

Cada receita saiu de projeto real [testado]. Antes de recortar, trocar fundo ou animar o rosto de alguém, tenha o consentimento da pessoa por escrito ([capítulo 11](11-licencas-e-consentimento.md)). Os parâmetros finos estão em `references/receitas.md`, na skill [estudio-motion](../skills/estudio-motion/SKILL.md).

### Receita 1: 3D atrás da pessoa

Quando usar: selfie vertical de baixa resolução que precisa de profundidade, em trechos de 10 a 20 s.

Passos:

1. Recorte a pessoa com um modelo de matting em vídeo (usamos Robust Video Matting em ONNX na CPU) ou com `npx hyperframes remove-background pessoa.mp4 -o pessoa.webm`. Limpe o alfa: borda justa e preencha só buracos pequenos, nunca a área fechada entre braço e corpo.
2. Fundo em Three.js local, com `draw(t)` pura e palavras-chave da fala comandando cada entrada. HUD em composição transparente, render `.mov`.
3. Componha no ffmpeg com `alphamerge` e `overlay`, mais legenda, grão e vinheta leves.

Armadilhas: `maskedmerge` com máscara cinza em yuv420p deixa um fantasma do fundo; a sombra no topo da sala denuncia o recorte, então recorte só nos momentos de efeito; o matting derruba braço de microfone e pisca em objeto na mão [fornecedor]. Licença do modelo de matting: não verificamos.

Veredito: teste de 15 s aprovado para mostrar; sem veredito final.

### Receita 2: tela dividida vertical, motion em cima

Quando usar: vídeo falado (convite, aula, explicação) em 1080x1920 que não pode ter tela sem motion.

Passos:

1. Fala limpa: transcrição palavra a palavra sem limpeza (o Whisper escondia tropeços; o Scribe v2 da ElevenLabs manteve) e corte de vídeo e áudio no mesmo quadro (a diferença caiu de 120 ms para 0,1 ms).
2. Mapa do corpo: matting a 5 quadros por segundo acha a cabeça; depois do render, meça quanto dela o motion cobre (limite de 3%).
3. A metade de cima sai de um script: cada fala ganha um evento preso à frase (`T("frase")` acha o instante na transcrição), então trocar a fala regenera sem reescrever tempos. Palco 3D contínuo e takes reais em painéis inclinados.
4. Render do topo (1080x960, MP4 opaco, bem mais leve que ProRes) em pedaços de 50 s; montagem em partes de 80 s.

Armadilhas: flash com vários `fromTo` (use `immediateRender: false`); `<video>` sem `id` congela; GSAP em CDN no HTML gerado.

Veredito: aprovada depois de três versões horizontais reprovadas por falta de movimento no vídeo falado; para vídeo falado, partimos dela.

### Receita 3: dossiê (mesa de investigação)

Quando usar: episódio de ~3 min que apresenta uma pesquisa com dados públicos como dossiê, com provas caindo numa mesa.

Layout em 1080x1920: topo (y 0 a 960) com takes e imagens; divisória (960 a 1088) com a legenda; mesa (1088 a 1848), viewport sobre uma mesa gigante com provas em grade.

Passos:

1. Dossiê com fonte para cada número; takes transcritos por palavra; silêncios acima de 0,6 s cortados.
2. Cada prova é um evento com instante e efeito: cair, máquina de escrever, carimbo (escala 3,2 → 1 em 0,16 s, com tremor da mesa), pop, marca-texto, riscado e fio vermelho em SVG.
3. A câmera segue uma lista (instante, alvo, zoom) calculada depois de carregar as fontes e começa 0,32 s antes do item.
4. SFX gerados uma vez e mixados pelas deixas; render em VM (8 pedaços de 30 s); confira quadros e a transcrição do MP4 final.

Armadilhas: `<img>` escondida trava a preparação de cada worker por 45 s (use `background-image`); afirmação sobre empresa real exige fonte, e demo leva a marca "dados fictícios"; o layout (legenda em y 1024, mesa até y 1848) é anterior à régua de área segura: reajuste.

Veredito: estilo aprovado pelo dono depois de reprovar preto e dourado.

### Receita 4: ilustração em giz (marca sem filmagem)

Quando usar: Reel de cerca de 1 min que "gera tudo": ilustração, B-roll, voz e trilha.

Passos:

1. Roteiro em JSON; voz por TTS a velocidade 1,0 (a 0,9 o vídeo estourou o tempo previsto); tempo por palavra com faster-whisper local; trilha sintetizada; ilustrações em giz pastel, proporção 2:3.
2. Script gera o HTML 1080x1920; render em pedaços de 60 s; mixagem com sidechain (a trilha abaixa quando a voz entra). Confira com `ffmpeg -v error -f null -`.
3. A revelação em giz usa canvas: um campo de ruído semeado define quando cada ponto aparece, primeiro como esboço (cinza e sépia), depois em cor. O grão salta 8 vezes por segundo, como em stop motion.

Armadilhas: filtro sépia no wrapper, não no `<video>`; ilustração em JPG até 1080 px; logo com fundo transparente de verdade (`multiply` deixa um quadrado); uma mixagem saiu corrompida e só o `-v error` mostrou. Não verificamos a licença do B-roll nem das imagens geradas.

Veredito: a legenda palavra por palavra foi aprovada.

### Receita 5: profundidade a partir de imagem

Quando usar: vídeo vertical longo feito de ilustrações geradas, com paralaxe 2.5D.

Passos:

1. Gere as imagens (2:3). O gerador que usamos travou com 4 pedidos em paralelo; ficamos em 2.
2. Mapa de profundidade com modelo monocular (Depth Anything V2 small em ONNX na CPU), normalizado pelos percentis 1 a 99 e levemente desfocado.
3. Em Three.js, planos deslocados pelo mapa criam a paralaxe; brilhos em blending aditivo; câmera dirigida pela timeline. Render em pedaços de 60 s.

Armadilhas: Three.js e GSAP em arquivos locais (o CDN derrubou o render num pedaço do meio); blending aditivo estoura o brilho, então use intensidades baixas; a versão leve em 720p ficou muitas vezes menor que o master. Licença do modelo de profundidade: não verificamos.

### Receita 6: reel com detecção real

Quando usar: takes de celular de um lugar real em que a IA mostra um sistema funcionando. O motion precisa parecer real: sistema de verdade sobre a filmagem, não card genérico.

Passos:

1. Monte o mapa antes: roteiro, pipeline e público (quem vende o serviço, não o dono do negócio). Transcreva os takes por palavra e gere a narração com marcas de tempo.
2. Rode a detecção em VM com GPU (YOLO com rastreador, ~3 min por take). Salve um JSON a 30 fps com ids, primeira aparição e contagem acumulada; o mapa de calor sai dos rastros reais.
3. No HyperFrames, desenhe caixas, rastros e contadores num canvas sincronizado com o vídeo, a partir do JSON. Traduza os nomes das classes e use confiança mínima de 0,45.
4. Os takes entram inteiros, na velocidade real e mudos, com blocos de narração por cima e telas só de motion entre eles. Render em VM, em pedaços de 10 s.

Armadilhas: não corte o take no meio da fala nem ponha voz gerada por cima da fala da própria pessoa (narre sobre takes mudos); nada de caixa de detecção no rosto de quem fala nem HUD dentro do vídeo horizontal, porque polui; em vídeo deitado, mantenha o vídeo inteiro no meio com cópia borrada no fundo (cortar em 9:16 some o rosto). Licença do modelo de detecção: não verificamos.

## Ferramentas de motion por código

Regra comum: a animação precisa ser função do tempo do quadro, não do relógio do navegador. Transição CSS solta e `requestAnimationFrame` livre quebram o determinismo [oficial]. Licenças vistas em 01/11/2026 [oficial]:

| Ferramenta | Licença | Armadilha |
|---|---|---|
| HyperFrames | Apache-2.0 | Pré-1.0; o app Studio pede conta HeyGen gratuita; mídia HeyGen gasta créditos |
| Remotion | Própria, código disponível, não é open source; grátis para indivíduos, até 3 pessoas em empresa lucrativa e sem fins lucrativos | De 4 pessoas em diante: Creators US$ 25 por mês por pessoa; Automators US$ 0,01 por render, mínimo US$ 100 por mês. O FAQ já soma contratados; a 5.0 também |
| Revideo, Motion Canvas, Three.js | MIT | Revideo é 0.x, de uma empresa; Motion Canvas não publica no npm desde 02/2025 |
| GSAP | "No Charge" da Webflow, uso comercial livre desde 30/04/2025 | Não é OSI e é revogável; veta ferramenta que concorra com a Webflow; o texto não fala em vídeo renderizado |
| Lottie | Players MIT; arquivos do LottieFiles sob a Lottie Simple License | Derivado segue a mesma licença; cada arquivo pode ter outra |
| Rive | Runtimes MIT | Plano gratuito exporta com selo de abertura; export oficial em MP4 não encontrado |
| Claude Motion | Produto da Anthropic, beta em Team e Enterprise desde 08/10/2026 | Exporta MP4, sem modelo de vídeo gerativo; não testamos |

## Escolas de estilo

| | Contenção [fornecedor, praticante] | Impacto [testado] |
|---|---|---|
| Marca | Sem quique em letra, câmera viva e contida, poucos elementos, um acento, título que pousa sem continuar deslizando | `back.out` em letra, giro 3D, glitch, tremor, carimbo com escala 3,2, cena nova a cada 2 a 4 s, nunca tela sem motion |
| Funciona quando | A marca é o assunto (vinheta, logo, lançamento) e ninguém disputa a atenção | Há pessoa falando e o motion compete com o scroll; série com conceito e gancho em 2 s |
| Falha quando | O vídeo falado fica com tela parada: versões nossas com motion tímido foram reprovadas | Cobre o rosto, briga com a legenda ou entra em marca que pede calma |

Não existe medição independente de qual converte mais [sem medição]. O chefe do Instagram prevê estética mais crua e o guia do TikTok diz que o público quer momentos reais, não polimento perfeito [oficial]; nenhum dos dois fala de motion. Critério prático: decida por quem ocupa o centro da atenção. Rosto e voz pedem a densidade do impacto, com rosto livre e legenda como apoio; a marca pede contenção. Overshoot em letra e deriva de escala em toda cena só no impacto.

## O que funcionou e o que foi reprovado

Funcionou [testado]: sistema, produto e acervo reais do dono no lugar de ilustração e card; motion que não para mas não cobre o rosto; transição suave em vez de só corte seco; gancho em 2 s com som nos golpes; marca inventada em vez de logo real; palavras de impacto em motion em vez de legenda inteira; aprovar em etapas, primeiro só para o dono.

Evite [testado]: profundidade falsa (motion 2D chapado quando a peça pede 3D); qualquer motion sobre o rosto; fundo preto em excesso; material genérico do pacote no lugar do acervo do dono; narração gerada por cima de uma fala que a pessoa já faz; cards e painéis de exemplo grandes demais; roteiro escrito para o público errado; trilha alta sob a voz; legenda baixa, grande ou que pula; motion encostado nas laterais; qualquer card parado por mais de 5 a 6 s.

## O que deu errado aqui

- **Efeito que existe na prévia e some no vídeo.** Tween ou pulso solto, fora da timeline, roda no relógio real. Solução: tudo na timeline. `tl.call()` também não dispara no render, e iframes ficam congelados.
- **Render em branco ou travado.** GSAP e Three.js de CDN derrubaram um pedaço no meio da fila. Solução: arquivos locais com versão fixa.
- **Planeta virou disco amarelo na VM.** `smoothstep` com `edge0` maior ou igual a `edge1` é indefinido: no PC deu certo, no Chrome da VM não. Solução: bordas crescentes e largura positiva.
- **Transcrição em inglês.** O `transcribe` padrão traduz: use `--model small --language pt`.
- **Skills com referências inexistentes.** Três skills do pacote citavam arquivos que não existem na versão instalada: rode `npx hyperframes skills update <nome>`.
- **Regra externa contra o gosto do dono.** Seguir à risca uma skill de estilo gerou peça reprovada. Nossa ordem: contrato técnico, pedido do dono, marca, referência, gosto da casa.

## Links

- [HyperFrames (Apache-2.0)](https://github.com/heygen-com/hyperframes) e [guia rápido](https://hyperframes.heygen.com/quickstart): motor, skills oficiais e instalação.
- [cinetic (MIT, Leonxlnx)](https://github.com/leonxlnx/cinetic): direção de motion em código. [ANIMATE (MIT, cth9191)](https://github.com/cth9191/animate): animação procedural em canvas.
- [Meta Ads Guide, Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels) e [Meta Business Help](https://www.facebook.com/business/help/980593475366490/): formatos e zona de 14%, 35%, 6%.
- [Instagram Help, tamanho do Reel](https://help.instagram.com/1038071743007909) e [gravar Reel](https://help.instagram.com/225190788256708): proporção, fps, duração.
- [TikTok Ads, in-feed](https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads?redirected=2), [boas práticas](https://ads.tiktok.com/help/article/creative-best-practices?lang=en) e [API de envio](https://developers.tiktok.com/docs/en/content-posting-api-media-transfer-guide): formatos, gancho, limites.
- [YouTube, Shorts de 3 minutos](https://support.google.com/youtube/answer/15424877?hl=en), [Shorts](https://support.google.com/youtube/answer/10059070?hl=en) e [codificação](https://support.google.com/youtube/answer/1722171?hl=en): duração, resolução, H.264 e AAC.
- [WCAG 2.2, três flashes](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html): critério 2.3.1. [Material 3, tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs): curvas e durações.
- [Netflix](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide) e [BBC](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles): velocidade de legenda. [EBU R 128](https://tech.ebu.ch/docs/r/r128.pdf): loudness.
- [Temporal typography, 2024](https://www.grid.uns.ac.rs/symposium/download/2024/89.pdf) e [Dost e Huang, 2026](https://archives.marketing-trends-congress.com/2026/pages/PDF/paper_professor_DOST_HUANG.pdf): estudos pequenos citados.
- [Remotion, licença](https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md) e [FAQ](https://www.remotion.pro/faq); [GSAP](https://gsap.com/community/standard-license/); [Lottie](https://lottiefiles.com/page/license); [Rive](https://rive.app/pricing): licenças e preços.
- [Revideo](https://github.com/midrender/revideo), [Motion Canvas](https://github.com/motion-canvas/motion-canvas), [Three.js](https://github.com/mrdoob/three.js) e [Claude Motion](https://support.claude.com/en/articles/17454997-get-started-with-claude-motion): ferramentas citadas.
- Neste repositório: [workflow](01-workflow-completo.md), [folha de storyboard](03-folha-de-storyboard.md), [edição e corte](04-edicao-e-corte.md), [GPU como se fosse local](06-gpu-como-local.md), [conferência e entrega](10-conferencia-e-entrega.md), [licenças e consentimento](11-licencas-e-consentimento.md) e [/escolhermotion](09-escolhermotion.md).
