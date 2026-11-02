# CHECKLIST DE ENTREGA · <slug do projeto> · v<N>

> Marque cada item com o resultado MEDIDO. "Ficou bom" sem número ou sem quadro de referência não vale.
> Itens marcados com (script) saem do relatório do `conferir_video.py`; os demais são conferência visual ou de conteúdo.
> Reprovou em qualquer item: corrija e refaça a versão. Não envie e não peça aprovação do dono.
> Guarde este arquivo preenchido em `qa/` junto com a transcrição do final e as folhas de contato.

## A. Arquivo

- [ ] Nome `<slug>_vN.mp4`, mais `<slug>_vN_whats.mp4` (e `<slug>_vN_post.mp4` se for publicar). Resultado:
- [ ] 1080x1920 (ou 1920x1080), 30 fps fixos, yuv420p, tags bt709, faststart, sem HDR (script). Medido:
- [ ] Nenhum erro em `ffmpeg -v error -i ARQUIVO -f null -` (script). Linhas de erro:
- [ ] Duração e tamanho anotados (script). Duração: ___ · Tamanho: ___

## B. Fala

- [ ] Transcrição do arquivo FINAL (não do roteiro), comparada com o roteiro e salva como `transcricao_final.txt`. Semelhança medida (script com `--roteiro` e `--transcricao`):
- [ ] Palavras de risco conferidas no texto transcrito: nomes próprios, marcas, números, siglas. Divergências:
- [ ] Cada bloco de voz cabe no seu take, sem aviso de "voz passa do take". Resultado:
- [ ] Talking head: nenhuma sobra de voz de entrevistador no corte; fala começa antes de 0,5 s; nenhum silêncio acima de 2 s (script). Medido:

## C. Imagem

- [ ] Folha de contato com um quadro a cada 8 a 10 s, mais o primeiro, o último e os picos de motion (script). Arquivos:
- [ ] Folhas de contato dos três momentos guardadas em `qa/`: material de entrada, imagens geradas e quadros finais. Arquivos:
- [ ] Snapshot de rosto: em todo quadro com pessoa, nenhum texto, legenda, cartão ou caixa de detecção encosta no rosto, inclusive nos picos de escala e zoom. Quadros conferidos:
- [ ] Área segura (vertical 1080x1920): topo 250 px, base 480 px, esquerda 80 px, direita 140 px; legenda com a linha de base entre y 1150 e 1300; motion em x 80-940 e y 250-1440. Medido:
- [ ] Gancho: motion e fala nos 2 primeiros segundos. Medido:
- [ ] Nenhuma cena parada além do limite da folha de storyboard; nenhum quadro preto (script); nenhum buraco de legenda. Medido:
- [ ] Nenhum logo ou marca real vetado; selo "exemplo" nas simulações; créditos de terceiros em `CREDITOS.md`. Conferido:
- [ ] Português na tela revisado. Erros achados:

## D. Áudio

- [ ] Loudness integrado entre -16 e -14 LUFS e pico real até -1 dBTP (script). Medido: ___ LUFS · ___ dBTP
- [ ] Trilha cerca de 15 dB abaixo da voz, com duck que não "respira". Medido:
- [ ] Áudio remuxado (o render de vídeo descarta o áudio) e sincronia conferida no início, no meio e no fim. Resultado:

## E. Versões derivadas

- [ ] `_whats`: 720p, crf cerca de 26, maxrate 2,2 M, AAC 128k (script com `--resolucao`). Tamanho:
- [ ] `_post`: até o limite de tamanho da sua ferramenta de agendamento, bt709, 48 kHz (script com `--tamanho-max`). Tamanho:
- [ ] Se o vídeo vai para uma página: versão web (HLS) e poster. Arquivos:

## F. Conteúdo e conformidade

- [ ] Todo fato tem fonte ou está marcado "estimativa" ou "exemplo"; preço, prazo e vaga só se o dono confirmou. Conferido:
- [ ] Vetos do cliente cumpridos (lista do campo 21 do rosto). Conferido:
- [ ] Autorizações pendentes listadas (imagem ou voz de terceiros, dados internos). Lista:

## G. Aprovação e envio

- [ ] A conferência passou. Se reprovou, corrigiu e refez sem pedir aprovação. Versão refeita:
- [ ] Em entrega longa, revisão independente por outro modelo, com cada apontamento conferido no quadro. Apontamentos aceitos e recusados:
- [ ] Enviado só ao dono, pelo canal combinado. "Enviado" só depois do status de entregue ou lido (aceito pelo servidor não conta). Status:
- [ ] Ok explícito do dono ("pode publicar") antes de publicar ou mandar a terceiros. Data e texto do ok (resumido):

## H. Pós-entrega

- [ ] Legenda do post guardada com o mesmo nome do `_post` (`<slug>_vN_post.txt`), com collab e hashtags. Conferido:
- [ ] Se o CTA pede "comenta PALAVRA": isca no ar com link testado, campanha registrada, automação ativa e comentário de teste respondido. Resultado:
- [ ] Máquina alugada destruída depois de baixar o vídeo e conferir o hash. Conferido:
- [ ] `HANDOFF.md` com versão, status, pendências e comando de retomada. Atualizado em:
