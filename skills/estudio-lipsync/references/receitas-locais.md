# Receitas de modelos abertos numa A100 alugada

Selo `[testado]` = comando usado numa A100 de 80 GB alugada na Vast em outubro de 2026. Não reexecutamos nenhum deles ao escrever este material: nomes de arquivo e versões podem ter mudado, então confira o README de cada repositório. Para alugar, usar e destruir a máquina, siga a skill `estudio-gpu`. Passe a licença pelo portão de `consentimento-e-licenca.md` antes de qualquer uso comercial.

Convenções: `base.mp4` é o vídeo-base em 25 fps, sem áudio, 0,5 s mais longo que a fala; `voz.wav` é mono, 16 kHz, com 0,5 s de silêncio no fim (o `preparar_teste.py` gera os dois). Um ambiente conda por modelo, Python 3.10, com versões fixas. Antes de tudo: `apt-get install -y ffmpeg git` e `export PATH=/usr/bin:$PATH`, porque o ffmpeg do conda vem sem `libx264`. Use `export OMP_NUM_THREADS=4`.

## TBDub Student (o que escolhemos depois do teste de pior plano) [testado]

Ambiente com torch 2.9.0 e CUDA 12.8. Só Linux. Cerca de 28 GB de VRAM por processo: no máximo 2 ao mesmo tempo numa A100 de 80 GB.

```bash
git clone https://github.com/TaoLiveAIGC/TBDub && cd TBDub
hf download TaoLiveAIGC/TBDub config.json null_prompt_emb.pt tbdub_student.safetensors tbdub_teacher.safetensors --local-dir checkpoints
hf download KlingTeam/X-Dub Wan2.2_VAE.safetensors --local-dir checkpoints
hf download facebook/hubert-large-ll60k config.json preprocessor_config.json pytorch_model.bin --local-dir checkpoints/hubert-large-ll60k
# baixe também o face_landmarker.task do MediaPipe para checkpoints/ (o README indica a origem)
python inference.py --video base.mp4 --audio voz.wav --inference-mode student --num-student-steps 2 --sigma-shift 1.0 --motion-from-latents --seed 42 --output-dir saida
```

O modo Teacher (30 passos) não rodou por falta de memória e não repetimos com um único processo na placa:

```bash
python inference.py --video base.mp4 --audio voz.wav --inference-mode teacher --ref-cfg-scale 2.0 --audio-cfg-scale 6.0 --num-inference-steps 30 --seed 42 --output-dir saida_teacher
```

Lote em blocos [testado]:

- Um bloco por trecho de fala, de 25 a 55 s. Monte a base de cada bloco alternando os clipes-base de câmera fixa (cerca de 10 s cada), para a sequência não se repetir, até cobrir a duração do áudio mais 0,5 s (`ffmpeg -f concat -safe 0 -i lista.txt -c copy base.mp4`).
- No máximo 2 processos em paralelo (`ThreadPoolExecutor(2)`), saída `ok`, `ja` (já existia) ou `FALHOU` por bloco, para a rodada poder ser repetida sem refazer o que já saiu.
- Dispare com `setsid nohup python3 lote.py > lote.log 2>&1 < /dev/null &` e confira `nvidia-smi` e `df -h` entre lotes.
- Ao final, baixe só as saídas, não os pesos, limpe o disco (`conda clean -a`, `~/.cache/huggingface/hub`) e destrua a máquina.

## LatentSync 1.6 [testado]

Ambiente conda `ls`, Python 3.10. 18 GB de VRAM. Aqui: 23 a 27 s de vídeo em 9 a 14 min. Em trabalho pago, troque o detector InsightFace (veja a licença).

```bash
git clone https://github.com/bytedance/LatentSync && cd LatentSync && pip install -r requirements.txt
hf download ByteDance/LatentSync-1.6 whisper/tiny.pt --local-dir checkpoints
hf download ByteDance/LatentSync-1.6 latentsync_unet.pt --local-dir checkpoints
python -m scripts.inference --unet_config_path configs/unet/stage2_512.yaml --inference_ckpt_path checkpoints/latentsync_unet.pt --inference_steps 20 --guidance_scale 1.5 --enable_deepcache --video_path base.mp4 --audio_path voz.wav --video_out_path saida.mp4
```

Duas caras no quadro dão "Face not detected". RTX 50 falha por causa do PyTorch 2.5.1 fixado. No Windows há relato de falha de compilação (MSVC).

## MuseTalk 1.5 [testado, um teste]

Ambiente conda `mt`, Python 3.10, torch 2.0.1 com CUDA 11.8. A instalação deu atrito: as versões de mmcv, mmdet e mmpose têm de ser exatamente estas, e o `chumpy` só instala sem isolamento de build.

```bash
git clone https://github.com/TMElyralab/MuseTalk && cd MuseTalk && pip install -r requirements.txt
pip install -U openmim && mim install mmengine "mmcv==2.0.1" "mmdet==3.1.0" "mmpose==1.1.0"
pip install --no-build-isolation chumpy
bash download_weights.sh        # mais pesos extras por hf download ou gdown, conforme o README
# configs/inference/job.yaml:  task_0: {video_path: base.mp4, audio_path: voz.wav, bbox_shift: 0}
python -m scripts.inference --inference_config configs/inference/job.yaml --result_dir saida --unet_model_path models/musetalkV15/unet.pth --unet_config models/musetalkV15/musetalk.json --version v15
```

## InfiniteTalk, foto + áudio [testado]

Uma foto e um áudio viram um vídeo novo (cabeça e corpo regenerados). Resolução 480p com 8 passos e a LoRA FusionX; aqui, 26 s de vídeo em 64 min com a GPU dividida com outro treino. A cor deriva depois de ~1 min e o modelo foi treinado sobretudo em inglês e chinês.

```bash
export HF_HUB_ENABLE_HF_TRANSFER=1
git clone https://github.com/MeiGen-AI/InfiniteTalk && cd InfiniteTalk
hf download Wan-AI/Wan2.1-I2V-14B-480P --local-dir W/Wan2.1-I2V-14B-480P
hf download MeiGen-AI/InfiniteTalk --include "single/*" --local-dir W/InfiniteTalk
hf download TencentGameMate/chinese-wav2vec2-base --local-dir W/chinese-wav2vec2-base
# a LoRA FusionX de 8 passos vem de outro repositório: veja o README do InfiniteTalk
sed -i 's/^from inspect import ArgSpec/# from inspect import ArgSpec/' wan/multitalk.py     # conserto para Python novo
python generate_infinitetalk.py --ckpt_dir W/Wan2.1-I2V-14B-480P --wav2vec_dir W/chinese-wav2vec2-base \
  --infinitetalk_dir W/InfiniteTalk/single/infinitetalk.safetensors --size infinitetalk-480 --sample_steps 8 \
  --lora_dir W/fusionx/FusionX_LoRa/Wan2.1_I2V_14B_FusionX_LoRA.safetensors --lora_scale 1.0 --mode streaming --motion_frame 9 \
  --sample_shift 2 --sample_text_guide_scale 1.0 --sample_audio_guide_scale 2.0 --input_json job.json --save_file saida
# job.json: {"prompt": "uma pessoa falando", "cond_video": "foto.png", "cond_audio": {"person1": "voz.wav"}}
```

Menos memória: `--num_persistent_param_in_dit 0`. Mais velocidade: `--use_teacache --teacache_thresh 0.2`. O InfiniteTalk não teve veredito nosso de qualidade [sem medição]; as imagens de rosto geradas por IA que usamos como entrada foram reprovadas.
