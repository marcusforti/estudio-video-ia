# Portão de licença

Rode este portão antes de baixar pesos ou alugar máquina. Os dados abaixo foram lidos em 01/11/2026 nos READMEs, cartões e arquivos de licença de cada modelo [oficial]. Licença muda: reabra a página do modelo antes de usar e guarde a data em que leu.

## Regra

- Trabalho pago, peça entregue a cliente, anúncio ou conteúdo que gera receita conta como uso comercial.
- Pesos não comerciais não servem para uso comercial sem verificar a licença atual e, se preciso, falar com advogado. Isto vale para tudo marcado como "restrito" abaixo.
- Ensaio e uso interno não dispensam o consentimento do dono da voz (portão 1).
- Este arquivo relata o que as fontes dizem. Não é parecer jurídico.

## Pesos permissivos (clonam e falam português)

| Modelo | Licença dos pesos | Observações |
|---|---|---|
| Qwen3-TTS (Base 0,6B e 1,7B, jan/2026) | Apache-2.0 | 10 idiomas, português incluído |
| VoxCPM2 (abr/2026) | Apache-2.0 (pesos e código) | 30 idiomas, português incluído; o README diz "livre para uso comercial" |
| MOSS-TTS e MOSS-TTS-v1.5 | Apache-2.0 | licença do código não encontrada |
| Chatterbox Multilingual V3 e pacote pt-BR | MIT | marca d'água PerTh embutida em toda saída |

Nenhum comparativo cego independente em pt-BR foi encontrado para estes quatro. As medições em português que existem são dos próprios autores. [sem medição]

## Restritos (clonam e falam português)

| Modelo | Licença dos pesos | O que ela diz |
|---|---|---|
| OmniVoice | CC-BY-NC (código Apache-2.0) | não comercial, por causa dos dados de treino |
| F5-TTS | CC-BY-NC (código MIT) | não comercial; o português só existe em ajuste comunitário, também CC-BY-NC |
| XTTS-v2 | CPML | só uso não comercial, e o texto cobre também o áudio gerado |
| Voxtral TTS | CC BY-NC 4.0 | uso comercial só pela API do fabricante |
| Higgs Audio v3 | Boson Research and Non-Commercial License | produção, serviço hospedado e revenda pedem licença comercial à parte |
| Fish Audio Drama 3 | Fish Audio Community License v1.0 | comercial grátis só abaixo de US$ 500 mil de faturamento anual; exige atribuição "Built with Fish Audio"; proíbe imitar pessoa identificável sem consentimento e remover marca d'água |
| Fish Audio S2-Pro | Fish Audio Research License | uso comercial exige licença à parte |

## Fora da lista (sem português ou sem clonagem aberta)

IndexTTS-2.5 (licença própria da bilibili, sem português), GPT-SoVITS, CosyVoice 3, OpenVoice V2 (sem português nativo), Dia e Orpheus (inglês), Kokoro-82M e Supertonic 2 (português, mas sem clonagem).

Conversão de voz: RVC e Applio são MIT. Seed-VC é GPL-3.0 e foi arquivado pelo autor em 21/11/2025.

## Pontos de atenção

- O texto da CC BY-NC 4.0 fala em "Licensed Material" e "Adapted Material". As fontes que lemos não dizem se o áudio gerado por pesos CC-BY-NC é "Adapted Material". O XTTS-v2 e a licença da bilibili dizem expressamente que cobrem a saída. O Fish diz que o usuário é dono da saída "na medida em que a lei permitir". Na dúvida, trate a peça paga como uso comercial.
- O app VoiceStudio (debpalash, https://github.com/debpalash/VoiceStudio) é AGPL-3.0; o pacote `omnivoice` é Apache-2.0. Para uma receita pública, chame o pacote direto e não copie código do app. [fornecedor]
- Segundo a documentação do VoiceStudio, o tokenizer que o OmniVoice usa tem termos próprios (Boson e Meta Llama 3), com atribuição "Built with...". Não conferimos na fonte. [fornecedor]
- Não remova marca d'água nem metadados de proveniência: a ElevenLabs e o Fish proíbem.

## Fontes

- OmniVoice (README, licença dos pesos): https://huggingface.co/k2-fsa/OmniVoice/raw/main/README.md
- Qwen3-TTS: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base
- VoxCPM2: https://github.com/OpenBMB/VoxCPM e https://huggingface.co/openbmb/VoxCPM2
- MOSS-TTS: https://huggingface.co/OpenMOSS-Team/MOSS-TTS
- Chatterbox: https://github.com/resemble-ai/chatterbox e https://huggingface.co/ResembleAI/Chatterbox-Multilingual-pt-br
- F5-TTS: https://github.com/SWivid/F5-TTS
- XTTS-v2 (CPML): https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt
- Voxtral TTS: https://huggingface.co/mistralai/Voxtral-4B-TTS-2603
- Higgs Audio v3: https://huggingface.co/bosonai/higgs-audio-v3-tts-4b
- Fish Audio (licença): https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE
- IndexTTS (licença): https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE
- Texto legal da CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/legalcode
- RVC: https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- Seed-VC: https://github.com/Plachtaa/seed-vc
