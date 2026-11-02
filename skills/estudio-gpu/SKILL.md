---
name: estudio-gpu
description: Use quando o usuário pedir para alugar GPU ou VM na nuvem (Vast.ai, RunPod, Colab) para renderizar vídeo, rodar lip sync, voz clonada, treino de voz ou Whisper, ou disser "meu PC não aguenta", "roda na nuvem", "aluga uma máquina", "usa a VM como se fosse meu PC", "destrói a máquina" ou "esqueci uma máquina ligada".
---

# Estúdio GPU: alugar, usar e destruir

Conduz o ciclo de vida de uma máquina alugada (GPU ou CPU de muitos núcleos). O ciclo só termina quando a lista de instâncias volta vazia. Parar não é destruir: o disco da máquina parada continua cobrando.

Nos comandos, `<skill>` é a pasta desta skill.

## Portões (obrigatórios, nesta ordem)

1. **Gasto.** Antes de criar qualquer máquina, rode `python <skill>/scripts/estimar_gasto.py --preco-hora P --horas H --extra D --teto T`. Mostre o resultado ao usuário e espere um OK explícito, com o teto. Sem OK, não crie. Acima do teto: peça nova autorização.
2. **Dado de terceiro.** Se o trabalho usa rosto ou voz de outra pessoa, pergunte se existe consentimento por escrito que cubra processamento em nuvem fora do Brasil. Sem consentimento, pare. Com consentimento, use só nuvem segura (Vast `datacenter=True`, RunPod Secure Cloud ou Lambda), nunca o Colab: a FAQ dele lista "creating deepfakes" entre os usos proibidos e não define o termo [oficial] (https://research.google.com/colaboratory/faq.html, lida em 01/11/2026). Detalhes em `references/seguranca-dados.md`.
3. **Destruir.** Ao terminar, baixe, confira, destrua e prove a lista vazia (passos 6 a 9). Se a sessão for interrompida, destrua a máquina antes de encerrar.
4. **Dono primeiro.** O resultado vai só ao dono do vídeo. Não publique nem compartilhe link.
5. **Segredos.** A chave da API fica em variável de ambiente (`VAST_API_KEY`). Não imprima, não grave em arquivo versionado, não copie para dentro da máquina alugada. IP, porta e ID ficam só na sessão.

## Quando usar

| Situação | Decisão |
|---|---|
| Render de HTML ou motion com mais de ~2 min de vídeo | VM de CPU, 32 a 80 núcleos (a GPU não ajuda) |
| Lip sync, TTS clonado, treino, detecção de objetos | VM com GPU; a VRAM vem do README do modelo, com 20% de folga |
| Whisper curto | PC ou Colab grátis, se não houver rosto nem voz de terceiro |
| Trabalho de segundos | Não alugue: preparar a máquina custa mais que o trabalho |

Preços e comparação entre serviços: `references/precos-2026-11-01.md`.

## Ciclo

Cada passo tem o comando em `references/vast-comandos.md` (Vast, testado em produção). RunPod, Lambda e Colab: `references/runpod-colab.md` (só documentação).

1. **Confirmar o gasto** (portão 1).
2. **Escolher e criar.** Veja antes `vastai show instances --raw` (pode haver máquina de outra sessão). Filtros `verified=true reliability>0.98`. Alugue 2 ou 3 ofertas baratas, fique com a primeira que ligar e destrua as outras. Guarde só o ID.
3. **Entrar por SSH.** Chave ed25519 cadastrada antes de criar. Desligue o tmux automático no primeiro acesso.
4. **Subir o projeto.** Pacote pequeno (`tar czf`); o pesado se baixa dentro da máquina.
5. **Rodar sem depender do SSH.** `setsid nohup ... < /dev/null &`, log em arquivo, script que pula o que já existe.
6. **Baixar o resultado.**
7. **Conferir:** `python <skill>/scripts/conferir_download.py ARQUIVO --md5 HASH_DA_MAQUINA --duracao SEGUNDOS --midia`. Se falhar, não destrua: baixe de novo.
8. **Destruir:** `echo y | vastai destroy instance ID`. Nunca só parar.
9. **Provar:** `vastai show instances --raw | python <skill>/scripts/lista_vazia.py --meu-id ID` deve dizer "OK". Saída 3 significa que o comando falhou: rode de novo, não conclua nada. Se houver instância que não é sua, não mexa e avise o usuário.
10. **Registrar** data, custo estimado e "destruída" no HANDOFF do projeto, sem IP, porta nem chave.

## Sinais de alerta: pare e releia os portões

| Pensamento | Realidade |
|---|---|
| "Ele está com pressa, crio e conto o custo depois" | Gasto sem OK é falha de portão |
| "Paro a máquina para economizar" | O disco segue cobrando; destrua |
| "Deixo ligada para a próxima sessão" | Recrie a partir do pacote |
| "O vídeo toca, não preciso conferir o md5" | Download truncado também toca; confira |
| "Tem uma máquina que não conheço na lista" | Pode ser de outra sessão; só destrua o seu ID |
| "É só um teste, o Colab serve para o rosto dele" | Rosto e voz de terceiro não vão para o Colab |
| "A chave vai no `.env` da máquina" | Nunca; use variável da sessão e rotacione depois |

## Erros comuns

Oferta que não sobe, processo que morre ao fechar o SSH, `pkill -f` que derruba a sessão, disco cheio, ffmpeg sem libx264, download que cai: causa e solução em `references/armadilhas.md`.

## Selos de evidência

`[testado]` = rodou em produção na Vast em outubro de 2026. `[sem medição: rodado só contra simulação]` = trecho de shell rodado contra um `vastai` falso com JSON sintético, sem alugar. `[oficial]` = vem só da documentação do fornecedor e não foi rodado por nós. Os scripts de `scripts/` (rode com `python` ou `python3`, conforme o sistema) foram testados com entradas sintéticas e não falam com nenhuma API.
