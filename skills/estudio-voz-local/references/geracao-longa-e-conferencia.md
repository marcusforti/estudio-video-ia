# Geração longa, conferência e pronúncia

## Regras da geração em blocos

1. Um arquivo por bloco, e se o arquivo existe, pula. Para refazer um bloco, apague só o arquivo dele.
2. Quebre o texto por frase. Aqui usamos blocos de até 260 caracteres e 0,3 s de pausa entre eles. [testado] Os modelos têm janelas de geração: o F5-TTS aceita 30 s por geração (referência mais saída), o Dia acelera acima de 20 s e o Chatterbox Turbo fica instável depois de 25 a 30 s. [oficial]
3. Guarde um manifesto com o SHA-256 da amostra e a configuração (amostra, passos, velocidade). Recuse mudança silenciosa no meio da geração.
4. Separe síntese, alinhamento e mistura: um modelo pesado por vez na memória.
5. Registre a hora de cada bloco, para ter tempo medido.
6. Gere uma prévia curta (cerca de 35 s) e mostre ao dono da voz antes do resto.
7. Em máquina alugada, destrua a máquina num `trap` e baixe tudo antes (`gpu-alugada.md`).

## Esqueleto com retomada

`sintetizar(texto, destino)` é a sua chamada ao modelo (uma das receitas).

```python
import hashlib, json, pathlib, time

def sha256(caminho):
    return hashlib.sha256(pathlib.Path(caminho).read_bytes()).hexdigest()

def gerar_roteiro(blocos, pasta, sintetizar, config):
    pasta = pathlib.Path(pasta)
    pasta.mkdir(exist_ok=True)
    manifesto = pasta / "manifesto.json"
    atual = {"config": config, "amostra_sha256": sha256(config["amostra"])}
    if manifesto.exists():
        if json.loads(manifesto.read_text(encoding="utf-8")) != atual:
            raise SystemExit("A configuração mudou. Use outra pasta ou apague o manifesto de propósito.")
    else:
        manifesto.write_text(json.dumps(atual, indent=1), encoding="utf-8")
    for b in blocos:                                  # b = {"id": "b01", "texto": "..."}
        destino = pasta / f"{b['id']}.wav"
        if destino.exists() and destino.stat().st_size > 10_000:
            continue                                  # retomada: pula o que já existe
        t0 = time.time()
        sintetizar(b["texto"], destino)
        print(f"{time.strftime('%H:%M:%S')} {b['id']} {time.time() - t0:.1f}s", flush=True)
```

## Conferência por transcrição

Depois de gerar, transcreva cada bloco e compare com o texto do roteiro. Whisper `small` na CPU serve de conferência; `large-v3` é melhor. [testado]

```python
import difflib, re, unicodedata

def palavras(texto):
    sem_acento = "".join(c for c in unicodedata.normalize("NFD", texto.lower())
                         if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", sem_acento)

def casamento(roteiro, ouvido):
    a, b = palavras(roteiro), palavras(ouvido)
    iguais = sum(m.size for m in difflib.SequenceMatcher(None, a, b).get_matching_blocks())
    return iguais / max(len(a), len(b), 1)
```

A transcrição, no script que usamos:

```python
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")

def ouvir(wav, prompt=None):
    trechos, _ = asr.transcribe(wav, language="pt", word_timestamps=True, initial_prompt=prompt,
                                vad_filter=False, condition_on_previous_text=False)
    return " ".join(t.text for t in trechos)
```

Regra de aceite [testado]:

- Passa se `casamento(roteiro, ouvir(wav, prompt=roteiro))` for 0,88 ou mais.
- Abaixo disso, repita sem `prompt`: o prompt pode esconder o erro. Se ainda falhar, pare e revise o bloco.
- Numa narração de 18 blocos, 17 ficaram entre 0,96 e 1,00. Um deu 0,52 com o prompt e 0,96 sem. Outro deu 0,00 com o prompt e 0,882 sem.
- O Whisper escreve números por extenso ("cento e dez"), então o roteiro precisa ter o número por extenso para o casamento bater.
- Confira também o arquivo FINAL, o que vai ser entregue, e não só os blocos.

A função `casamento` foi executada com textos de teste. O trecho do `faster_whisper` é o do nosso script e não foi reexecutado ao montar esta referência.

## Dicionário de pronúncia

Escreva como se fala: acento nos nomes, números por extenso, frases curtas, pontuação de fala. O OmniVoice admite no paper tratamento de números "não otimizado". [oficial] A biblioteca `num2words` tem `lang="pt_BR"` para número, ordinal, ano e moeda. [oficial, não testamos]

```python
import re

def aplicar_pronuncia(texto, dicionario):
    for palavra, fala in dicionario.items():
        texto = re.sub(rf"\b{re.escape(palavra)}\b", fala, texto)
    return texto

PRONUNCIA = {"CRM": "cê érre ême", "110": "cento e dez", "kkkk": "rárárárá"}
```

Aplique antes de chamar o modelo. Depois de cada ajuste, gere só o bloco e confira por transcrição. A palavra que o modelo lê errado muda de modelo para modelo: monte o dicionário com as palavras difíceis do seu projeto.

## Pós-processo

Cortar o silêncio das pontas de cada bloco e deixar uma folga curta:

```bash
ffmpeg -v error -y -i bloco.wav -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,adelay=40|40,apad=pad_dur=0.06" -ar 48000 -ac 1 bloco_limpo.wav
```

Nível da voz de cada bloco, sempre com `aresample` depois (o `loudnorm` sobreamostra e o áudio "engasga" se ficar a 96 kHz ou mais):

```bash
ffmpeg -v error -y -i bloco_limpo.wav -af "loudnorm=I=-18:TP=-3:LRA=7,aresample=48000" -ar 48000 bloco_nivelado.wav
```

Vício no começo da fala (palavra que o modelo inventou): corte com `-ss` e suavize com `-af afade=t=in:d=0.03`. A causa quase sempre é a amostra (`SKILL.md`, seção Erros comuns).

Esticar a voz abaixo de 0,74x (`atempo`) soou robótico; abandonamos. Mantenha a voz a 1,0x e ajuste o vídeo ao áudio, ou gere mais devagar com `speed` menor. [testado]

Não medimos nem tratamos sibilância. O filtro `deesser` do ffmpeg é candidato e não foi testado. [sem medição]

## Verificação final

```bash
ffmpeg -v error -i final.wav -f null -                  # decodifica tudo: sem saída = sem erro
ffmpeg -hide_banner -i final.wav -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | python -I -c "import sys,re,json; d=json.loads(re.search(r'\{.*\}', sys.stdin.read(), re.S).group(0)); print('LUFS', d['input_i'], 'pico dBTP', d['input_tp']); assert float(d['input_tp']) < -0.5"
sha256sum final.wav amostra.wav                         # guarde junto da amostra, do texto e da configuração
```

Depois transcreva o arquivo final e confira o texto. Só então envie, e só ao dono da voz.
