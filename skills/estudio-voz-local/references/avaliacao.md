# Avaliação: o ouvido decide, a métrica ajuda

Ordem de peso, do maior para o menor [testado]:

1. **Prova cega de ouvido**, feita pelo dono da voz.
2. **Transcrição** do áudio gerado, para pegar palavra trocada (`geracao-longa-e-conferencia.md`).
3. **Similaridade de locutor** (ECAPA), só como apoio.
4. **Perda do treino**: diz que o ajuste está acontecendo, não que a voz ficou boa.

## 1. Prova cega

- Use a mesma frase em todas as tomadas, com a palavra difícil do projeto.
- Inclua uma gravação real da pessoa (`REAL`) como referência.
- Nivele todas as tomadas para o mesmo loudness (cerca de -18 LUFS) antes de comparar: a mais alta tende a parecer melhor. [praticante]
- Embaralhe as letras e guarde o gabarito num arquivo separado, que não vai ao dono da voz.
- Anote o veredito por escrito, com a data. Aqui parte dos vereditos ficou só em memória, e isso dificultou reconstituir os resultados depois.
- Mostre um trecho curto ao dono antes de gerar uma peça longa.

Montador (copia as tomadas com letras, cria a página e grava o gabarito à parte):

```python
import json, pathlib, random, shutil

def montar_prova(real, candidatas, pasta_prova, pasta_gabarito, semente=None):
    """candidatas: {"modelo e amostra": "caminho.wav"}. A pasta da prova vai ao dono; o gabarito fica com você."""
    assert len(candidatas) <= 10, "no máximo 10 tomadas (letras A a J)"
    prova = pathlib.Path(pasta_prova)
    prova.mkdir(parents=True, exist_ok=True)
    ordem = list(candidatas.items())
    random.Random(semente).shuffle(ordem)
    letras = "ABCDEFGHIJ"[:len(ordem)]
    gabarito = {}
    for letra, (nome, caminho) in zip(letras, ordem):
        shutil.copy(caminho, prova / f"{letra}.wav")
        gabarito[letra] = nome
    shutil.copy(real, prova / "REAL.wav")
    itens = "".join(f"<p><b>{n}</b><br><audio controls src='{n}.wav'></audio></p>" for n in ["REAL", *letras])
    (prova / "index.html").write_text(
        f"<meta charset='utf-8'><h1>Qual soa mais como a voz real?</h1>{itens}", encoding="utf-8")
    gab = pathlib.Path(pasta_gabarito)
    gab.mkdir(parents=True, exist_ok=True)
    (gab / "gabarito.json").write_text(json.dumps(gabarito, ensure_ascii=False, indent=1), encoding="utf-8")
    return gabarito
```

## 2. Similaridade de locutor (ECAPA)

Mede o cosseno entre o "retrato de voz" (embedding) do áudio gerado e o de um trecho real que ficou **fora** da amostra e do treino. A chamada abaixo é a do cartão oficial do SpeechBrain; o nosso script não ficou arquivado. [oficial]

```python
from speechbrain.inference.speaker import SpeakerRecognition
verificacao = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                              savedir="modelo_ecapa")
nota, _ = verificacao.verify_files("real_fora_do_treino.wav", "gerado.wav")
```

O modelo foi treinado com áudio de 16 kHz mono e converte sozinho. A equipe do SpeechBrain não garante desempenho em outros conjuntos de dados. [oficial]

Notas que medimos com a voz do próprio autor (1 = mesma voz) [testado]:

| Áudio | Nota |
|---|---|
| voz de outra pessoa (catálogo) | 0,334 |
| MiniMax, clone v3 | 0,644 e 0,680 |
| OmniVoice, amostra do microfone de estúdio | 0,663 |
| OmniVoice, amostra de aula | 0,698 |
| OmniVoice com RVC de 40 épocas | 0,723 |
| a própria amostra aprovada | 0,687 |
| trechos reais do autor | 0,675 e 0,741 |

O que isso ensina:

- Voz real contra voz real varia de 0,675 a 0,741. A régua tem ruído de uns 0,03, e diferenças de 0,03 a 0,05 não separam vozes. Calibre sempre com "real contra real" da mesma pessoa.
- Acima de 0,66 já se está na faixa do próprio autor. Por isso a régua não serviu para escolher entre OmniVoice, MiniMax com treino e clonagem profissional paga.
- A nota deu vantagem à amostra de aula (0,698 contra 0,663) e o ouvido do autor preferiu a do microfone de estúdio. A régua foi calibrada no tipo de áudio do treino (aulas gravadas em vídeo) e tem esse viés.
- Números de artigos usam outro modelo (WavLM) e não se comparam com os do ECAPA. Só compare dentro da mesma régua.

## 3. O que o ouvido decidiu aqui [testado]

- Entre seis amostras na mesma OmniVoice, venceu a de cerca de 18 s do microfone de estúdio, a -18 LUFS. Mesmo assim o autor a achou ainda abaixo da voz real.
- No ajuste fino, o checkpoint de 750 passos ganhou do de 500, que tinha a menor perda.
- Na nossa comparação de outubro de 2026, a clonagem profissional paga de um provedor foi a única que o autor aceitou como igual à própria voz. O clone local, o clone rápido pago e o de outro provedor pago foram reprovados ao lado dela.
- Para a mesma voz profissional, as versões v2 e v3 do modelo foram reprovadas em outubro de 2026 e só a v4 serviu.
