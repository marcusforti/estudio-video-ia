# Voz local: clonar voz com TTS, conversão de voz e GPU alugada

Este capítulo ajuda criadores e editores a decidir como clonar a voz do próprio criador, ou de quem autorizou por escrito, para narrar vídeos: modelo aberto no seu PC, modelo aberto numa GPU alugada ou serviço pago. Traz a receita que seguimos, os tempos que medimos, as licenças que decidem o uso comercial e os erros que custaram horas. A skill [estudio-voz-local](../skills/estudio-voz-local/SKILL.md) conduz o passo a passo. Nos números e nas notas de ouvido deste capítulo, "o autor" é Marcus Forti, que autorizou o uso da própria voz.

## Resumo em 30 segundos

- Para a voz do autor em peça publicada, a clonagem profissional paga (modelo mais novo do provedor) foi a única que ele aceitou como igual à própria voz [testado].
- Modelo aberto serve para rascunho, ensaio de pronúncia e volume interno. Na CPU de um notebook comum custou de 19 a 74 s de processamento por segundo de fala [testado].
- A amostra decide quase tudo: 14,8 a 18 s, WAV 24 kHz mono, cerca de -18 LUFS, com o texto exato. Nota de similaridade não substitui o ouvido [testado].
- Pesos de OmniVoice, F5-TTS, Voxtral, Higgs e XTTS-v2 são não comerciais: não use em trabalho pago sem verificar a licença [oficial]. Qwen3-TTS, VoxCPM2, MOSS-TTS e Chatterbox clonam, falam português e têm pesos permissivos [oficial], mas não achamos comparativo cego independente em pt-BR [sem medição].
- Antes de começar, tenha autorização escrita do dono da voz. Ao terminar, destrua a máquina alugada.

## Qual caminho escolher

<!-- diagrama:voz-decisao -->

Áudio necessário: PVC de 30 min a 3 h, clone instantâneo de 1 a 3 min [oficial]. O limite de 8 GB no passo 6 é estimativa pelo tamanho dos pesos [sem medição].

## TTS com clonagem ou conversão de voz (RVC)

| | TTS com clonagem | Conversão de voz (RVC) |
|---|---|---|
| Entrada | texto e amostra de 3 a 30 s | uma fala já gravada |
| O modelo decide | pronúncia, ritmo, entonação e timbre | só o timbre |
| Treino | nenhum (zero-shot) | 10 min ou mais de fala limpa [fornecedor] |
| Herda da entrada | nada | ritmo, sotaque e defeitos |
| Use quando | tem texto novo e não quer gravar | grava uma leitura-guia e troca o timbre |

Empilhar os dois (TTS e depois RVC) subiu a nota de similaridade de 0,663 para 0,723, com 32,2 min de aulas no treino [testado]. Ao ouvido a diferença foi pequena, segundo anotação nossa sem registro em arquivo [sem medição]. Um estudo independente com voz infantil em pt-BR viu o RVC amplificar a artificialidade da fala sintética, e só melhorar quando a entrada era voz humana [independente]. Com os TTS de 2026, gaste primeiro na amostra.

## Modelos: licença e português

Licenças e idiomas conforme README e cartão de cada modelo, lidos em 01/11/2026 [oficial].

Pesos permissivos, com clonagem e português:

| Modelo | Pesos | Português | Amostra pedida | GPU |
|---|---|---|---|---|
| Qwen3-TTS (jan/2026) | Apache-2.0 | sim, entre 10 idiomas | 3 s e a transcrição | não informada |
| VoxCPM2 (abr/2026) | Apache-2.0 | sim, entre 30 | áudio e transcrição exata | cerca de 8 GB |
| MOSS-TTS e v1.5 (fev e mai/2026) | Apache-2.0 | sim, entre 20 e 30+ | não encontrada | não informada |
| Chatterbox Multilingual V3 | MIT | sim, com pacote pt-BR | 10 s ou mais, no mesmo idioma | não informada |

Amostra pedida e GPU: dados do fabricante [fornecedor].

Com clonagem e português, mas restritos:

| Modelo | Pesos | O que a licença diz |
|---|---|---|
| OmniVoice | CC-BY-NC (código Apache-2.0) | não comercial, por causa dos dados de treino |
| F5-TTS | CC-BY-NC (código MIT) | não comercial; português só em ajuste comunitário, também não comercial |
| XTTS-v2 | CPML | só uso não comercial; o texto cobre também o áudio gerado |
| Voxtral TTS | CC BY-NC 4.0 | uso comercial só pela API do fabricante |
| Higgs Audio v3 | Boson Research and Non-Commercial License | produção, serviço hospedado e revenda pedem licença à parte |
| Fish Audio Drama 3 | Community License v1.0 | comercial grátis só abaixo de US$ 500 mil de faturamento anual; proíbe imitar pessoa sem consentimento |

**Pesos não comerciais não servem para trabalho comercial sem verificar a licença.** As fontes que lemos não dizem se o áudio gerado por pesos CC-BY-NC herda a restrição, e o XTTS-v2 diz que herda. Trate a peça paga como uso comercial. Isto relata o que as fontes dizem e não é parecer jurídico.

Sem português ou sem clonagem aberta: IndexTTS-2.5, GPT-SoVITS, CosyVoice 3, OpenVoice V2, Dia e Orpheus (sem português); Kokoro-82M e Supertonic 2 (português, sem clonagem). Conversão de voz: RVC e Applio (MIT); Seed-VC (GPL-3.0, arquivado em 21/11/2025).

Só o Chatterbox (pacotes separados) e o Higgs v3 dizem se o português é pt-BR ou pt-PT [oficial]. Não encontramos comparativo cego independente em pt-BR: as medições em português são dos próprios autores, e o ranking independente mais citado é em inglês [sem medição]. Dos modelos desta seção, rodamos aqui só o OmniVoice e, sem veredito, o XTTS-v2 na CPU; os quatro permissivos ficaram sem teste.

## GPU necessária

| Tarefa | Onde rodamos | O que sabemos |
|---|---|---|
| OmniVoice, gerar voz | CPU de notebook modesto (sem GPU compatível com o CUDA atual); T4 do Colab; A100 alugada | roda sem GPU, devagar; o app VoiceStudio (debpalash; AGPL-3.0) recomenda 6 GB de VRAM e mediu pico de 2,05 GB numa T4 [fornecedor] |
| OmniVoice, ajuste fino | A100 80 GB alugada | mínimo não medido |
| RVC, treino | T4 de 16 GB do Colab grátis | bastou [testado] |
| Os quatro permissivos | não rodamos | estimativa só pelo tamanho dos pesos [sem medição]: Qwen3-TTS de 1,7 bi cabe em 8 GB e MOSS-TTS de 8,49 bi pede 24 GB |

## Preparo da amostra

O que medimos com a voz do autor, microfone perto, sala sem eco:

| Amostra | Duração | Formato | Nível | Resultado |
|---|---|---|---|---|
| Candidata aprovada | 14,8 s | WAV 16 bits, 24 kHz, mono | -17,6 LUFS | a que usamos |
| Preferida entre seis | cerca de 18 s | idem | -18 LUFS | ganhou a prova cega, ainda abaixo da voz real |
| Gravação original | 95,7 s | AAC 44,1 kHz, estéreo | -34,6 LUFS | reprovada como amostra |
| Amostra antiga | 12,0 s | WAV 24 kHz, mono | -25 LUFS | reprovada: curta, baixa, suja e com texto que não batia |

- Normalize para cerca de -18 LUFS. O texto da amostra tem de bater com o áudio palavra por palavra: texto errado piora o clone e insere palavras no começo da fala [testado]. A sala entra no clone, então use microfone perto e sem eco [fornecedor].
- O fabricante do OmniVoice indica 3 a 10 s [fornecedor]; aqui funcionaram 14,8 a 18 s [testado]. Outras faixas: Qwen3-TTS 3 s, Chatterbox 10 s ou mais, F5-TTS menos de 12 s, XTTS-v2 6 s [fornecedor].

```bash
python skills/estudio-voz-local/scripts/preparar_amostra.py gravacao.m4a -o amostra.wav
python skills/estudio-voz-local/scripts/preparar_amostra.py aula.mp4 -o amostra.wav --inicio 1:23 --duracao 16
```

O script mede o loudness, escolhe o trecho de cerca de 16 s com menos pausa (ou usa o que você indicar), gera WAV mono a 24 kHz em -18 LUFS e relata duração, pico e silêncio [testado com áudio sintético]. Depois transcreva com Whisper (`small` para rascunho, `large-v3` melhor), revise palavra por palavra e salve `amostra.txt` ao lado.

## Receita do zero até a voz pronta

Trate a GPU alugada como o seu PC: mesma pasta, mesmos comandos, e ela some no fim. O ciclo completo, os preços e a segurança estão em [GPU como local](06-gpu-como-local.md). O exemplo é o OmniVoice, o modelo aberto que usamos de ponta a ponta [testado]. Para os permissivos, a skill traz o que a documentação diz.

1. **Portões.** Autorização escrita do dono da voz ([modelo de termo](../modelos/AUTORIZACAO-VOZ-E-IMAGEM.md)), licença do modelo conferida e preço por hora aprovado antes de alugar.
2. **Gravar e preparar.** Microfone perto, sem eco, sem música, 2 a 3 min de leitura natural; amostra e texto como na seção anterior.
3. **Alugar e subir** os arquivos:

```bash
vastai set api-key "$VAST_API_KEY"   # uma vez por sessão
vastai search offers 'gpu_name in [A100_PCIE,A100_SXM4] num_gpus=1 reliability>0.98 inet_down>500 disk_space>=100 rentable=true' -o dph --raw
vastai create instance <OFERTA> --image pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel --disk 100 --ssh --direct --raw
scp -P <PORTA> amostra.wav amostra.txt roteiro.json root@<IP>:/root/voz/
```

4. **Instalar** na máquina, por ssh:

```bash
pip install -q -U brotli soundfile
pip install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
git clone -q https://github.com/k2-fsa/OmniVoice.git && pip install -q -e OmniVoice
hf download k2-fsa/OmniVoice
```

5. **Gerar 3 candidatas** com a mesma frase de teste, uma com a palavra difícil do projeto:

```python
import torch, soundfile as sf
from omnivoice import OmniVoice
frase = "Sua frase de teste, com a palavra difícil."
modelo = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
prompt = modelo.create_voice_clone_prompt(ref_audio="amostra.wav", ref_text=open("amostra.txt", encoding="utf-8").read().strip())
torch.manual_seed(7)   # repete a mesma tomada
audio = modelo.generate(text=frase, voice_clone_prompt=prompt, language="pt", num_step=16, speed=1.0)
sf.write("candidata1.wav", audio[0], 24000)
```

6. **Conferir** por transcrição, ouvir e fazer a prova cega com o dono da voz.
7. **Gerar o roteiro inteiro** em blocos (próxima seção), pós-processar, verificar o arquivo final e entregar só ao dono da voz.
8. **Baixar e destruir** a máquina. O disco cobra parado:

```bash
scp -P <PORTA> -r root@<IP>:/root/voz/saida ./saida
echo y | vastai destroy instance <ID>
vastai show instances --raw   # tem de imprimir []
```

Na CPU, use `device_map="cpu"` e `dtype=torch.float32` [sem medição: rodamos a CPU pelo app, não por este código]. No Windows: paginação fixa de 16.384 a 32.768 MB, uma geração por vez e nunca `OMNIVOICE_CPU_DTYPE=bfloat16` [testado]. O pacote `omnivoice` é Apache-2.0; o app [VoiceStudio](https://github.com/debpalash/VoiceStudio) (debpalash) é AGPL-3.0 [fornecedor].

## Geração longa, conferência e pronúncia

**Blocos com retomada** [testado]: um arquivo por bloco, e se existe, pula; para refazer, apague só aquele. Blocos de até 260 caracteres, 0,3 s de pausa entre eles. Manifesto com o SHA-256 da amostra e a configuração, recusando mudança silenciosa. Um modelo pesado por vez, hora de cada bloco no log e prévia de cerca de 35 s ao dono antes do resto. Cortar por frase tem motivo: o F5-TTS aceita 30 s por geração, o Dia acelera acima de 20 s e o Chatterbox Turbo fica instável depois de 25 a 30 s [oficial].

**Conferência por transcrição** [testado]: transcreva cada bloco com Whisper `small` (CPU, int8) e compare com o roteiro. A razão é palavras casadas dividido pela maior contagem de palavras. Passa com 0,88 ou mais. Abaixo disso, repita sem o prompt do roteiro, porque o prompt pode esconder o erro. Numa narração de 18 blocos, 17 ficaram entre 0,96 e 1,00; um deu 0,52 com o prompt e 0,96 sem. Confira também o arquivo final. O código está na skill.

**Pronúncia:** escreva como se fala, com número por extenso e acento nos nomes, e aplique antes do TTS um dicionário que troca a palavra escrita pela forma falada. Funcionaram `CRM` por `cê érre ême`, `110` por `cento e dez` e `kkkk` por `rárárárá` [praticante]. O paper do OmniVoice admite tratamento de números "não otimizado" [oficial].

**Nível:** `loudnorm=I=-18:TP=-3:LRA=7,aresample=48000` em cada bloco. Sem o `aresample`, o `loudnorm` deixa o áudio a 96 kHz ou mais e ele engasga [testado].

## Avaliação: métrica e ouvido

| Camada | O que mede | Limite |
|---|---|---|
| Prova cega de ouvido | tudo | decide; precisa do dono da voz |
| Transcrição (Whisper) | texto certo | não mede naturalidade |
| Similaridade de locutor (ECAPA, 16 kHz mono) | timbre | ruído de uns 0,03 |
| Perda do treino | se o ajuste avança | a menor perda (500 passos) perdeu no ouvido para 750 |

Notas ECAPA com a voz do autor (1 = mesma voz) [testado]: trechos reais 0,675 e 0,741; OmniVoice com microfone de estúdio 0,663 e com amostra de aula 0,698; OmniVoice com RVC 0,723; voz de outra pessoa 0,334. O autor preferiu a amostra de menor nota. Calibre sempre com "real contra real", e use a régua só como apoio [testado].

Prova cega: mesma frase, letras embaralhadas, gabarito em arquivo separado e tomadas no mesmo loudness [praticante]. Registre o veredito por escrito, com a data.

## Quando usar local e quando pagar

| Situação | Use | Por quê |
|---|---|---|
| Voz do autor em peça publicada | Clonagem profissional paga do provedor, 106,6 min de áudio em 25 amostras | única aceita como igual à voz real; as versões v2 e v3 do modelo foram reprovadas e só a v4 serviu [testado] |
| Rascunho, ensaio de texto e pronúncia | Modelo local | sem custo, offline, a amostra não sai do PC |
| Volume grande sem pagar por caractere | Pesos permissivos em GPU alugada, depois da prova cega | paga GPU em vez de caractere [sem medição] |
| Poucos minutos de áudio limpo | Clone instantâneo pago ou modelo local | a PVC pede 30 min ou mais [oficial] |
| Voz de outra pessoa | Só com autorização escrita | a PVC só aceita a própria voz, com verificação [oficial] |
| Treinar modelo local com a saída de um serviço pago | Leia os termos antes | não achamos a resposta nas fontes [sem medição] |

Preços vistos em 01/11/2026, em USD [fornecedor]: ElevenLabs Creator US$ 22/mês, com PVC; API a US$ 0,08 por 1.000 caracteres; Voxtral via API a US$ 0,016 por 1.000. GPU A100 80 GB: US$ 1,23/h pagos em outubro de 2026 e US$ 1,19 a 1,79/h na página da RunPod de 28/10/2026. Os créditos do Creator aparecem com números diferentes em duas páginas do fabricante: confira antes de assinar.

## Tempos medidos

| Execução | Passos | Fala gerada | Tempo | s por s de fala |
|---|---|---|---|---|
| CPU de notebook, amostra antiga | 16 | 132,5 s, 17 blocos | 62,1 min | 28 (19 a 40) |
| CPU de notebook, amostra antiga | 32 | 131,5 s | 119,9 min | 55 (39 a 71) |
| CPU de notebook, amostra nova | 16 | 25,8 s, 2 blocos | 26,5 min | 61 (53 a 74) |
| A100 80 GB, seis amostras | 16 | 166,1 s, 6 blocos | 15,0 s | 0,09 (0,06 a 0,17) |

[testado] A carga do modelo na CPU levou 43 a 115 s. A amostra nova ficou 2 a 3 vezes mais lenta no mesmo PC, causa não registrada. Entre 16 e 32 passos não registramos veredito de ouvido [sem medição]. Ajuste fino: 0,66 a 0,78 s por passo, 750 passos em cerca de 9 min, segunda rodada inteira em cerca de 35 min e US$ 0,60 [testado]. O tempo de treino da PVC não foi medido [sem medição].

## Base legal: o que as fontes dizem

Não é parecer jurídico. Situação em 01/11/2026.

- **Consentimento.** A política de uso da ElevenLabs proíbe clonar ou imitar a voz de qualquer pessoa viva sem consentimento explícito e informado [oficial]. Licenças como a do Fish Audio e o README do OmniVoice trazem proibições parecidas [oficial].
- **Por escrito e dado biométrico.** A LGPD (Lei 13.709/2018) pede consentimento por escrito ou outro meio que demonstre a vontade do titular (art. 8º). O art. 5º, II inclui o dado biométrico vinculado a uma pessoa entre os sensíveis, e o art. 11, I pede consentimento específico e destacado [oficial]. Se a gravação de voz e o modelo de voz contam como dado biométrico, é pergunta em aberto nas fontes que lemos; não achamos orientação da ANPD sobre clonagem de voz. A abordagem conservadora é tratar os dois como sensíveis [praticante].
- **Voz e imagem.** A Constituição (art. 5º, X e XXVIII, "a") e o Código Civil (arts. 11, 12 e 20) protegem imagem e voz, e o art. 20 diz que, sem autorização, o uso da imagem ou da palavra pode ser proibido se atingir a honra ou tiver fins comerciais [oficial]. Pelas fontes, não há lei brasileira específica sobre clonagem de voz em vigor.
- **Rótulo nas plataformas.** O YouTube pede aviso para conteúdo alterado ou gerado por IA que pareça realista; clonar a própria voz para locução fica sem aviso. A Meta pode exigir rótulo em áudio realista (cita um Reel narrado por voz gerada). O TikTok pede rótulo para IA com cenas ou pessoas realistas, sem tratar de voz [oficial].
- **PL 2338/2023 (marco da IA).** O Senado aprovou em 10/12/2024 e enviou à Câmara em 17/03/2025. Em 01/11/2026 a Comissão Especial segue em "Aguardando Parecer do Relator", sem parecer nem votação; a última movimentação visível é de 27/10/2026 [oficial]. Não lemos o texto dos artigos sobre conteúdo sintético [sem medição].

O quadro completo está em [Licenças e consentimento](11-licencas-e-consentimento.md). Para registrar o consentimento, use o [modelo de termo](../modelos/AUTORIZACAO-VOZ-E-IMAGEM.md), que é ponto de partida e não substitui advogado.

## O que deu errado aqui

| Sintoma | Causa | Solução |
|---|---|---|
| Palavra inventada no começo, "célula" por "celular", "R" final engolido | amostra de 12 s, a -25 LUFS e com texto que não batia | amostra de 14,8 a 18 s a -18 LUFS, texto exato |
| Erro 1455 ao carregar no Windows | o modelo aloca cerca de 8,5 GB virtuais e o arquivo de paginação era de 8 GB | paginação fixa de 16.384 a 32.768 MB |
| CPU 10 vezes mais lenta | `OMNIVOICE_CPU_DTYPE=bfloat16` num CPU sem AVX-512 BF16 | não definir; usar float32 |
| Um bloco com 4 h 18 min | PC parado no meio da geração, causa não registrada | um bloco por arquivo, pula se existe, log com hora; descarte o bloco ao calcular médias |
| Checkpoint escolhido sumiu | máquina destruída antes do download; o re-treino com os mesmos dados e semente não reproduziu | baixar o `checkpoint-N` antes do `destroy`; guardar semente e lista de trechos |
| O ajuste fino decorou | 12,5 min de dados, cerca de 4 passos por época | salvar a cada 250 passos e comparar de ouvido |
| Voz robótica ao encaixar no vídeo | `atempo` abaixo de 0,74 | manter 1,0x e ajustar o vídeo |
| Métrica boa, voz ruim | a régua mede timbre, não naturalidade | prova cega; mostrar um trecho curto antes de gerar a peça longa |

## Links

- [OmniVoice](https://github.com/k2-fsa/OmniVoice): repositório oficial.
- [OmniVoice, README](https://huggingface.co/k2-fsa/OmniVoice/raw/main/README.md): licença dos pesos e aviso de uso.
- [VoiceStudio](https://github.com/debpalash/VoiceStudio): app de terceiros (debpalash), AGPL-3.0; este manual não usa o código dele.
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS): repositório e README.
- [VoxCPM](https://github.com/OpenBMB/VoxCPM): VoxCPM2, licença e requisitos.
- [MOSS-TTS](https://huggingface.co/OpenMOSS-Team/MOSS-TTS): cartão do modelo.
- [Chatterbox](https://github.com/resemble-ai/chatterbox): idiomas, licença e marca d'água.
- [Chatterbox pt-BR](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-pt-br): pacote só de pt-BR.
- [F5-TTS](https://github.com/SWivid/F5-TTS): licença dos pesos.
- [XTTS-v2, licença](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt): texto da CPML.
- [Voxtral TTS](https://mistral.ai/news/voxtral-tts): idiomas e preço da API.
- [Higgs Audio v3](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b): licença.
- [Fish Audio, licença](https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE): Community License v1.0.
- [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI): conversão de voz.
- [STIL 2026](https://aclanthology.org/2026.stil-1.29/): estudo independente em pt-BR, voz infantil.
- [Artificial Analysis](https://artificialanalysis.ai/text-to-speech/leaderboard): ranking independente, em inglês.
- [SpeechBrain ECAPA](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb): modelo da régua de similaridade.
- [ElevenLabs, clonagem profissional](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning/professional-voice-cloning): requisitos da PVC.
- [ElevenLabs, clonagem instantânea](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning/instant-voice-cloning): requisitos.
- [ElevenLabs, política de uso](https://elevenlabs.io/use-policy): consentimento.
- [ElevenLabs, preços](https://elevenlabs.io/pricing): planos.
- [RunPod, preços](https://www.runpod.io/pricing): GPU por hora.
- [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm): Lei 13.709/2018.
- [Constituição](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm): art. 5º.
- [Código Civil](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm): arts. 11, 12 e 20.
- [PL 2338/2023, Senado](https://www25.senado.leg.br/web/atividade/materias/-/materia/157233): matéria no Senado.
- [PL 2338/2023, Câmara](https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2487262): tramitação.
- [YouTube](https://support.google.com/youtube/answer/14328491): conteúdo alterado ou sintético.
- [Meta](https://www.meta.com/en-gb/help/artificial-intelligence/1783222608822690/): rótulo de IA.
- [TikTok](https://www.tiktok.com/community-guidelines/en/integrity-authenticity): conteúdo gerado por IA.
