# GPU alugada, tratada como máquina local

A máquina alugada é o seu PC por algumas horas: mesma pasta de trabalho, mesmos comandos, e ela some no fim. Os comandos abaixo são os do provedor que usamos (Vast.ai); qualquer provedor com acesso por SSH serve. A chave vem de variável de ambiente (`VAST_API_KEY`), nunca escrita no comando, no script ou no log.

## Portão de gasto (antes de alugar)

Mostre ao dono do projeto, por escrito: provedor, GPU, preço por hora, tempo estimado, custo total estimado e disco. Só alugue depois do "sim". Se o tempo estimado dobrar no meio do trabalho, pare e pergunte de novo.

Preços de referência (por hora):

- Vast.ai, A100 80 GB com disco: US$ 1,23, valor que pagamos em outubro de 2026. [testado]
- RunPod, página de 28/10/2026, nuvem comunitária e nuvem segura: RTX 4090 US$ 0,34 e 0,89; A100 80 GB PCIe US$ 1,19 e 1,79; H100 PCIe US$ 1,99 e 2,89. [fornecedor]

## Ciclo

```bash
vastai set api-key "$VAST_API_KEY"   # uma vez por sessão

# 1. procurar (ordenado por preço)
vastai search offers 'gpu_name in [A100_PCIE,A100_SXM4] num_gpus=1 reliability>0.98 inet_down>500 disk_space>=100 rentable=true' -o dph --raw

# 2. alugar (anote o ID devolvido)
vastai create instance <OFERTA> --image pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel --disk 100 --ssh --direct --raw

# 3. subir amostra, texto e roteiro; rodar por ssh
scp -P <PORTA> amostra.wav amostra.txt roteiro.json root@<IP>:/root/voz/
ssh -p <PORTA> root@<IP> 'cd /root/voz && python gerar.py'

# 4. baixar a saída E os checkpoints, só depois destruir
scp -P <PORTA> -r root@<IP>:/root/voz/saida ./saida
echo y | vastai destroy instance <ID>
vastai show instances --raw   # tem de imprimir []
```

`<IP>`, `<PORTA>`, `<OFERTA>` e `<ID>` saem da resposta do provedor. Nada disso vai para o repositório.

## Destruir sempre

O disco cobra mesmo com a máquina parada. Se você orquestra por script, deixe a destruição num `trap`, que roda até quando o script falha (testado com o `vastai` simulado):

```bash
ID=""                      # preencha com o ID devolvido por 'create instance'
fim() { [ -n "$ID" ] && echo y | vastai destroy instance "$ID"; }
trap fim EXIT
```

Ao terminar, confira que `show instances` imprime `[]` (nenhuma instância sobrou) e diga ao dono do projeto quanto foi gasto.

## O que aprendemos alugando [testado]

- Três placas 3090 baratas não ligaram (erro de CDI, travamento). Se uma oferta não ligar, alugue três ao mesmo tempo, fique com a primeira que ligar e apague as outras.
- Baixe o resultado e os checkpoints antes do `destroy`. Perdemos um checkpoint escolhido assim.
- Nunca use `pkill -f` com uma palavra que aparece no próprio comando do ssh: ele mata a sessão.
- O Colab grátis (T4) bastou para treinar RVC.
