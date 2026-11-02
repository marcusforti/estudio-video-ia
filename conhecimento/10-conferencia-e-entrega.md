# Conferência e entrega

Este capítulo cobre o que acontece entre o render e o post: o checklist de conferência com valores medidos, o script que mede o que dá para medir, as versões derivadas (`_whats`, `_post`, web) e o caminho até publicar, com os portões em que o trabalho espera o dono do vídeo. Serve a quem entrega vídeo para outra pessoa e não quer descobrir o erro depois de enviado.

## Resumo em 30 segundos

- Todo item do checklist leva um resultado medido. "Ficou bom" sem número ou sem quadro de referência não vale.
- O [`conferir_video.py`](../skills/estudio-entrega/scripts/conferir_video.py) mede o arquivo, a cor, os erros de decodificação, o loudness, os quadros pretos e o silêncio, e gera a folha de contato. Rosto livre, área segura, português na tela e fatos são conferência visual sobre a folha.
- Reprovou na conferência: o agente corrige e refaz a versão, sem pedir aprovação ao dono.
- O vídeo vai primeiro só ao dono. "Enviado" só vale com status de entregue ou lido. Publicar só com "pode publicar" escrito.
- Guarde em `qa/` a transcrição do arquivo final, as folhas de contato e o checklist preenchido ([modelo](../modelos/CHECKLIST-ENTREGA.md)).

## Checklist por blocos

Cada bloco abaixo vira uma seção do [modelo CHECKLIST-ENTREGA.md](../modelos/CHECKLIST-ENTREGA.md). Termos: **LUFS** é a unidade de volume percebido; **dBTP** é o pico real, medido com sobreamostragem, que pega picos entre as amostras; **faststart** é o índice do MP4 no começo do arquivo, para tocar antes de baixar tudo; **pix_fmt** é o formato de pixel; **fps fixo** significa o mesmo intervalo entre todos os quadros.

### A. Arquivo

| Item | Como conferir | Aprova se |
|---|---|---|
| Nomes | `<slug>_vN.mp4`, `_vN_whats.mp4`, `_vN_post.mp4` | Os três existem e o `vN` é o certo |
| Formato | `conferir_video.py` | 1080x1920 (ou 1920x1080), 30 fps fixos, h264, yuv420p, tags bt709, faststart, sem HDR |
| Decodificação | `ffmpeg -v error -i ARQUIVO -f null -` | Nenhuma linha de erro |
| Duração e tamanho | Relatório do script | Anotados no checklist |

### B. Fala

| Item | Como conferir | Aprova se |
|---|---|---|
| Transcrição do final | Whisper ou Scribe sobre o arquivo FINAL (não o roteiro); `--roteiro` e `--transcricao` no script | Só diferenças de grafia (semelhança de 95% ou mais). Salve `transcricao_final.txt` |
| Palavras de risco | Lista do script | Nomes próprios, marcas, números e siglas conferidos no texto transcrito |
| Voz cabe no take | Script de linha do tempo do projeto | Nenhum aviso de "voz passa do take" |
| Talking head | Relatório (silêncio) e escuta | Sem sobra de voz de entrevistador; fala começa em até 0,5 s; nenhum silêncio acima de 2 s |

### C. Imagem

| Item | Como conferir | Aprova se |
|---|---|---|
| Folha de contato | Script, um quadro a cada 8 a 10 s, mais o primeiro, o último e os picos de motion | Gerada e olhada de ponta a ponta |
| Três momentos | `qa/`: material de entrada, imagens geradas, quadros finais | Os três arquivos existem ([capítulo 03](03-folha-de-storyboard.md)) |
| Rosto livre | Snapshot em todo quadro com pessoa, inclusive nos picos de escala e zoom | Nenhum texto, legenda, cartão ou caixa de detecção encosta no rosto |
| Área segura (vertical 1080x1920) | Régua sobre os quadros | Topo 250 px, base 480 px, esquerda 80 px, direita 140 px; legenda com a linha de base entre y 1150 e 1300; motion em x 80-940 e y 250-1440 [praticante]. Na horizontal: margem de 5% para motion e 10% para texto; legenda em y 900-960 [praticante] |
| Gancho | Primeiros 2 s | Motion e fala já presentes |
| Cena parada e quadro preto | Teto da folha de storyboard; script | Nenhuma cena acima do teto, nenhum quadro preto, nenhum buraco de legenda |
| Marca e crédito | Vetos do rosto (campo 21) | Nenhum logo vetado; selo "exemplo" nas simulações; créditos em `CREDITOS.md` |
| Português na tela | Leitura dos quadros | Nenhum erro |

### D. Áudio

| Item | Como conferir | Aprova se |
|---|---|---|
| Loudness e pico | Script | Integrado entre -16 e -14 LUFS e pico real até -1 dBTP |
| Trilha | Escuta e relatório | Cerca de 15 dB abaixo da voz, com duck que não "respira" |
| Remux | Escuta no início, no meio e no fim | O áudio está no arquivo e em sincronia (o render de vídeo descarta o áudio) |

### E. Versões derivadas

| Item | Aprova se |
|---|---|
| `_whats` | 720p, crf cerca de 26, maxrate 2,2 M, AAC 128k; passa no script com `--resolucao 720x1280` |
| `_post` | Até o limite de tamanho da sua ferramenta de agendamento (22 MB na nossa), bt709, 48 kHz; passa no script com `--tamanho-max` |
| Página | Versão web (HLS) e poster, se o vídeo vai para uma página |

### F. Conteúdo e conformidade

| Item | Aprova se |
|---|---|
| Fatos | Todo fato tem fonte ou está marcado "estimativa" ou "exemplo"; preço, prazo e vaga só com a confirmação do dono |
| Vetos | A lista do campo 21 do rosto foi cumprida |
| Autorizações | As pendentes estão listadas (imagem ou voz de terceiros, dados internos) |

### G. Aprovação e envio

| Item | Aprova se |
|---|---|
| Conferência | Passou. Se reprovou, o agente corrigiu e refez sem pedir aprovação |
| Revisão independente | Em entrega longa, outro modelo assistiu e cada apontamento foi conferido no quadro |
| Envio | Só ao dono, pelo canal combinado; "enviado" só depois do status de entregue ou lido |
| Ok para publicar | Há um "pode publicar" explícito antes de publicar ou mandar a terceiros |

### H. Pós-entrega

| Item | Aprova se |
|---|---|
| Legenda | Guardada com o mesmo nome do `_post` (`<slug>_vN_post.txt`), com collab e hashtags |
| CTA com "comenta PALAVRA" | Isca no ar com link testado, campanha registrada, automação ativa e comentário de teste respondido |
| Máquina alugada | Destruída depois de baixar o vídeo e conferir o hash |
| Registro | `HANDOFF.md` com versão, status, pendências e comando de retomada |

## O script conferir_video.py

Só biblioteca padrão do Python 3.10 ou mais novo, mais `ffmpeg` e `ffprobe` no PATH. Foi escrito sem dependências do sistema, para Windows, macOS e Linux; só rodamos no Windows [testado].

```
python conferir_video.py video_v1.mp4
python conferir_video.py video_v1.mp4 --roteiro ROTEIRO.md --transcricao transcricao_final.txt
python conferir_video.py video_v1_whats.mp4 --resolucao 720x1280
python conferir_video.py video_v1_post.mp4 --tamanho-max 22
```

Ele grava `qa/<nome>/relatorio.md`, as folhas `folha_01.jpg`, `folha_02.jpg` e assim por diante (um quadro a cada `--intervalo` segundos, 10 por padrão) e `ultimo_quadro.jpg`. O código de saída é 0 se aprova, 1 se reprova e 2 se faltar arquivo ou ffmpeg. Coloque o caminho do vídeo antes das opções.

| Verificação | Aprova se | Opções |
|---|---|---|
| Resolução | 1080x1920 ou 1920x1080 | `--resolucao` (aceita várias) |
| FPS fixo | 30 fps e nenhum intervalo entre quadros fora de 25% da mediana | `--fps` |
| Codec | h264 no vídeo, aac no áudio, áudio a 48 kHz | `--codec-video`, `--codec-audio`, `--taxa-audio` |
| pix_fmt | yuv420p | |
| Cor | bt709 em espaço, primárias e transferência; HDR reprova | |
| Faststart | `moov` antes de `mdat` | |
| Duração vídeo x áudio | Diferença de até 0,2 s | |
| Erros de decodificação | `ffmpeg -v error` sem nenhuma linha | |
| Loudness integrado | De -16 a -14 LUFS, com 0,5 de tolerância de medição | `--lufs-min`, `--lufs-max` |
| Pico real | Até -1 dBTP, com 0,2 dB de tolerância | `--pico-max` |
| Quadros pretos | Nenhum trecho de 0,1 s ou mais | `--preto-dur` |
| Silêncio longo | Nenhum trecho de 2 s ou mais abaixo de -40 dB | `--silencio-dur`, `--silencio-db` |
| Tamanho | Até o limite, se informado | `--tamanho-max` (em MB) |
| Fala x roteiro | Semelhança de 95% ou mais; palavras de risco presentes | `--roteiro`, `--transcricao`, `--similaridade-min` |

A tolerância de medição existe porque o AAC pode mexer no pico e no loudness em décimos depois da normalização [praticante]. Os alvos de -16 a -14 LUFS e -1 dBTP são os que usamos [testado]. Não confirmamos alvos de loudness por plataforma nesta varredura [sem medição].

Com `--roteiro`, o script lista as palavras de risco do texto (números, siglas, marcas, nomes próprios). Se o roteiro for um `STORYBOARD.md`, ele usa só a coluna Fala. Com `--transcricao` também, compara os dois textos palavra a palavra e mostra as diferenças. Ele não transcreve: use Whisper ou Scribe antes e passe o arquivo.

Excerto real do relatório de um vídeo sintético com áudio alto demais (o resto da tabela estava OK):

```
## Resultado: REPROVADO (2 falha(s), 0 aviso(s))

| FALHA | Loudness integrado | -3,5 LUFS (LRA 0,1) | -16,0 a -14,0 LUFS (±0,5 de medição) |
| FALHA | Pico real | -0,1 dBTP | até -1,0 dBTP (±0,2 de medição) |
```

O que o script não faz: rosto livre, área segura, português na tela, fatos e vetos. Isso é olhar a folha de contato com o checklist na mão.

Testamos o script com material sintético: dois vídeos aprovados (um em 1080x1920 e um derivado em 720x1280) e 16 casos com um defeito cada (resolução, quadro preto, silêncio, sem faststart, sem tags de cor, HDR, yuv444p, fps 24, fps variável, áudio alto, áudio baixo, sem áudio, áudio mais longo que o vídeo, arquivo corrompido, tamanho acima do limite, arquivo que não é vídeo). Cada defeito foi pego pela verificação certa [testado]. Em um vídeo de 8 s a 1080x1920, a conferência com folhas levou cerca de 25 s no nosso PC [testado]. Cada passada decodifica o vídeo inteiro, então o tempo cresce com a duração; não medimos um vídeo longo [sem medição].

## Versões derivadas

Rodamos os comandos abaixo em vídeo sintético, e os MP4 gerados passaram no próprio `conferir_video.py` [testado]. No HLS conferimos que a lista e os segmentos são gerados, sem testar a reprodução. As tags de cor entram pelo filtro `setparams`: no ffmpeg 8.1, as opções `-colorspace`, `-color_primaries` e `-color_trc` sozinhas gravaram só o espaço de cor quando a fonte não tinha metadados [testado].

**`_whats`**, para vídeo vertical (na horizontal, troque por `scale=-2:720`):

```bash
ffmpeg -i vN.mp4 -vf "scale=720:-2,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset medium -crf 26 -maxrate 2200k -bufsize 4400k -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart vN_whats.mp4
```

**`_post`**, para caber em um limite (aqui, 22 MB; 1 MB = 1.000.000 bytes). Calcule o bitrate de vídeo com a duração em segundos (o 0,93 é a folga para o container) e confira o tamanho depois:

```bash
python -c "import sys; d=float(sys.argv[1]); print(int(22*8000*0.93/d - 128))" 180
# 781 (kbps de vídeo para 180 s)
ffmpeg -i vN.mp4 -vf "setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset medium -b:v 781k -maxrate 781k -bufsize 1562k -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart vN_post.mp4
python conferir_video.py vN_post.mp4 --tamanho-max 22
```

**Web (HLS) e poster**, para uma página:

```bash
ffmpeg -i vN.mp4 -c copy -f hls -hls_time 6 -hls_playlist_type vod -hls_segment_filename "seg_%03d.ts" index.m3u8
ffmpeg -ss 1 -i vN.mp4 -frames:v 1 -update 1 poster.jpg
```

**Consertos sem recodificar:**

```bash
# faststart faltando
ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4
# tags de cor faltando (H.264)
ffmpeg -i in.mp4 -c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 -movflags +faststart out.mp4
```

## O caminho até publicar

| Passo | Quem | Para seguir é preciso | Se falhar |
|---|---|---|---|
| 1. Conferência (portão Conferência) | Agente | Relatório sem FALHA e checklist A a F fechado | Corrige e refaz, sem pedir aprovação |
| 2. Derivados | Agente | `_whats` e `_post` passam no script com as opções certas | Recodifica |
| 3. Revisão independente (vídeo longo) | Outro modelo | Cada apontamento conferido no quadro e aceito ou recusado | Corrige o que foi aceito e confere de novo |
| 4. Entrega (portão Entrega) | Agente | Envio só ao dono; status de entregue ou lido | Reenvia; nada vai a terceiros |
| 5. Aprovação ou feedback | Dono | Resposta do dono, resumida no campo 31 do rosto | Gera a vN+1 e volta ao passo 1 |
| 6. Publicar (portão Publicar) | Dono, depois o agente | "Pode publicar" escrito; legenda gravada | Sem o ok, nada sai |
| 7. Isca e automação | Agente | Se o CTA pede "comenta PALAVRA": automação ativa e testada antes do post | Sem automação, o post não sai |
| 8. Encerramento | Agente | `HANDOFF.md` atualizado; máquina destruída; hash conferido | Destrua a máquina e atualize o registro |

Um segundo modelo que assiste ao vídeo dá nota e aponta minutagens. Em um vídeo longo, a nota subiu da primeira para a terceira versão [praticante]. Confira cada apontamento no quadro antes de aceitar: o revisor também erra [praticante].

## O que deu errado aqui

- **Mixagem corrompida.** Uma mixagem saiu com 5.943 erros de decodificação, e a checagem com `-f null` é a que os mostra [praticante]. Por isso o checklist tem a linha da decodificação.
- **Música alta.** A versão com a trilha cerca de 7 dB abaixo da voz foi reprovada; a seguinte, com cerca de 15 dB, passou [testado].
- **Legenda fora da zona segura.** Uma versão tinha a legenda em y 1700 e foi reprovada [testado].
- **Texto sobre rosto.** A conferência achou texto encostando no cabelo de uma pessoa [testado].
- **Transcrição do final que não foi guardada.** A regra existia, e mesmo assim dois de quatro projetos recentes não guardaram a transcrição do arquivo final; em um deles a guardada era a da voz editada, anterior à composição [testado]. Guarde sempre, em `qa/`.
- **"Enviado" com status pendente.** O status "pendente" só diz que a API aceitou o pedido. "Enviado" vale a partir de entregue ou lido [testado].
- **Tags de cor que não gravam.** Veja a nota na seção de versões derivadas [testado].

## Links

- [Workflow completo](01-workflow-completo.md): etapas 10 a 16 e os portões.
- [Folha de storyboard](03-folha-de-storyboard.md): o teto de cena parada e as três folhas de contato.
- [Modelo CHECKLIST-ENTREGA.md](../modelos/CHECKLIST-ENTREGA.md): o checklist em branco.
- [Skill estudio-entrega](../skills/estudio-entrega/SKILL.md): roda a conferência e gera as versões derivadas.
- [conferir_video.py](../skills/estudio-entrega/scripts/conferir_video.py): o script descrito acima.
