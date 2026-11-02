# Folha de rosto

A folha de rosto é a página de abertura de um projeto de vídeo: um arquivo só, na raiz da pasta, que uma sessão nova (ou outra pessoa) lê para continuar o trabalho sem perguntar nada. Este capítulo explica o que ela contém, por que cada campo existe e traz um exemplo preenchido, adaptado, para você copiar o formato.

## Resumo em 30 segundos

- Um arquivo `ROSTO.md` na raiz do projeto, criado na etapa 2 do [workflow](01-workflow-completo.md) e atualizado a cada versão.
- O núcleo mínimo tem **11 campos** (marcados com ★). Projeto curto e sem cliente usa só eles: [ROSTO-MINIMO.md](../modelos/ROSTO-MINIMO.md). Cliente, VSL ou CTA com "comenta X" usa os 31: [ROSTO.md](../modelos/ROSTO.md).
- Escreva o público e para quem você NÃO fala. Uma v1 já foi reprovada por falar com o público errado [testado].
- Pergunte ao dono do vídeo só o que bloqueia. O resto segue um padrão proposto e registrado no campo 27.
- Nunca escreva valor de chave ou senha. Escreva o NOME da variável (por exemplo, `VOZ_ID`).

## O que é e por que existe

Nos nossos projetos essa informação vivia espalhada em seis tipos de arquivo: mapa do material, brief com cabeçalho, handoff, regras permanentes do cliente, briefing estratégico e a especificação do HyperFrames [testado]. Quem retomava o trabalho lia tudo, não achava o estado atual e repetia etapas. A folha de rosto junta o que uma sessão nova precisa em um lugar:

- o que foi pedido, para quem, e o que NÃO fazer;
- que material existe, que voz vale e que vetos valem;
- qual versão está em vigor e onde cada aprovação está.

Ela é escrita na etapa 2 e consultada em todas as seguintes. O storyboard ([capítulo 03](03-folha-de-storyboard.md)) herda dela o arco, a linguagem visual e os vetos.

## Núcleo mínimo: 11 campos

O menor briefing real que encontramos tinha 528 bytes e já trazia formato, duração, voz, tema, visual, CTA e entrega [testado]. O núcleo abaixo parte daí.

| # | Campo | Em uma linha |
|---|---|---|
| 2 | Dono do vídeo e destino da saída | Quem aprova e recebe, e a pasta da saída |
| 4 | Tipo de projeto e modo | Qual das cinco linhas de produção; autônomo ou acompanhado; com ou sem storyboard |
| 6 | Objetivo e "sai pensando" | O que a pessoa faz ou sente no fim |
| 7 | Público | Quem assiste e quem NÃO é |
| 8 | Arco com tempos | Do gancho ao CTA, com faixas de tempo |
| 11 | Inventário de material | O que chegou, para que serve, o que descartar |
| 14 | Quem fala, com que voz | Real, clone, gerada ou de terceiro; modelo; nome da variável |
| 17 | Formato, duração, teto e derivados | Resolução, fps, duração-alvo e versões derivadas |
| 18 | Linguagem visual | Referência, paleta, tipografia, o que é proibido |
| 21 | Vetos | Lista curta de "nunca" |
| 26 | Portões | Estado de cada portão e de cada trava de segurança |

Três campos ficam fora do núcleo, mas passam a obrigatórios sob condição:

- **Campo 1, slug.** É o título do arquivo (`REEL-TEMA-AAAA-MM-DD`). Sempre existe, mas não precisa de linha própria.
- **Campo 9, CTA e mecânica.** Obrigatório quando o vídeo pede uma ação. No mínimo, o CTA entra como último trecho do arco (campo 8).
- **Campo 25, retomada.** Obrigatório quando o projeto tem scripts para rodar de novo.

## Os 31 campos

★ marca o núcleo. Os blocos A a I seguem a ordem em que as perguntas aparecem no trabalho.

| # | Campo | O que escrever | Por que existe |
|---|---|---|---|
| | **A. Identificação** | | |
| 1 | Slug, série e episódio | `REEL-TEMA-AAAA-MM-DD`; série e número do episódio | Pastas com o mesmo padrão se acham, se ordenam e se retomam; o episódio novo copia o molde do anterior |
| 2 ★ | Dono do vídeo e destino da saída | Quem é o dono (criador ou cliente) e a pasta onde a saída fica | Define quem aprova e quem recebe. A saída vai para a pasta do dono, nunca para dentro das ferramentas |
| 3 | Pedido original | Canal, data, hora e o que chegou (áudio de 3 min, 12 vídeos, 6 fotos) | Permite reler o pedido e provar o que foi pedido |
| 4 ★ | Tipo de projeto e modo | `talking-head`, `reel-motion`, `explicativo`, `vsl` ou `aula`; modo `collaborative` ou `autonomous`; storyboard sim ou não | O tipo muda o pipeline inteiro ([capítulo 01](01-workflow-completo.md)). A chave `mode` espelha a do STORYBOARD.md do HyperFrames |
| 5 | Versão vigente e tabela de versões | A vN em vigor; cada versão com status (reprovada, aprovada, descartada, no ar) e motivo | Uma versão descartada precisou ser marcada como "não usar" e duas foram sobrescritas por um script antes de existir essa tabela [testado] |
| | **B. Intenção** | | |
| 6 ★ | Objetivo e "sai pensando" | Uma frase do que a pessoa sente ou faz no fim, e a frase que ela diria ao sair | Dá critério para cortar: cena que não leva a essa frase sai |
| 7 ★ | Público | Quem assiste e para quem NÃO se fala | Uma v1 foi reprovada por falar com o dono do negócio e não com quem vende a solução [testado]. Termo que o público não conhece fica de fora |
| 8 ★ | Arco com tempos | Gancho, desenvolvimento, prova, oferta e CTA, cada um com uma faixa de tempo | É a espinha do roteiro e do storyboard. Um Reel de 3 min usou nove blocos com tempo [testado] |
| 9 | CTA e mecânica de captura | Palavra do "comenta X", destino, isca e automação | Post que pede comentário sem automação de DM não sai. Obrigatório se o vídeo pede uma ação |
| 10 | Oferta e preço | Valores, prazos, vagas, quem confirmou e o que pode ser dito | Preço, prazo e vaga são do dono. Uma faixa de preço foi dita como fato quando era estimativa [testado] |
| | **C. Entrada** | | |
| 11 ★ | Inventário de material | Tabela arquivo, o que tem, uso; inclua descartados e duplicados | Em um pedido de 18 takes, 7 foram descartados por erro; cópias idênticas aparecem [testado] |
| 12 | Referências de estilo e créditos | Vídeo de referência, o que se aproveita e o que NÃO se copia | Inspiração de ritmo e técnica, sem copiar marca, logo ou texto. Créditos em `CREDITOS.md` |
| 13 | Fatos a provar | Dado, fonte e estado (confirmado, estimativa ou exemplo) | Número só entra com fonte. Simulação aparece marcada "exemplo" |
| | **D. Voz e som** | | |
| 14 ★ | Quem fala, com que voz | Real, clone com autorização por escrito, gerada ou de terceiro; modelo; NOME da variável do ID; regra de uso | A voz oficial pode mudar de modelo, e o rosto diz qual vale. Uma versão aprovada teve o agendamento cancelado para trocar a voz [testado] |
| 15 | Dicionário de pronúncia | Palavra e grafia fonética | Sigla e nome estrangeiro saem errados no TTS. "SaaS" vira "sás" |
| 16 | Trilha, SFX e loudness | Origem, nível em relação à voz, duck, alvo de LUFS e de pico | Música alta reprovou uma versão. Aprovadas: trilha cerca de 15 dB abaixo da voz, -14 LUFS, pico até -1 dBTP [testado] |
| | **E. Formato e linguagem visual** | | |
| 17 ★ | Formato, duração, teto e derivados | Resolução, fps, duração-alvo, teto, `_whats`, `_post` | O teto de duração e o limite de tamanho da ferramenta de agendamento (22 MB, no nosso caso) mudam o plano [testado] |
| 18 ★ | Linguagem visual | Referência, paleta em hex, tipografia, o que é proibido | Cada adjetivo vira um número: "moderno" vira hex, px e segundos. A lista do proibido evita retrabalho (texto dentro de imagem gerada, logo, fantasia, 3D) |
| 19 | Regra de imagem | O que pode ser foto real, gerada ou simulada; selo; rostos; marcas | Real, gerada e simulada não se misturam sem marca quando o dono exige foto real. Marca só inventada, nunca logo real |
| 20 | Área segura e zona de rosto | Régua aplicada e onde fica o rosto | Legenda em y 1700 reprovou uma versão. Texto nunca cobre rosto. Valores que usamos na vertical: legenda entre y 1150 e 1300; motion em x 80-940 e y 250-1440 [praticante] |
| | **F. Vetos e conformidade** | | |
| 21 ★ | Vetos | Lista curta de "nunca" | Cada projeto tem os seus: termo técnico que o público não conhece, nome de outro cliente, preço, promessa de resultado |
| 22 | Autorizações e privacidade | Imagem e voz de terceiros, dado interno, onde NÃO subir o material | Sem autorização por escrito o trecho sai. Relatórios ficam em arquivo local, não em serviço de terceiros |
| | **G. Produção e custo** | | |
| 23 | Onde roda e quanto pode gastar | Local, máquina alugada ou Colab; teto de gasto; quem destrói a máquina | Render pesado vai para a máquina alugada. Definir o teto antes evita gasto sem ok; "destruir ao baixar" evita cobrança esquecida |
| 24 | Responsáveis e destinatários | Quem produz, quem aprova, quem recebe | Para fora, só com o ok do dono. Sócio e equipe do cliente recebem pelo dono |
| 25 | Caminhos e comando de retomada | Pastas (`_bruto`, `_materiais`, `hf`, saída), scripts na ordem e o comando para continuar | É o que permite retomar sem reconstituir. Obrigatório se o projeto tem scripts |
| | **H. Portões e estado** | | |
| 26 ★ | Portões | Para cada portão e cada trava, estado, data e quem aprovou | Diz onde o projeto parou. "Pode publicar" só vale se estiver escrito, com data |
| 27 | Perguntas abertas e padrão adotado | Pergunta, proposta e o que foi adotado se o dono não respondeu | O dono nem sempre responde. O fluxo segue com o padrão proposto e registra, para ele corrigir depois |
| 28 | Riscos e atenção | O que pode dar errado e o plano B | Exemplo: "pouca gente nos takes, a detecção real vai pegar pouco; o resto entra como simulação marcada" |
| | **I. Pós-publicação** | | |
| 29 | Publicação | Link do post, data, collab e arquivo da legenda | Fecha o ciclo e deixa o rastro |
| 30 | Automação e isca | Palavra, campanha, URL da página; o ID da automação fica fora do repositório | O painel de leads lê a campanha daqui. ID é dado de conta, não de projeto |
| 31 | Resultado e feedback do dono | Resumo do que o dono disse, sem citação literal, e o que mudou | O feedback de uma v1 virou quatro regras para as versões seguintes [testado] |

## Exemplo preenchido (adaptado)

Exemplo montado a partir de um Reel nosso, com nicho, nomes, tempos e valores trocados. A "Lavanderia Exemplo" não existe, o criador é fictício e as datas são de mentira. O mesmo projeto aparece no [capítulo 03](03-folha-de-storyboard.md).

```markdown
# ROSTO · REEL-LAVANDERIA-AAAA-MM-DD (EXEMPLO ADAPTADO)

## A. Identificação
1. Slug, série e episódio: REEL-LAVANDERIA-AAAA-MM-DD · série de exemplo, ep. 3
2. ★ Dono do vídeo e destino da saída: criador (perfil de exemplo); saída em `saida/` da pasta do criador. Cliente do caso: nenhum ("Lavanderia Exemplo", fictícia)
3. Pedido original: áudio de 1:50, 7 vídeos e 3 fotos, recebidos no chat do agente
4. ★ Tipo e modo: reel-motion · autonomous · storyboard sim
5. Versão vigente: v1 em aprovação · histórico: nenhum

## B. Intenção
6. ★ Objetivo e "sai pensando": quem assiste entende onde procurar a primeira venda (o dado parado) e sai querendo visitar um negócio do bairro. Sai pensando: "dá pra eu fazer isso na lavanderia perto de casa".
7. ★ Público: quem quer vender implantação de IA para negócio local. NÃO é o dono da lavanderia (aprendizado de uma versão anterior reprovada).
8. ★ Arco: gancho 0:00-0:06 · o cliente 0:06-0:22 · diagnóstico por câmera 0:22-0:58 · 3 soluções 0:58-1:45 · o que precisa 1:45-2:00 · preço de referência 2:00-2:15 · CTA 2:15-2:30
9. CTA: "Comenta LAVANDERIA" leva a uma DM com o link da página do material (isca). Automação obrigatória.
10. Oferta e preço: faixa de implantação e mensalidade é ESTIMATIVA do criador, dita como "referência, não tabela". Valores: a confirmar com o criador.

## C. Entrada
11. ★ Inventário de material:
| arquivo | o que tem | uso |
|---|---|---|
| v01 | fachada ao amanhecer com letreiro aceso | gancho |
| v02 | corredor das máquinas | diagnóstico por câmera |
| v03 | balcão com atendente | alerta do atendente |
| v04, v05 | cópias exatas de v02 | descartar |
| f01 a f03 | fotos de cestos vazios | tela do painel |
12. Referências e créditos: um Reel de referência (ritmo e técnica; NÃO copiar marca, logo nem texto); créditos em `CREDITOS.md`
13. Fatos a provar: "abre cedo" = confirmado (placa na fachada, v01) · "pico às 18h" = exemplo (simulação marcada)

## D. Voz e som
14. ★ Voz: clone do criador, feito com a autorização dele (modelo mais novo aprovado); ID em `VOZ_ID`, variável de ambiente (nunca o valor). Takes mudos e inteiros, na velocidade real; bloco que passa do take é reescrito.
15. Pronúncia: "SaaS" vira "sás"; "QR" vira "quiú-érre"
16. Trilha e som: instrumental cerca de 15 dB abaixo da voz, duck forte, efeitos nos golpes · alvo -14 LUFS, pico até -1 dBTP

## E. Formato e linguagem visual
17. ★ Formato: 1080x1920 a 30 fps · 2:30, teto de 3:00 · derivados `_whats` (720p) e `_post` (até 22 MB)
18. ★ Linguagem visual: "sistema de verdade sobre a filmagem" (caixas de detecção e HUD, nunca no rosto) · paleta #0F1B2D, #F4EFE6, #E07B39 · Anton e Inter · proibido: cartões genéricos, logo real, texto legível dentro de imagem gerada
19. Regra de imagem: takes reais; imagem gerada só onde não há take; simulação sempre com o selo "exemplo"
20. Área segura: legenda entre y 1150 e 1300; motion em x 80-940 e y 250-1440

## F. Vetos e conformidade
21. ★ Vetos: sem logo nem nome de marca · sem promessa de resultado · sem nome de cliente real · o cliente fictício não ganha rosto
22. Autorizações: nenhuma pessoa identificável nos takes sem autorização de imagem

## G. Produção e custo
23. Onde roda: voz e imagens no PC; render em máquina alugada de 64 núcleos; destruir ao baixar e conferir o hash · teto de gasto: US$ 2 (exemplo)
24. Responsáveis: produz o agente · aprova o criador · recebe só o criador
25. Retomada: pastas `_bruto/`, `_materiais/`, `hf/`, `saida/`; comando: os scripts do projeto, na ordem (linha do tempo, composição, mix)

## H. Portões e estado
26. ★ Portões:
| portão ou trava | conteúdo | estado | data |
|---|---|---|---|
| Decisões | perguntas abertas | aprovado | 02/11 |
| Roteiro | texto por bloco | aprovado | 02/11 |
| Consentimento (trava) | voz do criador e termo assinado | aprovado | 02/11 |
| Quadros e fala | storyboard e folha de contato | pendente | |
| Entrega | v1 pronta (`_whats`) | pendente | |
| Publicar | "pode publicar" | pendente | |
27. Perguntas abertas: (1) palavra do CTA → padrão adotado: LAVANDERIA; (2) mostrar o nome da lavanderia? → padrão adotado: não
28. Riscos: pouca gente nos takes → detecção real só onde há gente; o resto marcado "exemplo"

## I. Pós-publicação
29. Publicação: link e data pendentes · arquivo da legenda: `REEL-LAVANDERIA_v1_post.txt`
30. Automação e isca: campanha `lavanderia-ep03.json` (ID da automação fora do repositório)
31. Feedback do dono: pendente
```

## Como preencher a partir de um pedido solto

1. Leia tudo que chegou (transcreva o áudio) e catalogue o material antes de escrever qualquer campo.
2. Preencha o que o pedido já responde. Anote a fonte quando o dado vier de um arquivo.
3. Para cada campo que falta, decida: bloqueia ou tem padrão? Sem público, sem consentimento de voz, sem preço quando o roteiro exige preço: bloqueia. O resto segue um padrão proposto.
4. Mande ao dono de uma vez, no máximo 5 perguntas numeradas, cada uma com o padrão que será adotado se ele não responder.
5. Registre tudo no campo 27 e marque o portão Decisões.

A skill [estudio-folha-de-rosto](../skills/estudio-folha-de-rosto/SKILL.md) automatiza esse roteiro e carrega a lista de campos que bloqueiam.

## O que deu errado aqui

- **Rosto sem público.** A v1 de uma série foi reprovada por falar com quem compra a solução e não com quem a vende. Depois disso o campo 7 passou a exigir "quem NÃO é" [testado].
- **Versões sem tabela.** Uma versão descartada precisou ser marcada como "não usar" e um script sobrescreveu duas versões. O campo 5 existe por causa disso [testado].
- **Preço como fato.** Uma faixa de preço estimada foi dita como valor firme. Hoje o campo 10 exige quem confirmou, e o que não foi confirmado vai marcado como referência [testado].
- **Voz sem registro.** Uma versão já aprovada teve o agendamento cancelado para trocar a voz pela voz oficial. O campo 14 registra qual voz e qual modelo valem [testado].
- **Rosto desatualizado.** Um HANDOFF parado fez outra sessão repetir trabalho já feito [praticante].

## Links

- [Workflow completo](01-workflow-completo.md): onde a folha de rosto entra (etapa 2).
- [Folha de storyboard](03-folha-de-storyboard.md): o que herda do rosto.
- [Modelo ROSTO.md](../modelos/ROSTO.md) e [modelo ROSTO-MINIMO.md](../modelos/ROSTO-MINIMO.md): folhas em branco.
- [Skill estudio-folha-de-rosto](../skills/estudio-folha-de-rosto/SKILL.md): preenche a folha a partir de um pedido solto.
- [HyperFrames](https://github.com/heygen-com/hyperframes): origem das chaves `format`, `duration`, `message`, `arc` e `audience` usadas no storyboard.
