---
name: estudio-folha-de-rosto
description: Use quando chegar um pedido de vídeo solto (áudio de briefing, takes, fotos, texto ou link) e ainda não existir a folha de rosto do projeto, quando o ROSTO.md estiver incompleto ou desatualizado, ou quando o público e o objetivo do vídeo não estiverem claros antes de escrever o roteiro.
---

# Folha de rosto

Cria ou atualiza o `ROSTO.md` do projeto: a página única que uma sessão nova lê para continuar o trabalho sem perguntar nada. Você pergunta ao dono do vídeo só o que bloqueia. O resto segue um padrão que você propõe e registra no campo 27.

## Portões obrigatórios

- **Consentimento.** Se o pedido envolve clonar voz ou mexer no rosto de alguém, escreva isso no campo 14 ou 22 como pergunta que bloqueia: sem termo escrito da pessoa, nada de clone. Nunca marque "clone" como decidido sem o termo.
- **Preço, prazo e vaga** só entram com a confirmação do dono. Sem confirmação, escreva "estimativa" e deixe o valor "a confirmar".
- **Segredos.** Escreva só o NOME da variável (por exemplo, `VOZ_ID`). Nunca copie o valor, o token nem a senha para o arquivo.
- **Gasto.** Para transcrever com serviço pago, peça ok antes. Prefira o que roda no PC (faster-whisper).
- **Dado de terceiros** (nome, telefone, e-mail, endereço de pessoas do pedido) fica fora do rosto, a não ser que o projeto precise dele e o dono confirme.

## Passo a passo

1. **Leia tudo que chegou.** Transcreva o áudio de briefing por palavra. Liste os arquivos.
2. **Catalogue o material.** Tabela arquivo, o que tem, uso. Compare hashes para achar cópias idênticas e marque-as "descartar". Anote o que está corrompido ou ilegível.
3. **Escolha o modelo.**
   - `references/ROSTO-MINIMO.md` (11 campos): Reel curto, sem cliente, sem CTA de comentário.
   - `references/ROSTO.md` (31 campos): cliente, VSL, aula, CTA com "comenta X", várias pessoas, ou qualquer projeto com mais de uma sessão.
   Copie o modelo para a raiz do projeto e troque o título pelo slug (`REEL-TEMA-AAAA-MM-DD`).
4. **Preencha o que o pedido já responde.** Cite a fonte quando o dado vier de um arquivo. Não invente número, preço, prazo, vaga nem fato; marque "estimativa" ou "exemplo".
5. **Decida o que falta** com `references/campos.md`: a coluna "Bloqueia?" diz se você pergunta ou adota o padrão. Registre cada padrão adotado no campo 27 (pergunta, proposta, adotado).
6. **Escreva o público com "quem NÃO é".** Uma v1 já foi reprovada por falar com o dono do negócio e não com quem vende a solução.
7. **Pergunte de uma vez.** Mande ao dono no máximo 5 perguntas numeradas. Cada uma leva o padrão que você adotará se ele não responder (formato abaixo).
8. **Marque os portões.** Campo 26: Decisões como "pendente" até o dono responder; as demais linhas "pendente". Se o dono não responder, siga com o padrão, registre e avise que ele pode corrigir.

### Formato das perguntas

```
Antes de eu montar o roteiro, preciso de 3 respostas (se você não responder, sigo com o padrão):
1. A palavra do "comenta X" no final. Padrão: LAVANDERIA.
2. Pode aparecer o nome da lavanderia? Padrão: não.
3. Para quem o vídeo NÃO fala? Padrão: o dono do negócio.
```

## O que bloqueia (resumo)

Pergunte sempre que faltar: quem é o dono e onde fica a pasta; o público, se o pedido admite mais de um (quem compra x quem vende); clone de voz ou rosto de alguém; preço quando o roteiro precisa dele; vetos (uma vez, no começo); autorização de terceiros; gasto com máquina ou serviço pago. O resto tem padrão em `references/campos.md`.

## Sinais de alerta

| Pensamento | Realidade |
|---|---|
| "O pedido é curto, não preciso de rosto" | Use o mínimo: são só 11 campos, feitos para o pedido de cinco linhas |
| "O público é óbvio" | Escreva quem NÃO é. Foi aí que uma v1 errou |
| "Vou perguntar tudo para garantir" | Mais de 5 perguntas travam o projeto. Adote padrão e registre |
| "Cole a chave aqui para não esquecer" | Só o nome da variável. O valor fica no ambiente |
| "O preço que ele falou de passagem serve" | Só vale o que ele confirmou. O resto é "referência, não tabela" |
| "O dono não respondeu, então paro" | Siga com o padrão registrado no campo 27 |

## Pronto quando

Os 11 campos do núcleo estão preenchidos (ou o `ROSTO.md` completo, com `n/a` e motivo onde não se aplica); as perguntas abertas estão no campo 27 com o padrão adotado; o campo 26 mostra o estado de cada portão e trava; nenhum valor de segredo está no arquivo.
