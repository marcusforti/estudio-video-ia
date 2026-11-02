# Modelo de SPEC

A SPEC é o roteiro técnico do vídeo. Copie para `SPEC.md` na pasta do projeto, preencha, mostre à pessoa e só escreva código depois do ok. Cada cena leva uma frase que diz o que acontece e por que acontece. "Entra um título" só descreve; "o título cai sobre o preço e o carimbo o esmaga" explica.

```
# SPEC: <nome da peça>
Status: rascunho | aprovada em <data> por <quem>

## 1. Brief
- Objetivo (uma frase):
- Quem assiste e onde (plataforma, com ou sem som):
- Formato (1080x1920 | 1920x1080 | 1080x1350), fps (30 ou mais) e duração:
- Marca: cores (hex), fontes (arquivo local e licença), logo, tom:
- Material fornecido: takes, imagens, dados (com fonte), áudio:
- Referência de outro criador (autor, link, mecânica que se mantém):

## 2. Escola de estilo
Contenção | impacto | mista (onde). Justificativa em uma frase.

## 3. Gancho (0 a 2 s)
- Visual:
- Fala:
- Som:
- Quadro 0 (miniatura):

## 4. Cenas
| # | Início e fim (s) | Fala ou texto | O que se move e por quê | Técnica | Entrada e saída | Som |
|---|---|---|---|---|---|---|
| 1 | 0,0 a 2,4 | | | | | |

Um quadro parado por cena, o do momento mais forte, com o segundo em que ele acontece.

## 5. Áreas e proibições
- Área segura (1080x1920): x 80 a 940, y 250 a 1440; legenda com linha de base entre y 1150 e 1300. Anúncio: y 269 a 1248.
- Intervalos em que o rosto aparece (nada pode cobri-lo):
- Flashes: no máximo 3 por segundo.
- Legenda: estilo, tamanho, palavras por bloco.
- Proibido: logo de terceiros, número ou nome sem fonte.

## 6. Áudio
- Voz: gravada | TTS | clone com consentimento registrado.
- Alvo: perto de -14 LUFS, pico até -1 dBTP. Trilha bem baixa sob a voz.
- Efeitos sonoros: lista, cada um com a causa visível.

## 7. Técnica e render
- Motor e versão fixa (HyperFrames <versão>); bibliotecas e fontes locais.
- Onde renderiza: PC | VM (custo estimado, confirmado por <quem>).
- Pedaços de <n> s.

## 8. Portões
[ ] Consentimento de rosto ou voz (se houver)
[ ] SPEC aprovada
[ ] Quadros e fala aprovados
[ ] Gasto confirmado (se houver)
[ ] Entregue só ao dono; máquina destruída
```

## Como mostrar

Mostre a SPEC em texto curto: do que trata o filme (uma frase), o gancho, a tabela de cenas e uma pergunta que se responde com sim, não ou uma escolha. Se a pessoa pedir ajustes com as próprias palavras (por exemplo, "deixa a abertura mais calma"), refaça só as cenas mexidas. Código só depois do ok.
