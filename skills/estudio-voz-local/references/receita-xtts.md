# Receita: XTTS-v2 (CPML, só uso não comercial)

Licença dos pesos: CPML. Só uso não comercial, e o texto da licença cobre também o áudio gerado. Passe pelo portão de licença (`licencas.md`) antes de qualquer trabalho pago. [oficial]

A empresa que criou o modelo encerrou as atividades (dezembro de 2023 segundo um estudo, início de 2024 segundo outra fonte). O pacote `coqui-tts` é mantido pelo fork da Idiap. [oficial]

Aqui rodamos só o clone sem treino (zero-shot) na CPU, com a voz do próprio autor. Ficou sem veredito e foi superado pelo OmniVoice. [testado]

## Instalar e gerar

```bash
pip install coqui-tts        # versão que usamos: 0.27.5
```

```python
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
tts.tts_to_file(text=texto, speaker_wav="referencia.wav", language="pt", file_path="saida.wav")
```

- Referência que usamos: 30 s, WAV mono a 22,05 kHz. O modelo pede cerca de 6 s. [fornecedor]
- 17 idiomas, português incluído. A saída vem a 24 kHz. [fornecedor]
- O modelo baixa na primeira execução (a pasta ocupa cerca de 1,8 GB).
- Um estudo independente com voz infantil em pt-BR (STIL 2026, UFMT, https://aclanthology.org/2026.stil-1.29/) relatou dias de ajuste de PyTorch, torchaudio e CUDA para instalar, e emoção atenuada na fala. [independente]
- Sem log de tempo da nossa execução. [sem medição]

Se o objetivo é trabalho pago, prefira os modelos de pesos permissivos (`receita-modelos-abertos.md`).
