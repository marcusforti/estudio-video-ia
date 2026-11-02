# Adaptar um prompt mantendo a mecânica

Adaptar é separar duas listas. A mecânica fica. O resto troca.

| Fica (mecânica) | Troca |
|---|---|
| Ritmo: duração, quantas ideias, intervalo entre elas | Todo texto, número e nome |
| Câmera: empurrão, voo, parada | Paleta, fontes e logo |
| Transição: corte duro, whip, zoom, flash | Idioma e tom de voz |
| Técnica: tipografia cinética, SVG, Three.js, contador | Formato, se a referência for horizontal |
| Estrutura: gancho, desenvolvimento, fecho | Duração, se o conteúdo pedir |
| Som: onde entra, com que causa | Qualquer arte, foto ou marca de terceiros |

## Ficha de mecânica (modelo)

Escreva com as suas palavras, sem copiar frase do prompt original.

```
Ritmo:        duração total; número de ideias; intervalo médio entre ideias
Câmera:       o que faz em cada cena
Transições:   tipos e onde ocorrem
Técnica:      tipografia cinética | SVG | canvas | Three.js | GSAP ...
Texto:        papel do texto em cada cena (não o conteúdo)
Som:          onde entra e com que causa visível
Estrutura:    gancho, desenvolvimento, fecho, com os intervalos de tempo
```

## Prompt adaptado (modelo)

```
Crie um filme <formato, fps, duração> para <marca>, com <motor>, numa única timeline pausada.
Bibliotecas e fontes locais, sem rede.

MECÂNICA (inspirada em uma referência; só a mecânica, nenhum texto, marca ou arte do original):
- <itens da ficha, um por linha>

ROTEIRO (use exatamente estes textos e números, não invente nada):
<tempo inicial a tempo final  "texto" ou descrição da cena>

MARCA: <cores em hex, um acento só>, <fonte>, <como o nome da marca entra>.
ÁREA SEGURA: x 80 a 940 e y 250 a 1440 em 1080x1920; nada nos últimos 480 px.
VERIFICAÇÃO: check, snapshot e folha de quadros antes de renderizar.
```

## Exemplo completo (marca e valores fictícios)

Pedido: story vertical de 15 s para a cafeteria fictícia "Café Exemplo" anunciar o combo da manhã.

Referência hipotética, só a mecânica: filme de lançamento de produto de 15 s que abre com uma palavra gigante na batida, corta duro entre fundo claro e escuro, empurra a câmera 6% a cada cena, faz um número subir até o valor final, traz uma ideia nova a cada 2 s (7 cenas) e fecha com o nome da marca parado por 1 s.

Ficha de mecânica:

```
Ritmo:        15 s; ideia nova a cada 2 a 2,5 s
Câmera:       empurrão de 6% por cena (scale 1 → 1,06), sem rotação
Transições:   corte duro na batida, fundo claro e escuro alternados; flash de 120 ms só na virada do gancho
Técnica:      tipografia cinética, contador, formas vetoriais, GSAP
Texto:        uma palavra gigante por cena (1 a 3 palavras); o número é o protagonista
Som:          golpe curto em cada corte; riser de 1 s antes do número; 0,3 s de silêncio antes do fecho
Estrutura:    gancho, problema, produto, preço, chamada
```

O que troca: as 7 cenas viram 6, porque o conteúdo tem 6 informações (o intervalo médio de 2,5 s continua). Textos em português, caixa alta. Preço de R$ 18,90, valor fictício. Paleta e fonte da cafeteria.

Prompt adaptado:

```
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

Depois do prompt: a pessoa aprova a SPEC, o agente escreve o código, mostra a folha de quadros com a área segura e a fala, e só então renderiza.
