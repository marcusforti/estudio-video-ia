# Serviços pagos de lip sync: preços, limites e custo por trabalho

Nenhum serviço desta lista foi testado por nós: não temos conta em nenhum. Tudo vem das páginas dos fornecedores e dos hospedeiros (fal.ai, Replicate), lidas em 01/11/2026. Preços em dólares. Selos: `[fornecedor]` = o fornecedor ou o hospedeiro diz; `[independente]` = terceiro; `[sem medição]` = não achamos. Preço muda: confira a página antes de rodar.

Qualidade: toda avaliação que achamos é do próprio fornecedor ou de revisor com laço comercial (afiliado ou concorrente). Não há teste cego independente nem teste de sincronia em português [sem medição]. Teste no seu pior plano (`teste-pior-plano.md`).

## Filmagem real: o que cada um faz

| Serviço | Preço | Limites e termos |
|---|---|---|
| sync.so | Por segundo, no plano base: lipsync-1.9 0,02 a 0,025; lipsync-2 0,05; lipsync-2-pro 0,083; sync-3 0,133 (4K; US$ 8 por minuto). Planos por mês: Hobbyist 5, Creator 19, Growth 49 (5% de desconto no uso), Scale 249 (20%). Grátis: 3 gerações por mês de até 15 s [fornecedor] | Vídeo máximo por plano: 1, 5, 10 e 30 min. Marca d'água tirada a partir do Creator. "Vídeos longos são divididos em trechos de 30 a 40 s e a qualidade cai nas emendas; prefira trechos de menos de 2 min". Por padrão sincroniza o rosto mais proeminente; para vários falantes, recorte ou mascare os outros. Perfil extremo e mão ou microfone na boca pioram no lipsync-2; o sync-3 diz tratar sozinho. react-1 (edita expressão) custa 0,167 por segundo e vai a 15 s |
| fal.ai | Sem mensalidade: sync lipsync-2 US$ 3 por minuto; lipsync-2-pro US$ 5; sync-3 US$ 8; VEED Lipsync US$ 0,40 por minuto; LatentSync US$ 0,20 por vídeo de até 40 s e 0,005 por segundo depois [fornecedor] | Os preços da sync.so na fal batem com o preço-base por segundo vezes 60 (conta nossa). "Uso comercial permitido" nas páginas dos modelos. O cliente garante direitos e consentimentos |
| HeyGen | Lipsync via Replicate: Speed 0,0333 por segundo (~2 por minuto); Precision 0,0667 (~4 por minuto). Plano web Creator US$ 29 por mês (600 créditos); tradução gasta 4, 6 ou 10 créditos por minuto (só áudio, Speed, Precision) [fornecedor]. Um concorrente cita 5 créditos por minuto (conflito sem solução) | Precision lida melhor com troca de falante, ângulo, perfil e oclusão. "Só uma pessoa deve falar por vez". Preço da tradução por API: não achamos |
| VEED Lipsync | US$ 0,40 por minuto, na fal; cerca de 2 a 2,5 min de espera por minuto de vídeo [fornecedor] | Duração máxima e vários rostos: não informados |
| Magic Hour | API a partir de US$ 0,023 por segundo [fornecedor] | Português listado; uma só face visível, de frente; grátis com marca d'água e 10 s |
| Kling Lip Sync | US$ 0,014 por segundo de entrada, arredondado a 5 s, na fal [fornecedor] | Clipes de 2 a 10 s; ~12 min por job; os termos do app proíbem uso comercial da saída sem permissão escrita |
| ElevenLabs Dubbing | v1 US$ 0,33 por minuto com marca d'água, US$ 0,50 sem; v2 US$ 2,20 por minuto, em alpha, com pt-BR e pt-PT [fornecedor] | Traduz e troca a voz; não mexe na boca |
| Captions Lipdub, D-ID, Higgsfield | Planos de aplicativo (Captions Max US$ 24,99 por mês); sem preço de API que tenhamos achado [fornecedor] | Não pesquisamos a fundo |
| Hedra, Tavus, Pika, Runway Act-Two | Animam foto ou avatar, ou transferem atuação; não consertam filmagem real. Hedra de US$ 0,025 a 0,0625 por segundo [fornecedor] | Hedra proíbe subir mídia de outras pessoas |

Conflitos entre fontes, sem solução: a sync.so diz que há API em todos os planos e a Replicate diz que o lipsync-2-pro exige o Scale; os créditos de tradução do HeyGen aparecem como 4, 6 e 10 numa página e 5 em outra.

## Custo por trabalho (preço de tabela, um take)

Em material difícil, multiplique por 2 a 3 [sem medição: regra nossa].

| Rota | Reel de 30 s | VSL de 5 min | Dublagem de 5 min, áudio + lip sync |
|---|---|---|---|
| LatentSync na A100 alugada (conta nossa: 9 a 14 min de máquina por 23 a 27 s de vídeo, a US$ 1,07 a 1,23 por hora) | 0,18 a 0,37 | 1,78 a 3,74 | voz por fora |
| LatentSync na fal | 0,20 | 1,50 | 4,00 |
| VEED na fal | 0,20 | 2,00 | 4,50 |
| HeyGen Speed | 1,00 | 10,00 | ~1,45 no plano web |
| HeyGen Precision | 2,00 | 20,01 | ~2,42 no plano web |
| sync lipsync-2-pro na fal | 2,50 | 25,00 | 27,50 |
| sync-3 na fal | 4,00 | 40,00 | 42,50 |
| sync-3 no plano Scale (US$ 0,107 por segundo) | 3,21 | 32,10 | n/d |

Notas: a coluna de dublagem soma 5 min de ElevenLabs v1 sem marca d'água (US$ 2,50) ao lip sync; com o v2 são US$ 11,00. Os valores do HeyGen web saem dos créditos do plano Creator (US$ 29 por 600) e só valem se o preço do crédito for o do site. Sem montagem da máquina alugada, que não medimos. O Scale (US$ 249 por mês) só compensa acima de ~160 min de sync-3 por mês (conta nossa: 249 dividido por 1,56 de economia por minuto).

## Orçamento

- Até uns US$ 10 por mês: fal pagando por uso, VEED ou LatentSync no dia a dia, lipsync-2-pro ou sync-3 só nos planos difíceis.
- US$ 20 a 50 por mês: sync.so Creator (US$ 19) se for só lip sync; HeyGen Creator (US$ 29) ou Pro (US$ 49) se houver tradução.
- Muito volume em modelo aberto: alugar A100 por hora e destruir ao terminar (skill `estudio-gpu`).

## Fontes

Páginas vistas em 01/11/2026.

- sync.so: [preços](https://sync.so/pricing), [modelos](https://sync.so/docs/models), [dicas de qualidade](https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality) e [termos](https://sync.so/terms).
- fal.ai: [sync-3](https://fal.ai/models/fal-ai/sync-lipsync/v3/llms.txt), [VEED Lipsync](https://fal.ai/models/veed/lipsync), [LatentSync](https://fal.ai/models/fal-ai/latentsync) e [Kling Lip Sync](https://fal.ai/models/fal-ai/kling-video/lipsync/audio-to-video/llms.txt): preços e uso comercial.
- HeyGen: [Speed](https://replicate.com/heygen/lipsync-speed) e [Precision](https://replicate.com/heygen/lipsync-precision) na Replicate, [planos](https://www.heygen.com/pricing) e [tradução de vídeo](https://help.heygen.com/en/articles/10029081-video-translation-101).
- [VEED Lipsync](https://www.veed.io/learn/lipsync-api) e [Magic Hour](https://magichour.ai/products/lip-sync): preços e limites.
- [Kling: política de uso](https://kling.ai/docs/user-policy): termos do app.
- ElevenLabs: [preços da API](https://elevenlabs.io/pricing/api) e [Dubbing](https://elevenlabs.io/docs/overview/capabilities/dubbing).
- [Captions: preços](https://captions.ai/pricing).
- Hedra: [preços](https://www.hedra.com/pricing) e [uso aceitável](https://www.hedra.com/acceptable-use).
