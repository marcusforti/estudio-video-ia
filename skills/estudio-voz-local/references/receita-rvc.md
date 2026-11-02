# Receita: conversão de voz (RVC e Applio)

Use só se a entrada for uma fala humana já gravada que você quer trocar de timbre, ou se já tem um TTS bom de pronúncia e quer aproximar o timbre. O RVC não lê texto e herda ritmo, sotaque e defeitos da entrada. Licença: RVC e Applio são MIT. Os dados de treino têm de ser da voz de quem autorizou (portão 1).

Parte destas notas vem de anotação de memória, sem log para conferir. Onde for assim, está marcado [sem medição].

## Dados de treino

- RVC pede 10 min ou mais de fala limpa do alvo; o autor recomenda. [fornecedor]
- Rodamos com 16 a 32 min de aulas do próprio autor, em trechos FLAC. [testado]
- Para cortar: meça o piso de ruído e o nível de fala de cada fonte. O limiar de fala que usamos ficou entre 10 e 13 dB abaixo do nível RMS da fala de cada aula, e o ganho por fonte para nivelar ficou entre -2,1 e +0,6 dB. [testado]
- Filtre por locutor (semelhança ECAPA contra a voz do alvo) e por fundo. Descartamos trechos com fundo alto e trechos com outra voz (semelhança 0,33). [testado]
- Aula com música contínua por baixo (piso de -36 dB) foi descartada como fonte. [sem medição]

## Treino

- Applio, na T4 do Colab grátis, com 20, 40 e 80 épocas. Quarenta épocas foram 4.280 passos e 80 foram 8.560. [testado]
- Cerca de 62 s por época com lote 8: anotação de memória. [sem medição]
- Na A100 alugada, 150 épocas (5.700 passos) com cerca de 16 min de dados limpos. O tempo não foi registrado.
- O `--save-every-weights` não gerou o modelo pequeno. Extraímos do `G_*.pth` com `rvc.train.process.extract_model.extract_model`. [sem medição]

## Inferência

- A entrada é uma fala pronta (TTS ou gravação). Ao passar saída de TTS pelo RVC, ajuste de tom 0. [sem medição]
- O microfone de estúdio do autor soava cerca de 4 semitons mais agudo que o das aulas, por isso o tom importa quando as fontes diferem. [sem medição]
- A saída do modelo veio a 40 kHz. Para outros usos, reamostre.

## O que mediu e o que ouvimos

| Áudio | Nota ECAPA (1 = mesma voz) |
|---|---|
| voz genérica de catálogo | 0,334 |
| a mesma voz, depois do RVC treinado com a voz do autor (40 épocas) | 0,656 |
| OmniVoice sem RVC (amostra do microfone de estúdio) | 0,663 |
| OmniVoice com RVC de 40 épocas | 0,723 |
| trechos reais do autor | 0,675 e 0,741 |

- O RVC trocou o timbre da voz de catálogo, e a nota foi de 0,334 para 0,656. A nota mede timbre, não ritmo nem entonação, que continuam os da entrada.
- Empilhar RVC sobre o OmniVoice subiu a nota (0,663 para 0,723). Ao ouvido, a diferença foi pequena (anotação de memória). [sem medição]
- A régua tem ruído de uns 0,03: ela deu 0,675 e 0,741 para dois trechos reais da mesma pessoa. Veja `avaliacao.md`.
- Um estudo independente com voz infantil em pt-BR (STIL 2026, UFMT, https://aclanthology.org/2026.stil-1.29/) viu o RVC amplificar a artificialidade de fala sintética de TTS e melhorar quando a entrada era voz humana. [independente]

Conclusão: com o TTS de 2026, gaste primeiro na amostra e na prova cega. Deixe o RVC para quando houver uma leitura humana de guia. [praticante]
