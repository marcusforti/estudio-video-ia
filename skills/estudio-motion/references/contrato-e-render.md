# Contrato do HyperFrames, render em pedaços e VM

Resumo do que usamos. A fonte oficial é o repositório do HyperFrames (HeyGen, Apache-2.0) e as skills dele; se algo divergir, vale o oficial. Fixe a versão do CLI em cada projeto: `npx --yes hyperframes@<versão> ...`. Em outubro de 2026 usamos a 0.7.57 e a 0.8.105.

## Contrato

1. Todo elemento temporizado leva `class="clip"`, `data-start` e `data-duration` (segundos) e aparece em [início, início + duração). A raiz leva `data-composition-id`, `data-width`, `data-height` e `data-duration`.
2. A duração do vídeo é o `data-duration` da raiz, lido uma vez na compilação.
3. Cada composição monta uma timeline GSAP pausada e a registra depois dos tweens: `window.__timelines["<data-composition-id>"] = tl`. Se montar dentro de `document.fonts.ready.then(...)`, registre só no fim do callback.
4. Proibidos: `Date.now()`, `Math.random()` sem semente, rede, timers e `repeat: -1`. Tudo o que se vê é função do tempo da timeline.
5. Não anime `display`, `visibility` nem `autoAlpha` num `.clip`; anime um filho. Sem `transform` de CSS no elemento que o GSAP move; use `fromTo`. Anime transform, não `left`, `top`, `width` ou `height`.
6. Nunca chame `play()`, `pause()` ou seek em mídia. `<video>` com som leva `data-has-audio="true"`; sem som, `muted`. Música e voz são `<audio>` separado.
7. Todo `<audio>` e `<video>` leva `id`. Sem `id`, o áudio fica fora do mix e o render sai mudo.
8. Só 18 fontes embutidas resolvem por nome; as outras pedem `@font-face` para arquivo em `assets/fonts/`.
9. Caminhos de asset são relativos à raiz (`assets/...`).
10. Grade, grão, desfoque e vinheta sobre filmagem passam por `npx hyperframes media-treatment`, não por filtro CSS.
11. Three.js, canvas, Lottie e CSS keyframes desenham a partir do tempo do evento `hf-seek`. Nosso padrão: um tween de relógio, `tl.to(clock, { v: DUR, ease: "none", onUpdate: () => draw(clock.v) })`, com `draw(t)` função pura.
12. Pulso ambiente precisa estar na `tl`: `gsap.to` solto roda no relógio real e some do vídeo. `tl.call()` não dispara no render. Iframes não são escrubados.
13. Vários `fromTo` no mesmo elemento (flash) pedem `immediateRender: false`.
14. Bibliotecas e fontes em arquivo local com versão fixa. Um CDN fora do ar derruba o render.

## Laço de trabalho

```
npx hyperframes init <pasta> --non-interactive --example=blank
npx hyperframes check --json                 # lint, layout, contraste
npx hyperframes snapshot --review            # folhas de quadros
npx hyperframes preview --background
npx hyperframes render --quality draft --output rascunho.mp4
npx hyperframes render --quality delivery --output final.mp4
```

Transparência: `--format mov` (ProRes 4444). `webm` em qualidade draft saiu sem alfa. `npx hyperframes transcribe` traduz para inglês no modelo padrão: passe `--model small --language pt`. Se uma skill do pacote citar referência que não existe, rode `npx hyperframes skills update <nome>`.

Variáveis que usamos em scripts: `HF_CAPTURE_PARALLEL_STREAM=true` (com `TEMP` e `TMP` em outro disco, evita ~70 GB no disco do sistema), `PRODUCER_ENABLE_CHUNKED_ENCODE=true`, `FFMPEG_ENCODE_TIMEOUT_MS=7200000`, `PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=300000` e `PRODUCER_PLAYER_READY_TIMEOUT_MS=300000` (páginas pesadas na VM), `ONNXRUNTIME_NODE_INSTALL_CUDA=skip` (máquina com GPU em que o onnx quebra).

## Render em pedaços

Uma timeline mestra toca só o trecho de T0 a T1 da original. Um script reescreve o HTML de cada pedaço: ajusta o `data-duration` da raiz, desloca o `data-start` de cada `<video>`, soma o corte em `data-media-start` (vezes `data-playback-rate`), apara o `data-duration` e remove do DOM o vídeo fora da janela. No fim, troca o registro da timeline:

```js
const __m = gsap.timeline({ paused: true });
__m.add(tl.tweenFromTo(T0, T1, { ease: "none", duration: T1 - T0 }), 0);
window.__timelines["main"] = __m;
```

```
npx hyperframes render -c chunk_N.html --workers 2 --output chunks/N.mp4
ffmpeg -f concat -safe 0 -i lista.txt -c copy saida.mp4
```

Tamanhos que funcionaram: 50 a 60 s no PC (2 workers, um pedaço por chamada) e 10 a 30 s na VM, vários em paralelo. Num pedaço de 50 s com topo opaco 1080x960, ~2,5 min cada.

## Memória e disco no PC

- Cada worker abre um Chrome (~256 MB). No máximo 2 coisas pesadas por vez; não encerre o navegador do usuário sem pedir.
- Um pedaço por chamada: o agente de código encerra processos em segundo plano quando falta RAM, e os pedaços prontos ficam.
- Com o navegador aberto, o commit de memória do Windows chegou a ~1,7 GB. Rode `loudnorm` (segura ~3 s de quadros) em passo separado e o ProRes 4444 com `-threads 1`.
- Montagem final acima de 10 min é encerrada: monte em partes de 80 s e junte com `concat -c copy`. Com `-ss` depois das entradas o ffmpeg processa tudo antes: busque direto nas fontes.
- Nunca use a mesma entrada em dois ramos do ffmpeg com deslocamento de tempo. Somas de ~100 `between()` falham: some em blocos de 8.
- Alfa de mais de 30 min passa de 30 GB; ProRes 4444 ≈ 350 MB por 80 s. Não emende: componha com `-f concat`.
- PNG de 3 MB derruba o `snapshot` por tempo esgotado: use JPG até 1080 px e `--timeout 90000`.
- `<video>` mais longo que a fonte quebra o render (ajuste `data-playback-rate`). B-roll com keyframe a cada 10 s congela no seek: recodifique com `-g 30`.

## VM alugada

Só depois do portão de gasto. O HyperFrames renderiza em CPU: 64 núcleos bastam. No provedor que usamos (Vast, CLI `vastai`), ofertas de 64 núcleos custaram US$ 0,27 a 0,54 por hora (em outubro de 2026; o preço varia por oferta).

1. Prefira ofertas verificadas. Uma de 128 núcleos deu "GPU error"; duas travaram em "loading" (`create` com `success False` não sobe; destrua com `-y`).
2. Imagem `ubuntu:22.04` com SSH direto funcionou, e `node:22-bookworm` também. Imagem de PyTorch traz ffmpeg do conda sem `libx264`: `export PATH=/usr/bin:$PATH`.
3. Instale `unzip` antes de `hyperframes browser ensure`; depois as bibliotecas do Chrome (`libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2`) e `fonts-noto-color-emoji` (sem ela o emoji vira quadrado). Use fontes abertas.
4. Sessão: `touch /root/.no_auto_tmux`, `ssh -n` e `setsid ... < /dev/null` (com `nohup &` o terminal prende). Nunca escreva `pkill -f "texto"` dentro do comando ssh: ele casa com o próprio comando e derruba a sessão. Mate por script em arquivo.
5. Veja o limite de processos do contêiner (`pids.max`). Numa oferta era 1792 e cada pedaço usava ~450 threads: só 3 pedaços cabiam. Em outras rodamos 8 e 9 em paralelo. Um processo só com 24 ou mais workers empaca.
6. Transferência: um `scp` de 150 MB caiu em 95%. Retome com `tail -c +N | ssh "cat >>"` e confira o md5. Suba o bruto e recrie os clipes na VM.
7. Leia a segunda linha do resumo do render: `screenshot` com GPU por software no Linux é o caminho lento.
8. Baixe, confira o md5 e destrua a máquina (não só pare). Uma VM esquecida parada continua custando.

## Depois do render

- `ffprobe` do arquivo: duração, tamanho, fps.
- `ffmpeg -v error -i final.mp4 -f null -` não pode imprimir nada.
- Transcreva o áudio do MP4 final e compare com a fala da SPEC.
- Confira o volume (perto de -14 LUFS, pico até -1 dBTP) e olhe a folha de quadros do arquivo final.
