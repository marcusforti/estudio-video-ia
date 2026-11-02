# Receitas: modelos com pesos permissivos

Qwen3-TTS, VoxCPM2, MOSS-TTS e Chatterbox clonam, falam português e têm pesos permissivos (ver `licencas.md`). **Não rodamos nenhum deles aqui.** O que segue vem dos READMEs e cartões oficiais, lidos em 01/11/2026 [oficial], e não foi executado por nós [sem medição]. O nome das funções muda entre versões: confira o README no dia.

Nenhum comparativo cego independente em pt-BR foi encontrado. Antes de escolher um deles para trabalho pago, faça o teste curto: a mesma amostra, a mesma frase de teste, uma candidata por modelo, e prova cega com o dono da voz (`avaliacao.md`). Anote o tempo por segundo de fala e a memória de GPU usada: não temos esses números.

Preparar a amostra com `scripts/preparar_amostra.py` vale para todos. O que muda é a duração e se o modelo pede o texto dela:

| Modelo | Amostra (documentação) | Pede o texto da amostra? |
|---|---|---|
| Qwen3-TTS | 3 s | sim (`ref_text`); sem ele use `x_vector_only_mode=True`, com qualidade menor |
| VoxCPM2 | não informada (referência de 16 kHz, saída de 48 kHz) | sim, exato, no modo "ultimate cloning" |
| MOSS-TTS | não informada no cartão | não aparece no exemplo |
| Chatterbox | 10 s ou mais, no mesmo idioma do texto | não |

## Qwen3-TTS (Apache-2.0)

```bash
pip install -U qwen-tts
```

```python
import torch, soundfile as sf
from qwen_tts import Qwen3TTSModel

modelo = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",      # ou Qwen/Qwen3-TTS-12Hz-0.6B-Base
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)
wavs, taxa = modelo.generate_voice_clone(
    text=texto,
    language="Portuguese",                # o README usa "English"; troquei por Portuguese [sem medição]
    ref_audio="amostra.wav",
    ref_text=texto_amostra,
)
sf.write("saida.wav", wavs[0], taxa)
```

Para reutilizar a mesma voz em várias falas, o README manda montar o prompt uma vez com `create_voice_clone_prompt` e passá-lo em `voice_clone_prompt`. O modelo Base não tem controle de tom ou emoção por instrução. Memória de GPU não informada (1,93 bilhão de parâmetros em BF16).

## VoxCPM2 (Apache-2.0)

```bash
pip install voxcpm
```

```python
import soundfile as sf
from voxcpm import VoxCPM

modelo = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
wav = modelo.generate(
    text=texto,
    prompt_wav_path="amostra.wav",
    prompt_text=texto_amostra,
    reference_wav_path="amostra.wav",
)
sf.write("saida.wav", wav, modelo.tts_model.sample_rate)
```

O fabricante informa cerca de 8 GB de VRAM e fator de tempo real de cerca de 0,30 numa RTX 4090 (0,13 com Nano-vLLM) [fornecedor]. Ajuste fino com LoRA pede de 5 a 10 min de áudio [fornecedor]. Limitações declaradas: o clone controlável varia entre execuções e entradas muito longas ou muito expressivas podem ficar instáveis.

## MOSS-TTS (Apache-2.0)

```bash
git clone https://github.com/OpenMOSS/MOSS-TTS.git
cd MOSS-TTS
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e .
```

```python
import torch, torchaudio
from transformers import AutoModel, AutoProcessor

device = "cuda:0"
processor = AutoProcessor.from_pretrained("OpenMOSS-Team/MOSS-TTS", trust_remote_code=True)
processor.audio_tokenizer = processor.audio_tokenizer.to(device)
modelo = AutoModel.from_pretrained("OpenMOSS-Team/MOSS-TTS", trust_remote_code=True,
                                   torch_dtype=torch.bfloat16).to(device)

conversas = [[processor.build_user_message(text=texto, reference=["amostra.wav"])]]
with torch.no_grad():
    lote = processor(conversas, mode="generation")
    saidas = modelo.generate(input_ids=lote["input_ids"].to(device),
                             attention_mask=lote["attention_mask"].to(device),
                             max_new_tokens=4096)
    audio = processor.decode(saidas)[0].audio_codes_list[0]
    torchaudio.save("saida.wav", audio.unsqueeze(0), processor.model_config.sampling_rate)
```

`trust_remote_code=True` executa código do repositório do modelo: leia-o antes. O cartão não informa memória de GPU. Só pelo tamanho dos pesos (8,49 bilhões de parâmetros em BF16, cerca de 17 GB) a estimativa é uma placa de 24 GB [sem medição]. Existe também uma variante local de 1,7 bilhão.

## Chatterbox Multilingual V3 (MIT)

```bash
pip install chatterbox-tts
```

```python
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
wav = modelo.generate(texto, language_id="pt", audio_prompt_path="amostra.wav")
ta.save("saida.wav", wav, modelo.sr)
```

- Use um clipe no mesmo idioma do texto: com outro idioma o sotaque do clipe vaza. Para reduzir, `cfg_weight=0`. Padrões do fabricante: `exaggeration=0.5` e `cfg_weight=0.5`.
- Toda saída leva a marca d'água PerTh (resiste a MP3 e a edição comum). Não a remova.
- Existe um pacote só de pt-BR, `ResembleAI/Chatterbox-Multilingual-pt-br` (ajuste de uma língua só, MIT). Siga o cartão dele para carregar.
- Issues abertas no repositório: instabilidade do Turbo depois de 25 a 30 s (#543), falha com texto muito curto (#548) e falta de suporte nativo a fp16/bf16 (#564).

## Fontes

- https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/README.md
- https://github.com/OpenBMB/VoxCPM e https://huggingface.co/openbmb/VoxCPM2
- https://huggingface.co/OpenMOSS-Team/MOSS-TTS
- https://github.com/resemble-ai/chatterbox e https://huggingface.co/ResembleAI/chatterbox
- https://resemble.ai/learn/models/chatterbox-multilingual
