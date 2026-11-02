# Escolher o gancho e os cortes

Gancho é o trecho mais forte do vídeo colocado no começo. Depois dele o vídeo segue do início do corpo. É a decisão que mais muda o resultado, e é a sua: o script só executa.

## Método, nesta ordem

1. **Leia a fala inteira** (`python <skill>/scripts/cortar.py --transcricao palavras.json --texto`). Pegar a abertura só porque é conveniente é o erro mais comum.
2. **Liste de 3 a 5 candidatos, com tempo.** Os tipos que costumam parar o dedo, sempre concretos e nunca a tese abstrata. Exemplos inventados:
   - dor nomeada: "Você atende o dia inteiro e no fim do mês não sobra nada."
   - afirmação contra o senso comum: "Postar todo dia não faz sua loja vender mais."
   - ameaça ou perda: "Quem demora cinco minutos para responder perde o cliente."
   - pergunta provocativa que o vídeo responde: "Por que o cliente some depois de pedir o orçamento?"
   - número surpreendente: "Em quarenta minutos dá para responder duzentos clientes."
3. **Ranqueie por "isso faz parar o dedo?"** e fique com o primeiro, onde ele estiver. A frase forte quase sempre está no meio ou no fim do bruto.
4. **Complete o arco.** Se o candidato é preparação seguida de revelação, o gancho inclui a revelação. Uma versão que levou só a preparação da frase ficou morna, e a que incluiu a revelação funcionou [testado].
5. **Traga a tensão para os 3 primeiros segundos.** Se a preparação é longa, passe dois intervalos em `--gancho` e deixe de fora o miolo.
6. **Não repita a abertura.** Se o gancho é a primeira frase do corpo, ela toca duas vezes seguidas e parece falha. Puxe o gancho de outro ponto ou comece o corpo depois dele (`--inicio-corpo` igual ao fim do gancho). O script avisa quando o gancho cai nos 10 primeiros segundos do corpo; repetido mais tarde, ele fixa a frase em vez de soar como erro [praticante].
7. **Mostre ao dono do vídeo** o texto e o tempo do gancho antes de renderizar.

## Como passar ao script

```
--gancho "42.5-48.0,50.2-51.6"
```

Dois trechos colados; a pausa entre eles sai. O script encosta as pontas no limite das palavras e acrescenta a folga. Os tempos saem do `--texto`, em segundos.

## Corpo

| Opção | Use quando | Observação |
|---|---|---|
| `--inicio-corpo` | os primeiros segundos são aquecimento ("então...", "deixa eu ver") | em bruto de celular com falso começo (a pessoa começa, é interrompida e recomeça a mesma fala), comece na última tomada limpa [testado] |
| `--fim-corpo` | a saída é fraca ou há conversa depois do fim | |
| `--remover` | vício ou interrupção curta no meio da fala | gera jump cut visível: só com aval do dono do vídeo [testado]. Os intervalos removidos não ganham folga |

Cada corte tem de fechar um arco sozinho. Na dúvida, estenda: 20 segundos a mais valem mais que um corte que termina no meio da ideia [testado].

## Quando não editar

- Entrevista com sobreposição de vozes, ou áudio ruim: pule o vídeo [testado].
- Transcrição em que a mesma frase se repete quatro ou cinco vezes, ou com linhas sem sentido: o Whisper inventou texto sobre áudio ruim. Descarte o vídeo; não tente cortar [testado].
- Outra pessoa identificável no quadro ou na fala (videochamada, entrevista): peça autorização ao dono do vídeo antes de continuar.
- Nunca monte gancho e cortes que mudem o sentido do que a pessoa disse.

## Um caso

Um bruto de pouco mais de 3 minutos virou um corte de cerca de 2 minutos: gancho em forma de pergunta puxado do meio do vídeo, corpo começando por volta de 20 s (aquecimento fraco), folga depois de cada trecho em 0,18 s. A versão anterior, sem essa folga, cortava o fim das palavras. O dono do vídeo aprovou o corte [testado].
