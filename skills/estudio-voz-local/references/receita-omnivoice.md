# Receita: OmniVoice (clonagem sem treino, CPU ou GPU)

Licença dos pesos: CC-BY-NC. Passe pelo portão de licença (`licencas.md`) antes de usar em trabalho pago.

Onde rodamos o OmniVoice [testado]: CPU de notebook modesto, sem GPU compatível, Windows, pelo app VoiceStudio (debpalash, AGPL-3.0, https://github.com/debpalash/VoiceStudio); GPU T4 do Colab; GPU A100 80 GB alugada, em fp16, com o pacote `omnivoice` direto. As medições de qualidade deste arquivo são da voz do próprio autor. Voz de terceiro: só nuvem segura (skill estudio-gpu), nunca o Colab. A receita abaixo vem dos scripts reais que usamos, sem os caminhos do PC.

## 1. GPU alugada (ou qualquer máquina com CUDA)

```bash
pip install -q -U brotli faster-whisper soundfile
pip install -q torch==2.6.0 torchaudio==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
git clone -q https://github.com/k2-fsa/OmniVoice.git && pip install -q -e OmniVoice
for r in eustlb/higgs-audio-v2-tokenizer k2-fsa/OmniVoice Qwen/Qwen3-0.6B Systran/faster-whisper-large-v3; do hf download $r; done
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 TOKENIZERS_PARALLELISM=false
```

Use `hf download` (o `huggingface-cli` sumiu). Se o `hf download` quebrar, atualize o `brotli`. Depois do download, `HF_HUB_OFFLINE=1`.

Gerar:

```python
import torch, soundfile as sf
from omnivoice import OmniVoice

modelo = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
texto_amostra = open("amostra.txt", encoding="utf-8").read().strip()
prompt = modelo.create_voice_clone_prompt(ref_audio="amostra.wav", ref_text=texto_amostra)
torch.manual_seed(7)   # antes de cada fala, para repetir a mesma tomada
audio = modelo.generate(text=texto, voice_clone_prompt=prompt, language="pt", num_step=16, speed=1.0)
sf.write("saida.wav", audio[0], 24000)
```

- O README oficial passa `ref_audio` e `ref_text` direto no `generate`; o `create_voice_clone_prompt` serve para reutilizar a voz em várias falas e tem `prompt.save`. [oficial]
- No script que rodamos, a saída era um tensor e gravávamos com `out[0].cpu().numpy().squeeze()`. Se o seu `audio[0]` vier como tensor, converta assim.

## 2. CPU (notebook, Windows)

Rodamos pelo app VoiceStudio, que usa float32. Com o pacote direto, o equivalente seria `device_map="cpu"` e `dtype=torch.float32`. [sem medição: não rodamos este código exato na CPU]

Regras que valeram [testado]:

- Arquivo de paginação fixo de 16.384 a 32.768 MB. O modelo aloca cerca de 8,5 GB virtuais; com 8 GB o Windows devolve o erro 1455.
- `torch.set_num_threads(4)` e `torch.set_num_interop_threads(1)` num notebook de 4 núcleos.
- Nunca defina `OMNIVOICE_CPU_DTYPE=bfloat16` em CPU sem AVX-512 BF16: ficou 10 vezes mais lento.
- Uma geração por vez, prioridade abaixo do normal, navegador fechado. A cada bloco: `torch.no_grad()`, apagar o tensor (`del`) e chamar `gc.collect()`.
- Tempo: de 19 a 74 s de CPU por segundo de fala a 16 passos.
- Se o driver da placa for antigo demais, o PyTorch avisa `NVIDIA driver ... too old`. Trate a máquina como só CPU.

## 3. Parâmetros

| Parâmetro | Valor que usamos | Observação |
|---|---|---|
| `num_step` | 16 | o padrão do fabricante é 32; 32 passos custou o dobro do tempo e não registramos veredito de ouvido entre os dois [sem medição] |
| `speed` | 1.0 | |
| `language` | `"pt"` | |
| amostra | 14,8 a 18 s | o fabricante recomenda 3 a 10 s [fornecedor]; o texto tem de bater palavra por palavra |

## 4. Ajuste fino (fine-tune)

Rodamos duas vezes com 12,5 min de aulas do próprio autor. Com tão pouco dado o modelo decora cedo, e o checkpoint escolhido tem de ser baixado antes de destruir a máquina.

1. Transcreva a fonte (24 kHz) com `faster-whisper large-v3` (`vad_filter`, `word_timestamps`, `beam_size=5`), guardando a probabilidade média por trecho.
2. Prepare os trechos: junte vizinhos (probabilidade de 0,6 ou mais, intervalo menor que 0,6 s, até 14 s), mantenha os de 2 a 15 s, corte com 0,1 s antes e 0,15 s depois, embaralhe com semente fixa, separe 15 trechos para avaliação e o resto para treino. Formato `jsonl`: `{id, audio_path, text, language_id}`.
3. Configure:

```bash
cd OmniVoice/examples
python - <<'P'
import json
c = json.load(open("config/train_config_finetune.json"))
c.update(steps=2000, save_steps=250, eval_steps=250, logging_steps=25, num_workers=2)
json.dump(c, open("config/voz.json", "w"), indent=1)
json.dump({"train": [{"manifest_path": ["/root/voz/tokens/train/data.lst"]}],
           "dev": [{"manifest_path": ["/root/voz/tokens/dev/data.lst"]}]}, open("config/voz_data.json", "w"))
P
```

4. Tokenize o áudio e treine:

```bash
for s in train dev; do
  python -m omnivoice.scripts.extract_audio_tokens --input_jsonl /root/voz/$s.jsonl \
    --tar_output_pattern "/root/voz/tokens/$s/audios/shard-%06d.tar" \
    --jsonl_output_pattern "/root/voz/tokens/$s/txts/shard-%06d.jsonl" \
    --tokenizer_path eustlb/higgs-audio-v2-tokenizer --nj_per_gpu 1 --shuffle True
done
export PYTHONPATH=/root/OmniVoice HF_HUB_OFFLINE=1
accelerate launch --gpu_ids 0 --num_processes 1 -m omnivoice.cli.train \
  --train_config config/voz.json --data_config config/voz_data.json --output_dir /root/voz/exp
```

5. Gere a partir do checkpoint: `OmniVoice.from_pretrained("/root/voz/exp/checkpoint-750", device_map="cuda:0", dtype=torch.float16)`. Use como amostra o trecho de avaliação mais longo com até 15 s. Quebre o texto em frases de até 260 caracteres, com 0,3 s de pausa entre blocos, e apare o silêncio das pontas (limiar 0,01, borda de 0,1 s).

Configuração efetiva do log: `init_from_checkpoint=k2-fsa/OmniVoice`, `llm_name_or_path=Qwen/Qwen3-0.6B`, 8 codebooks de áudio, `learning_rate=1e-05`, `mixed_precision=bf16`, `attn_implementation=flex_attention`, `batch_tokens=8192`, `use_lora=false`.

Medido [testado]: 0,66 a 0,78 s por passo (250 passos a cada 2 min 47 s na A100). A segunda rodada inteira (instalar, tokenizar, treinar até 775 passos e gerar 15 blocos de narração) levou cerca de 35 min e custou cerca de US$ 0,60; a primeira custou cerca de US$ 0,70. Com 12,5 min de dados são cerca de 4 passos por época, então 750 passos equivalem a umas 186 épocas. A perda de teste ficou mínima entre 250 e 500 passos e subiu depois (5,44 aos 1.000 na primeira rodada). No ouvido, o checkpoint de 750 passos ganhou do de 500.

Lições: salve a cada 250 passos e compare de ouvido; baixe o `checkpoint-N` escolhido antes do `destroy`; guarde a semente e a lista de trechos. O re-treino com os mesmos dados e a mesma semente não reproduziu as perdas (4,35, 4,54 e 4,86 contra 4,74, 4,68 e 4,87).
