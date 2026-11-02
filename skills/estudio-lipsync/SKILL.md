---
name: estudio-lipsync
description: Use quando o usuário quiser sincronizar a boca com um áudio novo, dublar um vídeo, "consertar a boca", "fazer a foto falar", "lip sync", trocar a voz de um vídeo e a boca acompanhar, escolher entre LatentSync, TBDub, MuseTalk, InfiniteTalk, sync.so, HeyGen ou VEED, ou orçar lip sync de um Reel, uma VSL ou uma dublagem.
---

# Estúdio lip sync: escolher, testar e rodar

Lip sync mexe em boca e rosto de pessoas reais. Cinco portões vêm antes de qualquer teste, e o teste de 10 a 15 s no pior plano escolhe o modelo. Não existe benchmark independente nem teste em português para nenhum modelo ou serviço: a decisão sai do material do usuário.

Nos comandos, `<skill>` é a pasta desta skill.

## Portões (obrigatórios, nesta ordem)

1. **Consentimento.** Pergunte: há consentimento escrito de cada pessoa que aparece e de cada voz usada, cobrindo o que será feito, onde será publicado, processamento em nuvem fora do Brasil e revogação? Sem "sim", pare e diga o que falta. Perguntas e termos em `references/consentimento-e-licenca.md`.
2. **Licença.** Pergunte se o uso é comercial. Se for, descarte o que a tabela de `references/consentimento-e-licenca.md` bloqueia (Wav2Lip, CodeFormer, GFPGAN; LatentSync e LivePortrait só com outro detector no lugar do InsightFace; LTX-2 acima de US$ 10 milhões de receita; HunyuanVideo-Avatar com restrição territorial).
3. **Custo.** Estime antes de rodar (`references/servicos-pagos.md` para pagos; GPU alugada: skill `estudio-gpu`). Mostre o valor ao usuário e espere o OK. Serviço pago: o teste de 12 s custa de US$ 0,20 a 1,60 a preço de tabela; mensalidade soma à parte.
4. **Dono primeiro.** O resultado vai só ao dono do vídeo. Ele aprova antes de qualquer publicação.
5. **Onde roda.** Rosto e voz de terceiro: nuvem segura, nunca o Colab (a FAQ lista "creating deepfakes" entre os usos proibidos e não define o termo [oficial] (https://research.google.com/colaboratory/faq.html, lida em 01/11/2026)). Antes de subir material a um serviço pago, leia os termos dele sobre rosto e voz.

## Passo 1: qual é o trabalho?

| O usuário tem | Trabalho | Caminho |
|---|---|---|
| Vídeo da pessoa + áudio novo | Consertar a boca (vídeo para vídeo) | Passo 2 |
| Só foto ou ilustração + áudio | Animar a foto: cabeça e corpo são gerados | InfiniteTalk 480p; LongCat-Video-Avatar 1.5 (não testado). Se a pessoa real precisa ser reconhecível, evite rosto gerado por IA a partir de foto: as imagens de rosto geradas por IA que testamos como entrada foram reprovadas, e o InfiniteTalk em si não teve veredito nosso [sem medição]. Filme um take e vá ao Passo 2 |
| Quer traduzir ou dublar | Dublagem | ElevenLabs Dubbing troca a voz e não mexe na boca. Para traduzir e sincronizar: HeyGen Translate ou sync.so Dubbing. Com o áudio novo pronto: só lip sync |
| Nenhum dos dois | Falta a base | Filme um take de câmera fixa, de frente, boca livre |

## Passo 2: candidatos

| Situação | Candidatos |
|---|---|
| Plano fácil (de frente, boca livre, uma pessoa, boa luz), rascunho, placa de 4 GB ou mais | MuseTalk 1.5 (MIT) |
| Plano fácil, qualidade de entrega, aceita alugar GPU de 24 a 80 GB | TBDub Student (Apache-2.0, ~28 GB de VRAM, só Linux); LatentSync 1.6 (18 GB) como reserva |
| Plano difícil (perfil, mão ou microfone na boca, duas pessoas, rosto pequeno, pouca luz) | TBDub e X-Dub alugados; sync-3 ou HeyGen Precision |
| Não quer montar nada | VEED ou LatentSync na fal, depois lipsync-2-pro, depois sync-3 |

Leve ao teste dois modelos abertos e um serviço pago, ou três serviços de preços diferentes. Detalhes de licença, VRAM, velocidade e manutenção: `references/modelos-locais.md`.

## Passo 3: o teste de 10 a 15 s no pior plano

Escolha o pior plano do material. Use a voz final do projeto, em português do Brasil, com lábios fechados (p, b, m), vogais nasais (não, mão) e vogais arredondadas (o, u).

```bash
python <skill>/scripts/preparar_teste.py --video bruto.mp4 --inicio 83 --duracao 12 --audio voz_nova.wav --saida teste
# gera teste/original_trecho.mp4, teste/base_25fps.mp4 e teste/voz_16k_mono.wav
# rode o MESMO par (base_25fps.mp4 + voz_16k_mono.wav) em cada candidato, depois:
python <skill>/scripts/comparar_lado_a_lado.py --original teste/original_trecho.mp4 --resultado saida_a.mp4 saida_b.mp4 --saida teste/comparacao.mp4
```

Mostre `comparacao.mp4` ao usuário, com som, e use as sete perguntas de `references/teste-pior-plano.md`. O veredito é do dono do vídeo, não seu. Decida pelo mais barato que passa no pior plano; se nenhum passar, refilme o plano antes de trocar de ferramenta. Registre custo e segundos de máquina por segundo de vídeo.

## Passo 4: rodar de verdade

- **Modelo aberto:** comandos em `references/receitas-locais.md`, com selo do que rodou em produção. Para alugar a GPU, use a skill `estudio-gpu` e respeite os portões dela.
- **Serviço pago:** preços, limites e termos em `references/servicos-pagos.md`. Não temos conta em nenhum; peça a chave ao usuário por variável de ambiente e nunca a imprima.
- **Blocos:** 25 a 55 s nos modelos abertos; menos de 2 min nos pagos. A base de vídeo cobre o áudio mais 0,5 s, e o áudio leva 0,5 s de silêncio no fim.
- **Emenda:** `ffmpeg -f concat -safe 0 -i lista.txt -c copy saida.mp4`.

## Passo 5: conferir e entregar

Confira a última palavra, a sincronia nas consoantes labiais, o remendo em volta da boca, a cor da boca e se a pessoa continua parecendo ela mesma. Mande ao dono. Se alugou GPU, destrua a máquina e prove a lista vazia antes de encerrar.

## Sinais de alerta

| Pensamento | Realidade |
|---|---|
| "É só um teste, não precisa de consentimento" | O teste já processa rosto e voz |
| "O Wav2Lip é o mais conhecido" | Licença não comercial e boca de 96 px |
| "O README diz 15 GB, roda na minha 4090" | O TBDub usa ~28 GB sem `--cpu-offload`; com ele, 15 GB, e o autor avisa que não testou numa RTX 4090 |
| "O paper mostra 96% de sucesso" | É do modelo interno do X-Dub, medido pelos autores; o público é mais fraco |
| "O serviço diz 95+ idiomas, então o português está testado" | Nenhum mostra teste em português |
| "Pulo o teste do pior plano" | O pior plano decide; o fácil passa em tudo |
| "Dois processos de TBDub numa placa de 40 GB" | São ~28 GB cada: dois só em 80 GB |

## Selos de evidência

`[testado]` = rodou numa A100 alugada em outubro de 2026. `[fornecedor]` = o fabricante diz. `[oficial]` = só da documentação, não rodado por nós. Serviços pagos de lip sync: nenhum foi testado por nós. Os scripts de `scripts/` (rode com `python` ou `python3`) foram testados com vídeo sintético e não usam nenhuma API.
