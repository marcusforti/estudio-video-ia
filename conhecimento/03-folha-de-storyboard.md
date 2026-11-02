# Folha de storyboard

A folha de storyboard é a tabela cena a cena que liga o que a voz diz ao que o público vê. Ela é escrita antes de gerar imagens e de renderizar. O dono do vídeo aprova, e só então a composição é montada. Este capítulo traz o cabeçalho, as 14 colunas, as 17 regras de preenchimento, um exemplo de 10 cenas, a folha de contato e o validador que confere a tabela.

## Resumo em 30 segundos

- O arquivo é `STORYBOARD.md`: cabeçalho, tabela de 14 colunas (9 obrigatórias) e uma linha de rodapé com a contagem de cenas por tipo.
- A regra que manda: a imagem mostra literalmente o que a voz diz. Nunca foto solta.
- O tempo é estimado primeiro (2,33 palavras por segundo mais 0,35 s entre falas) e medido depois, na palavra-gatilho.
- Valide com `python checar_storyboard.py STORYBOARD.md --teto 5` antes de mostrar ao dono.
- Tabela e folha de contato esperam o ok do dono antes do render (portão "Quadros e fala" do [workflow](01-workflow-completo.md)).

<!-- diagrama:folhas -->

## O que é e onde ela vive

Nos nossos projetos o storyboard apareceu de várias formas: tabela de roteiro com tempo, narração, visual e texto; imagem gerada por script, com a fala ao lado de cada quadro; lista de "beats" de uma VSL longa; código que posiciona cada objeto no tempo da fala; e o `STORYBOARD.md` do HyperFrames [testado]. A folha abaixo reúne os campos que se repetiam.

Ela nasce do [rosto](02-folha-de-rosto.md): o arco vira a coluna Bloco, a linguagem visual vira o cabeçalho e os vetos viram a coluna Checagens.

## Cabeçalho

Vem sempre antes da tabela, como lista.

| Campo | Conteúdo |
|---|---|
| Nome e versão | `Storyboard N · nome · Ns` |
| Objetivo e "sai pensando" | Na voz de quem assiste |
| Sentimento | Uma palavra: desejo, encantamento, surpresa |
| Ideia | Duas ou três linhas do arco |
| Linguagem visual | Paleta, tipografia, movimento, tratamento do material real |
| Códigos de tipo | R real · IA imagem gerada · B banco · M motion · T tela real · S simulação |
| Régua de tempo | Estimada com 2,33 palavras/s + 0,35 s entre falas; depois ancorada na palavra-gatilho medida |
| Trilha e SFX | Estilo, nível em relação à voz, silêncios |
| Custo de geração | Imagens geradas x custo unitário (estimado no cabeçalho, real no rodapé) |
| Versão curta | Por exemplo, "30 s: mesma ideia, metade das cenas" |

## As 14 colunas

★ marca as 9 colunas obrigatórias. O validador aceita a tabela sem as outras 5.

| # | Coluna | O que vai | Valores e regra |
|---|---|---|---|
| 1 ★ | `#` | Id estável da cena (`c01`) | Não renumere ao inserir: use `c04b` |
| 2 | Bloco | Gancho, problema, mecanismo, prova, oferta, CTA | Bate com o arco do rosto (campo 8) |
| 3 ★ | Tempo | Início e fim da cena | `0:03,8-0:08`. Estimado primeiro, medido depois (regra 4) |
| 4 ★ | Fala | Texto exato que o TTS lê; ou "take real, sem a voz do dono"; ou "(silêncio de 1 s, sem voz)" | Números e siglas por extenso; grafia fonética onde o TTS erra |
| 5 ★ | Gatilho | A palavra falada que dispara a cena | Uma palavra (ou duas coladas) que está na Fala. Cena sem voz leva `-` |
| 6 ★ | Tipo | R, IA, B, M, T, S, ou combinações com `+` (R+M) | S (simulação) leva sempre o selo "exemplo" no texto em tela |
| 7 ★ | Visual | O que se vê | Literalmente o que a voz diz (regra 1) |
| 8 | Câmera / transição | Ken Burns, push-in, whip, zoom, fade, drop, flash | Uma transição de entrada por cena |
| 9 ★ | Texto em tela | Texto exato; posição e janela, se houver | Até 2 linhas, separadas por `<br>`; dentro da área segura; janela mínima (regra 8). `-` se não houver |
| 10 | Som | SFX, silêncio, mudança de trilha | "1 s de silêncio", "sem voz, só música" |
| 11 ★ | Origem do asset | Arquivo ou ID, prompt-base, foto de referência, busca de banco, licença ou crédito, "PRÓPRIO" | Rastreável (regra 11) |
| 12 | Checagens | Rosto livre, área segura, marca ou logo, autorização, fato com fonte | Marque com o resultado da conferência |
| 13 ★ | Status | outline, imagem aprovada, construído, animado, conferido | Mapeia para `outline → built → animated` do HyperFrames |
| 14 | Nota do portão | Decisão do dono e a data | "Quadros e fala, 02/11: seguir com os padrões" |

## As 17 regras de preenchimento

| Regra | Texto | Por quê |
|---|---|---|
| R1 Imagem = fala | A imagem mostra literalmente o que a voz diz, nunca foto solta. Teste: tape a coluna Fala; só pelo Visual e pelo Texto em tela alguém adivinha o assunto, e o substantivo-chave da fala está no Visual | Foto solta, que não mostra o que a voz diz, apareceu entre as causas de reprovação [testado]. O teste de tapar a coluna Fala é nosso, sem medição [praticante] |
| R2 Mapa primeiro | Inventário de material, roteiro por tempo e perguntas abertas vêm antes de qualquer cena | Em um pedido grande, o dono pediu o mapa antes de tudo [praticante] |
| R3 Quadros e fala antes do render | A folha (tabela e folha de contato) vai ao dono e espera o ok. Arte em etapas: gera, o dono escolhe, só então monta | Corrigir quadro depois do render custa um render inteiro [praticante] |
| R4 Tempo estimado, depois medido | Estime com 2,33 palavras/s + 0,35 s entre falas. Com a voz pronta, troque pelo tempo medido da palavra-gatilho. TTS com timestamps já entrega o alinhamento | A estimativa serve para planejar; o render usa o medido [praticante] |
| R5 Um gatilho por cena | Se a palavra não alinha com a fala, corrija o gatilho | O validador avisa quando o gatilho não está na fala |
| R6 Ritmo e teto de cena parada | Nenhuma cena acima de cerca de 5 s sem troca de imagem ou entrada de texto; em VSL, nada acima de 3 s sem elemento animado | Médias que medimos: entre 2 s e 4,5 s por cena em VSLs e em pilotos de VSL [testado]. A especificação do HyperFrames pede algo novo a cada 2 a 4 s [oficial] |
| R7 Gancho | Cena 1 com motion e fala nos 2 primeiros segundos; cartão do gancho em cerca de 0,9 s. Em talking head o gancho é a frase mais forte de qualquer ponto do bruto, nunca a primeira | A mesma frase voltando a menos de 12 s da abertura soa como gagueira [praticante] |
| R8 Texto em tela | Texto exato, até 2 linhas. Fonte de 28 px ou mais a 1080 de largura; janela de 0,5 s + 0,3 s por palavra; dentro da área segura | Um cartão de 2 linhas fica 3 s ou mais no ar; com 1,2 s ninguém lê [praticante]. Os 28 px e a janela por palavra vêm da especificação do HyperFrames [oficial] |
| R9 Rosto livre | Nenhum texto, legenda ou motion sobre rosto. Confira por snapshot em todo o intervalo, inclusive nos picos de escala. Sem caixa de detecção no rosto | A conferência achou texto encostando no cabelo de uma pessoa [testado] |
| R10 Tipo sempre marcado | Real, gerada e simulada não se misturam sem marca quando o dono exige foto real | A regra de imagem de um projeto mudou no meio do caminho; com o tipo marcado em cada cena, saber o que trocar é uma busca na tabela [testado] |
| R11 Origem rastreável | Arquivo ou ID, prompt-base, foto de referência de rosto, busca de banco, licença, "PRÓPRIO" para material do cliente. Créditos em `CREDITOS.md` | Sem origem não dá para refazer, creditar nem provar a licença |
| R12 Ficha de direção de imagem | Bloco fixo "direção de fotografia igual em todas" e "proibido" (texto, logos, mascotes, fantasia, 3D). Assunto longe das bordas se a imagem será cortada. No máximo 2 gerações em paralelo | Quatro gerações em paralelo travaram o gerador [praticante] |
| R13 Reuso | Cada imagem no máximo 2 vezes, com recortes diferentes | Uma VSL longa, com mais de 300 cenas, usou menos de 70 imagens e clipes; sem limite de reuso, a mesma arte voltaria o tempo todo [praticante] |
| R14 Silêncio é cena | "Sem voz, só música" e "1 s de silêncio" entram como linha própria, com `-` no gatilho | O silêncio tem duração e entra na conta do tempo |
| R15 Pronúncia | Escreva a fala como o TTS deve ler; o dicionário fica no rosto (campo 15) | Sigla e nome estrangeiro saem errados |
| R16 Rodapé de contagem | Planos por tipo e custo de geração real. O validador compara a contagem com a tabela | Dá ao dono, de relance, o peso de cada origem e o custo de geração. A soma por tipo tem de fechar com o número de cenas |
| R17 Conferência por folha de contato | Antes do render, monte a folha com um quadro a cada 10 s (VSL) ou por cena (Reel), com a fala na tabela | Ver as imagens lado a lado acha o que a tabela esconde: repetição, imagem escura, quadro fora do padrão [praticante] |

## Exemplo de 10 cenas (adaptado)

É o Reel adaptado do [capítulo 02](02-folha-de-rosto.md), na versão curta. Os tempos são estimados com a régua da regra 4. O mesmo arquivo está em `skills/estudio-storyboard/references/exemplo-storyboard.md` e passa no validador.

- **Nome e versão:** Storyboard 1 · "A lavanderia que abre cedo" · ~39 s
- **Objetivo:** quem vende serviço de IA entende onde procurar a primeira venda
- **Sai pensando:** "dá pra eu fazer isso no meu bairro"
- **Sentimento:** curiosidade
- **Ideia:** uma lavanderia cheia de movimento gera dado o dia inteiro e ninguém olha; as câmeras e as máquinas que já existem viram a primeira venda
- **Linguagem visual:** fundo #0F1B2D, texto #F4EFE6, destaque #E07B39, fonte Anton nos títulos; caixas de detecção nunca sobre rosto
- **Códigos de tipo:** R real · IA imagem gerada · B banco · M motion · T tela real · S simulação (S leva o selo "exemplo")
- **Régua de tempo:** estimada com 2,33 palavras/s + 0,35 s entre falas; depois ancorada na palavra-gatilho medida
- **Trilha e SFX:** instrumental baixa, 15 dB abaixo da voz; 1 s de silêncio antes do CTA
- **Custo de geração (estimado):** 1 imagem gerada (valor a medir)
- **Versão curta:** 20 s, mesma ideia com metade das cenas

| # | Tempo | Fala | Gatilho | Tipo | Visual | Câmera / transição | Texto em tela | Som | Origem do asset | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| c01 | 0:00-0:03,8 | Essa lavanderia abre antes do sol, fecha tarde. | abre | R | Fachada ao amanhecer com o letreiro aceso | corte seco | ABRE ANTES DO SOL | impacto leve em 0:01 | `v01.mp4` 0:00-0:04 (PRÓPRIO) | conferido |
| c02 | 0:03,8-0:08 | Mas o controle de tudo ainda vive num caderno. | caderno | R | Atendente anotando num caderno no balcão, sem tela | push-in 1,00 a 1,06 | NO CADERNO | - | `v03.mp4` 0:02-0:06 (PRÓPRIO) | animado |
| c03 | 0:08-0:12,2 | Quem vende IA vê dado sobrando e ninguém lendo. | dado | R+M | Corredor com pessoas passando; contador "pessoas hoje:" vazio no canto | whip | DADO SOBRANDO<br>NINGUÉM LENDO | tic no contador | `v02.mp4` 0:00-0:04 + motion | animado |
| c04 | 0:12,2-0:16 | Começa pelas câmeras que já existem na loja. | câmeras | R+M | Câmera de teto da lavanderia com caixa de detecção em cada pessoa, nunca no rosto | zoom suave | CÂMERAS QUE JÁ EXISTEM | - | detecção real do `v02` (`deteccoes.json`) | animado |
| c05 | 0:16-0:20,2 | Cada máquina vira um sensor: livre, ocupada ou terminando. | máquina | S | Planta da loja com máquinas em verde, amarelo e vermelho | corte seco | EXEMPLO · MÁQUINAS | pop por máquina | motion; simulação marcada | animado |
| c06 | 0:20,2-0:24,4 | E o atendente recebe o alerta direto no celular. | atendente | IA | Atendente jovem olhando o celular com o alerta "Máquina 6 terminou" (genérico, sem marca) | corte seco | MÁQUINA 6 TERMINOU | blip | imagem gerada com foto de referência `balcao.jpg`; prompt "sem logo nem texto legível" | imagem aprovada |
| c07 | 0:24,4-0:29 | Para montar: câmera, computador pequeno e um agente de chat. | agente | M | Três blocos empilham: câmera, computador pequeno e uma conversa de chat genérica | whip | O QUE PRECISA | tic x3 | motion; ícones próprios | construído |
| c08 | 0:29-0:33,2 | Quanto cobrar? Uma taxa inicial e um valor mensal. | cobrar | M | Cartão de preço com selo ESTIMATIVA; valores pendentes | corte seco | REFERÊNCIA<br>NÃO É TABELA | impacto | motion; valores a confirmar com o criador | outline |
| c09 | 0:33,2-0:34,2 | (silêncio de 1 s, sem voz) | - | R | Corredor vazio ao fim da tarde, take mudo | fade | - | silêncio total | `v02.mp4` 0:08-0:09 (PRÓPRIO) | outline |
| c10 | 0:34,2-0:38,8 | Comenta LAVANDERIA e o material chega na sua conversa. | LAVANDERIA | R+M | Mesmo corredor; pílula "comenta LAVANDERIA" dentro da zona segura | corte seco | COMENTA LAVANDERIA | trilha volta e sobe 1 dB | `v02.mp4` 0:09-0:13 + motion | outline |

**Contagem:** 10 cenas = R 3, R+M 3, S 1, IA 1, M 2

**Custo de geração (real):** 1 imagem (c06), valor a medir.

Três escolhas do exemplo: o c05 é simulação e leva "EXEMPLO" no texto em tela; o c09 é silêncio, com linha própria e `-` no gatilho; nenhuma cena passa de 4,6 s, abaixo do teto padrão de 5 s.

## Folha de contato: os três momentos

A folha de contato é uma imagem com vários quadros lado a lado. Ela entra em três momentos do projeto, e cada uma fica em `qa/`:

| Momento | Etapa | O que mostra | Como gerar |
|---|---|---|---|
| 1. Material de entrada | 1 | Um quadro de cada take e as fotos recebidas, para catalogar e descartar | Um quadro por arquivo e `tile` (abaixo) |
| 2. Imagens geradas | 6 | As imagens do storyboard na ordem das cenas, para o dono escolher | Sequência numerada e `tile` (abaixo) |
| 3. Quadros finais | 11 | Um quadro a cada 8 a 10 s do vídeo pronto | `conferir_video.py` ([capítulo 10](10-conferencia-e-entrega.md)) |

Momento 1, com um quadro de cada take, todos na mesma moldura mesmo com formatos diferentes [testado]:

```bash
mkdir -p qa/_tmp; i=0
for f in _bruto/*.mp4; do i=$((i+1)); ffmpeg -v error -y -ss 1 -i "$f" -frames:v 1 \
  -vf "scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2" \
  -update 1 "qa/_tmp/t$(printf %03d $i).png"; done
ffmpeg -v error -y -framerate 1 -i qa/_tmp/t%03d.png \
  -vf "tile=6x4:margin=3:padding=3:color=0x404040" -frames:v 1 -update 1 qa/videos.jpg
```

Momento 2, com imagens numeradas `img_01.png`, `img_02.png`, e assim por diante [testado]:

```bash
ffmpeg -v error -y -framerate 1 -i imgs/img_%02d.png \
  -vf "scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2,tile=6x3:margin=3:padding=3:color=0x404040" \
  -frames:v 1 -update 1 qa/imgs.jpg
```

O fundo da grade é cinza de propósito: o preto é a cor de um quadro preto de verdade, e o fundo preto o esconderia. Ajuste `tile=6x4` ao número de arquivos. No Windows, rode os comandos no Git Bash ou peça ao agente que adapte o laço.

## Checagens automáticas

O `checar_storyboard.py` (em `skills/estudio-storyboard/scripts/`) lê o `STORYBOARD.md` e confere o que dá para decidir só com a tabela. Só biblioteca padrão do Python 3.10 ou mais novo. Código de saída 0 aprova, 1 reprova.

```
python checar_storyboard.py STORYBOARD.md
python checar_storyboard.py STORYBOARD.md --teto 3    # VSL
```

| Checagem | Regra | Quem faz |
|---|---|---|
| Colunas obrigatórias | As 9 existem e nenhuma célula obrigatória está vazia | `checar_storyboard.py` |
| Ids únicos | Nenhum id repetido | `checar_storyboard.py` |
| Tempo | Crescente, sem buraco e sem sobreposição; a primeira cena começa em 0:00 | `checar_storyboard.py` |
| Cena acima do teto | Falha acima de `--teto` segundos (padrão 5; use 3 em VSL) | `checar_storyboard.py` |
| Gatilho | A palavra do gatilho está na fala (cena sem voz leva `-`) | `checar_storyboard.py` |
| Tipo | R, IA, B, M, T, S, ou combinações com `+` | `checar_storyboard.py` |
| Simulação | Tipo S leva "exemplo" no texto em tela | `checar_storyboard.py` |
| Texto em tela | No máximo 2 linhas, separadas por `<br>` ou ` · ` | `checar_storyboard.py` |
| Status | Um dos cinco valores | `checar_storyboard.py` |
| Rodapé | A contagem por tipo bate com a tabela | `checar_storyboard.py` |
| Duração | Vídeo e áudio do arquivo final diferem em até 0,2 s | `conferir_video.py` |
| Asset ausente | Todo arquivo da coluna Origem existe | Não incluído; script do projeto |
| Buraco de legenda ou cartão | Intervalo sem texto (VSL); em Reel de cartões, buraco acima de 4 s ou cobertura abaixo de cerca de 80% | Não incluído; script do projeto |
| Cartão fora da fala | Compara a frase do cartão com a janela da fala e diz para onde mover | Não incluído; script do projeto |
| Voz passando do take | `início + duração da voz > duração do take - 0,1 s` | Não incluído; script de linha do tempo do projeto |

Testes que rodamos: o exemplo acima aprova, e 19 variações defeituosas dele (id repetido, buraco, sobreposição, cena longa, gatilho fora da fala, tipo inválido, simulação sem selo, rodapé errado, coluna faltando e outras) reprovam, cada uma na verificação certa [testado].

## Do STORYBOARD.md para o HyperFrames

A tabela converte para o `STORYBOARD.md` do HyperFrames sem perder campo. O formato dele tem um cabeçalho em YAML e uma seção `## Frame N` por cena, com `- chave: valor` [oficial]:

| Esta folha | HyperFrames |
|---|---|
| Cabeçalho: formato, duração, mensagem, arco, público | Cabeçalho YAML: `format`, `duration`, `message`, `arc`, `audience` |
| Tempo | `duration` (por exemplo, `4s`) |
| Visual | `scene` (legenda de uma linha da cena) |
| Fala | `voiceover` |
| Texto em tela e janela | `reads` (chave extra que o HyperFrames preserva) |
| Som | `sound` (chave extra) |
| Câmera / transição | `transition_in` |
| Status | `status`: outline e imagem aprovada viram `outline`; construído vira `built`; animado e conferido viram `animated` |
| Origem do asset | `asset` (chave extra, preservada em `extra`) |

## O que deu errado aqui

- **Foto solta.** Versões foram reprovadas por imagens que não mostravam o que a voz dizia. Daí a regra 1 [testado].
- **Cartão fora da fala e tela vazia.** Os projetos de VSL passaram a proibir cartão distribuído por régua em vez de pela fala e tela vazia por mais de 4 s. O gatilho e o teto de cena parada são a defesa [testado].
- **Texto sobre rosto.** A conferência achou texto encostando no cabelo de uma pessoa em um quadro de um Reel. Por isso a regra 9 pede snapshot em todo o intervalo, inclusive nos picos de escala [testado].
- **Arte repetida, sempre no mesmo enquadramento.** Uma leva de imagens foi reprovada por esse defeito. A ficha de direção de imagem (regra 12) existe para que todas partam da mesma fotografia e das mesmas proibições [praticante].
- **Gerador travado.** Quatro gerações de imagem em paralelo travaram o gerador. O limite é 2 [praticante].
- **Checador perdido.** O plano de uma VSL descrevia um `checar.py` que ficou numa pasta de trabalho descartável e não foi encontrado depois. Uma tabela em Markdown permite reimplementar as checagens sem depender de HTML, e foi o que fizemos neste validador [praticante].

## Links

- [Workflow completo](01-workflow-completo.md): a etapa 6 e o portão "Quadros e fala".
- [Folha de rosto](02-folha-de-rosto.md): de onde o storyboard herda arco, linguagem visual e vetos.
- [Conferência e entrega](10-conferencia-e-entrega.md): a folha de contato final e o `conferir_video.py`.
- [Modelo STORYBOARD.md](../modelos/STORYBOARD.md): tabela em branco.
- [Skill estudio-storyboard](../skills/estudio-storyboard/SKILL.md) e [validador](../skills/estudio-storyboard/scripts/checar_storyboard.py).
- [HyperFrames](https://github.com/heygen-com/hyperframes): formato `STORYBOARD.md` de referência.
