---
name: estudio-motion
description: Use quando a pessoa pedir para criar, animar ou editar um vídeo de motion escrito em código (reel, vinheta, tipografia cinética, motion sobre vídeo falado, anúncio, explicativo), disser "faz um motion", "anima isso" ou "põe motion no vídeo", ou antes de escrever qualquer composição HyperFrames.
---

# Estúdio de motion

Conduz motion escrito em código (HTML com GSAP, Three.js, canvas) até um MP4 conferido. Duas regras mandam: nenhum código antes de a SPEC ser aprovada e nenhum render antes de a pessoa ver quadros e fala. O conhecimento por trás está em https://github.com/marcusforti/estudio-video-ia/blob/main/conhecimento/08-motion.md.

## Dependência recomendada

Skills oficiais do HyperFrames (HeyGen, Apache-2.0): contrato, CLI e rotas para peça curta, filme longo e lançamento. Instalação no Claude Code, segundo o README do projeto (lido em 01/11/2026, não testada aqui), por uma destas duas formas:

```
claude plugin marketplace add heygen-com/hyperframes
# ou, com o CLI do HyperFrames disponível:
npx hyperframes skills update
```

Requer Node 22 ou superior e FFmpeg. Sem as skills, use `references/contrato-e-render.md`. Caminhos vêm do que a pessoa informar. Chaves ficam em variáveis de ambiente (`ELEVENLABS_API_KEY`, `VAST_API_KEY`), nunca no código.

## Portões obrigatórios

- **Consentimento.** Antes de recortar, trocar o fundo ou animar o rosto de alguém, ou clonar uma voz, peça o consentimento por escrito da pessoa. O repositório estudio-video-ia traz um modelo em https://github.com/marcusforti/estudio-video-ia/blob/main/modelos/AUTORIZACAO-VOZ-E-IMAGEM.md (a skill `estudio-voz-local` tem uma cópia). Sem consentimento, pare.
- **SPEC.** Nenhum código antes de a pessoa aprovar a SPEC.
- **Quadros e fala.** Nenhum render antes de a pessoa ver a folha de quadros, com a caixa da área segura, e a fala (transcrição) e aprovar.
- **Gasto.** Antes de alugar máquina ou chamar API paga, diga o custo estimado e espere a confirmação. Máquina alugada: baixe o resultado, confira e destrua (não só pare).
- **Conferência.** Reprovou em qualquer item do arquivo final: corrija e refaça. Não entregue nem peça aprovação.
- **Dono primeiro.** O vídeo vai primeiro só ao dono dele. Nada é publicado nem enviado a terceiros sem o ok dele.

## Fluxo

1. **Brief.** Em uma frase: objetivo, quem assiste e onde (com ou sem som), formato (1080x1920 ou 16:9), duração, fps (30 ou mais), marca (cores, fontes, logo), material (takes, imagens, dados com fonte) e idioma. Pergunte só o que falta.
2. **Rota.** Escolha pela tabela abaixo. Se a pessoa tem uma referência de outro criador, use antes a skill `estudio-escolher-motion`.
3. **SPEC.** Preencha `SPEC.md` com `references/spec-modelo.md`, mostre e pare até o ok. Se o projeto já tem a folha de storyboard (skill `estudio-storyboard`), use a tabela dela como tabela de cenas e preencha na SPEC só o resto.
4. **Construir.** Siga o contrato resumido abaixo; detalhes em `references/contrato-e-render.md`.
5. **Verificar.** `npx hyperframes check --json` e `npx hyperframes snapshot --review`. Gere a folha de quadros com a caixa da área segura (`references/area-segura.md`).
6. **Mostrar quadros e fala.** Pare até o ok.
7. **Renderizar.** `draft` primeiro, `delivery` depois. Acima de 1 a 2 min, em pedaços. Máquina alugada só depois do portão de gasto.
8. **Conferir o arquivo final.** `ffprobe`, `ffmpeg -v error -i final.mp4 -f null -`, transcrição do áudio contra a fala da SPEC e volume. Se a skill `estudio-entrega` estiver instalada, rode o `conferir_video.py` dela.
9. **Entregar ao dono.** Se houve referência de terceiros, escreva o `CREDITOS.md`.

## Rota

| Situação | Caminho |
|---|---|
| Pessoa falando, motion ocupa metade da tela | tela dividida (`references/receitas.md`, receita 2) |
| Pessoa falando, profundidade atrás dela | 3D atrás da pessoa (receita 1) |
| Takes reais mostrando um sistema funcionando | detecção real (receita 6) |
| URL de produto ou site | skill oficial `product-launch-video` |
| Peça curta (até ~30 s), sem locução | skill oficial `motion-graphics` |
| Filme narrado ou multi-cena | skill oficial `general-video` |
| Explicar sem filmar ninguém | receitas 4 e 5, ou skill oficial `faceless-explainer` |
| Série com conceito próprio | receita 3 (dossiê) |

## Contrato do HyperFrames em 6 linhas

- Elemento temporizado: `class="clip"`, `data-start`, `data-duration`. A raiz leva `data-composition-id`, `data-width`, `data-height` e `data-duration`.
- Uma timeline GSAP pausada por composição, registrada no fim: `window.__timelines["<id>"] = tl`.
- Tudo é função do tempo da timeline: sem `Date.now()`, `Math.random()` sem semente, rede, timers nem `repeat: -1`.
- Todo `<audio>` e `<video>` leva `id` (sem ele o render sai mudo ou congelado); nunca `play()` ou seek em mídia.
- Bibliotecas, fontes e mídia em arquivo local com versão fixa; nada de CDN.
- Fixe a versão do CLI: `npx --yes hyperframes@<versão> render ...`.

## Gancho e ritmo

- Gancho visual e de fala nos 2 primeiros segundos, com som no golpe. O quadro 0 já é uma miniatura: nunca preto nem só logo.
- Vídeo falado: cena nova a cada 2 a 4 s e nenhum card parado por mais de 5 a 6 s. Marca e vinheta pedem contenção: sem quique em letra, um acento de cor.
- Leitura de texto: 0,5 s mais 0,3 s por palavra. Legenda é apoio: a palavra ativa só muda de cor.
- Flashes: no máximo 3 por segundo; o flash de virada do gancho é único.
- Som só com causa visível; trilha bem baixa sob a voz; áudio final perto de -14 LUFS com pico até -1 dBTP.

## Área segura (1080x1920)

Texto e motion em x 80 a 940 e y 250 a 1440. Legenda falada com linha de base entre y 1150 e 1300, nunca abaixo de y 1400. Para anúncio, nada acima de y 269 nem abaixo de y 1248 (zona recomendada pela Meta: 14% topo, 35% base, 6% laterais). Desenhe a caixa antes de animar, confira começo, meio, fim e picos da animação com ela por cima e tire no final. Comandos e o script `scripts/area_segura.py` em `references/area-segura.md`.

## Erros que custam caro

| Erro | Efeito | Evite com |
|---|---|---|
| Biblioteca em CDN | render quebra no meio | arquivos locais |
| `<video>` ou `<audio>` sem `id` | congela ou sai mudo | `id` em toda mídia |
| Efeito fora da timeline | aparece na prévia, some no vídeo | tudo na timeline |
| Motion ou legenda sobre o rosto | peça reprovada | conferir quadros em todo o intervalo |
| Render pesado sem pedaços | processo encerrado por falta de RAM | pedaços (`references/contrato-e-render.md`) |
| Máquina alugada esquecida | custo sem fim | destruir ao terminar |
| Número ou nome inventado | peça perde credibilidade | só dado com fonte |
