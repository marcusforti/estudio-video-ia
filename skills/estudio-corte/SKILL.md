---
name: estudio-corte
description: Use quando o pedido for editar ou cortar vídeo de uma pessoa falando para Reels, Shorts ou TikTok - "corta os silêncios", "tira os vícios de linguagem", "legenda esse vídeo", "faz um corte vertical", "escolhe o gancho", "deixa o áudio em -14 LUFS" - ou quando o corte comeu o fim das palavras, a cor do iPhone saiu lavada ou a legenda foi coberta pela interface do app.
---

# estudio-corte

Corta um vídeo de uma pessoa falando para a câmera em um Reel vertical legendado: gancho no topo, pausas removidas, legenda dentro da área segura e áudio em -14 LUFS. Roda na sua máquina, sem nuvem e sem custo. Contexto, fontes e armadilhas: capítulo "Edição e corte" do Estúdio de Vídeo com IA (https://github.com/marcusforti/estudio-video-ia/blob/main/conhecimento/04-edicao-e-corte.md).

Nos comandos, `<skill>` é a pasta desta skill.

## Portões (obrigatórios)

1. **Plano antes do render.** Rode `cortar.py` sem `--aprovado`. Mostre ao dono do vídeo o gancho (texto e tempo), a lista de trechos mantidos, as pausas removidas e os avisos, e espere o "pode". Só então rode o mesmo comando com `--aprovado CODIGO`. Se ele pedir qualquer mudança, gere e mostre o plano de novo: o código muda e o script recusa o código antigo.
2. **Instalar ou baixar.** Peça confirmação antes de `pip install faster-whisper` e antes de baixar modelo (`large-v3-turbo` tem cerca de 1,5 GB). Se a transcrição for por serviço pago, diga o custo e espere o OK.
3. **Pessoas e sentido.** Se houver outra pessoa identificável no quadro ou na fala (videochamada, entrevista), pare e peça autorização ao dono do vídeo. Nunca monte gancho ou cortes que mudem o que a pessoa quis dizer.
4. **Entrega.** O arquivo vai só ao dono do vídeo. Não publique, não agende e não envie a terceiros sem pedido dele.

Você está pulando o portão 1 se pensar "é só um teste", "ele já aprovou algo parecido", "mostro depois de renderizar", ou se reaproveitar um código depois de mudar gancho, trechos ou legenda.

## Requisitos

- Python 3.10 ou mais novo; `ffmpeg` e `ffprobe` no PATH, com os filtros `subtitles`, `zscale`, `loudnorm` e o `libx264` (`ffmpeg -filters` lista).
- Opcional: `faster-whisper` (MIT), só para transcrever aqui. Com uma transcrição por palavra pronta, não precisa instalar nada.

## Passo a passo

### 1. Olhe a fonte

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,color_transfer:stream_side_data=rotation -of default=nw=1 bruto.mp4
```

- Pessoa num quadrado pequeno de videochamada em grade: pare e peça o original ou a visão do orador. Ampliar um quadrado de uns 100 px para 1080 não tem conserto.
- Entrevista com vozes sobrepostas ou áudio ruim: pule o vídeo.
- HDR (`arib-std-b67` ou `smpte2084`), rotação e fonte horizontal: o script trata e avisa no plano.

### 2. Transcreva por palavra

```
python <skill>/scripts/transcrever.py bruto.mp4 palavras.json
python <skill>/scripts/cortar.py --transcricao palavras.json --texto
```

O segundo comando imprime a fala com os tempos. Pode usar um JSON de outra ferramenta (`references/formato-transcricao.md`). Frase repetida em loop ou palavras sem sentido: o Whisper inventou texto sobre áudio ruim; descarte o vídeo.

### 3. Escolha o gancho e os cortes (seu julgamento)

Leia a fala inteira, liste de 3 a 5 candidatos, fique com o que mais faz parar o dedo, onde quer que esteja, e complete o arco até a revelação. Nunca use a primeira frase como gancho se o corpo também começa nela. Método completo e exemplos: `references/gancho.md`.

### 4. Mostre o plano

```
python <skill>/scripts/cortar.py --entrada bruto.mp4 --transcricao palavras.json --gancho 42.5-48.0 --inicio-corpo 12
```

Nada é renderizado. A saída traz o gancho, cada trecho com início, fim e texto, as pausas removidas, as legendas de amostra, os avisos e o **código do plano**. Leia os avisos antes de mostrar ao dono. Pare aqui até ele responder.

### 5. Renderize depois do OK

Repita o mesmo comando acrescentando `--aprovado CODIGO`. Por padrão a saída fica ao lado do vídeo, como `<nome>_corte.mp4`. Um arquivo existente só é substituído com `--sobrescrever`.

### 6. Confira e entregue

O script mostra o ffprobe do arquivo final e o loudness medido nele. Faça o resto de `references/qualidade.md`: quadros, régua sobre o quadro, emendas ouvidas, legenda lida contra a fala. Entregue só ao dono.

## Regras de corte embutidas

| Regra | Valor padrão |
|---|---|
| Base do corte | palavra, nunca segmento; a fronteira cai no limite de uma palavra |
| Pausa que corta | 0,6 s ou mais (`--pausa`); menores ficam |
| Folga | 0,05 s antes e 0,18 s depois de cada trecho (`--folga-antes`, `--folga-depois`) |
| Emenda | fade de áudio de 30 ms em cada ponta (`--fade`) |
| Áudio | -14 LUFS, pico verdadeiro até -1,5 dB, medido no áudio já cortado, 2 passadas, 48 kHz |
| Imagem | 1080x1920, 30 fps, H.264; fonte HDR vira SDR bt709 sozinha (`--hdr auto`) |
| Legenda | Arial negrito 64, amarela, até 5 palavras em até 2 linhas, linha de base em y 1200 (régua: 1150 a 1300) |

`python <skill>/scripts/cortar.py --help` lista todas as opções.

## Armadilhas

| Sintoma | O que fazer |
|---|---|
| Palavra cortada no fim | `--folga-depois 0.22` |
| Gancho toca duas vezes seguidas | `--inicio-corpo` igual ao fim do gancho, ou outro gancho |
| Cor lavada depois de postar | fonte HDR sem conversão: `--hdr sim` |
| Chiado no início depois de um agendador re-codificar | `--silencio-inicial 0.08` |
| Vício no meio da frase | `--remover`, só com aval do dono (gera jump cut) |
| Pouca memória ou "trechos demais" | suba `--pausa` ou divida o bruto; o limite é de 100 trechos por render |

## Fora do escopo

Logo ou tag do criador, transição entre gancho e corpo, correção de cor, música e motion. Para motion, gere o corte-base limpo com `--sem-legenda` e siga o capítulo de motion.

## Estado do teste

Os dois scripts foram escritos para este repositório e testados com vídeo sintético (tons de frequências diferentes no áudio, rampa de luminância no vídeo) e transcrições falsas: sequência de trechos, sincronismo de áudio e imagem, loudness, posição da legenda, HDR, rotação, portão por código e limites. A conversão do `transcrever.py` foi testada com objetos de teste; a transcrição real com faster-whisper e o uso em projeto real ainda não. Os selos [testado] em references/ vêm do método aplicado antes, à mão e com outro script, em projetos reais; o cortar.py em si só passou nos testes sintéticos acima.
