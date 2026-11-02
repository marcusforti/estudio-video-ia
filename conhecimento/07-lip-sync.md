# Lip sync: consertar a boca em filmagem real ou animar uma foto com áudio

Este capítulo ajuda quem edita vídeo com agente de código a escolher e rodar lip sync (sincronia da boca com o áudio): qual dos dois trabalhos você tem, qual modelo aberto ou serviço pago serve, quanto custa e como testar antes de gastar. Baseia-se num teste real com quatro modelos abertos e na leitura das páginas dos fornecedores em 01/11/2026. Preços em dólares, vistos em 01/11/2026.

## Resumo em 30 segundos

- São dois trabalhos: consertar a boca de uma filmagem real (vídeo + áudio novo; o resto do quadro fica) e animar uma foto com áudio (cabeça e corpo são gerados). Escolha o trabalho antes do modelo.
- Rodamos quatro modelos abertos numa A100 alugada: LatentSync 1.6, InfiniteTalk, MuseTalk e TBDub. O TBDub saiu melhor que o LatentSync no nosso comparativo lado a lado. Rosto gerado do zero a partir de imagem foi rejeitado [testado].
- Não testamos nenhum serviço pago de lip sync. Os preços abaixo são do fornecedor, de 01/11/2026 [fornecedor].
- Não existe benchmark independente nem teste em português para nenhum modelo [sem medição]. Faça o teste de 10 a 15 s no seu pior plano antes de decidir.
- Consentimento por escrito vem antes de qualquer teste. Confira também a licença: vários modelos proíbem uso comercial.

## Mapa de decisão

Responda na ordem. A primeira pergunta é um portão: sem consentimento, para ali.

<!-- diagrama:lipsync-decisao -->

Todo destino que fala em teste leva à seção "O teste de 10 a 15 s".

## Portões antes de rodar

1. **Consentimento.** Por cautela, trate voz e rosto ligados a uma pessoa como dado pessoal sensível: a LGPD (Lei 13.709/2018) inclui o dado biométrico entre os sensíveis (art. 5, II), e o consentimento específico e destacado é uma das bases para tratá-lo (art. 11, I). Se a gravação de voz e o rosto em vídeo contam como biométrico é pergunta em aberto nas fontes que lemos. A transferência para fora do Brasil segue o art. 33 [oficial]. Tenha consentimento escrito de cada pessoa que aparece e de cada voz, dizendo o que será feito, onde será publicado, se roda em nuvem fora do Brasil e como revogar [praticante]. Não é parecer jurídico.
2. **Termos do serviço.** Leia antes de subir material de terceiros. A ElevenLabs proíbe clonar voz sem consentimento explícito e a Hedra proíbe mídia de outras pessoas [oficial]. Os termos da sync.so que encontramos são de 06/06/2024 e podem ter mudado. Naquela versão, o usuário mantém a propriedade do conteúdo e dá à empresa uma licença não exclusiva, mundial, perpétua e irrevogável para operar, melhorar e divulgar o serviço, e a empresa pode analisar características de rosto e voz, só por instrução do usuário [oficial]. Leia a versão atual antes de subir material de terceiros.
3. **Licença** do modelo: tabela abaixo.
4. **Custo e dono.** Mostre o valor estimado ao dono antes de rodar; o resultado vai só a ele antes de publicar.
5. **Onde roda.** Rosto e voz de terceiro vão para nuvem segura, não para o Colab: a FAQ proíbe "creating deepfakes" sem definir o termo [oficial]. Veja [GPU como se fosse local](06-gpu-como-local.md).

## Os dois trabalhos

| | Consertar a boca em filmagem real | Animar uma foto com áudio |
|---|---|---|
| Entra | Vídeo da pessoa + áudio novo | Foto (ou ilustração) + áudio |
| Sai | O mesmo vídeo, com a boca refeita | Um vídeo novo: cabeça, corpo e expressão são gerados |
| Fica igual | Câmera, mãos, fundo, cabeça | Só a identidade da foto |
| Modelos abertos | MuseTalk, LatentSync, TBDub, X-Dub, LTX Dub-It | InfiniteTalk, LongCat-Video-Avatar |
| Serviços pagos | sync.so, HeyGen, VEED | Hedra (só foto) |
| Risco principal | Plano difícil | Rosto que não parece a pessoa; cor que deriva depois de ~1 min |

O modo de dublagem do InfiniteTalk também sincroniza cabeça, corpo e expressões: não é edição local da boca [oficial]. Traduzir e trocar a voz (ElevenLabs Dubbing) é outra coisa, e não mexe na boca [oficial].

## O que testamos aqui

Quatro modelos abertos numa A100 de 80 GB alugada na Vast, a US$ 1,07 a 1,23 por hora em outubro de 2026 [testado]. A comparação foi visual e nossa, sem métrica de sincronia e sem teste cego.

| Modelo | Entrada | Resultado técnico | Veredito |
|---|---|---|---|
| LatentSync 1.6 | Vídeo real de frente + 3 áudios | 3 vídeos de 24 a 27 s (720x1280, 25 fps), 9 a 14 min cada | Fez o que promete (trocar a boca de uma filmagem existente). Num segundo teste, lado a lado, perdeu para o TBDub |
| InfiniteTalk | Foto + áudio | 26,6 s em 448x832, 64 min com a GPU dividida com um treino. Noutro dia, com imagens geradas por IA, saiu só um clipe | Sem veredito do modelo; as imagens de rosto geradas por IA que usamos como entrada foram reprovadas na revisão |
| MuseTalk 1.5 | Clipe-base de 720x720 + 25 s de áudio | Um teste; instalação com atrito | Sem veredito registrado; apagamos o ambiente |
| TBDub Student | Clipes-base de câmera fixa, de frente, ~10 s, em rodízio + áudio | Blocos de 25 a 55 s em 1280x720 e 25 fps; ~28 GB de VRAM por processo, no máximo 2 ao mesmo tempo | **Escolhido**: melhor que o LatentSync no comparativo lado a lado |

O TBDub Teacher (30 passos) não rodou por falta de memória e não repetimos com um único processo na placa. Não registramos tempo por bloco do TBDub. Nada rodou no notebook (sem GPU compatível) e nenhum serviço pago entrou no teste.

## Modelos abertos: licença, VRAM, velocidade, manutenção

VRAM é a memória da placa de vídeo. Para consertar a boca:

| Modelo | Licença | VRAM | Velocidade | Manutenção | Limite conhecido |
|---|---|---|---|---|---|
| MuseTalk 1.5 | MIT; pesos liberados, até comercial [oficial] | 4 GB em fp16 [fornecedor] | 30 fps+ numa V100; 8 s de vídeo em ~5 min na placa de 4 GB [fornecedor] | Último commit 26/09/2025 | Boca de 256 px; perde bigode; tremor [oficial] |
| LatentSync 1.6 | Código Apache-2.0; detector com InsightFace (ver licenças) [oficial] | 18 GB; o 1.5 pede 8 [fornecedor] | Aqui: 23 a 27 s de vídeo em 9 a 14 min na A100 [testado] | Último commit 20/06/2025; 229 issues abertas | Duas caras dão erro de detecção; falha em RTX 50 [independente] |
| TBDub Student | Apache-2.0, código e pesos [oficial] | ~28 GiB; 15 com `--cpu-offload` [fornecedor]; aqui ~28 GB [testado] | 7,13 fps numa H20 [fornecedor] | Criado em 02/09/2026, push de 12/09/2026, 40 estrelas | Só Linux; sem validação independente |
| X-Dub público | Apache-2.0 [oficial] | ~21 GB [fornecedor] | ~60 s para 3 s de vídeo, no paper [fornecedor] | Último commit 03/08/2026 | Modelo do paper é interno; o público tem tremor e ~2% de quadros com ruído [oficial] |
| LTX-2.3 Dub-It | LTX-2 Community License (ver licenças) [oficial] | Não achamos | Não achamos | LoRA de 22/10/2026 | Exige vídeo de referência; português não testado |

Para animar foto + áudio:

| Modelo | Licença | VRAM | Velocidade | Manutenção | Limite conhecido |
|---|---|---|---|---|---|
| InfiniteTalk | Apache-2.0 [oficial] | 480p roda em 24 GB; 720p estourou numa RTX 4090 [independente] | De ~200 s (4090, 480x832) a 64 min (aqui, 26 s de vídeo, GPU dividida) [independente] [testado] | Código parado desde 25/08/2025 | Cor deriva depois de ~1 min; treinado sobretudo em inglês e chinês [oficial] |
| LongCat-Video-Avatar 1.5 | MIT [oficial] | Não informada; um terceiro cita 16 GB (INT8) e 24 a 40 GB [sem medição] | Não achamos | 21/05/2026 | Não testamos; avaliação dos autores só em chinês e inglês |

Evite: Wan2.2-S2V (80 GB), HunyuanVideo-Avatar (24 GB "muito lento"; 96 GB recomendados) e SadTalker (parado desde 10/2023) [oficial]. Os tempos publicados de um mesmo modelo vão de minutos a horas conforme a configuração [independente].

### Licenças que travam uso comercial

Leitura de texto de licença, não parecer jurídico.

| Item | O que o texto diz | O que fazer |
|---|---|---|
| InsightFace (detector do LatentSync) | Modelos treinados com os dados dele: só pesquisa, sem fins comerciais [oficial] | Troque o detector (MediaPipe ou DWPose) ou licencie antes de trabalho pago |
| Wav2Lip | Pessoal, pesquisa ou não comercial [oficial] | Não use em trabalho pago |
| CodeFormer | Licença S-Lab 1.0: só uso não comercial [oficial] | Idem |
| LivePortrait | MIT, mas manda trocar os modelos do InsightFace para uso comercial [oficial] | Troque o detector |
| GFPGAN | Apache-2.0 "exceto componentes de terceiros"; a licença NVIDIA StyleGAN2 incluída limita a uso não comercial [oficial] | Trate como não comercial até esclarecer |
| HunyuanVideo-Avatar | Território exclui UE, Reino Unido e Coreia do Sul (o Brasil está dentro); proíbe usar a saída para melhorar outro modelo [oficial] | Cuidado ao distribuir fora do território |
| LTX-2 e Dub-It | Grátis só abaixo de US$ 10 milhões de receita anual; acima, licença paga [oficial] | Confira a receita de quem usa |
| TBDub | Apache-2.0 no [repositório](https://github.com/TaoLiveAIGC/TBDub) e nos pesos do Hugging Face (`TaoLiveAIGC/TBDub`) [oficial]. Não conferimos a licença dos pesos auxiliares (codificador de áudio) | Confira antes de uso comercial |

## Serviços pagos (não testados aqui)

Não temos conta em nenhum serviço pago de lip sync e não testamos nenhum. Tudo abaixo é o que o fornecedor publica [fornecedor]. Toda avaliação de qualidade que achamos vem do próprio fornecedor ou de revisor com laço comercial; não há teste cego independente [sem medição].

| Serviço | Para quê | Preço (US$) | O que limita |
|---|---|---|---|
| sync.so | Filmagem real: lipsync-2, lipsync-2-pro, sync-3 | Por segundo: 0,05, 0,083 e 0,133 (3, 5 e 8 por minuto). Planos por mês: 5, 19, 49 e 249. Grátis: 3 gerações de até 15 s | Marca d'água até o plano de 19, que vai a 5 min. Divide em trechos de 30 a 40 s; pede menos de 2 min. Sincroniza o rosto mais proeminente |
| fal.ai, hospeda modelos sem mensalidade | Os da sync.so e outros | sync-3 8 por minuto; VEED 0,40 por minuto; LatentSync 0,20 por vídeo de até 40 s, depois 0,005 por segundo | O cliente garante direitos e consentimentos |
| HeyGen, Lipsync via Replicate | Filmagem real; Precision para perfil e oclusão | Speed 0,0333 por segundo (~2 por minuto); Precision 0,0667 (~4 por minuto) | Só uma pessoa deve falar por vez. Preço da tradução por API: não achamos |
| ElevenLabs Dubbing | Só dublar o áudio | v1 0,50 por minuto (0,33 com marca d'água); v2 2,20 por minuto, em alpha, com pt-BR | Não mexe na boca |
| Magic Hour | Lip sync por API | A partir de 0,023 por segundo (~1,38 por minuto) | Uma só face visível, de frente |
| Kling Lip Sync | Clipes de 2 a 10 s | 0,014 por segundo de entrada, na fal | Termos do app restringem uso comercial da saída |
| Captions Lipdub, D-ID, Higgsfield | Aplicativos | Sem preço de API que tenhamos achado | Não pesquisamos a fundo |
| Hedra, Tavus, Pika, Runway Act-Two | Animam foto ou avatar; não consertam filmagem real | Hedra: 0,025 a 0,0625 por segundo | A Hedra proíbe mídia de outras pessoas |

Português: a sync.so diz "95+ idiomas"; HeyGen, Magic Hour e Captions listam português; nenhum mostra teste de sincronia em português [fornecedor]. Conflito sem solução: a sync.so diz que há API em todos os planos e a Replicate diz que exige o plano Scale.

## Custo por trabalho

Preço de tabela, um take. Em material difícil, multiplique por 2 a 3 [praticante].

| Rota | Reel de 30 s | VSL de 5 min | Dublagem de 5 min, áudio + lip sync |
|---|---|---|---|
| LatentSync na A100 alugada (conta nossa) | 0,18 a 0,37 | 1,78 a 3,74 | voz por fora |
| LatentSync na fal | 0,20 | 1,50 | 4,00 |
| VEED na fal | 0,20 | 2,00 | 4,50 |
| HeyGen Speed | 1,00 | 10,00 | ~1,45 no plano web |
| HeyGen Precision | 2,00 | 20,01 | ~2,42 no plano web |
| sync lipsync-2-pro na fal | 2,50 | 25,00 | 27,50 |
| sync-3 na fal | 4,00 | 40,00 | 42,50 |

A dublagem soma 5 min de ElevenLabs v1 sem marca d'água (US$ 2,50) ao lip sync; com o v2 são US$ 11,00. O HeyGen web sai dos créditos do plano Creator (US$ 29 por 600) e só vale se o preço do crédito for o do site. A linha da A100 usa 9 a 14 min de máquina por 23 a 27 s de vídeo e não inclui a montagem, que não medimos. O README do TBDub mede 63 s para um clipe de 15 s numa placa de 72 GB, sem carga do modelo [fornecedor]: no mesmo ritmo, 5 min seriam ~21 min de máquina, perto de US$ 0,40. Não medimos.

## Pipeline recomendado

1. Passe pelos portões: consentimento, termos, licença, custo.
2. Escolha uma base de câmera fixa, de frente, boca livre, que cubra o áudio mais 0,5 s [testado].
3. Conforme a entrada: 25 fps constantes e áudio mono de 16 kHz, sem música [oficial, README do MuseTalk].
4. Rode o teste de 10 a 15 s com 2 ou 3 candidatos.
5. Rode em blocos: 25 a 55 s nos modelos abertos [testado]; menos de 2 min nos serviços pagos [fornecedor].
6. O modelo faz sozinho a detecção do rosto, o recorte de 512 px, a geração e a colagem com correção de cor [oficial, README do TBDub]. Restauração de rosto só para saídas de 96 a 256 px, depois de conferir a licença [praticante].
7. Junte os blocos (`ffmpeg -f concat -c copy`), ponha o áudio e confira a última palavra e a sincronia.
8. Revise quadro a quadro e mande ao dono antes de publicar.

```bash
ffmpeg -ss 83 -t 12.5 -i bruto.mp4 -an -vf fps=25 -c:v libx264 -crf 14 -pix_fmt yuv420p base_25fps.mp4
ffmpeg -i voz.mp3 -ac 1 -ar 16000 -af apad=pad_dur=0.5 voz_16k.wav
```

## Falhas típicas e como evitar ao filmar

| Falha | Causa | Como evitar |
|---|---|---|
| Boca deformada em perfil | A detecção do rosto falha em ângulo extremo [fornecedor] | Filme de frente; o perfil indispensável roda à parte, em modo para plano difícil |
| Mão, microfone, cabelo ou óculos escuros na boca | Escondem a região que o modelo refaz [fornecedor] | Microfone abaixo do queixo; mãos baixas na fala |
| Duas pessoas ou rosto pequeno | O modelo escolhe o rosto mais proeminente ou não acha rosto [fornecedor] | Uma pessoa por plano; mascare o outro rosto; rosto grande no quadro |
| Música ou ruído no áudio | Confundem o tempo da boca [fornecedor] | Voz limpa e seca |
| Última palavra cortada | Áudio mais longo que o vídeo | Vídeo 0,5 s mais longo que o áudio [testado] e 0,5 s de silêncio no fim do áudio [praticante] |
| Dessincronia ou deriva | fps variável ou diferente de 25 [oficial] | 25 fps constantes |
| Dentes artificiais; barba ou bigode perdidos | Boca de 256 px ou limite do modelo [oficial] | Modelo de 512 px; teste com barba antes |

## O teste de 10 a 15 s no seu pior plano

Não existe benchmark independente nem teste em português para nenhum modelo ou serviço [sem medição]. A decisão tem de sair do seu material.

1. **Escolha o pior plano:** perfil, mão perto da boca, dentes à mostra, barba, pouca luz, fala rápida.
2. **Escolha a fala** na voz final do projeto, em português do Brasil, com lábios fechados (pão, bom, mamãe), vogais nasais (não, mão, põe) e vogais arredondadas (o, u). A escolha é nossa: nenhum benchmark cobre o português [praticante].
3. **Prepare** com `preparar_teste.py`, da skill [estudio-lipsync](../skills/estudio-lipsync/SKILL.md) (recorte, vídeo de 25 fps sem áudio e áudio de 16 kHz), ou com os comandos do pipeline.
4. **Rode o mesmo par (base + voz)** em dois modelos abertos e em um serviço pago. Para 12 s de vídeo, a preço de tabela: LatentSync na fal US$ 0,20, lipsync-2-pro US$ 1,00, sync-3 US$ 1,60. Mensalidades somam à parte.
5. **Compare lado a lado, com som,** com `comparar_lado_a_lado.py`. Em ffmpeg puro: `-filter_complex "[0:v]scale=-2:540[a];[1:v]scale=-2:540[b];[a][b]hstack=inputs=2:shortest=1[v]" -map "[v]"`.
6. **Avalie com sete perguntas:** os lábios fecham em p, b, m? As nasais abrem certo? Os dentes parecem dentes? Há remendo em volta da boca? Cor e nitidez da boca batem com o rosto? Há tremor entre quadros? A última palavra saiu inteira? A pessoa continua parecendo ela mesma?
7. **Anote custo e tempo:** segundos de GPU por segundo de vídeo, na placa que você alugou.
8. **Decida pelo mais barato que passa no pior plano:** se passa no pior, passa nos outros [praticante]. Se nenhum passar, refilme o plano antes de trocar de ferramenta.

## Recomendação por caso

| Caso | Recomendação | Base |
|---|---|---|
| Reel de até 60 s, uma pessoa de frente | MuseTalk 1.5 para rascunho; LatentSync ou VEED na fal (US$ 0,20 a 0,40) | [fornecedor] |
| Reel com plano difícil | Teste de 10 a 15 s: TBDub ou X-Dub alugados, ou sync-3 / HeyGen Precision | [fornecedor] |
| Vídeo longo, um apresentador de frente | TBDub Student em blocos de 25 a 55 s | [testado] |
| Dublagem em outro idioma | Áudio novo pronto: só lip sync. Precisa traduzir: pacote (HeyGen Translate, sync.so Dubbing) | [fornecedor] |
| Personagem ou ilustração falando | InfiniteTalk 480p | [oficial] |
| Entrevista com duas pessoas | Mascare o rosto que não fala ou processe cada falante à parte | [fornecedor] |

## O que deu errado aqui

- **Escolhemos o modelo pelo que ele promete, não pelo trabalho a fazer.** O LatentSync conserta a boca de uma filmagem existente e não anima uma foto. Responda "o que eu tenho em mãos" antes de instalar.
- **Imagem de rosto gerada por IA foi reprovada na revisão.** Se a pessoa precisa parecer ela mesma, filme a base e conserte só a boca.
- **Instalação com atrito:** mmcv, mmdet e mmpose em versões fixas e `pip install --no-build-isolation chumpy` no MuseTalk; no InfiniteTalk, comentar a linha `from inspect import ArgSpec`.
- **O TBDub Teacher estourou a memória.** O Student usa ~28 GB por processo: no máximo 2 por A100 de 80 GB.
- **Placas baratas que não ligam, ffmpeg do conda sem `libx264` e disco cheio de pesos:** soluções em [GPU como se fosse local](06-gpu-como-local.md).

## O que não testamos

- Nenhum serviço pago de lip sync (sync.so, HeyGen, VEED, Kling, Magic Hour, Captions, D-ID, Hedra) e nenhuma conta neles.
- Nada no notebook: ele não tem GPU para esses modelos.
- Teste cego, métrica de sincronia (como SyncNet) e qualquer medição em português.
- TBDub Teacher, tempo por bloco do TBDub, veredito do MuseTalk e do InfiniteTalk.
- X-Dub, LongCat 1.5, LTX Dub-It: só documentação.
- Licença dos pesos auxiliares do TBDub e do detector S3FD (MuseTalk).

## Links

- [LatentSync](https://github.com/bytedance/LatentSync) e [issue 302](https://github.com/bytedance/LatentSync/issues/302): repositório; falha em RTX 50.
- [InsightFace](https://github.com/deepinsight/insightface#license): licença, só pesquisa.
- [MuseTalk](https://github.com/TMElyralab/MuseTalk) e [ficha](https://huggingface.co/TMElyralab/MuseTalk): licença e limites.
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip): licença não comercial.
- [X-Dub](https://github.com/KlingAIResearch/X-Dub): versão pública e limites.
- [TBDub](https://github.com/TaoLiveAIGC/TBDub) e [artigo](https://arxiv.org/abs/2609.06144): o modelo que usamos.
- [LTX-2: licença](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) e [Dub-It](https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-DubIt): teto de US$ 10 milhões.
- [InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk): modos e limites.
- [LongCat-Video-Avatar 1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5): ficha.
- [HunyuanVideo-Avatar](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/main/LICENSE), [LivePortrait](https://github.com/KlingAIResearch/LivePortrait/blob/main/LICENSE), [GFPGAN](https://github.com/TencentARC/GFPGAN/blob/master/LICENSE) e [CodeFormer](https://github.com/sczhou/CodeFormer/blob/master/LICENSE): licenças.
- [sync.so: preços](https://sync.so/pricing), [modelos](https://sync.so/docs/models), [dicas](https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality) e [termos](https://sync.so/terms).
- [fal: sync-3](https://fal.ai/models/fal-ai/sync-lipsync/v3/llms.txt), [VEED](https://fal.ai/models/veed/lipsync), [LatentSync](https://fal.ai/models/fal-ai/latentsync) e [Kling](https://fal.ai/models/fal-ai/kling-video/lipsync/audio-to-video/llms.txt): preços.
- [HeyGen Speed](https://replicate.com/heygen/lipsync-speed) e [Precision](https://replicate.com/heygen/lipsync-precision): preços por segundo.
- [ElevenLabs: preços](https://elevenlabs.io/pricing/api), [Dubbing](https://elevenlabs.io/docs/overview/capabilities/dubbing) e [política de uso](https://elevenlabs.io/use-policy).
- [Magic Hour](https://magichour.ai/products/lip-sync), [Hedra: uso aceitável](https://www.hedra.com/acceptable-use) e [Kling: termos](https://kling.ai/docs/user-policy).
- [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm): arts. 5 e 11.
- [Colab: FAQ](https://research.google.com/colaboratory/faq.html): "creating deepfakes".
