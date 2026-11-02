# Versões derivadas e consertos sem recodificar

Rodamos os comandos em vídeo sintético, no ffmpeg 8.1, e os MP4 gerados passaram no `conferir_video.py` [testado]. No remux usamos `-preset ultrafast`, por velocidade; no HLS conferimos que a lista e os segmentos são gerados, sem testar a reprodução. Substitua `vN` pela versão. Nos comandos, `<skill>` é a pasta da skill estudio-entrega. As tags de cor entram pelo filtro `setparams`: as opções `-colorspace`, `-color_primaries` e `-color_trc` sozinhas gravaram só o espaço de cor quando a fonte não tinha metadados [testado].

## Remux: juntar o vídeo mudo ao áudio

O render de vídeo descarta o áudio. Junte `hf.mp4` e `mix.wav`, normalize e, se tiver legenda `.ass`, queime-a (a legenda exige recodificar). Os alvos de loudness são os que usamos (`loudnorm I=-14 TP=-1 LRA=11`, AAC 192k a 48 kHz) [testado]. O `-crf 20` é ponto de partida, sem medição nossa [sem medição]:

```bash
ffmpeg -i hf.mp4 -i mix.wav -map 0:v -map 1:a \
  -vf "subtitles=caps.ass,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1:LRA=11" -c:a aac -b:a 192k -ar 48000 \
  -shortest -movflags +faststart <slug>_vN.mp4
```

Sem legenda, tire o `subtitles=caps.ass,` e mantenha só o `setparams` no `-vf`. Confira: `python <skill>/scripts/conferir_video.py <slug>_vN.mp4`.

## `_whats`: 720p, leve, toca em qualquer celular

Para vídeo vertical (na horizontal, use `scale=-2:720`). Alvo: crf cerca de 26, maxrate 2,2 M, AAC 128k [testado]:

```bash
ffmpeg -i <slug>_vN.mp4 -vf "scale=720:-2,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset medium -crf 26 -maxrate 2200k -bufsize 4400k -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart <slug>_vN_whats.mp4
python <skill>/scripts/conferir_video.py <slug>_vN_whats.mp4 --resolucao 720x1280
```

## `_post`: caber no limite de tamanho da ferramenta de agendamento

Aqui o limite foi 22 MB (1 MB = 1.000.000 bytes) [testado]. Calcule o bitrate de vídeo com a duração em segundos. O 0,93 é a folga para o container e o 128 é o áudio:

```bash
python -c "import sys; d=float(sys.argv[1]); print(int(22*8000*0.93/d - 128))" 180
# 781 (kbps de vídeo para 180 s)
ffmpeg -i <slug>_vN.mp4 -vf "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset medium -b:v 781k -maxrate 781k -bufsize 1562k -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart <slug>_vN_post.mp4
python <skill>/scripts/conferir_video.py <slug>_vN_post.mp4 --tamanho-max 22
```

Se o master já cabe no limite, copie o arquivo em vez de recodificar.

## Web (HLS) e poster

Para um vídeo que vai para uma página [testado]:

```bash
ffmpeg -i <slug>_vN.mp4 -c copy -f hls -hls_time 6 -hls_playlist_type vod -hls_segment_filename "seg_%03d.ts" index.m3u8
ffmpeg -ss 1 -i <slug>_vN.mp4 -frames:v 1 -update 1 poster.jpg
```

## Consertos sem recodificar

Faststart faltando (o MP4 só toca depois de baixar tudo) [testado]:

```bash
ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4
```

Tags de cor faltando em H.264 [testado]:

```bash
ffmpeg -i in.mp4 -c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 -movflags +faststart out.mp4
```

## Quando recodificar

Resolução errada, fps variável, pix_fmt diferente de yuv420p, HDR, áudio alto ou baixo e erros de decodificação pedem recodificar: ajuste o filtro (`scale`, `fps=30`, `format=yuv420p`, `loudnorm`) e rode o conferidor de novo. Erro de decodificação costuma vir de uma etapa anterior (mix ou render): refaça a etapa, não conserte o arquivo.
