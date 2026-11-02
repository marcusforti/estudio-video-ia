# Armadilhas: sintoma, causa e solução

Selos: `[testado]` = vivido em produção na Vast em outubro de 2026 (alguns limites vêm de anotações de projeto sem log guardado); `[oficial]` = da documentação do fornecedor.

## Cobrança e plataforma

| Sintoma | Causa | Solução |
|---|---|---|
| A cobrança continua com a máquina parada [oficial] | Vast cobra armazenamento enquanto a instância existe; RunPod cobra o disco de volume parado; DigitalOcean cobra a máquina desligada | Destruir. Guarde o que importa fora (bucket, `vastai cloud copy`) |
| Retomar não acha GPU [oficial] | Na Vast o restart entra em `SCHEDULING` e pode esperar sem prazo; na RunPod pode voltar com zero GPUs | Não dependa de parar e retomar; recrie a partir do pacote |
| Chave nova não entra [oficial] | A chave só vale para máquinas criadas depois de cadastrada | Cadastre antes de criar |
| Porta mudou [oficial] | Na RunPod as portas TCP podem mudar ao parar e retomar | Releia IP e porta a cada início |
| Saldo zerou [oficial] | A Vast para as instâncias; o disco segue cobrando; sem cartão salvo, destrói máquinas e dados após a carência | Mantenha saldo; acompanhe |
| Máquina interruptível parou [oficial] | Alguém deu lance maior | Só use para trabalho que retoma do último pedaço |

## Aluguel e acesso

| Sintoma | Causa | Solução |
|---|---|---|
| Oferta não sobe ("loading", "GPU error"); três placas de consumo baratas nunca ligaram [testado] | Host ou imagem com problema | Alugue 2 ou 3, fique com a primeira que ligar, destrua as outras; `verified=true reliability>0.98`; espera limitada (60 x 15 s) |
| Duas de três tentativas falharam ao subir [testado] | Provável: o script lia a máquina por ID e quebrava (`IndexError`) quando ela não aparecia na lista | Leia a lista inteira; trate "sumiu" como falha |
| O `ssh` cai num tmux e o `scp` estranha [testado] | Provável: a Vast abre tmux sozinha no SSH | `ssh -tt ... 'touch ~/.no_auto_tmux; exit'` uma vez |
| O processo morre ao fechar o SSH [testado] | SIGHUP e entrada padrão herdados | `setsid nohup cmd > log 2>&1 < /dev/null &` e `ssh -n` |
| `pkill -f "texto"` derruba a sessão [testado] | O padrão casa com o próprio comando remoto | Mate por PID; no treino, pelos PIDs de `nvidia-smi --query-compute-apps=pid --format=csv` |
| Instância de outra sessão na lista [testado] | Várias sessões usam a mesma conta | Destrua só o seu ID; avise o usuário |

## Transferência

| Sintoma | Causa | Solução |
|---|---|---|
| Upload grande cai perto do fim [testado] | Conexão direta instável | Retome com `tail -c +N arq \| ssh ... 'cat >> arq'` e confira o md5; empacote pouco e baixe os insumos na máquina |
| Download grande cai [testado] | O IP direto cai | Baixe pelo host proxy do painel (`sshN.vast.ai`) |
| Caminho com espaço ou acento quebra no Linux [testado] | `concat.txt` com caminho do Windows; nome com emoji ou `\|` quebra o `gdown` | `cygpath -m`; `python -X utf8`; nomes simples |
| `rsync` não existe no Windows [oficial] | A RunPod diz que exige Linux ou WSL | Use WSL ou `scp` |

## Ambiente na máquina

| Sintoma | Causa | Solução |
|---|---|---|
| Chrome do render não abre; `browser ensure` trava [testado] | Imagem mínima sem bibliotecas; falta `unzip` | Instale a lista de bibliotecas de `references/vast-comandos.md`, seção 7 |
| Emoji vira quadrado [testado] | Faltam fontes | `fonts-noto-color-emoji fonts-dejavu-core`; copie as fontes que a peça usa |
| Vídeo H.264 na página não toca [testado] | O Chromium baixado não decodifica H.264 (provável) | Instale o Google Chrome (.deb) |
| `npm i -g` quebra em máquina com GPU [testado] | O onnxruntime tenta instalar CUDA | `ONNXRUNTIME_NODE_INSTALL_CUDA=skip` |
| Render único com 24 ou mais workers empaca [testado] | Contenção | Pedaços de 8 a 30 s, 4 a 8 workers em cada, vários pedaços em paralelo, `ffmpeg -f concat -c copy` |
| Pedaços falham quando subo muitos [testado, anotação] | Limite de processos do contêiner: `pids.max` 1792 numa oferta, ~450 threads por pedaço | No máximo 3 pedaços ali; leia `/sys/fs/cgroup/pids.max`; em outras ofertas rodamos 8 e 9 |
| ffmpeg sem libx264 na imagem PyTorch [testado, anotação] | O ffmpeg do conda vem primeiro no PATH | `export PATH=/usr/bin:$PATH` ou `apt install ffmpeg` |
| `import wave` quebra [testado] | Um `chunk.py` local sombreia o módulo da biblioteca padrão | Renomeie o arquivo |
| A ferramenta mudou e quebrou [testado] | O `npx` pega a última versão | Fixe: `npx --yes NOME@VERSAO` |
| Dependência de modelo quebra [testado] | MuseTalk: mmcv, mmpose e `chumpy`; InfiniteTalk: `from inspect import ArgSpec`; `huggingface-cli` foi substituído por `hf`; `brotli` velho | Versões fixas; `pip install --no-build-isolation chumpy`; `hf download`; `pip install -U brotli` |
| Disco estoura [testado] | Camada de vídeo com alfa de mais de 30 min passa de 30 GB (anotação); caches de modelo | Componha lendo `-f concat`; rode `conda clean -a` e apague `~/.cache/huggingface/hub` ao fim de cada lote |
| O render no PC cai [testado] | pouca RAM; Chrome do usuário aberto | VM; no máximo 2 coisas pesadas por vez |
