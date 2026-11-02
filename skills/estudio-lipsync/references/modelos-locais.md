# Modelos abertos de lip sync: licença, VRAM, velocidade, manutenção

Estado de 01/11/2026. Selos: `[oficial]` = repositório ou ficha do modelo; `[fornecedor]` = número que os próprios autores publicam; `[independente]` = relato de terceiro (issue, blog); `[testado]` = rodamos numa A100 de 80 GB alugada em outubro de 2026; `[sem medição]` = não achamos. VRAM é a memória da placa de vídeo. Licenças: leitura de texto, não parecer jurídico (veja `consentimento-e-licenca.md`).

## Consertar a boca (vídeo + áudio novo)

| Modelo | Licença | VRAM | Velocidade | Manutenção | Limites conhecidos |
|---|---|---|---|---|---|
| MuseTalk 1.5 | MIT; pesos liberados para qualquer fim [oficial] | 4 GB em fp16, teste dos autores [fornecedor] | Mais de 30 fps numa V100; 8 s de vídeo em ~5 min na placa de 4 GB [fornecedor] | Último commit 26/09/2025; 177 issues abertas | Boca de 256 px; perde bigode e cor do lábio; tremor [oficial]; sucesso de 60,00% no benchmark publicado pelos autores de um modelo rival (X-Dub, https://arxiv.org/html/2512.25066v1) [fornecedor] |
| LatentSync 1.5 e 1.6 | Código Apache-2.0; pesos `openrail++`; o detector usa InsightFace (só pesquisa) [oficial] | 8 GB (1.5), 18 GB (1.6) [fornecedor] | Sem número oficial; aqui 23 a 27 s de vídeo em 9 a 14 min [testado] | Último commit 20/06/2025; 229 issues abertas; ainda muito baixado | Melhor de frente; duas caras dão "Face not detected"; falha em RTX 50 porque fixa PyTorch 2.5.1 com CUDA 12.1; sucesso de 59,77% no mesmo benchmark dos autores do modelo rival [fornecedor] |
| TBDub (Student e Teacher) | Apache-2.0, código e pesos [oficial] | ~28 GiB (27,95 Teacher, 27,93 Student); com `--cpu-offload` 19,49 e 15,01. RAM do computador chegou a ~22 GiB. Medido numa placa de 72 GB, "não é um teste em RTX 4090" [fornecedor]. Aqui ~28 GB por processo [testado] | 7,13 fps numa H20 (Student); 63 s para um clipe de 15 s numa placa de 72 GB, sem carga do modelo [fornecedor]. Aqui sem tempo por bloco | Criado em 02/09/2026, push de 12/09/2026, 40 estrelas; 1.876 downloads | Só Linux com GPU NVIDIA e Python 3.10; sem validação independente; Teacher não rodou aqui por falta de memória |
| X-Dub (versão pública, Wan2.2-5B) | Apache-2.0 [oficial] | ~21 GB [fornecedor] | ~60 s para 3 s de vídeo a 50 passos, no paper, GPU não informada [fornecedor] | Último commit 03/08/2026 | O modelo do paper é interno e mais forte; o público tem tremor ocasional, deriva de cor ou identidade, ~2% de quadros com ruído grave e é cerca de 2x mais lento; uma pessoa por vez; cabeça rápida atrapalha [oficial] |
| LTX-2.3 Dub-It (LoRA) | LTX-2 Community License: grátis abaixo de US$ 10 milhões de receita anual [oficial] | [sem medição] | [sem medição] | LoRA atualizada em 22/10/2026 | Exige vídeo de referência; opções `--quantization fp8-cast` e `--offload disk` para pouca RAM; exemplos em francês, russo, espanhol e alemão |
| Wav2Lip | Só pessoal, pesquisa ou não comercial [oficial] | [sem medição] | ~1 s para 3 s de vídeo, no paper dos autores do X-Dub [fornecedor] | README editado em 2025 | Boca de 96 px; evite em trabalho pago |

## Animar foto + áudio

| Modelo | Licença | VRAM | Velocidade | Manutenção | Limites conhecidos |
|---|---|---|---|---|---|
| InfiniteTalk | Apache-2.0; base Wan2.1 [oficial] | 480p roda em 24 GB; 720p estourou na decodificação de uma RTX 4090 [independente]. Windows com 32 GB de RAM: o app fp8 fecha sozinho [independente] | ~200 s numa RTX 4090 (480x832, 6 passos, duração do clipe não informada); 27 s de vídeo em ~20 min; 8 s em horas num relato [independente]. Aqui 26 s em 64 min com a GPU dividida [testado] | Código parado desde 25/08/2025; depois só README | Máximo de 40 s por rodada (1000 quadros); cor deriva depois de ~1 min; no vídeo para vídeo regenera cabeça, corpo e câmera; os lábios continuam mexendo depois do áudio acabar [independente] |
| LongCat-Video-Avatar 1.5 | MIT [oficial] | Oficial: não informada. Terceiro: 16 GB em INT8, 24 a 40 GB cheio [sem medição] | [sem medição] | Lançado em 21/05/2026; 3.391 downloads | Não testamos. Avaliação dos autores em chinês e inglês |
| Wan2.2-S2V-14B | Apache-2.0 [oficial] | 80 GB no comando oficial | [sem medição] | Código de 21/09/2026 | Modelo de 16 fps; codificador de áudio em inglês. Evite |
| HunyuanVideo-Avatar | Licença Tencent, com restrição territorial [oficial] | Mínimo 24 GB, "muito lento"; 96 GB recomendados | [sem medição] | Último commit 16/12/2025 | Evite |
| SadTalker | Apache-2.0 hoje [oficial] | [sem medição] | [sem medição] | Parado desde 10/10/2023 | Evite |

## Português

Nenhum modelo tem avaliação em português [sem medição]. O lip sync segue a acústica, então deve funcionar em algum nível, mas as vogais nasais do português do Brasil não aparecem em nenhum benchmark publicado. O que os autores mostram:

| Modelo | Codificador de áudio | Idiomas de exemplo ou avaliação |
|---|---|---|
| LatentSync, MuseTalk | Whisper tiny | MuseTalk cita chinês, inglês e japonês |
| X-Dub | Whisper large-v2 e Wav2Vec2 nos nós de ComfyUI | Inglês, mandarim, cantonês, japonês, russo, francês |
| TBDub | HuBERT large (o que baixamos) | Inglês, chinês, japonês, coreano, russo |
| LTX Dub-It | Não verificado | Francês, russo, espanhol, alemão |
| InfiniteTalk | wav2vec2 chinês | Treinado "principalmente em inglês e chinês"; os mantenedores dizem que funciona em outros e que não há plano de melhorar |
| LongCat 1.5 | Whisper large | Chinês e inglês |

Por inferência, e não por teste, codificadores de classe Whisper large tendem a ser mais robustos que um wav2vec2 de um só idioma [sem medição]. O teste de pior plano substitui essa dúvida por um resultado.

## Ecossistema

- InfiniteTalk: template de ComfyUI oficial, fluxos de Kijai, template de RunPod de terceiros e WanGP para pouca VRAM. LatentSync: nós de ComfyUI e pacote Cog da Replicate, sem Docker oficial. X-Dub: nós de ComfyUI (Linux). TBDub: Linux, sem nó de ComfyUI que tenhamos achado. LongCat 1.5: nós de ComfyUI da comunidade. Não achamos template de Vast específico para lip sync [sem medição].
- Em máquina alugada, prefira Ampere, Ada ou Hopper (A100, RTX 4090, L40S) a RTX 50 para o LatentSync.
