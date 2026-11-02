# O que muda por tipo de projeto

Escolha o tipo na tabela do `SKILL.md` e use as linhas abaixo para ajustar cada etapa. Selos: `[testado]` rodou em projeto real; `[praticante]` relato de quem faz, sem medição.

## talking-head (cortes)

- **Entrada:** um bruto por corte. HDR de celular vira master SDR (tonemap, tags bt709) [testado].
- **Transcrição:** Whisper por palavra; separe as vozes por timbre se há entrevistador [testado].
- **Rosto:** plano editorial com gancho, corpo e descartes [testado].
- **Voz:** a do próprio dono, real, sem clone.
- **Imagem:** cartões de motion ancorados na fala (cerca de um a cada 5 s) [testado].
- **Portões:** mostre antes de renderizar o gancho, os cortes e as frases dos cartões.
- **Render:** local.
- **Conferência específica:** silêncio inicial, voz do entrevistador, cor, gancho sem eco, cobertura dos cartões [testado].
- **Pós:** Reel e legenda do post.
- **Gancho:** a frase mais forte de qualquer ponto do bruto, nunca a primeira. Se ela voltar a menos de 12 s da abertura, soa como gagueira [praticante].

## reel-motion (takes e voz)

- **Entrada:** 9 a 18 takes de WhatsApp e um áudio de briefing.
- **Transcrição:** Whisper medium; confira as falas-chave duas vezes.
- **Rosto:** mapa com tabela de material e roteiro por tempo [testado].
- **Voz:** clone (com termo escrito) por cima de takes mudos e inteiros, ou a voz real em selfie. Voz real picotada sobre takes reprovou uma v1 [testado].
- **Imagem:** takes inteiros na velocidade real, telas de sistema real e detecção real; caixa de detecção nunca no rosto.
- **Portões:** Decisões e a entrega da v1.
- **Render:** máquina alugada de 64 núcleos, pedaços de 8 a 10 s.
- **Conferência específica:** transcrição do final, quadros e texto sobre rosto.
- **Pós:** post, isca e automação de DM.

## explicativo (100% gerado)

- **Entrada:** só roteiro e ideia, sem filmagem.
- **Transcrição:** Scribe ou faster-whisper sobre a voz gerada, ou o alinhamento do próprio TTS.
- **Rosto:** roteiros em JSON e um README da série.
- **Voz:** gerada; clone só se pedido e autorizado.
- **Imagem:** imagens geradas 2:3, no máximo 2 em paralelo, sem logo real.
- **Portões:** Quadros e fala; roteiro antes do render.
- **Render:** local, em pedaços de 60 s.
- **Conferência específica:** `ffmpeg -f null` e pronúncia.
- **Pós:** envio ao dono do vídeo.

## vsl (cliente)

- **Entrada:** questionário, reuniões, perfil do cliente, concorrentes.
- **Transcrição:** Scribe v2 com falante; alinhamento do TTS.
- **Rosto:** briefing estratégico longo, com fontes numeradas e as marcas INFERÊNCIA e VERIFICAR [testado].
- **Voz:** de quem vende, real ou clonada com consentimento por escrito; teste de pronúncia; amostra limpa.
- **Imagem:** mistura de IA, banco, material real mudo e motion; piloto antes da versão longa [testado].
- **Portões:** Roteiro; Quadros e fala; Prévia do piloto e da versão longa.
- **Render:** local com prévia a 15 fps e final em 2 blocos; ou máquina alugada.
- **Conferência específica:** duas revisões independentes e a lista de ressalvas de conformidade (regras de publicidade da área) antes de publicar [testado].
- **Pós:** página (HLS) publicada só com ok; anúncios.

## aula (longa)

- **Entrada:** gravação de reunião ou live de 1 h ou mais.
- **Transcrição:** Scribe v2 com falante por palavra [praticante].
- **Rosto:** tabela de candidatos a corte com nota, janela, gancho e cartão [testado].
- **Voz:** a real de quem fala; se houver clone (por exemplo, em abertura e recap), só com termo escrito de quem fala.
- **Imagem:** layout remontado (tela e câmera), cartões de módulo e de dúvida.
- **Portões:** Roteiro por tempo e lista de cortes.
- **Render:** máquina alugada, dezenas de pedaços de 30 s, camada com alpha, junção por `-f concat` [praticante].
- **Conferência específica:** privacidade: dúvida de participante vira cartão escrito, sem voz nem rosto [praticante].
- **Pós:** master e versão `_whats`.
