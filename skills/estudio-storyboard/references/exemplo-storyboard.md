# STORYBOARD · REEL-LAVANDERIA-AAAA-MM-DD · v1 (EXEMPLO ADAPTADO)

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
