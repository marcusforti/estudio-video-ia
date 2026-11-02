# GPU alugada como se fosse o seu PC: do aluguel à máquina destruída

Este capítulo ensina a alugar uma máquina com placa de vídeo (GPU) ou com muitos núcleos de processador, usá-la por SSH (acesso remoto por terminal) como se fosse o seu PC e devolvê-la sem deixar cobrança escondida. É para quem edita com agente de código (Claude Code, Codex) e esbarra em render demorado, lip sync ou treino de voz que o PC não aguenta. Preços em dólares, vistos em 01/11/2026.

## Resumo em 30 segundos

- Alugue quando o trabalho não cabe no PC. Render de cerca de 3 min de vídeo levava ~25 min aqui; numa VM (máquina virtual alugada) de 64 núcleos, renders parecidos saíram em 3 a 6 min [testado].
- Na nossa produção a Vast.ai é o caminho. O ciclo: confirmar o gasto, criar, entrar por SSH, subir um pacote pequeno, rodar sem depender do SSH, baixar, conferir o md5, destruir e ver a lista vazia.
- Parar não é destruir. Vast, RunPod e DigitalOcean seguem cobrando o disco da máquina parada [oficial].
- Trate voz e rosto como dado sensível. Para dado de terceiro, use nuvem segura (datacenter) e peça consentimento. Não use o Colab: a FAQ proíbe "creating deepfakes" sem definir o termo [oficial].
- Preço de GPU muda por oferta e por hora. A tabela abaixo é um retrato de 01/11/2026, não uma promessa.

## O ciclo em nove passos

Só termina quando a lista de instâncias volta vazia. Cada passo tem o comando na receita mais abaixo. A skill [estudio-gpu](../skills/estudio-gpu/SKILL.md) conduz o ciclo com confirmação de gasto e destruição conferida.

<!-- diagrama:gpu-ciclo -->

1. Confirmar o gasto: preço por hora, horas, disco e o teto aprovado pelo dono do vídeo.
2. Escolher e criar: GPU ou CPU, disco e imagem, só ofertas verificadas.
3. Entrar por SSH: chave, IP e porta lidos da CLI ou do painel, nunca guardados no repositório.
4. Subir o projeto: um pacote pequeno. O que é pesado você baixa dentro da máquina.
5. Rodar sem depender do SSH: `setsid nohup`, log em arquivo, etapas que retomam de onde pararam.
6. Baixar o resultado.
7. Conferir: md5 (impressão digital do arquivo) e duração.
8. Destruir a instância (a máquina alugada).
9. Provar: `vastai show instances` imprime `[]`.

## Quando alugar

| Situação | Decisão | Medido aqui |
|---|---|---|
| Render de motion com mais de ~2 min de vídeo | VM de CPU, 32 a 80 núcleos | cerca de 3 min de vídeo: ~25 min no PC, 3 a 6 min na VM [testado] |
| Lip sync, voz clonada, treino de voz, detecção de objetos | VM com GPU de 24 a 80 GB | O notebook não tem GPU compatível e não roda esses modelos [testado] |
| Transcrição curta (Whisper) | PC ou Colab grátis | Na T4 do Colab saiu bem mais rápido que no PC; relato de projeto, sem log guardado [praticante] |
| Rosto ou voz de terceiro | Nuvem segura. Nunca Colab nem host de mercado desconhecido | Seção Segurança |
| Trabalho de poucos segundos | Não vale alugar | Dez minutos de uma RTX 4090 custam de US$ 0,06 a 0,15 (preço por hora ÷ 6, RunPod a 0,34 e 0,89). O que pesa é preparação, tempo parado e disco [praticante] |

Qual placa serve a cada modelo de lip sync está em [Lip sync](07-lip-sync.md). Para render de HTML em pedaços, veja [Motion por código](08-motion.md).

## Onde alugar: preços vistos em 01/11/2026

| Serviço | Preço visto (US$ por hora) | Parado, o que cobra; notas |
|---|---|---|
| Vast.ai, mercado de máquinas de terceiros | Sem tabela: "o preço é do mercado" [oficial]. Nosso aluguel, em outubro de 2026: A100 80 GB a 1,23 e ~1,07; CPU de 64 núcleos de 0,27 a 0,54 [testado]. Agregadores: RTX 4090 de 0,59 a 0,80 [independente] | Disco cobra e a GPU volta ao mercado [oficial]. Pré-pago, cobrança por segundo. Nível interruptível é mais barato e para a máquina quando alguém dá lance maior [oficial] |
| RunPod Secure Cloud, datacenter | RTX 4090 0,89; RTX 5090 1,19; L40S 1,09; H100 PCIe 2,89 [oficial] | Disco de volume parado a US$ 0,20 por GB ao mês. Sem taxa de entrada e saída de dados. Contêiner [oficial] |
| RunPod Community Cloud | RTX 4090 0,34; RTX 5090 0,69; H100 PCIe 1,99 [oficial] | Fechada a novos hosts desde 24/02/2026; os existentes seguem [independente] |
| Lambda, VM de datacenter | H100 SXM de 3,99 a 4,29; sem placas de consumo [oficial] | Não há "parar", só terminar. Cobrança por minuto |
| Thunder Compute | A100 80 GB 1,09; L40 0,79 (comparativo do próprio site) [oficial] | Texto sobre máquina parada é ambíguo |
| Salad, PCs de terceiros | RTX 4090 de 0,16 a 0,44, por nível de prioridade [oficial] | Sem conceito de parar; pode ser interrompida |
| Modal, serverless | T4 0,59; A100 80 GB 2,50; H100 3,95 (preço por segundo × 3.600, conta nossa) [oficial] | Por segundo |
| Google Colab | Sem preço por hora. Pro US$ 9,99 ao mês (100 unidades), Pro+ US$ 49,99 (600). Uma T4 gasta ~1,19 unidade por hora, perto de US$ 0,12 [independente] | A página de planos exige login. Grátis: no máximo 12 h |
| Paperspace, DigitalOcean, TensorDock | Paperspace A5000 1,38 (página sem data); DigitalOcean L40S 1,57 [oficial] | DigitalOcean cobra a máquina desligada inteira. TensorDock: página de 24/07/2024, não confirmamos que opere |

Armazenamento parado também custa: 200 GB ficam em ~US$ 40 ao mês no disco de volume da RunPod e em ~US$ 14 num volume de rede (0,20 e 0,07 por GB; conta nossa).

## Receita: use a VM como se fosse o seu PC

Tudo abaixo foi o que fizemos em produção na Vast [testado], salvo onde o selo diz outra coisa. Chave, IP, porta e ID ficam em variáveis da sua sessão, nunca em arquivo do repositório.

```bash
export VAST_API_KEY="..."     # no seu terminal
IP=...; PORTA=...; ID=...     # lidos da CLI ou do painel
K="-i $HOME/.ssh/estudio_gpu -o StrictHostKeyChecking=no -o ConnectTimeout=30"
```

`StrictHostKeyChecking=no` aceita qualquer chave de máquina, inclusive trocada. Usamos porque o IP muda a cada aluguel; `accept-new` aceita só na primeira conexão e recusa se a chave mudar. Com dado de terceiro, prefira nuvem segura [praticante].

**0. Antes de tudo** [oficial]

```bash
pip install vastai
vastai set api-key "$VAST_API_KEY"
vastai show instances --raw     # o que já está ligado, inclusive de outra sessão
vastai show user                # saldo; a Vast é pré-paga
```

**1. Confirme o gasto.** Preço por hora × horas × 1,3 (folga) + disco. Exemplo: 1,10 × 2 × 1,3 = US$ 2,86. Mostre o número ao dono e só crie depois do OK.

**2. Escolha e crie.**

```bash
ssh-keygen -t ed25519 -f ~/.ssh/estudio_gpu -C estudio-gpu
vastai create ssh-key ~/.ssh/estudio_gpu.pub    # só vale para máquinas criadas depois [oficial]

# GPU de 80 GB (lip sync, treino): nossa consulta, sem o filtro de país que usávamos
vastai search offers 'gpu_name in [A100_PCIE,A100_SXM4] num_gpus=1 reliability>0.98 disk_space>=100 inet_down>500 rentable=true' -o dph --raw
# CPU de muitos núcleos (render). Não guardamos a consulta exata das sessões: esta foi montada pelo help da CLI [oficial]
vastai search offers 'cpu_cores_effective>=64 reliability>0.98 verified=true disk_space>=80 inet_down>=500 rentable=true' -o dph --raw

vastai create instance OFERTA_ID --image pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel --disk 100 --ssh --direct --raw
```

No JSON, `new_contract` é o ID da instância: guarde só ele. Para render em CPU usamos `--image ubuntu:22.04 --disk 80`. Oferta barata nem sempre sobe: alugue 2 ou 3, fique com a primeira que ligar e destrua as outras com `echo y | vastai destroy instance ID`. `--cancel-unavail` faz o comando falhar em vez de criar máquina parada [oficial].

**3. Espere subir e entre.** Repita a cada 15 s, até 60 vezes: `vastai show instances --raw` até `actual_status` ser `running` e existir a porta 22. A documentação oferece `vastai ssh-url ID` [oficial]. No primeiro acesso, desligue o tmux (a Vast costuma abrir esse terminal sozinha):

```bash
ssh -tt $K -p $PORTA root@$IP 'touch ~/.no_auto_tmux; exit'
```

SSH direto é mais rápido e estável que o proxy [oficial]. Se o IP direto cair num download grande, use o host proxy `sshN.vast.ai` do painel.

**4. Suba o projeto.** Um pacote pequeno; o pesado você baixa dentro da máquina (`gdown`, `yt-dlp`, `hf download`).

```bash
tar czf job.tgz projeto/
scp $K -P $PORTA job.tgz root@$IP:/root/
ssh $K -p $PORTA root@$IP 'mkdir -p /root/job && tar xzf /root/job.tgz -C /root/job && cd /root/job && bash setup.sh'
```

Para pastas grandes há `rsync -avz --partial -e "ssh -p $PORTA"`, que no Windows exige WSL [oficial]. Não testamos o `rsync` aqui.

**5. Rode sem morrer ao fechar o SSH.**

```bash
ssh -n $K -p $PORTA root@$IP 'cd /root/job && setsid nohup bash run.sh > run.log 2>&1 < /dev/null &'
ssh $K -p $PORTA root@$IP 'tail -n 5 /root/job/run.log'
```

`setsid` solta o processo da sessão, `nohup` ignora o fechamento do terminal, o redirecionamento solta a saída e `ssh -n` não prende a entrada. Escreva o `run.sh` para retomar: pule o que já existe (`[ -s "$saida" ] && continue`) e reexecutar não refaz nada.

**6 e 7. Baixe e confira.**

```bash
scp $K -P $PORTA root@$IP:/root/job/saida/final.mp4 .
ssh $K -p $PORTA root@$IP 'md5sum /root/job/saida/final.mp4'
md5sum final.mp4        # Git Bash ou WSL. No PowerShell: Get-FileHash -Algorithm MD5 final.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4
```

Os dois hashes têm de ser iguais e a duração, a esperada. Confira também o conteúdo: quadros e voz.

**8 e 9. Destrua e prove.**

```bash
echo y | vastai destroy instance $ID
vastai show instances --raw     # tem de imprimir []
```

Se aparecer instância que não é sua (outra sessão na mesma conta), não mexa e avise o dono. No script que aluga, `trap 'echo y | vastai destroy instance $ID' EXIT` destrói a máquina mesmo se o script quebrar.

**Editor e terminal na VM (opcional).** Um bloco `Host` no `~/.ssh/config` (`HostName`, `Port`, `User root`, `IdentityFile`) deixa o VS Code Remote-SSH abrir a pasta da máquina; `LocalForward` traz interfaces web para o `localhost` [oficial]. Releia IP e porta a cada início. Não testamos o VS Code Remote-SSH aqui.

## Render em CPU ou em GPU

| Trabalho | Roda em | Por quê e medida |
|---|---|---|
| Render de HTML para vídeo (HyperFrames, que transforma uma página HTML em vídeo) | CPU de 32 a 80 núcleos | A GPU não acelera e atrapalha a instalação: o onnxruntime tenta baixar CUDA, então use `ONNXRUNTIME_NODE_INSTALL_CUDA=skip` [testado] |
| Lip sync, TTS clonado, treino, detecção (YOLO) | GPU | Modelos de rede neural. LatentSync: 23 a 27 s de vídeo em 9 a 14 min numa A100 [testado] |
| Montagem e ffmpeg | CPU, no PC ou na VM | Só vale a VM se o PC cair por falta de RAM [testado] |

- Divida o render em pedaços de 8 a 30 s, com 4 a 8 workers em cada, vários pedaços em paralelo, e junte com `ffmpeg -f concat -c copy`. Um render único com 24 ou mais workers empaca [testado].
- Custo técnico por entrega: US$ 0,08 (79 s), US$ 0,09 (5:56) e ~US$ 0,30 (11:53) [testado].
- Uma oferta de 64 núcleos que alugamos trazia uma RTX 3060 acoplada (anotação de projeto). Para render a GPU não conta: filtre pelos núcleos [testado].

## Colab: grátis, mas com regras

- O Colab roda notebook no navegador, sem SSH no plano grátis. A T4 grátis dura no máximo 12 h e o runtime cai se ficar ocioso [oficial].
- A FAQ proíbe "creating deepfakes" sem definir o termo, e proíbe SSH, desktop remoto e "bypassing the notebook UI" em runtimes grátis sem saldo de unidades [oficial]. Lip sync ou clonagem de voz de terceiros no Colab pode custar a conta. É a nossa leitura do texto [praticante].
- A Colab CLI (Google, 05/06/2026) é o caminho oficial para agentes: `colab new --gpu T4`, `colab exec -f`, `colab download`, `colab stop` [oficial]. Em junho de 2026 só Linux e macOS [independente]. Não testamos.
- Usamos o Colab grátis até o início de outubro de 2026 (Whisper, remoção de fundo, treino curto de voz) [testado]. Depois passamos à Vast, que se opera por SSH sem navegador.

## Segurança: trate voz e rosto como dado sensível

- Por cautela, trate voz e rosto ligados a uma pessoa como dado pessoal sensível: a LGPD (Lei 13.709/2018) inclui o dado biométrico entre os sensíveis (art. 5, II), e o consentimento específico e destacado é uma das bases para tratá-lo (art. 11, I). Se a gravação de voz e o rosto em vídeo contam como biométrico é pergunta em aberto nas fontes que lemos. A transferência para fora do Brasil segue o art. 33 [oficial]. Isto não é parecer jurídico.
- A Vast diz que a segurança varia muito entre provedores e manda criptografar o que é sensível e não guardar credenciais na máquina [fornecedor]. Não achamos garantia documentada contra o dono da máquina física [sem medição]. Trate o host como alguém que pode ver tudo o que está nela [praticante].
- Para dado de terceiro, prefira o nível datacenter: `datacenter=True` na busca da Vast, RunPod Secure Cloud ou Lambda (VMs). Vast e RunPod declaram certificações dos parceiros (ISO 27001, SOC 2); para a Lambda não achamos [fornecedor].
- Criptografia protege o que está parado (pacote, bucket, backup), não o que o modelo lê da memória. O `rclone crypt` cifra conteúdo e nomes, mas não o tamanho do arquivo nem a data [oficial].
- Mande só o necessário: áudio mono recortado e recortes do rosto, não a gravação inteira [praticante].
- Credenciais: token só de leitura, por variável de ambiente, trocado depois; nunca dentro de imagem, template ou arquivo da máquina [praticante].
- Destrua, não pare. Nem Vast nem RunPod documentam apagamento seguro do disco [sem medição]. Não reaproveite volume entre clientes e anote a hora da destruição.
- Não lemos os termos de uso aceitável de Vast, RunPod e Lambda sobre rosto e voz. Leia antes de subir material de terceiros.

## Armadilhas da plataforma

| Armadilha | Causa | Solução |
|---|---|---|
| Parar não para a cobrança | Vast cobra armazenamento enquanto a instância existe; RunPod cobra o disco de volume parado; DigitalOcean cobra a máquina desligada [oficial] | Destruir. Guarde o que importa fora da máquina |
| Retomar pode não achar GPU | Na Vast o restart entra em `SCHEDULING` e pode esperar sem prazo; na RunPod pode voltar com zero GPUs [oficial] | Não conte com parar e retomar; recrie a partir do pacote |
| Porta mudou | Na RunPod as portas TCP podem mudar ao parar e retomar [oficial] | Releia IP e porta a cada início |
| Chave nova não entra | Na Vast a chave só vale para máquinas criadas depois [oficial] | Cadastre antes de criar |
| Saldo zerou | A Vast para as instâncias, o disco segue cobrando e, sem cartão salvo, destrói máquinas e dados após a carência [oficial] | Mantenha saldo e acompanhe |
| Volume preso à máquina | Volume da Vast fica na máquina física; volume de rede da RunPod só na Secure Cloud e preso a um datacenter [oficial] | Guarde fora (bucket, `vastai cloud copy`) |
| Interruptível parou sem aviso | Quem dá lance maior leva a máquina [oficial]; um terceiro diz que não há aviso [independente] | Só para trabalho que retoma do último pedaço |

## O que deu errado aqui

| Sintoma | Causa | Solução |
|---|---|---|
| Oferta não sobe ("loading", "GPU error"); três placas de consumo baratas nunca ligaram | Host ou imagem com problema | Alugue 2 ou 3 ofertas, fique com a primeira que ligar, `reliability>0.98`, espera limitada (60 × 15 s) |
| Duas de três tentativas falharam ao subir | Provável: o script lia a máquina por ID e quebrava (`IndexError`) quando ela não aparecia na lista | Leia a lista inteira e trate "sumiu" como falha |
| O `ssh` cai num tmux e o `scp` estranha | Provável: a Vast abre tmux sozinha no SSH | `touch ~/.no_auto_tmux` uma vez |
| O processo morre ao fechar o SSH | O sinal SIGHUP e a entrada são herdados | `setsid nohup ... < /dev/null &` e `ssh -n` |
| `pkill -f "texto"` derruba a sessão | O padrão casa com o próprio comando remoto | Mate por PID |
| Pedaços falham quando subo muitos | Limite de processos do contêiner: `pids.max` 1792 numa oferta, ~450 threads por pedaço | No máximo 3 ali; leia `/sys/fs/cgroup/pids.max`; em outras ofertas rodamos 8 e 9 [testado] |
| ffmpeg sem libx264 na imagem PyTorch | O ffmpeg do conda vem primeiro no PATH | `export PATH=/usr/bin:$PATH` ou `apt install ffmpeg` |
| Disco estoura | Camada de vídeo com alfa de mais de 30 min passa de 30 GB; caches de modelo | Componha lendo `-f concat`; limpe `conda clean -a` e `~/.cache/huggingface/hub` |
| Download grande cai | IP direto instável | Host proxy; retome com `tail -c +N arq \| ssh ... 'cat >> arq'` e confira o md5 |
| `import wave` quebra | Um `chunk.py` local sombreia o módulo da biblioteca padrão | Renomeie o arquivo |
| Instância de outra sessão na lista | Várias sessões na mesma conta | Destrua só o seu ID |
| Dependência de modelo quebra | `chumpy` do MuseTalk; `from inspect import ArgSpec` do InfiniteTalk; `huggingface-cli` virou `hf` | Versões fixas; `pip install --no-build-isolation chumpy`; `hf download` |
| A ferramenta mudou de versão e quebrou | O `npx` pega a última | Fixe a versão no comando: `npx --yes NOME@VERSAO` |
| Windows para Linux: caminho com espaço ou acento | `concat.txt` com caminho do Windows; nome com emoji ou `\|` quebra o `gdown` | `cygpath -m`, `python -X utf8`, nomes simples |
| O render local cai | pouca RAM, Chrome aberto | VM; no máximo 2 coisas pesadas por vez |

Bibliotecas do Chrome, fontes e codec H.264 no render de HTML ficam no capítulo [Motion por código](08-motion.md).

## O que não testamos

- RunPod, Lambda, Thunder, Salad, Modal e Paperspace: só documentação e preços de página. Nunca alugamos nelas.
- Colab CLI, `vastai ssh-url`, `vastai copy`, `rsync --append-verify` e VS Code Remote-SSH: só documentação.
- Banda e egress (a Vast cobra por byte, sem tabela pública) e o custo real do Colab grátis: sem medição.
- Segurança do host, criptografia dentro de contêiner (FUSE, LUKS) e apagamento seguro: não testamos nem achamos documentação.
- Alguns tempos e limites (`pids.max`, ffmpeg do conda, camada de mais de 30 GB, upload que caiu a 95%) vêm de anotações de projeto sem log guardado.

## Links

- [Vast: preços](https://vast.ai/pricing): sem tabela numérica, "o preço é do mercado".
- [Vast: CLI, primeiros passos](https://docs.vast.ai/cli/get-started): instalar, buscar, criar, destruir.
- [Vast: search offers](https://docs.vast.ai/cli/reference/search-offers.md): campos e sintaxe da busca.
- [Vast: create instance](https://docs.vast.ai/cli/reference/create-instance.md): flags do aluguel.
- [Vast: gerir instâncias](https://docs.vast.ai/guides/instances/manage-instances.md): parar, retomar, destruir.
- [Vast: SSH](https://docs.vast.ai/guides/instances/connect/ssh.md): chaves, direto e proxy.
- [Vast: cobrança](https://docs.vast.ai/guides/reference/billing.md): pré-pago e saldo zerado.
- [Vast: tipos de instância](https://docs.vast.ai/guides/instances/choosing/instance-types.md): sob demanda, reservada, interruptível.
- [Vast: segurança](https://docs.vast.ai/guides/reference/faq/security.md): isolamento e recomendações.
- [Vast: conformidade](https://vast.ai/compliance): SOC 2 e nível Secure Cloud.
- [RunPod: preços](https://www.runpod.io/pricing): tabela oficial de 28/10/2026.
- [RunPod: parar e terminar](https://docs.runpod.io/pods/manage-pods): o que cada ação preserva.
- [RunPod: segurança](https://docs.runpod.io/references/security-and-compliance.md): Secure Cloud e certificações.
- [RunPod: Community Cloud fechada a novos hosts](https://www.plushcap.com/companies/runpod/blog/summaries/2026/02): resumo de terceiro do anúncio de 24/02/2026.
- [Lambda: cobrança](https://docs.lambda.ai/public-cloud/billing/): por minuto, sem parar.
- [Thunder Compute](https://www.thundercompute.com/pricing), [Salad](https://salad.com/pricing/) e [Modal](https://modal.com/pricing): páginas de preço.
- [gpuperhour](https://gpuperhour.com/blog/vast-ai-alternatives): agregador usado para os preços de mercado da Vast.
- [Colab: FAQ](https://research.google.com/colaboratory/faq.html): limites e usos proibidos.
- [Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/): anúncio do Google, 05/06/2026.
- [Custo do Colab por unidade](https://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/): medição independente, março de 2026.
- [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm): arts. 5, 11 e 33.
- [rclone crypt](https://rclone.org/crypt/): criptografia do lado do cliente.
- [VS Code Remote-SSH](https://code.visualstudio.com/docs/remote/ssh): editor remoto.
- [rsync](https://download.samba.org/pub/rsync/rsync.1): manual de `--partial` e `--append-verify`.
