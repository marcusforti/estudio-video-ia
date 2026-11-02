# Edição e corte: ferramentas, receita de talking head e régua de legenda

Este capítulo é para quem edita vídeo de uma pessoa falando (Reels, Shorts, TikTok) com um agente de código, como Claude Code ou Codex. Traz o mapa das ferramentas de edição e quando escolher cada uma, a receita de corte que usamos em produção, a régua de legenda e de área segura e as armadilhas que já pagamos para aprender. A skill [estudio-corte](../skills/estudio-corte/SKILL.md) aplica a receita. Selos entre colchetes: [testado] rodamos aqui, em projeto real; [oficial] fabricante, plataforma ou norma; [fornecedor] o fabricante diz, sem confirmação independente; [independente] medição de terceiro sem interesse comercial; [praticante] opinião de quem faz, sem medição; [sem medição] não existe número confiável.

## Resumo em 30 segundos

- Reel de uma pessoa falando: corte por palavra, pausas de 0,6 s ou mais saem, folga de 0,05 s antes e 0,18 s depois de cada trecho, fade de 30 ms nas emendas e áudio em -14 LUFS (unidade de volume percebido) em duas passadas [testado].
- O gancho é a frase mais forte do vídeo inteiro, quase nunca a abertura. Mostre gancho e cortes ao dono do vídeo antes de renderizar.
- Legenda com linha de base entre y 1150 e 1300 (altura 1920). Livres: 250 px no topo, 480 embaixo, 80 à esquerda, 140 à direita [testado].
- Motion sobre a fala: HyperFrames. Vários takes: video-use. Rough cut para editor profissional: ButterCut, com alerta de licença.
- Antes de cortar, rode `ffprobe`: HDR, rotação, taxa variável e videochamada em grade mudam o que fazer.

## Mapa das ferramentas

Há duas camadas: a que corta e legenda (este repositório, sobre o FFmpeg) e a que monta ou anima (terceiros, cada um com autor e licença).

### Neste repositório

A skill [estudio-corte](../skills/estudio-corte/SKILL.md) tem dois scripts. `transcrever.py` gera a transcrição por palavra. `cortar.py` mostra o plano (gancho, cortes, avisos) e só renderiza com o código de aprovação. Serve a Reel de uma pessoa falando para a câmera, sem motion. Os dois scripts são novos, escritos a partir da receita abaixo e testados só em vídeo sintético. A receita vem de produção. O código ainda não passou por projeto real.

### Ferramentas de terceiros

| Ferramenta (autor, licença) | O que faz e quando escolher | Não escolha quando |
|---|---|---|
| **FFmpeg** ([ffmpeg.org](https://ffmpeg.org/); projeto FFmpeg; LGPL ou GPL conforme a compilação, a nossa é GPL v3 ou mais nova) | corta, junta, filtra, legenda, normaliza. Base de tudo | a decisão é editorial: ele executa e não decide |
| **faster-whisper** ([GitHub](https://github.com/SYSTRAN/faster-whisper); SYSTRAN, autoria no pacote de Guillaume Klein; MIT) | transcrição local por palavra, sem chave | o PC não tem memória para o modelo grande: use um menor |
| **video-use** ([GitHub](https://github.com/browser-use/video-use); Browser Use; MIT) | edição por conversa: transcreve com o Scribe (ElevenLabs, pago) e o agente decide os cortes lendo texto. Vários takes e entrevistas | lote de Reels no mesmo molde. Pelo código (lido, não rodado), o `render.py` fixa 24 fps, abaixo dos 30 que o Instagram exige |
| **HyperFrames** ([GitHub](https://github.com/heygen-com/hyperframes); HeyGen; Apache-2.0) | HTML vira vídeo: motion, overlays com transparência e 3D por cima da fala | cortar fala: ele toca o clipe inteiro [testado] |
| **ffmpeg-skill** ([GitHub](https://github.com/kajisho5/ffmpeg-skill); kajisho5; MIT) | 42 scripts de ffmpeg (cortar, silêncio, reenquadrar, loudness, conferir a entrega) para operação pontual e verificável | a decisão é editorial |
| **get-brolls** ([GitHub](https://github.com/engenheirodevideo/get-brolls); Bruno Moreira; MIT) | acha B-roll (cena de apoio) com origem e direitos, com prévias e aprovação humana | montar o vídeo final; imagem genérica |
| **embedded-captions, faceless-explainer, media-use** ([GitHub](https://github.com/heygen-com/hyperframes); HeyGen, skills do HyperFrames; Apache-2.0 pelo repositório, sem conferência arquivo a arquivo) | legenda atrás da pessoa; explicativo sem rosto; música, efeitos e voz | embedded-captions com vários falantes ou cortes duros |
| **video-shotcraft** ([GitHub](https://github.com/Vincentwei1021/video-shotcraft); Vincentwei1021; Apache-2.0) | filmes de produto em Remotion, com capturas reais de tela | vídeo de fala. A licença do Remotion é separada ([GitHub](https://github.com/remotion-dev/remotion)) |
| **ButterCut** ([GitHub](https://github.com/barefootford/buttercut); Andrew Ford, TubeSalt LLC; PolyForm Noncommercial 1.0.0 com a permissão adicional "Commercial Output") | rough cut (primeira montagem) de horas de bruto, exportado em XML para Final Cut Pro, Premiere ou DaVinci Resolve | quer Reel pronto, legenda ou motion; precisa de várias faixas (é faixa única) |

**Alerta de licença do ButterCut.** A permissão adicional deixa usar a ferramenta para produzir vídeos, inclusive comerciais. Não deixa distribuí-la, hospedá-la como serviço nem embuti-la em produto comercial (texto da LICENSE do repositório) [oficial]. Por isso este repositório não copia nem redistribui o código dele: só aponta o link. Leia a LICENSE antes de usar. Na nossa máquina Windows a transcrição dele não funcionou: o WhisperX trouxe duas bibliotecas (torch e ctranslate2) que brigam pela mesma DLL do OpenMP [testado]. Trocar o transcritor por faster-whisper foi proposto e não aplicado [sem medição].

Uso nosso: FFmpeg, faster-whisper e HyperFrames em produção [testado]. Do video-use adotamos regras (fade de 30 ms, corte no limite da palavra); o fluxo completo não rodou aqui. As demais foram lidas e não rodadas [sem medição], e as descrições vêm da documentação de cada projeto [fornecedor]. O HyperFrames exige Node 22 ou mais novo. Fixe a versão do pacote: uma versão publicada do CLI deu erro 404 aqui até fixarmos a anterior [testado].

## Quero X, uso Y

| Quero | Uso |
|---|---|
| Reel de uma pessoa falando, com gancho, legenda e -14 LUFS | `estudio-corte` |
| Transcrever em português, local, por palavra | `transcrever.py`. Já tenho a transcrição: `cortar.py --transcricao` |
| Melhor take entre vários, montado por beat | video-use (o Scribe é pago) |
| Tirar só o silêncio, sem transcrição | `silence.py` da ffmpeg-skill ou `silencedetect` do FFmpeg. Sem palavras, pode comer o fim da fala [praticante] |
| Motion e overlays sobre a fala | HyperFrames sobre um corte-base limpo (`--sem-legenda`); veja [Motion por código](08-motion.md) |
| Legenda estilizada atrás da pessoa | embedded-captions (um falante, sem cortes duros) |
| Rough cut para editor profissional | ButterCut (leia o alerta de licença) |
| B-roll com origem e direitos | get-brolls (aprovação humana obrigatória) |
| Cor lavada de iPhone | `estudio-corte` (`--hdr auto`). Comprimir não resolve [testado] |
| Taxa de quadros variável do celular | `ffmpeg -i in.mov -fps_mode cfr -r 30 -af aresample=async=1000:first_pts=0 -c:v libx264 -crf 16 out.mp4`. Roda no FFmpeg 8.1 em clipe sintético; o ganho em vídeo variável real não foi medido [sem medição] |

## A receita: cortar um talking head

### 1. Olhe a fonte antes de cortar

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,color_transfer:stream_side_data=rotation -of default=nw=1 bruto.mp4
```

| Você vê | Faça |
|---|---|
| `color_transfer` = `arib-std-b67` ou `smpte2084` (HDR; o iPhone grava em HLG) | converter para SDR bt709 (tonemap: ajusta o brilho do HDR à faixa do SDR). Sem isso a cor sai lavada depois que a rede reprocessa; comprimir não resolve [testado] |
| `rotation` de 90 ou -90, com 848x480 (vídeo de WhatsApp) | o FFmpeg endireita ao reencodar; confira as dimensões efetivas [testado] |
| `r_frame_rate` diferente de `avg_frame_rate` em mais de 1% (taxa variável) | fixar 30 fps na saída [praticante] |
| rosto num quadrado de uns 100 px de videochamada em grade | pare e peça o original. Ampliar para 1080 vira borrão sem conserto: confira a fonte antes de aceitar o projeto [testado] |
| duas vozes se alternando | entrevista: isole as respostas. Com sobreposição de vozes ou áudio ruim, pule o vídeo [testado] |

### 2. Transcreva por palavra

```
python transcrever.py bruto.mp4 palavras.json
python cortar.py --transcricao palavras.json --texto
```

Rodamos o faster-whisper com `large-v3-turbo`, CPU em `int8`, idioma `pt`, detecção de voz (VAD) com pausa mínima de 300 ms e `beam_size` 5 [testado]. Na CPU o tempo fica perto da duração do vídeo [sem medição]. O modelo grande estourou a memória com o navegador aberto: feche-o ou use um modelo menor [testado].

Revise antes de cortar. Palavra de quatro letras ou mais com menos de 0,1 s costuma ser erro de reconhecimento: uma vez "câmera" virou "criança" [testado]. Frase repetida quatro ou cinco vezes é o Whisper inventando texto sobre áudio ruim: descarte o vídeo [testado].

### 3. As regras do corte

| Regra e valor | Por quê | Selo |
|---|---|---|
| Corte por palavra, nunca por segmento | a fronteira cai no limite de uma palavra | [testado] |
| Corta pausa de 0,6 s ou mais | pausas menores são respiro e ficam | [testado] |
| Folga de 0,05 s antes de cada trecho | não morder o começo da palavra | [testado] |
| Folga de 0,18 s depois | o Whisper marca o fim da palavra uns 100 a 150 ms cedo; a folga cai no silêncio seguinte | número [praticante]; efeito [testado] |
| Fade de 30 ms nas duas pontas de cada trecho | tira o estalo do corte seco | [testado]; a regra aparece no video-use [fornecedor] |
| Normalizar depois do corte, medindo o áudio já cortado | o corte muda a medida | [testado] |

Uma pausa de 0,6 s não some inteira: sobram 0,23 s (0,18 mais 0,05). O video-use trata silêncio de 400 ms ou mais como candidato limpo, de 150 a 400 ms só com checagem visual e abaixo de 150 ms como inseguro [fornecedor]. A ffmpeg-skill usa 0,6 s por padrão [fornecedor]. Nosso 0,6 s veio do uso [testado]; não comparamos valores diferentes [sem medição]. Se disserem que o corte comeu uma palavra, suba a folga de depois para 0,22 s antes de mexer em qualquer outra coisa [testado].

### 4. O gancho

Gancho é o trecho mais forte colocado no começo; depois dele o vídeo segue do início do corpo. É a decisão que mais muda o resultado. Quem decide é o editor; o script só executa.

1. Leia a fala inteira. Pegar a abertura por conveniência é o erro comum.
2. Liste de 3 a 5 candidatos, com tempo. Funcionam melhor os concretos: dor nomeada, afirmação contra o senso comum, ameaça ou perda, pergunta provocativa que o vídeo responde, número surpreendente [praticante].
3. Ranqueie por "isso faz parar o dedo?" e fique com o primeiro, onde estiver. A frase forte costuma estar no meio ou no fim do bruto [praticante].
4. Complete o arco: se há preparação e revelação, inclua a revelação. Um gancho só com a preparação ficou morno [testado].
5. Traga a tensão para os 3 primeiros segundos; se a preparação é longa, use dois intervalos e deixe o miolo de fora.
6. Não repita a abertura. Se o gancho é a primeira frase do corpo, ela toca duas vezes seguidas e parece falha. Comece o corpo depois do gancho ou puxe o gancho de outro ponto [testado].

O guia de anúncios do TikTok pede gancho nos 6 primeiros segundos e a proposta nos 3 iniciais [oficial]. O Instagram diz que uma linha forte de texto no primeiro quadro pode pesar tanto quanto uma boa miniatura [oficial]. Não encontramos duração ideal de gancho publicada por nenhuma plataforma [sem medição].

### 5. Áudio em -14 LUFS, em duas passadas

No filtro `loudnorm` do FFmpeg, a primeira passada mede e a segunda aplica os valores medidos (`measured_*`) com `linear=true`, que usa ganho fixo quando é possível (ajuda do próprio filtro, `ffmpeg -h filter=loudnorm`) [oficial]. Numa passada só o ganho varia ao longo do arquivo, e isso foi a causa provável de um áudio que oscilava de volume ("bombeava") [praticante].

```
ffmpeg -hide_banner -i corte.mp4 -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i corte.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_LRA=<input_lra>:measured_TP=<input_tp>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 192k -ar 48000 saida.mp4
```

Copie os cinco valores que o primeiro comando imprime. Testamos as duas passadas em clipe sintético: o áudio saiu em -14,00 LUFS.

- **Por que -14.** Não achamos alvo de LUFS publicado por Instagram, TikTok ou YouTube; a Meta pede só AAC estéreo a 128 kbps ou mais nos anúncios de Reels [oficial]. O consenso de quem faz é -14 LUFS integrado, com limitador em -1 dBTP [praticante]. A norma de rádio e TV (EBU R 128) pede -23 LUFS e pico verdadeiro (true peak, o pico real da onda) de no máximo -1 dBTP [oficial]. Não persiga -23 em vídeo social.
- **Pico.** O `cortar.py` usa -1,5 dB de teto, para sobrar margem depois do AAC [praticante]. Meça o arquivo final.
- **48 kHz.** O `loudnorm` reamostra por dentro para 192 kHz. Sem `aresample=48000` o AAC saiu a 96 kHz, e um agendador de posts acusou áudio corrompido [testado].

### 6. Conferir

`ffprobe` do arquivo final: 1080x1920, 30 fps, cor `bt709` ou sem marcação (nunca `arib-std-b67`), áudio AAC a 48000 Hz. Depois, olhe e ouça: quadros no começo, no meio, no fim e em cada troca de legenda; de 3 a 5 emendas com fone; a legenda lida contra a fala. O Instagram exige no mínimo 720 px e 30 quadros por segundo, e acima de 3 minutos não recomenda o Reel a quem não segue o perfil [oficial]. O YouTube pede H.264 High, AAC-LC a 48 kHz e BT.709 [oficial].

## Legenda e área segura

### A régua (1080x1920)

| Zona | Medida |
|---|---|
| Livre | topo 250 px; base 480 px (nada abaixo de y 1440); esquerda 80 px; direita 140 px |
| Legenda falada | linha de base entre y 1150 e 1300 (60% a 68% da altura); nunca abaixo de y 1400 |
| Motion, cards e títulos | caixa x 80 a 940, y 250 a 1440 |
| Feed 4:5 | aparece só o miolo de 1080x1350 (somem uns 285 px em cima e embaixo): gancho e título entre y 300 e 1600 |
| Capa do Reel | a grade do perfil recorta o centro em 1080x1440 [praticante] |
| Horizontal 1920x1080 | margem de 5% (96 px) para motion, 10% (192 px) para texto; legenda com base em y 900 a 960 |

Esta régua é nossa. Nasceu quando uma legenda ficou baixa demais e a interface do Instagram a cortou, e quando o motion encostava nas laterais [testado]. Os números são convenção da casa; a plataforma não os publica [praticante]. Rotina: desenhe a caixa segura antes de animar, ponha a legenda mais alta do que parece necessário, nada encosta na borda nem no pico da animação (escala, zoom, entrada lateral) e nada cobre o rosto. Para ver a caixa sobre um quadro:

```
ffmpeg -ss 3 -i saida.mp4 -frames:v 1 -vf "drawbox=x=80:y=250:w=860:h=1190:color=red@0.8:t=4" quadro_regua.png
```

### O que as plataformas dizem

Só a Meta publica números de zona segura, e apenas para anúncios: deixar livres 14% do topo, 35% da base e 6% de cada lado [oficial]. Em 1080x1920 dá cerca de 65 px nas laterais, 269 no topo e 672 na base: caixa de x 65 a 1015 e y 269 a 1248 (conta nossa sobre o dado oficial). Nossa base livre é de 480 px, menor que os 672 da Meta, mas a legenda com linha de base até y 1248 cabe nas duas. Se o Reel puder virar anúncio, mantenha a legenda acima de y 1248. Não encontramos números oficiais para o YouTube Shorts nem para o TikTok orgânico, que publica só arquivos de modelo [sem medição].

### O estilo da legenda

O `cortar.py` usa Arial negrito de 64 px (em 1920 de altura), amarelo, contorno preto de 3 px e sombra de 3 px. Cada bloco leva até 5 palavras em até 2 linhas, medidas pela largura, com margem de 140 px dos dois lados; "e e" vira "e" só no texto exibido.

- Trate a legenda como apoio: primeiro o rosto, depois a legenda, depois o motion. Uma primeira versão com legenda grande, que pulava de tamanho, foi refeita porque roubava o olho do motion. Na aprovada, a palavra ativa só muda de cor [testado].
- Cada bloco termina quando o próximo começa. Com dois eventos sobrepostos, o libass (a biblioteca que desenha legenda no FFmpeg) empilha e aparece uma legenda fantasma [testado].
- Agrupe por largura, não por contagem fixa de palavras: palavra longa passa da margem, e o modo `WrapStyle 2` do formato ASS não quebra linha sozinho [testado].
- A BBC indica de 160 a 180 palavras por minuto e a Netflix, até 20 caracteres por segundo e 2 linhas [oficial]. São padrões de TV e streaming; não achamos estudo independente sobre legenda em vertical no celular [sem medição].

## Boas práticas, com base real

1. Confirme o plano em português claro antes de renderizar: gancho e cortes. O video-use também manda confirmar a estratégia antes de executar [fornecedor], e fazemos assim [testado].
2. Em bruto de celular com falso começo (a pessoa começa, é interrompida e recomeça a mesma fala), fique com a última tomada limpa [testado].
3. Cortar vício no meio da frase cria um jump cut (salto visível de imagem). Só com aval do dono do vídeo [testado].
4. Cada corte fecha um arco sozinho. Na dúvida, estenda: 20 segundos a mais valem mais que um corte que termina no meio da ideia [testado].
5. Marque a virada do gancho para o corpo com algo visível. Um clarão branco de 0,26 s passou despercebido; passamos a usar um zoom curto com batida grave, bem mais visível [testado]. O `estudio-corte` não faz transição.
6. Mídia de terceiros só com licença clara (CC BY ou CC0) e crédito junto do arquivo [testado]. O get-brolls segue a mesma lógica [fornecedor].
7. Terceiros numa videochamada: a dúvida vira cartão escrito, e só a resposta do dono do conteúdo fica [testado].
8. Ritmo: em 50 TikToks de talking head de alto desempenho mediu-se um corte a cada 2,7 s, e num experimento com 242 estudantes o ritmo mais alto reduziu o engajamento sustentado (amostra de conveniência) [independente]. Serve de aviso contra picotar sem motivo, não de meta.

## O que deu errado aqui

| Sintoma | Causa | Solução |
|---|---|---|
| Corte come o fim da palavra | o Whisper fecha a palavra cedo | folga de depois de 0,18 s; 0,22 s se persistir |
| Chiado nos primeiros milissegundos depois de postar por agendador | o início do AAC (priming) vira ruído quando o agendador re-codifica | 80 ms de silêncio no começo; se persistir, poste pelo celular |
| Áudio "corrompido" no agendador | AAC a 96 kHz, sem `aresample=48000` | reamostrar para 48 kHz |
| Cor lavada no Instagram | HLG BT.2020 mantido | converter para BT.709 e gravar as tags |
| Vídeo "horizontal" que era vertical | 848x480 com flag de rotação | ler a rotação no ffprobe antes de editar |
| Gancho tocou duas vezes seguidas | gancho era a abertura do corpo | corpo começa depois do gancho |
| Whisper grande estoura a memória | navegador aberto; o filtro de voz em 2 h de áudio carrega uns 2 GB | fechar o navegador, modelo menor, áudio em blocos com ponto de retomada |
| FFmpeg estoura a memória com dezenas de ramais `trim` do mesmo arquivo | cada ramal decodifica o vídeo todo | uma entrada por trecho com `-ss` antes do `-i` e um único encode, como faz o `cortar.py`. Com 70 trechos em 1080x1920, em vídeo sintético, o FFmpeg chegou a uns 1,6 GB [testado] |
| Agendador recusou arquivo grande | o que usamos limitava a uns 22 MB, e acima de 80 s o teto de taxa (`-maxrate`) não bastou | calcular o bitrate: kbit/s é aproximadamente MB x 8000 / segundos, em dois passos |
| Documentação diz uma coisa e o código faz outra (numa ferramenta nossa: pico de -1,5 dB na doc, -2,0 dB no código) | ninguém mediu o arquivo final | medir o arquivo final; o `cortar.py` imprime o resultado |

## Links

- [Instagram Help: especificações](https://help.instagram.com/1038071743007909): mínimo de 720 px e 30 fps.
- [Instagram Help: recomendação](https://help.instagram.com/225190788256708): limite de 3 minutos para novos públicos.
- [Meta Ads Guide: Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels): zona segura de anúncios, áudio AAC.
- [YouTube Help: codificação](https://support.google.com/youtube/answer/1722171?hl=en): H.264, AAC-LC a 48 kHz, BT.709.
- [About Instagram: Reels](https://about.instagram.com/blog/tips-and-tricks/how-to-make-instagram-reels): texto no primeiro quadro.
- [TikTok Ads: boas práticas](https://ads.tiktok.com/help/article/creative-best-practices?lang=en): gancho em 6 s, proposta em 3 s.
- [EBU R 128](https://tech.ebu.ch/docs/r/r128.pdf): -23 LUFS e pico de -1 dBTP em broadcast.
- [Critical Listening Lab](https://www.criticallisteninglab.com/en/learn/loudness/social-media): -14 LUFS em redes sociais.
- [BBC: legendas](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles): velocidade de leitura.
- [Netflix: legendas](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide): densidade de legenda.
- [Dost e Huang, Marketing Trends 2026](https://archives.marketing-trends-congress.com/2026/pages/PDF/paper_professor_DOST_HUANG.pdf): cortes por segundo no TikTok.
- [FFmpeg](https://ffmpeg.org/): projeto e licença.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): transcrição local, MIT.
- [video-use](https://github.com/browser-use/video-use): edição por conversa, MIT.
- [HyperFrames](https://github.com/heygen-com/hyperframes): HTML para vídeo e skills, Apache-2.0.
- [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill): 42 scripts de ffmpeg, MIT.
- [get-brolls](https://github.com/engenheirodevideo/get-brolls): B-roll com direitos, MIT.
- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft): filmes de produto, Apache-2.0.
- [Remotion](https://github.com/remotion-dev/remotion): vídeo em React, licença própria.
- [ButterCut](https://github.com/barefootford/buttercut): rough cut, PolyForm Noncommercial 1.0.0.
