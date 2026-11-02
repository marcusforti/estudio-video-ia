---
name: estudio-workflow
description: Use quando alguém pedir um vídeo do começo ao fim ("faz um Reel com esses takes", "monta uma VSL", "edita essa aula", "toca esse projeto de vídeo", "o que eu faço agora com esse pedido") ou quando for preciso decidir o tipo de projeto, a ordem das etapas e quando parar para pedir ok ao dono do vídeo.
---

# Workflow de vídeo: do pedido à publicação

Você conduz o projeto. As outras skills `estudio-*` fazem as partes; esta decide o tipo de projeto, a ordem das etapas e onde parar. O trabalho interno corre sem perguntar. Pare e peça ok só no que sai de dentro do projeto.

## Portões obrigatórios

Seis portões esperam o dono do vídeo. Três travas param você por conta própria. Nenhuma delas tem exceção por pressa.

| Tipo | Nome | Etapa | Regra |
|---|---|---|---|
| Portão | Decisões | 2 | Perguntas abertas do rosto. Sem resposta, siga o padrão proposto e registre |
| Portão | Roteiro | 4 | VSL e material de cliente: texto por bloco aprovado antes da voz. Reel curto: segue com a v1 |
| Trava | Consentimento | 5 | Clonar voz ou mexer no rosto de alguém exige termo escrito de quem aparece ou fala. Sem o termo, pare e avise o dono |
| Portão | Quadros e fala | 6 | Storyboard e folha de contato aprovados antes de renderizar |
| Portão | Prévia | 7 | Só em vídeo longo: prévia leve (15 fps) aprovada antes do render final |
| Trava | Gasto | 9 | Antes de alugar máquina ou gerar com serviço pago, mostre a estimativa e espere ok com teto. Destrua a máquina ao baixar |
| Trava | Conferência | 11 | Reprovou? Corrija e refaça. Não entregue e não peça aprovação |
| Portão | Entrega | 12 | O vídeo vai só ao dono. "Enviado" só com status de entregue ou lido |
| Portão | Publicar | 14 | Só com "pode publicar" explícito. Post com "comenta X" só sai com a automação ativa e testada |

Chaves de API ficam em variáveis de ambiente (`ELEVENLABS_API_KEY`, `VAST_API_KEY`, `VOZ_ID`). Nunca imprima, nunca grave em arquivo do projeto.

## Antes de começar

1. Descubra quem é o dono do vídeo e onde fica a pasta dele. Crie `<slug>/` com `_bruto/ _materiais/ hf/ qa/ saida/` ali, nunca dentro da pasta das ferramentas. Slug: `REEL-TEMA-AAAA-MM-DD`.
2. Rode `date` (ou o equivalente) e escreva datas exatas em todo registro.
3. Pergunte o teto de gasto. Sem teto, sem máquina alugada e sem geração paga.
4. Se o projeto já existe, leia `ROSTO.md` e `HANDOFF.md` antes de qualquer coisa. Se divergirem da pasta, confie na pasta e corrija o `HANDOFF.md`.

## 1. Decida o tipo de projeto

| O que chegou | Tipo | O que pesa |
|---|---|---|
| Pessoa falando para a câmera, bruto longo | `talking-head` | Cortes, gancho, legenda, áudio; voz real, sem clone |
| 9 a 18 takes curtos e um áudio de briefing | `reel-motion` | Mapa, voz por cima de takes mudos, motion, automação de DM |
| Só ideia e roteiro, sem filmagem | `explicativo` | Roteiro, voz gerada, imagens geradas, storyboard |
| Cliente que vende algo, com questionário e reuniões | `vsl` | Briefing, roteiro aprovado, piloto antes da versão longa, conformidade |
| Gravação de reunião ou live de 1 h ou mais | `aula` | Cortes por nota, layout remontado, render em pedaços |

Se não encaixar, pergunte uma vez. Detalhe de cada tipo: `references/tipos-de-projeto.md`.

## 2. Percorra as etapas

Detalhe de cada etapa (entrada, saída, ferramenta, erro típico): `references/etapas.md`. Rode as skills abaixo se estiverem instaladas; se não, siga o detalhe.

| Etapa | Ação | Skill |
|---|---|---|
| 0 | Baixe áudio, takes e fotos para `_bruto/` | |
| 1 | Transcreva por palavra (Whisper) e catalogue o material | |
| 2 | Escreva a folha de rosto | `estudio-folha-de-rosto` |
| 3 | Proponha estilo e registre créditos | `estudio-escolher-motion` |
| 4 | Roteiro por blocos, no tom do dono, números e siglas por extenso | |
| 5 | Voz com tempo por palavra | `estudio-voz-local` |
| 6 | Storyboard e imagens | `estudio-storyboard` |
| 7 | Linha do tempo e composição | `estudio-motion` |
| 8 | Mix de áudio | |
| 9 | Render, local ou em máquina alugada | `estudio-gpu` |
| 10 | Finalização: legenda, loudness, remux do áudio | `estudio-entrega` |
| 11 | Conferência | `estudio-entrega` |
| 12 | Entrega ao dono | `estudio-entrega` |
| 13 | Iteração: vN+1 e `HANDOFF.md` | |
| 14 | Postagem, na ferramenta de agendamento do usuário | |
| 15 | Isca e automação comentário→DM (opcional) | |
| 16 | Registro; máquina destruída | `estudio-gpu` |

Cortes de talking head: `estudio-corte`. Boca fora de sincronia em filmagem real: `estudio-lipsync`.

## Ao longo do projeto

- Um render pesado por vez no PC; no máximo 2 processos pesados em paralelo. Nunca feche programas do dono para liberar memória.
- Relatório, folha e playbook ficam em pasta local, nunca em serviço de terceiros.
- Feedback do dono vai resumido para o campo 31 do rosto, sem citação literal.
- Cada versão é um arquivo novo (`<slug>_vN.mp4`). Nunca sobrescreva uma versão existente. Registre versão, status e motivo no `HANDOFF.md`.
- Terceiros (cliente final, sócio, equipe) só recebem pelo dono, ou com o ok dele.

## Sinais de alerta: pare e releia os portões

| Pensamento | Realidade |
|---|---|
| "O dono está com pressa, pulo o rosto" | Uma v1 já foi reprovada por falar com o público errado. O rosto existe para isso |
| "Renderizo e mostro os quadros junto" | Quadros e fala vêm antes do render |
| "Reprovou na conferência, mas ninguém vai notar" | Reprovou, corrige. Não entrega |
| "É só um teste, mando direto ao cliente" | Terceiros recebem pelo dono |
| "A v1 foi aprovada, posto" | "Pode publicar" é um ok separado |
| "Deixo a máquina ligada para a próxima" | Destrua ao baixar. Parada ainda pode cobrar |
| "Clono a voz, depois peço o termo" | O termo vem antes. Sem ele, pare |
| "Outra sessão já cuida disso" | Leia o `HANDOFF.md`. Já houve duas sessões na mesma peça ao mesmo tempo |

## Pronto quando

O `HANDOFF.md` tem a versão em vigor, o status de cada versão, as pendências e o comando para retomar; a máquina alugada foi destruída; nenhum segredo foi gravado no projeto.
