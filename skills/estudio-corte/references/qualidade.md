# Conferir o resultado

Ao terminar, o `cortar.py` imprime o ffprobe do arquivo final e o loudness medido nele. Confira o resto abaixo antes de entregar.

## Números que o arquivo final tem de ter

| Item | Esperado | Como ver |
|---|---|---|
| Tamanho e taxa | 1080x1920, 30 fps | `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,pix_fmt,color_transfer -of default=nw=1 saida.mp4` |
| Cor | `bt709` (ou sem marcação, se a fonte já era SDR). Nunca `arib-std-b67` nem `smpte2084` | mesmo comando |
| Áudio | AAC, 48000 Hz | `ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate -of default=nw=1 saida.mp4` |
| Loudness | perto de -14 LUFS, pico verdadeiro de no máximo -1,5 dB | impresso pelo script |

## Olhar e ouvir

1. **Quadros** no começo, no meio, no fim e em cada troca de legenda: `ffmpeg -ss 3 -i saida.mp4 -frames:v 1 quadro.png`.
2. **Régua sobre o quadro** (caixa segura x 80 a 940, y 250 a 1440): `ffmpeg -ss 3 -i saida.mp4 -frames:v 1 -vf "drawbox=x=80:y=250:w=860:h=1190:color=red@0.8:t=4" quadro_regua.png`. A legenda tem de ficar com a linha de base entre y 1150 e 1300.
3. **Folha de contato**, um quadro a cada 3 s: `ffmpeg -i saida.mp4 -vf "fps=1/3,scale=270:-1,tile=4x3" -frames:v 1 folha.png`.
4. **Emendas**: ouça de 3 a 5 com fone. Sem estalo, sem fim de palavra comido, sem pausa que sobrou. Se cortou uma palavra, rode o plano de novo com `--folga-depois 0.22`.
5. **Texto**: leia a legenda contra a fala. Corrija a palavra errada no JSON da transcrição.

## Se algo sair errado

| Sintoma | Ação |
|---|---|
| Palavra cortada no fim | `--folga-depois 0.22` |
| Pausa longa que ficou | baixe `--pausa` (por exemplo 0.5) |
| Cortes demais, fala picotada | suba `--pausa` (por exemplo 0.8) |
| Cor lavada depois de postar | confirme `color_transfer`; se a fonte era HDR e o plano disse "conversão HDR: não", use `--hdr sim` |
| Chiado nos primeiros milissegundos depois de um agendador re-codificar | `--silencio-inicial 0.08`; se persistir, poste manualmente pelo celular |
| Legenda passa da margem | palavra muito larga: reduza `--tamanho-fonte` |
| ffmpeg fecha por falta de memória | suba `--pausa` para ter menos trechos, ou divida o bruto em partes antes |

## Custo de referência

Em vídeo sintético, no Windows, só com CPU: um corte de 44 s de saída montado com 70 trechos, em 1080x1920, levou cerca de 1,5 min e o ffmpeg chegou a cerca de 1,6 GB de memória (medido em vídeo sintético, não em projeto real). Com fala real e brutos longos o tempo muda; [sem medição].
