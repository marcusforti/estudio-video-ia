# Receitas: parâmetros finos

Passos, armadilhas e vereditos estão no capítulo 08 (https://github.com/marcusforti/estudio-video-ia/blob/main/conhecimento/08-motion.md). Aqui ficam os números que reproduzem cada receita. São valores de projetos reais nossos, não regras: ajuste ao seu material. Antes de recortar, trocar fundo ou animar o rosto de alguém, tenha o consentimento da pessoa. Não verificamos a licença dos modelos citados (matting, profundidade, detecção): confira antes de uso comercial.

## Receita 1: 3D atrás da pessoa

- Corte: palavras com pausa menor que 0,45 s se unem (folga de −0,05 s e +0,16 s), quadros arredondados a 1/30 s, `ffmpeg concat` com `-crf 14`.
- Matting: Robust Video Matting (`rvm_mobilenetv3_fp32.onnx`) em `onnxruntime` na CPU, entrada 540x960, `downsample_ratio` 0,4, estados recorrentes; saída em cinza (ffv1) escalada a 1080x1920; ~0,24 s por quadro.
- Pós-alfa (OpenCV): `soft = clip((a − 70) × 1,4)`; `hard = a > 110`; preencha só buracos com área menor que 22.000 px e `y > 0` (nunca a área entre braço e corpo); erosão elíptica 7x7; desfoque gaussiano 1,1.
- Fundo: Three.js local, `WebGLRenderer` 1080x1920 com `preserveDrawingBuffer`, neblina escura, grade, poeira, núcleo, cartões e 6 agentes em órbita. Palavras-chave da fala (`K = { palavra: segundo }`) comandam a entrada de cada elemento. Tween de relógio com `draw(t)` pura. 15 s renderizaram em 1 min 20 com GPU.
- HUD: raiz transparente, fonte por `@font-face` local, render `.mov`.
- Composição: `alphamerge` e `overlay` (nunca `maskedmerge`), HUD por cima, legenda ASS limpa, `noise=alls=4` e `vignette=PI/6`. Áudio: `highpass=70`, `afftdn=-25`, `loudnorm -14`, `amix` com os SFX e `alimiter 0,8`. `-threads 1` nas entradas; saída `-crf 17`.
- Alternativa nativa: `npx hyperframes remove-background pessoa.mp4 -o pessoa.webm` (`--quality balanced` crf 18; `best` crf 12 para plano-herói). Três camadas: `<video>` base opaco, título com `z-index` 2 e recorte `webm` num wrapper (a opacidade vai no wrapper; o framework força `opacity: 1` no elemento com `data-start`). `data-layout-allow-occlusion` no recorte. Palavra atrás da cabeça funciona com 30 a 55% coberta: com menos de 15% ela flutua, com mais de 65% some.
- Limites do matting: derruba braço de microfone, vaza com equipamento grande, pisca em objeto na mão; baixa ~168 MB na primeira vez; ~2 fps a 1080p na CPU.

## Receita 2: tela dividida vertical

- Motor de cena: entra em 0,55 s `expo.out`; sai em 0,26 s `power2.in`; pop `back.out(1.8)`; letras `rotateX −100 → 0` com `back.out(1.6)` e 0,03 s entre letras; deriva `scale 1 → 1,06`.
- Cenas: pop, esquerda, direita, sobe, flip, carimbo, fade, cresce. Transições: flip, zoom, whip, up, spin, drop, glitch. Peças: máquina de escrever com `steps()`, roleta, barra, riscado, palavra-chave com letras.
- Âncora: `T("frase")` acha o instante da frase na transcrição (sem acento, em minúsculas). O script gera o HTML do topo, a legenda ASS e a lista de eventos de SFX.
- Fala: transcrição verbatim; corte de vídeo e áudio no mesmo quadro numa só passada (0,1 ms de diferença; 120 ms na primeira versão); compense −30 ms do AAC no remux.
- Mapa do corpo: matting a 5 quadros por segundo em 480x270 (cabeça e faixa de entrada dos cards). Depois do render, mede quanto da cabeça o alfa do motion cobre: limite de 3%.
- Render do topo: cortes a cada 50 s, 2 workers, MP4 opaco 1080x960. Montagem em partes de 80 s: modo áudio, modo vídeo (início, fim) e modo trecho final com busca direta nas fontes; depois `concat -c copy` e o áudio.

## Receita 3: dossiê

- Layout 1080x1920: topo 0 a 960; divisória 960 a 1088 (128 px, borda vermelha de 6 px); mesa 1088 a 1848 (760 px), provas em grade de 6 colunas (cartão 1180x860, ziguezague, jitter ±50 px); barra de progresso de 8 px em y 1912 (`drawbox`).
- Efeitos por prova (instante e efeito): `drop` (cai 260 px, gira −18°, escala 1,25 → 1, 0,5 s `power3.out`); `type` (`clip-path` com `steps(n)`); `stamp` (escala 3,2 → 1 em 0,16 s `power4.in`, opacidade 0,93, a mesa treme com `elastic.out(1,.3)`); `mark` (marca-texto, `scaleX`); `write` (`clip-path`, 0,55 s); `pop` (`back.out(2.2)`); `slam` (escala 2,6 e desfoque 8 → 0 em 0,22 s); `draw` (círculo); `strike`; `grow` (barras); tarja; `fio` (SVG, `stroke-dashoffset`, 0,6 s).
- Câmera: lista (instante, alvo, zoom) calculada depois das fontes; move x, y, escala e rotação ±1,2° em 0,55 s `power3.inOut` (0,9 s para o plano aberto), começando 0,32 s antes do item.
- Provas: pasta, polaroid, crachá, memo, fita VHS, planta, post-it, ficha, papel, print de site, organograma, mapa com rota, envelope, lacre, bilhete, selo CONFIDENCIAL.
- Paleta e fontes: tinta `#1b1612`, vermelho `#D7261E`, papel `#F3EBDD`, kraft `#C9A06A`, manila `#E6CF9C`, azul de caneta `#1f4fb8`, marca-texto `#F5E74A`. Anton, Special Elite, Permanent Marker, IBM Plex Mono e Archivo Black (confira a licença de cada uma).
- Gancho: valor grande estoura aos 0,9 s e carimbo cai aos 2,36 s; deixas de SFX: whoosh em −0,3 s, papel em 0,0, impacto em 0,9, carimbo em 2,36.
- SFX gerados uma vez por texto (API de efeitos da ElevenLabs, `prompt_influence 0.6`): carimbo 1,0 s, máquina 2,0, whoosh 0,7, impacto 1,5, papel 0,8, foto 1,0, marcador 0,8, pop 0,5, tic 0,5, glitch 0,8 e trilha de suspense de 22 s em loop. Ganhos no mix: carimbo .55, máquina .22, whoosh .30, impacto .55, papel .18, foto .35, marcador .25, pop .25, tic .30, glitch .45, trilha .10; tetos de duração (máquina 1,1 s; papel e marcador 0,6 s); mínimo de 0,18 s entre repetições; fade de 60 ms; `tanh(x·1,1)·0,9` no fim; `amix` com pesos `1 0.85`.
- Render: 8 pedaços de 30 s, 4 workers cada, em VM. Um processo só com 24 workers empaca.
- O layout acima é anterior à régua de área segura: suba a legenda e mantenha as provas importantes acima de y 1440.

## Receita 4: ilustração em giz

- Revelação (canvas): campo de ruído semeado de 108x192 (0,58 direção + 0,32 ruído suave + 0,10 ruído branco), limiar `(p × 1,18 − F) / 0,18`. Primeiro o esboço (cinza, sépia 0,45, contraste 1,5) com `p × 1,7`; depois a cor com `(p − 0,3) / 0,7`. O relógio `p` vai de 0 a 1 em `sine.inOut`, 2,4 s por padrão.
- Pesponto rosa: `stroke-dasharray: 16 13` costurado por `strokeDashoffset`. Linha de giz: SVG com filtro e `strokeDashoffset` em `sine.inOut`.
- Texto à mão: fonte manuscrita local com `clip-path`; duração `clamp(n × 0,045; 0,6; 1,8)`.
- Legenda palavra por palavra: desfoque 6 px → 0, sobe 14 px, 0,32 s `power2.out`. Grão de giz: salta a cada 0,125 s (8 vezes por segundo), PRNG fixo, ±30 px.
- B-roll: banco gratuito de vídeo (troque `_tiny.mp4` por `_large.mp4` no CDN); sites de banco de imagem dão 403 para `curl`; rode `cropdetect` (alguns vêm com tarja); filtro sépia no wrapper; `#caps` com `z-index` alto.
- Voz por TTS a velocidade 1,0; render em pedaços de 60 s; sidechain na mixagem; confira com `ffmpeg -v error -f null -`.

## Receita 5: profundidade a partir de imagem

- Imagem a 518x770; normalização pelos percentis 1 a 99; mapa de 256x384 com desfoque 2,2 (Depth Anything V2 small em ONNX na CPU). Foto em JPG 1280x1920, qualidade 92.
- Placas em paralaxe 2.5D deslocadas pelo mapa, figura com blending aditivo (intensidades baixas), faixas, anéis, partículas e câmera dirigida pela timeline.
- Geração de imagens: no máximo 2 em paralelo (com 4 travou). Pedaços de 60 s, 4 a 8 min cada no PC.
- A versão leve em 720p ficou muitas vezes menor que o master (~15 min de CPU).

## Receita 6: reel com detecção real

- Detecção em VM com GPU: YOLO11 e YOLO-World com rastreador ByteTrack; ~3 min por take numa RTX 3060; duas GPUs em paralelo.
- JSON a 30 fps com ids, primeira aparição e contagem acumulada. O mapa de calor sai dos rastros reais. Câmera fixa do teto: estenda o rastreamento por template matching (o OpenCV local não tinha o rastreador CSRT).
- Camada em canvas sincronizada com o vídeo desenha caixas, rastros e HUD. Traduza os nomes das classes e use confiança mínima de 0,45.
- Takes inteiros, na velocidade real e mudos; narração em blocos com marcas de tempo; voz nivelada por RMS; trilha e SFX sintetizados; legenda ASS e `loudnorm -14` no fim.
- Render em VM, pedaços de 10 s. Render local de 2:50 levou ~25 min.
- Vídeo deitado (por exemplo 832x464): vídeo inteiro no meio e uma cópia borrada no fundo. Cortar em 9:16 some o rosto.
- Sem caixa de detecção no rosto de quem fala e sem HUD dentro do vídeo horizontal.
