# Formato da transcrição

O `cortar.py` precisa do tempo de início e de fim de cada palavra. Sem isso ele recusa o arquivo: cortar por segmento do Whisper pode ceifar o fim das palavras [testado].

## Formatos aceitos

**1. O do `transcrever.py`**

```json
{"language": "pt", "duration": 184.2,
 "words": [{"w": "Olá,", "s": 0.50, "e": 0.90, "p": 0.98}]}
```

`w` é o texto, `s` o início e `e` o fim, em segundos. `p` (confiança) é opcional.

**2. Segmentos com `words`** (Whisper em linha de comando com `--word_timestamps True`, faster-whisper e WhisperX):

```json
{"segments": [{"words": [{"word": " Olá,", "start": 0.5, "end": 0.9, "probability": 0.98}]}]}
```

Palavras sem `start` ou `end` são ignoradas. O WhisperX costuma deixar números e símbolos sem tempo: confira se a fala não perdeu trechos.

**3. Lista plana `words` com `type`** (formato do Scribe, da ElevenLabs):

```json
{"words": [{"text": "Olá,", "start": 0.5, "end": 0.9, "type": "word"},
           {"text": " ", "start": 0.9, "end": 0.91, "type": "spacing"}]}
```

Entradas com `type` diferente de `word` (espaços, risadas, ruídos) são ignoradas.

## Chaves que o script reconhece

| O quê | Chaves |
|---|---|
| texto | `w`, `word`, `text`, `palavra` |
| início | `s`, `start`, `inicio` |
| fim | `e`, `end`, `fim` |
| lista | `words` na raiz, `words` dentro de `segments`, ou uma lista simples na raiz |

Estado do teste: os três formatos foram lidos em arquivos de exemplo montados no formato descrito. Não foram testados com a saída real de cada ferramenta.

## Como obter

- Local, sem chave: `python <skill>/scripts/transcrever.py bruto.mp4 palavras.json`. Exige `faster-whisper` (opcional, MIT, SYSTRAN). Confirme com o dono do vídeo antes de instalar o pacote ou baixar o modelo; `large-v3-turbo` tem cerca de 1,5 GB. Em PC com pouca memória use `--modelo small` e feche o navegador.
- Outra ferramenta: exporte com tempo por palavra e passe o JSON direto.

## Revise antes de cortar

- Palavra com duração menor que 0,1 s e quatro letras ou mais costuma ser erro de reconhecimento (uma palavra trocada por outra de som parecido). O plano avisa.
- Frase repetida em sequência é alucinação sobre áudio ruim. O plano avisa; descarte o vídeo.
- Corrija a palavra errada direto no JSON e gere o plano de novo: o código muda e a aprovação anterior deixa de valer.
