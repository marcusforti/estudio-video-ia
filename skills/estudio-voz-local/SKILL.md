---
name: estudio-voz-local
description: Use quando o usuário quiser clonar uma voz (clone de voz, TTS com clonagem) com modelo aberto no próprio PC ou numa GPU alugada, narrar um vídeo com voz clonada de quem autorizou, preparar a amostra de voz, escolher entre OmniVoice, Qwen3-TTS, VoxCPM2, MOSS-TTS, Chatterbox ou RVC, ou comparar voz clonada com a real. Também quando falar em consentimento, autorização ou licença de voz clonada.
---

# Estúdio de voz local

Clonagem de voz com autorização, em máquina própria ou alugada. Capítulo de apoio no repositório: https://github.com/marcusforti/estudio-video-ia/blob/main/conhecimento/05-voz-local.md.

**Descumprir a letra dos portões é descumprir o espírito deles.** Valem para teste rápido, rascunho e voz de amigo.

## Portões (nesta ordem, sem pular)

1. **Consentimento por escrito.** Pergunte de quem é a voz. Se for de outra pessoa, ela precisa ter autorizado antes de qualquer gravação, treino ou geração, por termo assinado ou outro registro escrito (`references/AUTORIZACAO-VOZ-E-IMAGEM.md`, que é modelo e não substitui advogado). Sem registro, pare e entregue o modelo de termo. Se for a voz do próprio usuário, peça só a confirmação de que a voz é dele. Se o trabalho também mexe no rosto da pessoa (sincronia labial, avatar), marque imagem no termo.
2. **Licença do modelo.** Pergunte se a peça é paga, entregue a cliente ou gera receita. Se for, siga `references/licencas.md`: só pesos permissivos, ou licença atual verificada. Se não for, pesos não comerciais servem; avise o usuário de que a peça não pode virar uso comercial depois sem nova checagem.
3. **Confirmação antes de gastar.** Máquina alugada, API paga ou plano: diga provedor, preço por hora, tempo e custo total estimados, e espere o "sim" escrito.
4. **Só o dono da voz ouve antes de publicar.** Envie o áudio a ele. Publicar só com o ok dele.
5. **Destruir a máquina.** Ao terminar, ou se algo falhar, baixe o resultado e destrua a máquina alugada. Confira na lista do provedor e informe o gasto.

| Desculpa | Resposta |
|---|---|
| "É só um teste" | A gravação e o modelo de voz já são dado pessoal da pessoa. O portão 1 vale para o teste. |
| "Ela topou de boca" | Sem registro escrito não há como mostrar o consentimento. Peça uma mensagem registrada. |
| "O cliente me mandou o áudio" | Quem manda o áudio não é, por isso, o dono da voz. |
| "O modelo deve ser livre" | Leia a licença na página do modelo. OmniVoice, F5-TTS, Voxtral, Higgs e XTTS-v2 são não comerciais. |
| "Destruo a máquina depois" | O disco cobra parado. Programe a destruição (`trap`) antes de rodar. |

**Pare e pergunte** se: a voz é de menor de 18 anos; o pedido é fazer a pessoa dizer o que ela não aprovou, propaganda política, golpe ou falar com banco em nome dela; o serviço pede verificação de voz e o dono não sabe que é autorização de voz.

## Fluxo

1. Entenda: de quem é a voz, para quê, onde roda (PC, GPU alugada ou serviço pago), orçamento.
2. Passe pelos portões 1 e 2.
3. Escolha o caminho:

| Situação | Caminho |
|---|---|
| Sua própria voz em peça publicada, tem de soar igual | Clonagem profissional paga do provedor: 30 min ou mais de áudio limpo, e o próprio titular verifica a voz. Fora desta skill. |
| Rascunho, ensaio de pronúncia, amostra que não pode sair do PC | Modelo local: `references/receita-omnivoice.md` (pesos não comerciais) |
| Trabalho pago com modelo aberto | Pesos permissivos: `references/receita-modelos-abertos.md`, com prova cega antes |
| Já existe uma fala humana e só falta trocar o timbre | RVC: `references/receita-rvc.md` |

4. **Amostra.** Rode, a partir da pasta da skill:
   `python scripts/preparar_amostra.py gravacao.m4a -o amostra.wav` (acha o melhor trecho de cerca de 16 s) ou `--inicio 1:23 --duracao 16` para indicar o trecho. `--help` lista as opções.
   Depois transcreva com Whisper e **revise palavra por palavra** até o texto bater com o áudio. Salve ao lado como `amostra.txt`.
   Alvo medido: 14,8 a 18 s, WAV mono 24 kHz, cerca de -18 LUFS, microfone perto, sala sem eco. Cada modelo tem a sua duração recomendada: veja a receita.
5. **Máquina.** PC próprio, ou `references/gpu-alugada.md` (portões 3 e 5).
6. **Candidatas.** Gere 3 com a mesma frase de teste, que tenha a palavra difícil do projeto.
7. **Conferência.** Transcreva cada candidata e compare com o texto (`references/geracao-longa-e-conferencia.md`). Ouça.
8. **Prova cega** com o dono da voz (`references/avaliacao.md`). Sem o ok dele, não siga.
9. **Roteiro inteiro**, em blocos com retomada, manifesto e dicionário de pronúncia (mesma referência do passo 7).
10. **Entrega.** Pós-processe, verifique o arquivo FINAL (decodifica sem erro, LUFS, pico, transcrição) e envie só ao dono da voz.
11. **Fechamento.** Baixe tudo, destrua a máquina (portão 5) e registre: amostra, texto, modelo, passos, semente, data e o veredito da prova cega.

## Números que valem (medidos com a voz do próprio autor, que autorizou)

| O quê | Valor |
|---|---|
| CPU de notebook, OmniVoice, 16 passos | 19 a 74 s de processamento por segundo de fala |
| Mesmo modelo, 32 passos | cerca do dobro do tempo; sem veredito de ouvido entre 16 e 32 |
| GPU A100 80 GB alugada, 16 passos | 0,06 a 0,17 s por segundo de fala |
| Ajuste fino do OmniVoice (12,5 min de dados) | segunda rodada: cerca de 35 min e US$ 0,60 na A100 (a primeira custou cerca de US$ 0,70); decora cedo |
| Régua de similaridade (ECAPA), voz real contra voz real | 0,675 a 0,741: ruído de uns 0,03 |

A nota da régua não decide. O ouvido do dono da voz decide.

## Erros comuns

| Sintoma | Causa | O que fazer |
|---|---|---|
| Palavra inventada no começo, "célula" por "celular", "R" final engolido | amostra de 12 s, baixa (-25 LUFS) ou com texto que não bate | amostra nova de 14,8 a 18 s a -18 LUFS, texto exato |
| Geração 10 vezes mais lenta na CPU | `OMNIVOICE_CPU_DTYPE=bfloat16` em CPU sem AVX-512 BF16 | não definir; usar float32 |
| Erro 1455 ao carregar no Windows | arquivo de paginação pequeno (o modelo usa cerca de 8,5 GB virtuais) | fixar de 16.384 a 32.768 MB |
| Métrica alta e voz ruim | a régua mede timbre, não naturalidade | prova cega |
| Checkpoint escolhido sumiu | máquina destruída antes do download | baixar antes do `destroy` |
| Voz robótica ao encaixar no vídeo | `atempo` abaixo de 0,74 | manter 1,0x e ajustar o vídeo |

## Referências

- `references/AUTORIZACAO-VOZ-E-IMAGEM.md`: termo de autorização modelo (não substitui advogado).
- `references/licencas.md`: portão de licença e fontes.
- `references/receita-omnivoice.md`: CPU e GPU, ajuste fino, a receita que rodamos.
- `references/receita-modelos-abertos.md`: Qwen3-TTS, VoxCPM2, MOSS-TTS, Chatterbox (do README, não rodados por nós).
- `references/receita-xtts.md`: XTTS-v2 sem treino (pesos não comerciais).
- `references/receita-rvc.md`: conversão de voz.
- `references/gpu-alugada.md`: ciclo da máquina alugada.
- `references/geracao-longa-e-conferencia.md`: blocos, transcrição, pronúncia, pós-processo.
- `references/avaliacao.md`: prova cega e régua de similaridade.
