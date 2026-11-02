# Área segura

Área segura é a parte do quadro que a interface do app não cobre. Medidas para 1080x1920:

| Zona | Valor |
|---|---|
| Topo reservado | 250 px |
| Base reservada | 480 px |
| Esquerda reservada | 80 px |
| Direita reservada | 140 px |
| Texto e motion | x 80 a 940, y 250 a 1440 |
| Legenda falada | linha de base entre y 1150 e 1300 (60 a 68% da altura); nunca abaixo de y 1400 |

São medidas nossas, definidas depois que uma legenda foi cortada pela interface e o motion encostou nas laterais. Não medimos a interface de cada app. Em outros tamanhos 9:16, aplique por proporção.

## Anúncio

A Meta recomenda ("considere") deixar livres 14% do topo, 35% da base e 6% de cada lado em anúncios de Reels: em 1080x1920, cerca de 269, 672 e 65 px. A área útil fica em x 65 a 1015 e y 269 a 1248. Em anúncio, use a interseção com a nossa régua: x 80 a 940 e y 269 a 1248, com a linha de base da legenda até y 1240. Com aviso legal, a Meta pede 40% da base livre (768 px). O TikTok publica a zona só em arquivos de template. Para YouTube Shorts e para Reels orgânico não achamos números oficiais.

Contra a Meta, nossa régua reserva mais nas laterais (80 e 140 contra 65) e menos no topo e na base (250 e 480 contra 269 e 672).

## Outros recortes

- Feed 4:5 mostra o miolo de 1080x1350 e corta 285 px em cima e embaixo.
- Capa 3:4 (1080x1440) corta 240 px em cima e embaixo.
- Horizontal 1920x1080 (prática nossa): margem de 5% (96 px) para o motion e de 10% (192 px) para texto; legenda com linha de base entre y 900 e 960.

## Rotina

1. Desenhe a caixa antes de animar.
2. Coloque a legenda mais alta do que parece necessário.
3. Nada encosta na borda, nem no pico da animação (escala, zoom, entrada lateral).
4. Confira começo, meio, fim e os picos com a caixa por cima.
5. Tire a caixa antes do render final.

## Comandos

`scripts/area_segura.py` usa só a biblioteca padrão do Python e o ffmpeg. Nos comandos, `<skill>` é a pasta desta skill. Faça um render `draft` e passe o vídeo:

```
python <skill>/scripts/area_segura.py video.mp4 --t 3.5               # um quadro
python <skill>/scripts/area_segura.py video.mp4 --folha --cada 2      # folha de quadros
python <skill>/scripts/area_segura.py video.mp4 --video --anuncio     # vídeo inteiro, com o limite da Meta
```

Vermelho é a zona proibida, amarelo é a faixa da linha de base da legenda e ciano (com `--anuncio`) são os limites da Meta. O script aceita só vertical 9:16, não sobrescreve sem `--sobrescrever` e grava ao lado do vídeo, a menos que você passe `--saida`.

Sem o script, o mesmo quadro sai com o ffmpeg em 1080x1920 (troque `-ss 3` pelo instante):

```
ffmpeg -ss 3 -i video.mp4 -frames:v 1 -vf "drawbox=x=0:y=0:w=iw:h=250:color=red@0.35:t=fill,drawbox=x=0:y=ih-480:w=iw:h=480:color=red@0.35:t=fill,drawbox=x=0:y=0:w=80:h=ih:color=red@0.35:t=fill,drawbox=x=iw-140:y=0:w=140:h=ih:color=red@0.35:t=fill" area.png
```
