# Licenças e consentimento

Este capítulo responde a duas perguntas antes de você apertar o botão: posso usar esse modelo neste trabalho? Posso mexer na voz ou no rosto dessa pessoa? Nada aqui é parecer jurídico. É o que as fontes dizem, e o que fazemos por cautela.

## Resumo em 30 segundos

- Voz e rosto de outra pessoa: só com autorização por escrito, específica e destacada. Modelo aberto não tem trava, então o termo assinado é a única trava.
- "Open source" não quer dizer uso comercial. Confira a licença dos pesos, das dependências e, em alguns casos, do áudio gerado.
- Clonar a própria voz é o caso mais simples. Mesmo assim, a plataforma pode pedir rótulo de IA.
- Para trabalho comercial, comece por modelos de pesos permissivos. Os não comerciais ficam para teste.
- Trate gravações, modelos de voz e rostos como dado sensível: pouca gente com acesso, prazo para apagar, nada em máquina de desconhecido sem criptografia.

## As três perguntas de licença

Faça nesta ordem, para cada modelo:

| Pergunta | Onde olhar | Armadilha comum |
|---|---|---|
| Os pesos permitem uso comercial? | Arquivo LICENSE do modelo, card no Hugging Face | Código MIT com pesos não comerciais |
| As dependências permitem? | Detector de rosto, restaurador, modelo de áudio | O modelo é livre, mas o detector de rosto dele é só para pesquisa |
| A saída herda alguma restrição? | Texto da licença, seção de outputs | Há licença que cobre o áudio gerado, e há as que não dizem nada |

Se a licença não responde, trate como não comercial até confirmar com o autor.

## Voz: o que pode e o que não pode

O quadro completo, com link de cada licença, está em [Voz local](05-voz-local.md). O resumo em 01/11/2026:

| Grupo | Modelos |
|---|---|
| Clonagem, português e pesos permissivos | Qwen3-TTS, VoxCPM2, MOSS-TTS (Apache-2.0), Chatterbox (MIT) |
| Pesos não comerciais | OmniVoice (CC-BY-NC), F5-TTS (CC-BY-NC), Voxtral TTS (CC BY-NC), Higgs Audio v3, XTTS-v2 |
| Com teto de faturamento | Fish Audio Drama 3: grátis para uso comercial só abaixo de US$ 500 mil por ano [oficial] |
| Conversão de voz | RVC e Applio (MIT) |

Nenhuma fonte que lemos diz se o áudio gerado por um modelo CC-BY-NC herda a restrição. Quando a dúvida importa, troque de modelo ou pergunte ao autor.

## Lip sync: o que costuma pegar

O quadro completo está em [Lip sync](07-lip-sync.md). Os alertas que mais pesam:

| Modelo ou peça | Alerta |
|---|---|
| LatentSync | O detector de rosto usa InsightFace, cujos modelos são só para pesquisa não comercial |
| Wav2Lip, CodeFormer | Não comerciais |
| LivePortrait | Exige trocar o InsightFace para uso comercial |
| GFPGAN | Traz cláusula não comercial nas licenças de terceiros |
| HunyuanVideo-Avatar | Licença exclui União Europeia, Reino Unido e Coreia do Sul |
| LTX-2 | Grátis só abaixo de US$ 10 milhões de receita anual |

Cada alerta vem da licença do repositório ou do cartão do modelo [oficial]; links em [Lip sync](07-lip-sync.md).

## Motion: licenças das ferramentas

Detalhes em [Motion](08-motion.md).

| Ferramenta | Licença | Atenção |
|---|---|---|
| HyperFrames | Apache-2.0 | O app Studio exige conta HeyGen |
| Three.js, Revideo | MIT | Sem pegadinha |
| GSAP | Licença própria, gratuita para uso comercial desde 30/04/2025 | Não é licença aprovada pela OSI |
| Remotion | Licença própria | Grátis para equipes de até 3 pessoas; acima disso, plano pago |
| Lottie | Players MIT | A licença dos assets tem cláusula própria |

## Referências de outras pessoas

A coleção usada pela [/escolhermotion](09-escolhermotion.md) tem licença MIT, mas o README diz que cada vídeo e prompt pertence ao criador. Por isso este site só aponta para ela. Use a mecânica como inspiração, troque conteúdo e marca, e registre autor e link no `CREDITOS.md` do projeto.

Skills de terceiros não foram copiadas para este repositório. Elas são citadas com link para a origem.

## Consentimento: o que o termo precisa cobrir

Há um modelo pronto em [modelos/AUTORIZACAO-VOZ-E-IMAGEM.md](../modelos/AUTORIZACAO-VOZ-E-IMAGEM.md). É ponto de partida, não substitui advogado.

| Item | Por quê |
|---|---|
| Quem é a pessoa, com documento | Identifica o titular |
| Finalidade e escopo | Quais conteúdos, quais canais, se é comercial |
| Prazo | Autorização sem prazo gera discussão |
| Direito de revogar | O direito da personalidade não se transfere |
| Guarda e eliminação | Onde ficam as gravações e o modelo de voz, e quando são apagados |
| Proibição de ceder a terceiros | O modelo não passa para outro projeto |
| Rotulagem | Quando a plataforma exigir |

Provedores e licenças convergem nessa direção. A ElevenLabs proíbe clonar voz de pessoa viva sem consentimento explícito e, na clonagem profissional, aceita só a própria voz, com verificação [oficial]. A Microsoft exige gravação de consentimento antes do treino [oficial]. A licença do OmniVoice proíbe clonagem não autorizada e fraude [oficial].

Em modelo aberto, rodando na sua máquina, nenhum desses filtros existe. A responsabilidade fica com você.

## O que as fontes dizem no Brasil

Não encontramos lei brasileira específica sobre clonagem de voz em vigor em 01/11/2026. O quadro é feito de peças:

| Fonte | O que diz |
|---|---|
| [Constituição, art. 5º, X e XXVIII, a](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm) | Protege imagem e a "reprodução da imagem e voz humanas" |
| [Código Civil, arts. 11, 12 e 20](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) | Direitos da personalidade intransmissíveis; salvo autorização, pode proibir o uso comercial da imagem e da palavra |
| [LGPD, arts. 5º, II, 11 e 52](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) | Dado biométrico é sensível; consentimento específico e destacado; multa de até 2% do faturamento |
| [Nota Técnica 17/2025 da ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/participacao-social/outras-acoes/ts-01-2025-nota-tecnica-17-de-abertura.pdf/@@display-file/file) | Usa o critério de identificação única e não menciona voz |
| [Lei 15.123/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15123.htm) | Aumenta a pena da violência psicológica contra a mulher feita com IA que altere imagem ou som da vítima |
| [PL 2338/2023](https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2487262) | Marco da IA: na Câmara, aguardando parecer do relator, com última movimentação em 27/10/2026 |

Se a voz gravada conta como dado biométrico ainda é pergunta em aberto. Nossa conduta é tratar gravações e modelos de voz como dado sensível.

## Rótulo de IA nas plataformas

| Plataforma | Regra |
|---|---|
| [YouTube](https://support.google.com/youtube/answer/14328491) | Declare conteúdo realista gerado ou alterado por IA. Clonar a própria voz para narrar está isento. Voz de terceiro autorizado não aparece na isenção, então o rótulo é o caminho cauteloso [oficial] |
| [Meta](https://www.meta.com/en-gb/help/artificial-intelligence/1783222608822690/) | Pode exigir rótulo para áudio realista. O exemplo citado é um Reel narrado com voz de IA realista [oficial] |
| [TikTok](https://www.tiktok.com/community-guidelines/en/integrity-authenticity) | Rotule conteúdo gerado por IA ou muito editado com cenas ou pessoas realistas. A política não trata voz sintética de forma específica [oficial] |

## Dados sensíveis em máquina alugada

Em mercado de GPU, quem hospeda a máquina é um terceiro, e a segurança varia de host para host. Para gravação ou rosto de outra pessoa, prefira nuvem segura, criptografe os dados em repouso e destrua a instância ao terminar. O Colab lista "creating deepfakes" entre os usos proibidos na FAQ e não define o termo [oficial]: isso pesa em lip sync de terceiros. Veja [GPU como local](06-gpu-como-local.md).

## Créditos das imagens deste site

Todas via Wikimedia Commons, reduzidas para a web e exibidas em preto e branco.

| Imagem | Autor | Licença |
|---|---|---|
| [Moviola Flatbed Editor M-TT-16](https://commons.wikimedia.org/wiki/File:Moviola_Flatbed_Editor_M-TT-16.jpg) | Lucistian | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| [Clapperboard, O2 film, September 2008](https://commons.wikimedia.org/wiki/File:Clapperboard,_O2_film,_September_2008.jpg) | Mattbr | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) |
| [Decoupage1](https://commons.wikimedia.org/wiki/File:Decoupage1.jpg) | Irakli Metreveli | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) |
| [2015 04 08 009 Analogfilme](https://commons.wikimedia.org/wiki/File:2015_04_08_009_Analogfilme.jpg) | Friedrich Haag | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| [EYE Film Institute, Film storage](https://commons.wikimedia.org/wiki/File:EYE_Film_Institute_Netherland_-_Library_and_Collections_building_-_Film_storage_-_Overamstel,_Amsterdam_-_2.JPG) | Hansmuller | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| [DGB (large feed reels), Cinema projector](https://commons.wikimedia.org/wiki/File:DGB_(large_feed_reels)_-_Cinema_projector.webm) | La Fonderie | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/), trecho recortado e reencodado |

As versões reduzidas e em preto e branco são adaptações; as das imagens CC BY-SA 4.0 seguem a mesma licença.

Fontes Anton e Archivo sob SIL Open Font License.

## Links

- [Modelo de autorização de voz e imagem](../modelos/AUTORIZACAO-VOZ-E-IMAGEM.md): termo para adaptar com seu advogado.
- [Política de uso da ElevenLabs](https://elevenlabs.io/use-policy): regra de consentimento para voz.
- [Microsoft Custom Voice](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice): exemplo de gravação de consentimento.
- [Colab: FAQ](https://research.google.com/colaboratory/faq.html): limites e usos proibidos.
- [Pesquisa completa](12-pesquisa-estado-da-arte.md): todas as fontes.
