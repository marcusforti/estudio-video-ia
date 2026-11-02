# Vast.ai: comandos do ciclo completo

Selos: `[testado]` = usado em produção na Vast em outubro de 2026. `[sem medição: rodado só contra simulação]` = rodado contra um `vastai` falso com JSON sintético, sem alugar nada; o formato do JSON segue o script de produção. `[oficial]` = só da documentação oficial, não rodado por nós. Nos comandos, `<skill>` é a pasta da skill estudio-gpu.

Variáveis da sessão (nunca em arquivo versionado, nunca dentro da máquina alugada):

```bash
export VAST_API_KEY="..."
IP=...; PORTA=...; ID=...
CHAVE="$HOME/.ssh/estudio_gpu"
K="-i $CHAVE -o StrictHostKeyChecking=no -o ConnectTimeout=30"
```

`StrictHostKeyChecking=no` aceita qualquer chave de máquina, inclusive trocada. Usamos porque o IP muda a cada aluguel; `accept-new` aceita só na primeira conexão e recusa se a chave mudar. Com dado de terceiro, prefira nuvem segura [praticante].

## 0. Preparar [oficial]

```bash
pip install vastai
vastai set api-key "$VAST_API_KEY"
vastai show user                 # saldo; a Vast é pré-paga
vastai show instances --raw      # o que já está ligado, inclusive de outra sessão [testado]
```

## 1. Chave SSH [oficial]

```bash
ssh-keygen -t ed25519 -f "$CHAVE" -C estudio-gpu
vastai create ssh-key "$CHAVE.pub"
```

A chave só vale para máquinas criadas depois do cadastro.

## 2. Buscar ofertas

```bash
# GPU de 80 GB (lip sync, treino) [testado]
vastai search offers 'gpu_name in [A100_PCIE,A100_SXM4] num_gpus=1 reliability>0.98 disk_space>=100 inet_down>500 rentable=true' -o dph --raw

# CPU de muitos núcleos (render) [oficial]: montada pelo help da CLI; não guardamos a consulta exata das sessões
vastai search offers 'cpu_cores_effective>=64 reliability>0.98 verified=true disk_space>=80 inet_down>=500 rentable=true' -o dph --raw
```

Campos úteis: `dph` (preço por hora), `reliability`, `verified`, `datacenter`, `direct_port_count`, `inet_down`, `inet_down_cost`, `disk_space`, `cuda_vers`. Por padrão a busca já filtra `verified=true rentable=true`. `datacenter=True` restringe ao nível datacenter (use para dado de terceiro).

## 3. Criar [testado]

```bash
vastai create instance OFERTA_ID --image pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel --disk 100 --ssh --direct --raw
# render em CPU:  --image ubuntu:22.04 --disk 80
```

No JSON devolvido, `new_contract` é o ID da instância. `--cancel-unavail` faz o comando falhar em vez de criar máquina parada [oficial]. Para ofertas que não sobem, alugue 2 ou 3 e destrua as que sobrarem: `echo y | vastai destroy instance ID`.

## 4. Esperar subir [sem medição: rodado só contra simulação]

```bash
espera() {  # uso: espera ID  -> imprime "IP PORTA" quando a máquina estiver pronta
  for i in $(seq 1 60); do
    saida=$(vastai show instances --raw 2>/dev/null | python3 -c '
import json, sys
alvo = sys.argv[1]
for m in json.load(sys.stdin):
    if str(m.get("id")) == alvo and m.get("actual_status") == "running":
        porta = (m.get("ports") or {}).get("22/tcp")
        if porta:
            print(m.get("public_ipaddr"), porta[0]["HostPort"])
' "$1")
    [ -n "$saida" ] && { echo "$saida"; return 0; }
    sleep 15
  done
  return 1
}
read -r IP PORTA < <(espera "$ID") || { echo "não subiu"; }
```

Se não subir em 15 min, destrua e tente outra oferta. A documentação também oferece `vastai ssh-url ID` [oficial].

## 5. Primeiro acesso [testado]

```bash
ssh -tt $K -p $PORTA root@$IP 'touch ~/.no_auto_tmux; exit'   # desliga o tmux automático
ssh $K -p $PORTA root@$IP 'nvidia-smi; df -h /root'           # confira placa e disco
```

SSH direto (`--direct`) é mais rápido e estável que o proxy. Se o IP direto cair num download grande, use o host proxy `sshN.vast.ai` do painel (N é um número).

## 6. Subir o projeto [testado]

```bash
tar czf job.tgz projeto/
scp $K -P $PORTA job.tgz root@$IP:/root/
ssh $K -p $PORTA root@$IP 'mkdir -p /root/job && tar xzf /root/job.tgz -C /root/job'
```

Insumos pesados: baixe dentro da máquina (`gdown ID -O nome`, `yt-dlp`, `hf download`). Alternativas [oficial]: `rsync -avz --partial -e "ssh -p $PORTA" pasta/ root@$IP:/root/job/pasta/` (no Windows, via WSL), `vastai copy local:./dados/ ID:/root/job/dados/` e `vastai cloud copy` (S3, Drive, Backblaze, funciona com a máquina parada).

## 7. Preparar a máquina [testado]

Render de HTML em CPU (Chrome headless): `apt-get update && apt-get install -y ffmpeg unzip curl ca-certificates fonts-noto-color-emoji fonts-dejavu-core libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2`. Em máquina com GPU, `export ONNXRUNTIME_NODE_INSTALL_CUDA=skip` antes do `npm`. Fixe a versão das ferramentas (`npx --yes NOME@VERSAO`). Vídeo H.264 dentro da página pede Google Chrome (.deb) no lugar do Chromium baixado.

Modelos de IA: um ambiente conda por modelo, com versões fixas. `apt-get install -y ffmpeg git` e `export PATH=/usr/bin:$PATH` (o ffmpeg do conda vem sem libx264). `export OMP_NUM_THREADS=4`. Pesos com `hf download` (o comando `huggingface-cli` foi substituído por `hf`).

## 8. Rodar sem depender do SSH [testado]

```bash
ssh -n $K -p $PORTA root@$IP 'cd /root/job && setsid nohup bash run.sh > run.log 2>&1 < /dev/null &'
ssh $K -p $PORTA root@$IP 'tail -n 5 /root/job/run.log'
```

Escreva o `run.sh` idempotente: `[ -s "$saida" ] && continue` pula o que já existe, então reexecutar retoma. Em lote na GPU, use no máximo 2 processos por vez em modelos de ~28 GB e confira `nvidia-smi` e `df -h` entre lotes. Alguns renderizadores cancelam se o processo pai sair: mantenha uma sessão aberta durante o render.

## 9. Baixar e conferir [testado]

```bash
scp $K -P $PORTA root@$IP:/root/job/saida/final.mp4 .
ssh $K -p $PORTA root@$IP 'md5sum /root/job/saida/final.mp4'
python <skill>/scripts/conferir_download.py final.mp4 --md5 "HASH_DA_MAQUINA" --duracao SEGUNDOS --midia
```

Sem o script: `md5sum final.mp4` (Git Bash, WSL, Linux, macOS) ou `Get-FileHash -Algorithm MD5 final.mp4` (PowerShell). Download interrompido: `tail -c +N arquivo_local | ssh ... 'cat >> /caminho/arquivo'`, com N igual ao tamanho já enviado mais 1, e confira o md5 de novo.

## 10. Destruir e provar [testado]

```bash
echo y | vastai destroy instance "$ID"
vastai show instances --raw | python <skill>/scripts/lista_vazia.py --meu-id "$ID"
```

## 11. Destruir mesmo se o script quebrar [sem medição: rodado só contra simulação]

```bash
ID=""
fim() {
  [ -n "$ID" ] && echo y | vastai destroy instance "$ID"
  echo "DESTRUÍDA ${ID:-nenhuma}; restantes: $(vastai show instances --raw | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))')"
}
trap fim EXIT
```

Defina `ID` assim que o `create` devolver o `new_contract`.

## 12. Tipos de aluguel e armazenamento [oficial]

- Sob demanda: não é interrompida e guarda os dados parada. Interruptível (`--bid_price`, "50%+ mais barata"): para sem aviso quando alguém dá lance maior; só para trabalho que retoma. Reservada: até 50% de desconto.
- Parar libera a GPU e mantém o disco cobrando; retomar pode esperar sem prazo (`SCHEDULING`). Destruir apaga tudo.
- Volume local persiste depois de destruir a instância, mas fica preso à máquina física.
- Saldo zerado: a Vast para as instâncias, o disco segue cobrando e, sem cartão salvo, destrói máquinas e dados após a carência.

## 13. Editor na máquina [oficial]

Bloco no `~/.ssh/config`: `Host gpu`, `HostName IP`, `Port PORTA`, `User root`, `IdentityFile ~/.ssh/estudio_gpu`, e `LocalForward 127.0.0.1:8188 127.0.0.1:8188` para abrir uma interface web no `localhost`. O VS Code Remote-SSH conecta e instala um servidor na máquina. Releia IP e porta a cada início.

## Fontes

Páginas vistas em 01/11/2026.

- [Vast: CLI, primeiros passos](https://docs.vast.ai/cli/get-started): instalar, buscar, criar, destruir, `vastai copy`.
- [Vast: search offers](https://docs.vast.ai/cli/reference/search-offers.md): campos e sintaxe da busca.
- [Vast: create instance](https://docs.vast.ai/cli/reference/create-instance.md): flags do aluguel.
- [Vast: start instance](https://docs.vast.ai/cli/reference/start-instance.md): retomar e o estado `SCHEDULING`.
- [Vast: gerir instâncias](https://docs.vast.ai/guides/instances/manage-instances.md): parar, retomar, destruir.
- [Vast: SSH](https://docs.vast.ai/guides/instances/connect/ssh.md): chaves, SSH direto e proxy.
- [Vast: tipos de instância](https://docs.vast.ai/guides/instances/choosing/instance-types.md): sob demanda, reservada, interruptível.
- [Vast: tipos de armazenamento](https://docs.vast.ai/guides/instances/storage/types.md): volume local preso à máquina.
- [Vast: movimento de dados](https://docs.vast.ai/guides/instances/storage/data-movement.md): `vastai copy` e `vastai cloud copy`.
- [Vast: cobrança](https://docs.vast.ai/guides/reference/billing.md): pré-pago e saldo zerado.
- [Vast: FAQ de tipos de aluguel](https://docs.vast.ai/guides/reference/faq/rental-types.md): o que acontece com a interruptível.
- [rsync](https://download.samba.org/pub/rsync/rsync.1): manual de `--partial`.
- [VS Code Remote-SSH](https://code.visualstudio.com/docs/remote/ssh): editor remoto.
