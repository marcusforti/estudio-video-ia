# Análise do grafo

Rodamos o [graphify](https://github.com/Graphify-Labs/graphify) em tudo o que está neste repositório: capítulos, modelos, skills e scripts. Ele transforma os arquivos num mapa de conceitos ligados entre si. A pergunta era simples: olhando o conjunto, o que parece central, o que está solto e onde mora o risco?

[Abrir o grafo interativo](/static/grafo-interativo.html). Dá para buscar um conceito, clicar num nó e ligar ou desligar cada grupo.

## Resumo em 30 segundos

- O ponto mais conectado do fluxo é a voz, não o motion. Voz liga licença, GPU, roteiro, conferência e lei.
- Licença e consentimento são a segunda maior ponte. Quase toda escolha de ferramenta passa por eles.
- HyperFrames é a única ferramenta entre os nós mais conectados. É a maior dependência técnica do fluxo.
- A GPU alugada é a estrada comum de voz, lip sync e render.
- Os dois grupos mais soltos são consentimento e aluguel de GPU: juntam assunto demais e pedem divisão.

## Os números

| Medida | Valor |
|---|---|
| Arquivos analisados | 84, com cerca de 108 mil palavras |
| Conceitos (nós) | 1.447 |
| Ligações (arestas) | 3.091 |
| Grupos de assuntos | 76 |
| Ligações explícitas no texto | 2.831 (92%) |
| Ligações inferidas | 253 (8%), confiança média de 0,87 |
| Ligações ambíguas | 7 |

Ligação explícita é a que está escrita no arquivo. Inferida é uma leitura do modelo, com nota de confiança. Ambígua ficou marcada para revisão.

## O que é central

Conexões contam quantas ligações um conceito tem. Ponte mede quantos caminhos entre assuntos diferentes passam por ele: quanto maior, mais coisa depende dele.

| Conceito | Conexões | Ponte |
|---|---|---|
| Voz local | 39 | 0,137 |
| Licenças e consentimento | 31 | 0,132 |
| Pesquisa de estado da arte | 20 | 0,127 |
| Workflow completo | 31 | 0,119 |
| Skill de GPU | 23 | 0,110 |
| GPU como local | 25 | 0,109 |
| Motion por código | 33 | 0,103 |

Folha de storyboard, com 32 conexões, e lip sync, também com 32, vêm logo atrás em conexões. O termo de autorização tem 31 sozinho, o que diz muito: um documento de poucas páginas liga voz, rosto, lip sync, GPU e entrega.

## O que isso quer dizer na prática

**O risco mora na voz.** Quem olha um vídeo pronto acha que a parte difícil é o motion. O grafo mostra outra coisa: motion é grande, mas fica num canto bem resolvido, com regras e receitas. Voz encosta em licença de modelo, dado sensível, GPU alugada, pronúncia, conferência e rótulo de plataforma. Um erro ali vaza para o resto do projeto. Por isso a trava de consentimento vem antes do primeiro teste.

**Licença é decisão de arquitetura.** Ela não é nota de rodapé. O capítulo de licenças é a segunda maior ponte porque decide quais modelos podem entrar. Em lip sync, um detector de rosto só para pesquisa elimina um modelo inteiro para uso comercial. Confira a licença antes de testar qualidade.

**HyperFrames é um ponto único.** Composição, render, storyboard e receitas de motion dependem dele. Hoje isso funciona bem, e a licença Apache-2.0 reduz o risco. Mas vale fixar a versão usada em cada projeto, porque uma mudança ali afeta quase toda a montagem.

**A GPU é infraestrutura compartilhada.** Voz, lip sync e render pesado usam o mesmo ciclo: alugar, rodar, baixar, conferir, destruir. Daí a skill de GPU ser separada. Melhorar esse ciclo melhora os três.

## O que está solto

| Achado | Leitura | O que fazer |
|---|---|---|
| "Consentimento e clonagem de voz" tem coesão de 0,06 | Junta lei, plataforma, provedor e modelo no mesmo grupo | Separar em "o que a lei diz" e "o que cada ferramenta exige" |
| "Aluguel de GPU e preços" tem coesão de 0,08 | Preço, segurança e operação estão misturados | Manter a tabela de preços separada, porque ela envelhece rápido |
| 274 conceitos têm no máximo uma ligação | Em boa parte são fontes, selos e itens de referência | Normal em manual. Só preocupa se for regra importante sem nenhum uso |
| Regras repetidas em várias skills | Destruir a máquina e guardar chave em variável aparecem em mais de um lugar | Intencional, porque cada skill precisa funcionar sozinha. Ao mudar uma regra, atualize todas |
| Modelos copiados dentro das skills | Termo de autorização e folhas existem em `modelos/` e em `references/` | Mantenha as cópias iguais |

## Como ler com cuidado

- O grafo mostra estrutura, não qualidade. Muitas ligações não significam que o assunto está certo.
- Os capítulos têm tamanhos diferentes, e capítulo maior tende a ter mais ligações.
- 33 dos 67 documentos receberam correções pequenas depois da extração. Ajustamos os nós afetados, mas não refizemos a extração inteira. A estrutura geral não muda, e detalhes de um nó podem estar levemente atrás do texto.
- A extração usou 4 agentes e cerca de 2 milhões de tokens no total. O relatório da ferramenta mostra zero porque ela não recebe esse número nesse modo.

## Links

- [Grafo interativo](/static/grafo-interativo.html): o mapa completo no navegador.
- [graphify](https://github.com/Graphify-Labs/graphify): a ferramenta usada.
- [Voz local](05-voz-local.md): o ponto mais conectado.
- [Licenças e consentimento](11-licencas-e-consentimento.md): a segunda maior ponte.
