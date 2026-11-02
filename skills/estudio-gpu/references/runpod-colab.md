# RunPod, Lambda e Colab: só documentação

Nada deste arquivo foi rodado por nós: nunca alugamos na RunPod nem na Lambda, e o Colab foi usado só até o início de outubro de 2026, pelo navegador. Tudo vem da documentação dos fornecedores, lida em 01/11/2026. Confira cada comando com `--help` antes de usar. Selo: `[oficial]`.

## RunPod

- Cobrança por segundo, sem taxa de entrada e saída de dados. Contêiner, não VM.
- Parar libera a GPU, mantém o disco de volume (`/workspace`, US$ 0,20 por GB ao mês parado) e apaga o disco de contêiner. Terminar apaga tudo que não esteja num volume de rede. Ao retomar, a máquina pode voltar com zero GPUs.
- Volume de rede: só na Secure Cloud, preso a um datacenter, US$ 0,07 por GB ao mês até 1 TB. Saldo zerado: pods sem volume de rede são terminados e os dados não voltam.
- Community Cloud fechada a novos hosts desde 24/02/2026. Para dado de terceiro use Secure Cloud.

```bash
runpodctl pod create --name teste --gpu-id "NVIDIA A40" --image "runpod/pytorch:3.10-2.0.0-117"
runpodctl pod stop $RUNPOD_POD_ID       # libera a GPU; o volume segue cobrando
runpodctl pod delete $RUNPOD_POD_ID     # terminar: este é o fim do ciclo
```

SSH: chave em Credentials ou na variável `SSH_PUBLIC_KEY`. O SSH básico (`ssh.runpod.io`) passa por proxy e não faz SCP nem SFTP. O SSH completo (`ssh root@IP -p PORTA`) faz SCP, SFTP e redirecionamento de portas, mas exige IP público com a porta TCP 22 exposta; as portas podem mudar ao parar e retomar. Portas HTTP passam por proxy com limite de 100 s (erro 524). `runpodctl send arquivo` transfere com código de uso único. O `rsync` precisa de Linux ou WSL.

Segredos: `{{ RUNPOD_SECRET_nome }}` em templates; depois de criado, o valor não pode ser visto.

## Lambda

- VMs de datacenter, cobrança por minuto, sem placas de consumo (H100, A100, A10, A6000 e outras).
- Não existe parar: só criar, reiniciar, listar e terminar. A máquina cobra enquanto existir. Sistemas de arquivos cobram por GiB ao mês (exemplo da documentação: US$ 0,20).
- Sem taxa de entrada e saída.

## Google Colab

- Notebook no navegador. Grátis: no máximo 12 h por sessão e o runtime cai se ficar ocioso. Pro+ pode rodar até 24 h com unidades suficientes.
- A FAQ lista "creating deepfakes" entre os usos proibidos e não define o termo [oficial] (https://research.google.com/colaboratory/faq.html, lida em 01/11/2026). Rosto e voz de terceiro: não use o Colab.
- Em runtimes grátis sem saldo de unidades, a FAQ proíbe SSH, desktop remoto e "bypassing the notebook UI", e a conta pode ser encerrada sem aviso.
- Colab CLI (Google, 05/06/2026), feita para agentes com acesso a terminal: `colab new --gpu T4`, `colab install`, `colab exec -f script.py`, `colab log --output`, `colab download`, `colab stop`. Em junho de 2026 só Linux e macOS (no Windows, WSL). Sempre rode `colab stop` ao terminar: máquina ociosa consome unidades.
- Planos (fonte secundária; a página oficial exige login): Pay As You Go US$ 9,99 por 100 unidades; Pro US$ 9,99 ao mês com 100 unidades; Pro+ US$ 49,99 ao mês com 600. Consumo medido por um terceiro em março de 2026: T4 1,19 unidade por hora (cerca de US$ 0,12), L4 1,71, A100 de 40 GB 5,40, A100 de 80 GB 7,52.
- `/content` é apagado quando a VM é reciclada; monte o Drive para persistir.

## Fontes

Páginas vistas em 01/11/2026.

- [RunPod: preços dos Pods](https://docs.runpod.io/pods/pricing.md): cobrança por segundo e saldo zerado.
- [RunPod: parar e terminar](https://docs.runpod.io/pods/manage-pods): o que cada ação preserva.
- [RunPod: tipos de armazenamento](https://docs.runpod.io/pods/storage/types.md): disco de contêiner, de volume e de rede.
- [RunPod: volumes de rede](https://docs.runpod.io/storage/network-volumes.md): só na Secure Cloud.
- [RunPod: SSH](https://docs.runpod.io/pods/configuration/use-ssh.md): SSH básico e completo.
- [RunPod: portas](https://docs.runpod.io/pods/configuration/expose-ports.md): proxy HTTP e limite de 100 s.
- [RunPod: transferir arquivos](https://docs.runpod.io/pods/storage/transfer-files.md): `runpodctl send`, scp e rsync.
- [RunPod: segredos](https://docs.runpod.io/pods/templates/secrets.md): valor não pode ser visto depois de criado.
- [RunPod: Community Cloud fechada a novos hosts](https://www.plushcap.com/companies/runpod/blog/summaries/2026/02): resumo de terceiro do anúncio de 24/02/2026.
- [Lambda: cobrança](https://docs.lambda.ai/public-cloud/billing/): por minuto, sem parar.
- [Lambda: instâncias sob demanda](https://docs.lambda.ai/public-cloud/on-demand/): VMs e placas oferecidas.
- [Colab: FAQ](https://research.google.com/colaboratory/faq.html): limites e usos proibidos.
- [Colab CLI](https://developers.googleblog.com/introducing-the-google-colab-cli/): anúncio do Google, 05/06/2026.
- [Planos do Colab](https://gpuperhour.com/blog/google-colab-alternatives): fonte secundária, porque a página oficial exige login.
- [Custo do Colab por unidade](https://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/): medição de terceiro, março de 2026.
