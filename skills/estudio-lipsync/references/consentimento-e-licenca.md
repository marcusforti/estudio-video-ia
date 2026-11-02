# Consentimento e licença

Selos: `[oficial]` = norma ou documento do fabricante; `[praticante]` = recomendação nossa, sem medição. Nada aqui é parecer jurídico: são leituras de texto.

## Portão 1: consentimento

Por cautela, trate voz e rosto ligados a uma pessoa como dado pessoal sensível: a LGPD (Lei 13.709/2018) inclui o dado biométrico entre os sensíveis (art. 5, II), e o consentimento específico e destacado é uma das bases para tratá-lo (art. 11, I). Se a gravação de voz e o rosto em vídeo contam como biométrico é pergunta em aberto nas fontes que lemos. A transferência para fora do Brasil segue o art. 33 [oficial]. Rodar em GPU de outro país provavelmente cai nessa regra [praticante]. Isto não é parecer jurídico.

Perguntas ao usuário, uma por vez. Qualquer "não" ou "não sei" para o portão:

1. Quem aparece no vídeo e quem fala no áudio? Cada um deu consentimento por escrito?
2. O termo diz o que será feito (trocar a boca para acompanhar um áudio novo, dublar, clonar a voz)?
3. O termo diz onde o resultado será publicado e por quanto tempo?
4. O termo cobre processamento em nuvem, possivelmente fora do Brasil?
5. O termo diz como revogar e o que acontece com os arquivos?
6. A voz do áudio novo é de alguém que consentiu em ter a voz usada ou clonada?

Se algo faltar, pare e diga o que falta. Não rode "só para testar".

## Termos dos serviços (lidos em 01/11/2026)

| Serviço | O que os termos dizem |
|---|---|
| ElevenLabs | Proíbe clonar, sintetizar ou imitar voz, identidade ou imagem de qualquer pessoa viva sem consentimento explícito e informado, e gravações de menores de 18 anos [oficial] |
| Hedra | Proíbe subir fotos, áudio ou vídeo com pessoas que não sejam você [oficial] |
| sync.so | Termos de 06/06/2024, que podem ter sido trocados: licença não exclusiva, mundial, perpétua e irrevogável sobre o conteúdo para operar, melhorar e divulgar o serviço; pode analisar características de rosto e voz; proíbe violar privacidade e imitar [oficial] |
| HeyGen | Avatares exigem consentimento explícito de quem é representado; a política não trata de traduzir o vídeo de outra pessoa [oficial] |
| Kling (app) | Exige direitos ou autorização legal sobre as entradas; proíbe uso comercial da saída sem permissão escrita [oficial] |
| fal.ai | O cliente garante que tem direitos, consentimentos e permissões sobre o que sobe; regras de deepfake ficam numa política de uso aceitável que não lemos [oficial] |
| Google Colab | A FAQ lista "creating deepfakes" entre os usos proibidos e não define o termo (https://research.google.com/colaboratory/faq.html, lida em 01/11/2026): não use para rosto e voz de terceiro [oficial] |

Não lemos os termos de uso aceitável de Vast, RunPod, Lambda, Replicate, VEED, Magic Hour, Captions, D-ID e Higgsfield.

## Portão 2: licença do modelo

Descarte, em trabalho pago, o que a tabela bloqueia.

| Item | O que o texto diz | O que fazer |
|---|---|---|
| InsightFace (detector do LatentSync) | Modelos treinados com os dados dele: só pesquisa, sem fins comerciais, mesmo os baixados pela biblioteca [oficial] | Troque o detector por MediaPipe ou DWPose, ou licencie |
| Wav2Lip | Pessoal, pesquisa ou não comercial; comercial só sob contato [oficial] | Não use em trabalho pago |
| CodeFormer | Licença S-Lab 1.0: uso e redistribuição não comerciais [oficial] | Não use em trabalho pago |
| LivePortrait | MIT, mas manda remover e trocar os modelos do InsightFace para uso comercial [oficial] | Troque o detector |
| GFPGAN | Apache-2.0 "exceto componentes de terceiros"; a licença NVIDIA StyleGAN2 incluída limita a uso não comercial [oficial] | Trate como não comercial até esclarecer |
| HunyuanVideo-Avatar | Território exclui UE, Reino Unido e Coreia do Sul (o Brasil está dentro); proíbe usar a saída para melhorar outro modelo de IA; acima de 100 milhões de usuários mensais pede licença da Tencent [oficial] | Cuidado ao distribuir fora do território |
| LTX-2 e Dub-It | Grátis só abaixo de US$ 10 milhões de receita anual; acima, licença paga, com multa do dobro do valor por uso sem licença; proíbe uso em produto que concorra com a Lightricks [oficial] | Confira a receita de quem usa |
| LatentSync (pesos) | Etiqueta `openrail++`; o cartão do modelo não traz o texto da licença | Não verificamos o texto |
| MuseTalk | MIT; o README pede cumprir também a licença do detector S3FD [oficial] | Não conferimos a licença do S3FD |
| TBDub | Apache-2.0 no código e nos pesos, segundo o README (github.com/TaoLiveAIGC/TBDub) e o Hugging Face (`TaoLiveAIGC/TBDub`) [oficial]; usa MediaPipe (Apache-2.0) | Não conferimos a licença dos pesos auxiliares que o README manda baixar (codificador de áudio) |
| X-Dub, InfiniteTalk, LongCat 1.5 | Apache-2.0, Apache-2.0 e MIT [oficial] | Confira os pesos auxiliares |

O repositório do TBDub tem pouco tempo de vida (criado em 02/09/2026): não há validação independente nem histórico de uso.
