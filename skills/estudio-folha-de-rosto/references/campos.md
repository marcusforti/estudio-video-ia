# Os 31 campos: o que perguntar e qual padrão adotar

★ marca o núcleo mínimo (11 campos). "Bloqueia?" diz se você deve perguntar ao dono quando o pedido não responder. Onde não bloqueia, adote o padrão e registre no campo 27.

| # | Campo | Bloqueia? | Padrão se o dono não responder |
|---|---|---|---|
| 1 | Slug, série e episódio | Não | `REEL-TEMA-AAAA-MM-DD` com a data de hoje. Série e episódio só se o pedido citar |
| 2 ★ | Dono do vídeo e destino da saída | Sim, se não for óbvio | Quem mandou o pedido. Saída na pasta dele, nunca na das ferramentas |
| 3 | Pedido original | Não | Canal, data, hora e a lista de anexos |
| 4 ★ | Tipo de projeto e modo | Não | Decida pela tabela do `estudio-workflow`. Modo `collaborative` |
| 5 | Versão vigente e tabela de versões | Não | v1 em aprovação; histórico vazio |
| 6 ★ | Objetivo e "sai pensando" | Sim, se o pedido não disser | Proponha uma frase e marque como proposta |
| 7 ★ | Público (e quem NÃO é) | Sim, se o pedido admite mais de um público | Proponha e escreva "NÃO é: ..." |
| 8 ★ | Arco com tempos | Não | Gancho, desenvolvimento, prova e CTA, com faixas que somam a duração-alvo |
| 9 | CTA e mecânica de captura | Sim, se o vídeo pede ação e faltam palavra ou destino | Proponha uma palavra. Automação de DM obrigatória |
| 10 | Oferta e preço | Sim, se o roteiro precisa de preço | Deixe o preço fora do vídeo, ou use "referência, não tabela" com valores "a confirmar" |
| 11 ★ | Inventário de material | Não | Monte você. Cópias idênticas: "descartar" |
| 12 | Referências de estilo e créditos | Não | Proponha 2 opções. O que NÃO copiar: marca, logo, texto |
| 13 | Fatos a provar | Não | Todo fato sem fonte entra como "estimativa" ou "exemplo" |
| 14 ★ | Quem fala, com que voz | Sim, se for clonar a voz de alguém | Voz real do dono, ou voz gerada. Clone só com termo escrito. Registre o NOME da variável, nunca o valor |
| 15 | Dicionário de pronúncia | Não | Liste siglas e nomes estrangeiros do roteiro, com a grafia fonética |
| 16 | Trilha, SFX e loudness | Não | Trilha cerca de 15 dB abaixo da voz, duck, -14 LUFS e pico até -1 dBTP |
| 17 ★ | Formato, duração, teto e derivados | Não | Reel: 1080x1920 a 30 fps. VSL e aula: 1920x1080. Derivados `_whats` e `_post` |
| 18 ★ | Linguagem visual | Não | Duas opções com paleta em hex e tipografia. Proibido: logo real, texto legível dentro de imagem gerada |
| 19 | Regra de imagem | Não | Real onde há take; gerada só onde não há; simulação com o selo "exemplo" |
| 20 | Área segura e zona de rosto | Não | Vertical: legenda entre y 1150 e 1300; motion em x 80-940 e y 250-1440 |
| 21 ★ | Vetos | Sim, uma vez, no começo | Sem logo nem nome real, sem promessa de resultado, sem preço, sem nome de outro cliente |
| 22 | Autorizações e privacidade | Sim, se há pessoas ou dados de terceiros | Nenhuma pessoa identificável sem autorização de imagem. Relatórios só em arquivo local |
| 23 | Onde roda e quanto pode gastar | Sim, se precisa de máquina alugada ou serviço pago | Local, sem gasto |
| 24 | Responsáveis e destinatários | Não | Produz: o agente. Aprova e recebe: o dono |
| 25 | Caminhos e comando de retomada | Não | Preencha ao criar os scripts (obrigatório se houver scripts) |
| 26 ★ | Portões | Não | Todos "pendente" (portões e travas) |
| 27 | Perguntas abertas e padrão adotado | Não | É este campo que registra as respostas e os padrões |
| 28 | Riscos e atenção | Não | Liste o que você notou no material (pouca gente nos takes, áudio ruim, takes corrompidos) |
| 29 | Publicação | Não | Em branco até publicar |
| 30 | Automação e isca | Não | Em branco até criar. O ID da automação fica fora do repositório |
| 31 | Resultado e feedback do dono | Não | Em branco. Depois, resumo sem citação literal |

Campos que passam a obrigatórios sob condição: o 1 (é o título do arquivo), o 9 (se o vídeo pede uma ação) e o 25 (se o projeto tem scripts).
