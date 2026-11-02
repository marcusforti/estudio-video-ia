# /escolhermotion: escolher uma referência de motion e adaptar o prompt

Este capítulo explica de ponta a ponta uma forma de começar um motion por uma referência em vez de uma folha em branco: buscar numa coleção pública de prompts de vídeos feitos com Claude Opus 5.5, escolher 3 a 5 opções, adaptar o prompt mantendo a mecânica (ritmo, câmera, transição, técnica), trocar conteúdo e marca, produzir e conferir. É para quem usa agente de código e pede "um motion tipo aquele". A skill pública é a [estudio-escolher-motion](../skills/estudio-escolher-motion/SKILL.md). Selos entre colchetes: [oficial] documento da fonte; [testado] rodamos aqui; [fornecedor] quem vende diz, sem confirmação; [praticante] opinião de quem faz, sem medição; [sem medição] não existe número confiável.

## Resumo em 30 segundos

- A coleção `awesome-opus5-5-videos` (repositório MIT) tem 703 prompts, não 703 vídeos: 418 têm página de vídeo e 285 só têm o post no X. Em 207 dos 703, o criador publicou o prompt só em parte.
- Cada vídeo e cada prompt pertence ao criador. Aqui valem só link e crédito: não copie nem republique prompt, capa ou prévia.
- O fluxo é: pedido em uma frase, busca, 3 a 5 opções, prompt adaptado (mecânica fica, conteúdo e marca trocam), produção com SPEC e portões, conferência e crédito.
- O `buscar.py` da skill usa só a biblioteca padrão e acha a coleção por `--base` ou pela variável `MOTION_REFS_DIR`.
- A coleção é de posts virais escolhidos pelos criadores: serve como fonte de padrões de prompt, não como prova de resultado.

## O fluxo

Cada passo termina numa saída que a pessoa pode ver. Se você já tem a coleção clonada, comece no passo 1. No [workflow completo](01-workflow-completo.md), esta busca é a etapa 3, referência de estilo.

<!-- diagrama:escolhermotion-fluxo -->

| Passo | O que fazer | Saída |
|---|---|---|
| 0 | Clonar a coleção e apontar o caminho (`--base` ou `MOTION_REFS_DIR`) | `--resumo` mostra 703 prompts |
| 1 | Resumir o pedido em uma frase: para quê, plataforma, formato, duração, marca | Uma frase |
| 2 | Buscar com termos em inglês | Lista ordenada |
| 3 | Escolher 3 a 5 opções e mostrar uma linha cada | Opções com selo e link |
| 4 | Ler o prompt escolhido com `--ver` | Prompt na tela, não na página |
| 5 | Extrair a mecânica numa ficha | Ficha de mecânica |
| 6 | Escrever o prompt adaptado com o conteúdo e a marca da pessoa | Prompt adaptado |
| 7 | Produzir: SPEC, código, quadros e fala aprovados, render | MP4 conferido |
| 8 | Creditar e entregar ao dono | `CREDITOS.md` e arquivo |

## De onde vêm os dados

| Item | O que é | Selo |
|---|---|---|
| Repositório | `yihui-dev/awesome-opus5-5-videos`. Licença MIT, "Copyright (c) 2026 yihui-dev". O último commit que vimos é de 13/10/2026 e deixa a lista em 703 prompts | [oficial] |
| Direitos | O README diz que "every video and prompt belongs to its creator". A MIT cobre o repositório, não a obra de terceiros: é nossa leitura, não aconselhamento jurídico | [oficial], leitura nossa |
| Vitrine | O Skillry (skillry.dev) mostra o original e um remake lado a lado. Remake é a recriação do vídeo que o próprio Skillry diz ter feito com Opus 5.5 a partir do prompt do criador | [fornecedor] |
| Formato | `data/videos.json` (lista de 703 objetos) e `prompts/<slug>.md` (703 arquivos). Campos: `slug`, `author`, `author_url`, `post_url`, `category`, `tech_tags`, `prompt`, `prompt_partial`, `poster_url`, `skillry_url`, `added`, `has_remake` | [testado] |
| Modelo | Claude Opus 5.5, lançado em 22/09/2026. O post de lançamento não fala de motion design | [oficial] |

O Skillry é um mercado de skills com assinatura paga e põe parâmetros de campanha nos links [fornecedor]. Os posts são virais escolhidos pelos criadores, então há viés de sobrevivência. Não achamos avaliação independente de qualidade nem de desempenho de público [sem medição].

## Os números certos

Contagem nossa sobre a cópia local do JSON, em 01/11/2026 [testado]. O `python scripts/buscar.py --resumo` repete a conta na sua cópia.

| O quê | Quantos |
|---|---|
| Prompts (registros) | 703 |
| Com página de vídeo no Skillry (`has_remake`) | 418 |
| Só com o post no X | 285 |
| Prompts parciais (`prompt_partial`) | 207 |

| Categoria | Total | Com vídeo | Só post |
|---|---|---|---|
| `motion` | 369 | 229 | 140 |
| `3d` | 117 | 56 | 61 |
| `explainer` | 116 | 68 | 48 |
| `interactive` | 101 | 65 | 36 |

Mais números sobre o conteúdo:

- `tech_tags` (canvas 267, svg 183, threejs 131, shader 92, gsap 86, css 57, audio 39, entre outras) descreve a tecnologia do remake do Skillry, não necessariamente a do vídeo original, e vem vazio nos 285 só-post.
- O prompt tem de 11 a 15.583 caracteres, com mediana de 221.
- Só 25 a 26 dos 703 mencionam vertical (9:16, 1080x1920 ou a palavra "vertical") e 37 citam paisagem (16:9 ou 1920x1080); a conta varia um pouco com a expressão usada. A maioria não declara formato: trate toda referência como horizontal até assistir, e adapte para 1080x1920.
- O README destaca 100 vídeos e conta 58 em motion, 16 em explainers, 14 em 3D e 12 em jogos: são os destaques, não a base inteira.
- A galeria do Skillry anunciava 475 vídeos em 01/11/2026 [fornecedor], contra 703 prompts e 418 remakes no README [oficial]. Não conseguimos reconciliar.

## Como a busca funciona

Preparação, uma vez:

```
git clone https://github.com/yihui-dev/awesome-opus5-5-videos
export MOTION_REFS_DIR=CAMINHO/awesome-opus5-5-videos      # PowerShell: $env:MOTION_REFS_DIR = "CAMINHO\..."
git -C CAMINHO/awesome-opus5-5-videos pull                 # para atualizar
```

Uso, na pasta da skill:

```
python scripts/buscar.py "dashboard numbers" --cat motion --com-video --n 5
python scripts/buscar.py --ver SLUG
python scripts/buscar.py --resumo
```

| Opção | Efeito |
|---|---|
| (termos) | Palavras da busca, de preferência em inglês |
| `--base PASTA` | Pasta da coleção (vence a variável `MOTION_REFS_DIR`) |
| `--cat X` | Só uma categoria: `motion`, `3d`, `explainer` ou `interactive` |
| `--com-video` | Só entradas com página de vídeo |
| `--n N` | Quantos resultados mostrar (padrão 8) |
| `--ver SLUG` | Prompt completo da sua cópia local, com autor, post e vídeo |
| `--resumo` | Contagem por categoria, com vídeo e só post |

Como ordena [testado]: o texto pesquisável é o título, o prompt e as tags, em minúsculas. Cada termo soma o número de vezes em que aparece (por substring, sem radical nem sinônimo) e conta o triplo se aparece no título. Quem tem página de vídeo ganha 0,5 de desempate. Entra quem tem qualquer termo, não todos. Dois efeitos práticos: em 418 entradas o título é genérico (`Opus 5.5 video by @autor`), então o que decide é o corpo do prompt; e termos em português quase não acham nada, porque os prompts são em inglês.

Cada resultado mostra título, categoria, tags, o selo `[vídeo]` ou `[só post]`, o slug, o autor e o link do post, o link do vídeo (quando existe) e o começo do prompt. O script só lê: não altera a pasta da coleção, não abre navegador e não grava arquivo.

Quando algo falta, ele explica em vez de quebrar: sem coleção, ensina o `git clone` e as duas formas de apontar o caminho; com slug inexistente, sugere slugs parecidos; sem resultado, diz que termos tentar; categoria desconhecida lista as que existem.

## Categorias: o que esperar de cada uma

| Categoria | Quando olhar primeiro |
|---|---|
| `motion` (369) | Tipografia cinética, número subindo, vinheta, anúncio curto, lançamento de produto |
| `explainer` (116) | Explicar um processo, uma receita, um método, passo a passo |
| `3d` (117) | Cena 3D, ambiente, produto girando, sensação de profundidade |
| `interactive` (101) | Páginas e jogos que reagem ao usuário (22 levam a tag `playable`). Como referência de vídeo vale a parte visual: o clique não vira vídeo linear |

Para reel, comece por `motion` e `explainer`.

## Como escolher 3 a 5 opções

1. Rode a busca com `--com-video` e `--n 12`; se faltar opção, repita sem `--com-video`. Prefira `[vídeo]`: dá para assistir o original antes de decidir.
2. Use `[só post]` só se o post abrir e mostrar o vídeo. Se não abrir, descarte.
3. Escolha opções com mecânicas diferentes entre si (por exemplo, uma de tipografia, uma de câmera, uma de dados). Três variações do mesmo truque não são opções.
4. Descarte prompt parcial se a mecânica que você quer não estiver clara: o criador publicou só parte, ou a coleção traz o post que descreve o resultado (o README diz que, sem prompt publicado, a entrada leva o post original). Nesse caso, assista ao vídeo e descreva a mecânica com as suas palavras.
5. Mostre cada opção em uma linha: o que ela tem de bom para o seu pedido, a categoria, o selo e o link. Se a pessoa já disse qual quer, escolha e conte qual escolheu e por quê.

## Como adaptar um prompt mantendo a mecânica

Adaptar é separar duas listas. A mecânica fica. O resto troca.

| Fica (mecânica) | Troca |
|---|---|
| Ritmo: duração, quantas ideias, intervalo entre elas | Todo texto, número e nome |
| Câmera: empurrão, voo, parada | Paleta, fontes e logo |
| Transição: corte duro, whip, zoom, flash | Idioma e tom de voz |
| Técnica: tipografia cinética, SVG, Three.js, contador | Formato, se a referência for horizontal |
| Estrutura: gancho, desenvolvimento, fecho | Duração, se o conteúdo pedir |
| Som: onde entra, com que causa | Qualquer arte, foto ou marca de terceiros |

Escreva primeiro uma ficha de mecânica (ritmo, câmera, transições, técnica, papel do texto, som, estrutura), sem copiar frase do prompt original. Depois escreva o prompt adaptado em cima da ficha, com o conteúdo exato da pessoa, a marca dela, a área segura e o contrato técnico. Nada de preço, depoimento ou número que a pessoa não deu.

### Exemplo completo

Exemplo nosso, com marca e valores fictícios. A referência é hipotética: descrevemos só a mecânica, como você faria com uma entrada real.

**Pedido em uma frase:** story vertical de 15 s para a cafeteria fictícia "Café Exemplo" anunciar o combo da manhã.

**Referência (hipotética):** filme de lançamento de produto de 15 s. Abre com uma palavra gigante que bate na batida, corta duro entre fundo claro e escuro, empurra a câmera 6% a cada cena, faz um número subir até o valor final, traz uma ideia nova a cada 2 s (7 cenas) e fecha com o nome da marca parado por 1 s.

**Ficha de mecânica:**

| Item | Valor |
|---|---|
| Ritmo | 15 s; ideia nova a cada 2 a 2,5 s |
| Câmera | Empurrão de 6% por cena (`scale 1 → 1,06`), sem rotação |
| Transições | Corte duro na batida, fundo claro e escuro alternados; um flash de 120 ms só na virada do gancho |
| Técnica | Tipografia cinética, contador, formas vetoriais, GSAP |
| Texto | Uma palavra gigante por cena (1 a 3 palavras); o número é o protagonista |
| Som | Golpe curto em cada corte; riser de 1 s antes do número; 0,3 s de silêncio antes do fecho |
| Estrutura | Gancho, problema, produto, preço, chamada |

**O que troca:** as 7 cenas viram 6, porque o conteúdo tem 6 informações (o intervalo médio de 2,5 s continua). Textos em português, caixa alta. Preço de R$ 18,90, valor fictício. Paleta e fonte da cafeteria.

**Prompt adaptado (texto nosso, não copiado de nenhuma entrada da coleção):**

```text
Crie um filme vertical de 15 s (1080x1920, 30 fps) para o story da cafeteria "Café Exemplo",
com HTML e GSAP numa única timeline pausada registrada em window.__timelines.
Bibliotecas locais, sem rede, sem Math.random sem semente.

MECÂNICA (inspirada numa referência de lançamento de produto; só a mecânica, nenhum texto,
marca ou arte do original):
- uma ideia nova a cada 2 a 2,5 s, em 6 cenas;
- uma palavra gigante (1 a 3 palavras) bate na batida de cada cena;
- cortes duros alternando fundo claro e escuro; flash branco de 120 ms só na virada do gancho;
- a câmera empurra 6% em cada cena (scale 1 → 1,06);
- o preço sobe como contador até o valor final;
- som curto em cada corte, riser de 1 s antes do preço, 0,3 s de silêncio antes do fecho.

ROTEIRO (use exatamente estes textos e números, não invente nada):
 0,0 a  2,0  "SEGUNDA, 7H." (gancho: a palavra estoura no primeiro quadro)
 2,0 a  4,5  "CAFÉ FRACO?"
 4,5 a  7,0  "COMBO DA MANHÃ"
 7,0 a  9,5  "CAFÉ + PÃO DE QUEIJO"
 9,5 a 12,0  contador até "R$ 18,90"
12,0 a 15,0  "PASSA AQUI" e o nome "CAFÉ EXEMPLO", parado nos últimos 1,5 s

MARCA: marrom #3B2314, creme #F4E9D8 e laranja #D9531E (um acento só, em até 8% da tela).
Fonte Oswald, caixa alta. O nome da marca entra como texto; sem logo de terceiros.

ÁREA SEGURA: tudo em x 80 a 940 e y 250 a 1440; nada nos últimos 480 px.

VERIFICAÇÃO: rode `npx hyperframes check --json` e `npx hyperframes snapshot --review`
e mostre a folha de quadros antes de renderizar.
```

**Depois do prompt:** a pessoa aprova a SPEC, o agente escreve o código, mostra a folha de quadros com a área segura e a fala, e só então renderiza. O `CREDITOS.md` fica assim, com os dados que o `--ver` mostrou:

```text
Mecânica (ritmo, câmera e transições) inspirada em @AUTOR
Post original: LINK_DO_POST
Coleção: github.com/yihui-dev/awesome-opus5-5-videos (MIT; vídeos e prompts pertencem aos criadores)
Nenhum texto, marca ou arte do original foi copiado.
```

## Produzir e conferir

Produza com a skill [estudio-motion](../skills/estudio-motion/SKILL.md), que impõe a SPEC antes do código, o portão de quadros e fala antes do render e a área segura. O motor recomendado é o HyperFrames; as skills oficiais dele (Apache-2.0, HeyGen) se instalam, segundo o README do projeto, com `claude plugin marketplace add heygen-com/hyperframes`. Não testamos essa instalação aqui. O [capítulo 08](08-motion.md) traz o contrato, o render em pedaços e as receitas, e a conferência final segue o [capítulo 10](10-conferencia-e-entrega.md).

Confira, nesta ordem:

1. **Conteúdo.** Cada texto, número e nome do vídeo bate com o que a pessoa forneceu. Nada do original sobrou.
2. **Mecânica.** Assista ao original e ao seu lado a lado: mesmo número de ideias por segundo, mesma câmera, mesmo tipo de corte.
3. **Quadros.** Folha de quadros com a área segura por cima (`area_segura.py` da skill estudio-motion), rosto livre e texto legível.
4. **Fala.** Se há voz, transcreva o MP4 final e compare com o roteiro.
5. **Arquivo.** `ffmpeg -v error -i final.mp4 -f null -` não imprime nada.
6. **Entrega.** Primeiro só ao dono do vídeo. Publicar só com o ok dele.

## Termos de busca por tipo de negócio

Em inglês, porque os prompts são em inglês. Rodamos cada conjunto na coleção em 01/11/2026 e todos acharam resultados [testado]; o total é de entradas com algum dos termos.

| Uso | Buscar | Entradas |
|---|---|---|
| Cardápio animado para stories (hamburgueria, confeitaria) | `recipe menu food burger` | 10 |
| Oferta ou Black Friday de loja | `product launch sale price commercial` | 130 |
| Gráfico ou resultado do negócio (painel, caso de cliente) | `chart dashboard data numbers` | 51 |
| Vinheta de abertura de reels ou série | `title sequence intro opening` | 59 |
| Anúncio de imóvel | `house architecture 3d room` | 139 |
| Desafio de academia, palavra do dia, promoção de clínica | `countdown typography kinetic text` | 88 |
| Explicar um método ou processo | `explainer diagram process` | 50 |

Como o vídeo é código, preço, cor e marca saem exatos. Termos amplos como `product launch` trazem muita entrada: combine com `--cat` e `--com-video` para reduzir a lista.

## Regras de crédito

- Credite o autor e o link do post em um `CREDITOS.md` ao lado do vídeo e, se a mecânica for claramente a dele, na legenda da publicação.
- Cite a coleção (`github.com/yihui-dev/awesome-opus5-5-videos`, MIT; vídeos e prompts pertencem aos criadores).
- No site, no repositório e em redes: só link e crédito. Não publique prompt, capa nem prévia, nem parafraseando de perto.
- Não copie texto, marca, logo nem arte do original.
- Se um criador pedir remoção de um trabalho seu, atenda. O README da coleção diz que ele pode abrir uma issue para isso [oficial]. A política de licenças do repositório está no [capítulo 11](11-licencas-e-consentimento.md).

## O que deu errado aqui

- **"703 vídeos" na descrição da primeira versão da nossa skill.** São 703 prompts e 418 vídeos. Corrigido neste capítulo e na skill pública.
- **Link vazio em 285 de 703 resultados.** A versão interna imprimia `ver: None` para quem não tem página no Skillry e escondia o link do post, que é o que serve. A versão pública marca `[só post]` e mostra o post.
- **Slug errado derrubava o script com erro técnico.** Agora o script diz que o slug não existe e sugere parecidos.
- **Busca vazia sem aviso, e busca em português sem resultado.** Agora o script explica e pede termos em inglês.
- **`--ver` sem autor nem post.** Dava trabalho montar o `CREDITOS.md`. Agora mostra os dois.
- **Título genérico em 418 entradas.** A lista de resultados fica ilegível sem o começo do prompt: o script mostra autor e trecho.
- **Prompt parcial tratado como completo.** Em 207 entradas o criador publicou só parte. O script avisa.

## Links

- [awesome-opus5-5-videos (MIT)](https://github.com/yihui-dev/awesome-opus5-5-videos): coleção de prompts e links; vídeos e prompts pertencem aos criadores.
- [Skillry, galeria Opus 5.5](https://skillry.dev/ai-videos/opus-5-5): original e remake lado a lado.
- [Claude Opus 5.5, anúncio](https://www.anthropic.com/claude-opus-5-5): modelo, data e preços.
- [HyperFrames](https://github.com/heygen-com/hyperframes) e [guia rápido](https://hyperframes.heygen.com/quickstart): motor e skills oficiais.
- [Capítulo 08](08-motion.md): motion por código, área segura e render. [Workflow](01-workflow-completo.md), [conferência e entrega](10-conferencia-e-entrega.md) e [licenças e consentimento](11-licencas-e-consentimento.md): onde este fluxo se encaixa.
