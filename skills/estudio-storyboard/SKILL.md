---
name: estudio-storyboard
description: Use quando o roteiro (e, se já houver, o tempo da voz) estiver pronto e for preciso planejar as cenas antes de gerar imagem ou renderizar - "faz o storyboard", "monta a folha de cenas", "quais imagens uso em cada fala", "valida o storyboard" - ou quando uma versão foi reprovada porque a imagem não combinava com a fala.
---

# Folha de storyboard

Escreve e valida o `STORYBOARD.md`: a tabela cena a cena que liga o que a voz diz ao que o público vê. A regra que manda: **a imagem mostra literalmente o que a voz diz**. Nunca foto solta.

Nos comandos, `<skill>` é a pasta desta skill.

## Portões obrigatórios

- **Quadros e fala.** A tabela e a folha de contato vão ao dono do vídeo e esperam o ok antes de qualquer render. Arte em etapas: você gera, o dono escolhe, só então você monta.
- **Gasto.** Imagem gerada com serviço pago: mostre a estimativa (imagens x custo unitário) e espere ok com teto. No máximo 2 gerações em paralelo.
- **Consentimento.** Rosto, voz ou imagem de terceiros só com termo escrito. Foto de referência de rosto só de quem autorizou.
- **Dono primeiro.** A folha e as imagens vão só ao dono, nunca a terceiros.

## Passo a passo

1. Leia o `ROSTO.md` (arco, linguagem visual, vetos, regra de imagem), o roteiro por blocos e, se existirem, os tempos da voz.
2. Copie `references/STORYBOARD.md` para a raiz do projeto e preencha o cabeçalho.
3. Divida o roteiro em cenas: uma ideia por cena, uma troca de imagem por ideia.
4. Preencha a tabela (colunas e regras abaixo).
5. Valide e corrija até passar:

```
python <skill>/scripts/checar_storyboard.py STORYBOARD.md --teto 5
```

Use `--teto 3` em VSL. O código de saída é 0 se aprova e 1 se reprova.

6. Monte a folha de contato das imagens (comando em `references/regras.md`) e compare cada quadro com a fala da sua cena.
7. Envie tabela e folha ao dono. Espere o ok. Registre a decisão na coluna Nota do portão e no campo 26 do rosto.

## Colunas

Obrigatórias: `#`, Tempo, Fala, Gatilho, Tipo, Visual, Texto em tela, Origem do asset, Status. Opcionais: Bloco, Câmera / transição, Som, Checagens, Nota do portão.

| Coluna | Como preencher |
|---|---|
| `#` | Id estável (`c01`). Para inserir, use `c04b`; não renumere |
| Tempo | `0:03,8-0:08`. Estime com 2,33 palavras/s + 0,35 s entre falas; com a voz pronta, use o tempo medido da palavra-gatilho |
| Fala | Texto exato que a voz lê. Cena sem voz: `(silêncio de 1 s, sem voz)` ou `(take real, sem voz)` |
| Gatilho | Uma palavra falada que está na Fala. Cena sem voz leva `-` |
| Tipo | R real, IA imagem gerada, B banco, M motion, T tela real, S simulação. Combine com `+` (R+M) |
| Visual | O que a voz diz, literalmente. Teste: tape a coluna Fala; só pelo Visual e pelo Texto em tela alguém adivinha o assunto |
| Texto em tela | Texto exato, até 2 linhas (`<br>`), dentro da área segura. `-` se não houver. Tipo S leva "EXEMPLO" aqui |
| Origem do asset | Arquivo ou ID, prompt-base, foto de referência, busca de banco, licença ou crédito, "PRÓPRIO" |
| Status | outline, imagem aprovada, construído, animado, conferido |

Depois da tabela, uma linha de rodapé: `**Contagem:** 10 cenas = R 3, R+M 3, S 1, IA 1, M 2` (cenas por tipo, somando o total). Um exemplo completo que passa no validador: `references/exemplo-storyboard.md`.

## Quando o validador reprova

| Verificação | Conserto |
|---|---|
| Colunas obrigatórias | Acrescente a coluna que falta, com o nome do modelo |
| Células obrigatórias preenchidas | Preencha; use `-` onde não há texto, gatilho ou som |
| Ids únicos | Renomeie o repetido (`c04b`) |
| Tempo crescente e sem buraco | Feche o buraco ou desfaça a sobreposição; a primeira cena começa em 0:00 |
| Cena acima do teto | Divida a cena, troque a imagem no meio ou acrescente texto em tela |
| Gatilho presente na fala | Troque o gatilho por uma palavra que está na Fala |
| Tipo válido | Use R, IA, B, M, T ou S, combinados com `+` |
| Simulação com selo exemplo | Escreva "EXEMPLO" no texto em tela |
| Texto em tela de até 2 linhas | Corte palavras; separe as linhas com `<br>` |
| Status válido | Um dos cinco valores acima |
| Rodapé de contagem | Reconte por tipo; o total é o número de cenas |

O validador não confere se o arquivo da coluna Origem existe, nem buraco de legenda, nem cartão fora da fala: isso é seu, na folha de contato.

## Sinais de alerta

| Pensamento | Realidade |
|---|---|
| "Uma foto bonita serve para essa fala" | Foto solta que não mostra o que a voz diz reprova versão. Mostre a coisa dita |
| "Gero tudo e mostro o vídeo pronto" | Quadros e fala vêm antes do render |
| "O gatilho é qualquer palavra da frase" | É a palavra que dispara a cena. Se não alinha, o tempo sai errado |
| "Simulação não precisa de selo" | Real, gerada e simulada não se misturam sem marca |
| "Texto em 3 linhas fica mais claro" | O limite é 2. Corte palavras |
| "O texto cobre um pouco o rosto, é rápido" | Texto nunca cobre rosto, inclusive nos picos de escala |

## Pronto quando

O validador aprova; a folha de contato foi comparada com a fala de cada cena; o dono aprovou e a decisão está registrada.
