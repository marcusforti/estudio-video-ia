---
name: estudio-entrega
description: Use quando um vídeo estiver renderizado e for preciso conferi-lo antes de mostrar ao dono ou de postar - "confere esse vídeo", "tá pronto pra mandar?", "gera o _whats", "gera a versão pro post", "manda pro dono" - ou quando houver dúvida de volume, quadro preto, legenda fora da área segura, vídeo que não toca no celular ou arquivo grande demais para o WhatsApp.
---

# Conferência e entrega

Confere o vídeo final com números, gera as versões derivadas e leva o resultado ao dono do vídeo sem pular nenhum portão. Todo item leva um resultado medido: "ficou bom" sem número ou sem quadro de referência não vale.

Nos comandos, `<skill>` é a pasta desta skill.

## Portões obrigatórios

- **Conferência.** Reprovou em qualquer item? Corrija e refaça a versão. Não entregue e não peça aprovação.
- **Dono primeiro.** O vídeo vai só ao dono, pelo canal combinado, antes de qualquer outra pessoa. Terceiros recebem pelo dono ou com o ok dele.
- **"Enviado" é entregue ou lido.** O status "pendente" só diz que a API aceitou o pedido. Espere o status de entregue ou lido antes de dizer que enviou.
- **Publicar.** Só com "pode publicar" explícito do dono. Post que pede "comenta PALAVRA" só sai com a automação ativa e testada.
- **Gasto.** Revisor externo pago, transcrição em serviço pago ou máquina alugada: peça ok com teto antes. Destrua a máquina ao baixar o vídeo.
- **Consentimento.** Não mande o vídeo a um serviço de terceiros se ele tem rosto ou voz de quem não autorizou.

## Passo a passo

1. **Rode o conferidor:**

```
python <skill>/scripts/conferir_video.py VIDEO.mp4
```

Ele grava `qa/<nome>/relatorio.md`, as folhas de contato `folha_01.jpg`... e `ultimo_quadro.jpg`. O código de saída é 0 se aprova, 1 se reprova, 2 se faltar arquivo ou ffmpeg. Coloque o caminho do vídeo antes das opções. Opções úteis: `--resolucao 720x1280` (para `_whats`), `--tamanho-max 22` (MB, para `_post`), `--intervalo 8` (segundos entre quadros).

2. **Transcreva o arquivo FINAL**, não o roteiro (Whisper ou Scribe), salve `qa/transcricao_final.txt` e rode de novo com `--roteiro ROTEIRO.md --transcricao qa/transcricao_final.txt`. Alvo: só diferenças de grafia (semelhança de 95% ou mais). Confira as palavras de risco (nomes, marcas, números, siglas) no texto transcrito.
3. **Olhe a folha de contato** com `references/CHECKLIST-ENTREGA.md` na mão: rosto livre em todo quadro com pessoa, área segura, gancho nos 2 primeiros segundos, nenhum logo vetado, selo "exemplo" nas simulações, português na tela. O conferidor não faz isso por você.
4. **Reprovou?** Corrija a causa (comandos de conserto em `references/derivados.md`), gere a versão seguinte e volte ao passo 1. Nunca sobrescreva a versão anterior.
5. **Gere as derivadas** (`_whats`, `_post`, web) com os comandos de `references/derivados.md` e confira cada uma com o conferidor e as opções do passo 1.
6. **Preencha o checklist** (`references/CHECKLIST-ENTREGA.md`) com os valores medidos e guarde em `qa/`, junto com a transcrição e as folhas.
7. **Entregue ao dono.** Envie o `_whats` pelo canal combinado, com a versão, o que mudou e as perguntas abertas. Confirme o status de entregue ou lido.
8. **Espere a resposta.** Aprovou: peça o "pode publicar" só se for publicar. Reprovou: resuma o feedback no campo 31 do rosto, sem citação literal, e gere a vN+1.
9. **Depois de publicar:** legenda guardada ao lado do vídeo, com o mesmo nome do `_post` (`<slug>_vN_post.txt`); isca e automação testadas se o CTA pede comentário; `HANDOFF.md` atualizado; máquina alugada destruída.

## O que o conferidor mede

Resolução, fps fixo, codec, pix_fmt, cor (bt709; HDR reprova), faststart, duração de vídeo e de áudio, erros de decodificação, loudness integrado (de -16 a -14 LUFS), pico real (até -1 dBTP), quadros pretos, silêncio acima de 2 s e, se você passar o roteiro, a semelhança com a fala. Os limites mudam por opção (`--lufs-min`, `--pico-max`, `--silencio-dur` e outras; veja `--help`). As tolerâncias de medição são 0,5 LU no loudness e 0,2 dB no pico.

## Sinais de alerta

| Pensamento | Realidade |
|---|---|
| "O vídeo toca, está bom" | Tocar não prova nada. Rode o conferidor e olhe a folha de contato |
| "Transcrevo o roteiro, que é igual" | Transcreva o arquivo final. É ele que o público ouve |
| "A API aceitou, então enviei" | "Pendente" não é entregue. Espere entregue ou lido |
| "Reprovou, mas o dono decide" | Reprovou, você corrige. Ele só vê o que passou |
| "Mando uma versão para o sócio dele ver" | Terceiros recebem pelo dono |
| "A conferência demorou, pulo o decodificar" | Mixagem corrompida já saiu com milhares de erros de decodificação |
| "O dono aprovou a v1, posto agora" | "Pode publicar" é um ok separado |

## Pronto quando

O relatório não tem falha; o checklist está preenchido com valores medidos e guardado em `qa/`; o dono recebeu (status de entregue ou lido) e respondeu; nada foi publicado sem o "pode publicar".
