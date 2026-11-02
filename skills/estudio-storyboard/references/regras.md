# As 17 regras de preenchimento, a folha de contato e o mapeamento para o HyperFrames

Selos: `[testado]` rodou em projeto real; `[oficial]` vem da especificação do HyperFrames; `[praticante]` relato de quem faz, sem medição.

## As 17 regras

1. **Imagem = fala.** A imagem mostra literalmente o que a voz diz, nunca foto solta. Teste: tape a coluna Fala; só pelo Visual e pelo Texto em tela alguém adivinha o assunto, e o substantivo-chave da fala está no Visual.
2. **Mapa primeiro.** Inventário de material, roteiro por tempo e perguntas abertas vêm antes de qualquer cena.
3. **Quadros e fala antes do render.** Tabela e folha de contato vão ao dono e esperam o ok. Arte em etapas: gera, o dono escolhe, só então monta.
4. **Tempo estimado, depois medido.** Estime com 2,33 palavras/s + 0,35 s entre falas [praticante]. Com a voz pronta, troque pelo tempo medido da palavra-gatilho. TTS com timestamps já entrega o alinhamento.
5. **Um gatilho por cena.** Se a palavra não alinha com a fala, corrija o gatilho.
6. **Ritmo e teto de cena parada.** Nenhuma cena acima de cerca de 5 s sem troca de imagem ou entrada de texto; em VSL, nada acima de 3 s sem elemento animado. Médias que medimos: entre 2 s e 4,5 s por cena em VSLs e em pilotos de VSL [testado]. A especificação do HyperFrames pede algo novo a cada 2 a 4 s [oficial].
7. **Gancho.** Cena 1 com motion e fala nos 2 primeiros segundos; cartão do gancho em cerca de 0,9 s. Em talking head o gancho é a frase mais forte de qualquer ponto do bruto, nunca a primeira; a mesma frase voltando a menos de 12 s da abertura soa como gagueira [praticante].
8. **Texto em tela.** Texto exato, até 2 linhas. Fonte de 28 px ou mais a 1080 de largura; janela de 0,5 s mais 0,3 s por palavra [oficial]; um cartão de 2 linhas fica 3 s ou mais no ar, com 1,2 s ninguém lê [praticante]. Dentro da área segura.
9. **Rosto livre.** Nenhum texto, legenda ou motion sobre rosto. Confira por snapshot em todo o intervalo, inclusive nos picos de escala. Sem caixa de detecção no rosto [testado].
10. **Tipo sempre marcado.** Real, gerada e simulada não se misturam sem marca quando o dono exige foto real.
11. **Origem rastreável.** Arquivo ou ID, prompt-base, foto de referência de rosto (só de quem autorizou), busca de banco, licença, "PRÓPRIO" para material do cliente. Créditos em `CREDITOS.md`.
12. **Ficha de direção de imagem.** Bloco fixo "direção de fotografia igual em todas" e "proibido" (texto, logos, mascotes, fantasia, 3D). Assunto longe das bordas se a imagem será cortada. No máximo 2 gerações em paralelo [praticante].
13. **Reuso.** Cada imagem no máximo 2 vezes, com recortes diferentes.
14. **Silêncio é cena.** "Sem voz, só música" e "1 s de silêncio" entram como linha própria, com `-` no gatilho.
15. **Pronúncia.** Escreva a fala como o TTS deve ler; o dicionário fica no rosto (campo 15).
16. **Rodapé de contagem.** Cenas por tipo e custo de geração real. O validador compara a contagem com a tabela.
17. **Conferência por folha de contato.** Antes do render, monte a folha com um quadro a cada 10 s (VSL) ou por cena (Reel), e compare cada quadro com a fala na tabela.

## Folha de contato das imagens geradas

Imagens numeradas `img_01.png`, `img_02.png` e assim por diante, na ordem das cenas. Cada uma ocupa a mesma moldura, mesmo com proporções diferentes; o fundo é cinza para não se confundir com quadro preto. Ajuste `tile=6x3` ao número de imagens [testado]:

```bash
ffmpeg -v error -y -framerate 1 -i imgs/img_%02d.png \
  -vf "scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2,tile=6x3:margin=3:padding=3:color=0x404040" \
  -frames:v 1 -update 1 qa/imgs.jpg
```

Para o material de entrada (um quadro de cada take), pegue um quadro de cada arquivo com `ffmpeg -ss 1 -i ARQUIVO -frames:v 1` na mesma moldura e junte com o mesmo `tile`. A folha dos quadros finais sai do `conferir_video.py` da skill `estudio-entrega`.

## Do STORYBOARD.md para o HyperFrames

O `STORYBOARD.md` do HyperFrames tem um cabeçalho em YAML e uma seção `## Frame N` por cena, com `- chave: valor` [oficial]. A tabela converte sem perder campo:

| Esta folha | HyperFrames |
|---|---|
| Cabeçalho: formato, duração, mensagem, arco, público | Cabeçalho YAML: `format`, `duration`, `message`, `arc`, `audience` |
| Tempo | `duration` (por exemplo, `4s`) |
| Visual | `scene` (legenda de uma linha) |
| Fala | `voiceover` |
| Texto em tela e janela | `reads` (chave extra) |
| Som | `sound` (chave extra) |
| Câmera / transição | `transition_in` |
| Status | `status`: outline e imagem aprovada viram `outline`; construído vira `built`; animado e conferido viram `animated` |
| Origem do asset | `asset` (chave extra, preservada pelo HyperFrames) |
