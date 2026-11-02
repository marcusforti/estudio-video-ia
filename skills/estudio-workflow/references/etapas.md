# As 17 etapas: entrada, saída, ferramenta, portão e erro típico

Selos: `[testado]` rodou em projeto real; `[praticante]` relato de quem faz, sem medição. Portão = espera o dono. Trava = o agente para sozinho.

## Preparar

**0. Captar o pedido.** Entrada: áudio de briefing, 9 a 18 takes e fotos pelo canal do dono (WhatsApp, Drive, zip). Saída: `<slug>/_bruto/`. Ferramenta: a API do WhatsApp que o usuário tem, `gdown`, `yt-dlp`. Portão: nenhum. Erro típico: ler só uma conversa e perder as mídias que chegaram em outra [testado]; nome de arquivo com emoji quebra o `gdown` [praticante].

**1. Transcrever e catalogar.** Entrada: `_bruto/`. Saída: transcrição do briefing; tabela arquivo / o que tem / uso, com descartados e duplicados; folha de contato do material (1º momento). Ferramenta: Whisper medium por palavra; Scribe v2 quando precisa de fala literal. Portão: nenhum. Erro típico: o Whisper ouviu "três vezes" onde a pessoa disse "em 3D", então confira as falas-chave com uma segunda transcrição [testado]; o Whisper limpa gagueira, o Scribe v2 não [testado].

**2. Folha de rosto.** Entrada: transcrição, catálogo, pesquisa sobre o negócio. Saída: `ROSTO.md` (skill `estudio-folha-de-rosto`). Portão Decisões. Erro típico: falar com o público errado; uma v1 foi reprovada por se dirigir ao dono do negócio e não a quem vende a solução [testado].

**3. Referência de estilo e créditos.** Entrada: pedido de estilo. Saída: estilo escolhido e `CREDITOS.md`. Ferramenta: coleção de referências de motion, Pinterest, estudo de um Reel de referência. Portão: o dono escolhe entre as propostas. Erro típico: paleta genérica e motion sem conceito foram recusados [testado]; copiar marca, logo ou texto da referência.

**4. Roteiro por blocos.** Entrada: rosto aprovado. Saída: `BLOCOS` (id e texto exato que a voz lê) e `ROTEIRO.md` do gancho ao CTA. Ferramenta: você, no tom do dono; números e siglas por extenso. Portão Roteiro (VSL e material de cliente). Erro típico: promessa, número ou "pilha de valor" sem fonte; faixa de preço dita como fato quando era estimativa [testado].

**5. Voz.** Entrada: blocos e voz definida. Saída: `voz/bNN.mp3` e `bNN.json` com tempo por palavra. Ferramenta: ElevenLabs com timestamps, OmniVoice local, Edge TTS (skill `estudio-voz-local`); dicionário de pronúncia. Trava Consentimento. Erro típico: modelo novo falou cerca de 15% mais devagar e o bloco deixou de caber no take [praticante]; voz real picotada sobre takes reprovou uma v1 [testado].

## Montar

**6. Storyboard e imagens.** Entrada: roteiro, tempos da voz, catálogo de takes. Saída: `STORYBOARD.md` (skill `estudio-storyboard`), imagens geradas, clipes de banco, takes mapeados, folha de contato das imagens (2º momento). Ferramenta: gerador de imagem com foto real de referência; Pexels e Pixabay; ffmpeg. Portão Quadros e fala. Erro típico: arte repetida sempre no mesmo enquadramento reprovou uma versão; foto solta que não mostra o que a voz diz [testado]; quatro gerações em paralelo travam, use no máximo 2 [praticante].

**7. Linha do tempo e motion.** Entrada: voz com tempos e storyboard. Saída: `tempos.json`, `hf/index.html`, `caps.ass` (legenda), `events.json` (efeitos sonoros). Ferramenta: script de linha do tempo, gerador de composição, HyperFrames com GSAP e Three.js locais (skill `estudio-motion`). Portão Prévia (vídeo longo). Erro típico: cartão distribuído por régua e não pela fala; tela vazia por mais de 4 s; `tl.call()` não dispara no render; `<video>` sem `id` congela; biblioteca de CDN derruba o render [testado].

**8. Mix de áudio.** Entrada: voz, trilha, efeitos. Saída: `mix.wav` a 48 kHz. Ferramenta: script de mix, com voz nivelada por RMS, trilha baixa e duck forte. Portão: nenhum. Erro típico: uma versão com a trilha cerca de 7 dB abaixo da voz foi reprovada; a seguinte, com cerca de 15 dB, passou [testado].

**9. Render.** Entrada: composição e `mix.wav`. Saída: `hf.mp4` (mudo). Ferramenta: HyperFrames local (cerca de 25 min para 2:50) ou máquina alugada de 64 núcleos (3 a 6 min) (skill `estudio-gpu`) [testado]. Trava Gasto. Erro típico: oferta de máquina com erro de GPU; `nohup` simples morre ao fechar o SSH [testado]; limite de processos (no máximo 3 pedaços em paralelo); ffmpeg do conda sem libx264; emoji vira quadrado sem fonte de emoji [praticante].

**10. Finalização.** Entrada: `hf.mp4`, `mix.wav`, `caps.ass`. Saída: `<slug>_vN.mp4`, `_vN_whats.mp4`, `_vN_post.mp4`. Ferramenta: legenda queimada, `loudnorm I=-14 TP=-1 LRA=11`, AAC 192k a 48 kHz; `_whats` em 720p, crf 26 (comandos em `estudio-entrega/references/derivados.md`). Portão: nenhum. Erro típico: o render de vídeo descarta o áudio, então remuxe sempre; legenda fora da zona segura (y 1700) reprovou uma versão [testado].

**11. Conferência.** Entrada: master. Saída: `transcricao_final.txt`, quadros a cada 8 a 10 s, folha de contato final, `QA.md` (skill `estudio-entrega`). Trava Conferência. Erro típico: texto encostando no rosto de uma pessoa; voz do entrevistador sobrando no corte; fala diferente do roteiro [testado].

## Entregar e publicar

**12. Entrega ao dono.** Entrada: `_whats` e um resumo. Saída: mensagem com o vídeo, a versão e as perguntas. Ferramenta: canal combinado com o dono. Portão Entrega. Erro típico: marcar "enviado" com status "pendente" (a API só aceitou o pedido) [testado]. Mandar a terceiro antes do ok do dono é o que este portão existe para impedir.

**13. Iteração.** Entrada: feedback do dono. Saída: vN+1 e `HANDOFF.md` com tabela de versões. Ferramenta: o mesmo pipeline, com a versão como variável. Portão: o dono aprova ou reprova. Erro típico: recomeçar do zero em vez de ajustar o formato aprovado [praticante]; deixar um script sobrescrever a versão anterior [testado].

**14. Postagem.** Entrada: `_post.mp4` e a legenda (arquivo com o mesmo nome). Saída: post agendado ou publicado, com collab. Ferramenta: a ferramenta de agendamento do usuário. Portão Publicar. Erro típico: duas sessões na mesma peça, uma publicando enquanto a outra ainda ajustava [testado].

**15. Isca e automação comentário→DM (opcional).** Entrada: palavra do CTA, material e link. Saída: página com o material, campanha (JSON), automação (palavra exata, DM com botão, resposta pública) e painel de leads. Ferramenta: hospedagem de página estática e a ferramenta de automação de comentários do usuário. Regra fixa: post que pede "comenta PALAVRA" não sai sem a automação ativa e testada. Erro típico: um post pediu comentário e saiu sem automação; deploy que cai num arquivo de configuração esquecido numa pasta acima; erro intermitente de deploy, que repetir resolveu [testado].

**16. Registro.** Entrada: tudo. Saída: linha no `HANDOFF.md`; máquina destruída; segredos só em variável de ambiente ou gerenciador de segredos. Portão: nenhum. Erro típico: instância "parada" em vez de destruída ainda pode cobrar armazenamento; `HANDOFF.md` desatualizado faz outra sessão repetir o trabalho [praticante].
