# Workflow completo: do pedido à publicação

Este capítulo mostra a ordem de trabalho que usamos para levar um vídeo do pedido solto até o post: 17 etapas, o que entra e sai de cada uma, quem decide e onde o trabalho para e pede ok. Serve a quem edita com agentes de código (Claude Code, Codex) e quer um fluxo repetível em vez de uma conversa solta.

## Resumo em 30 segundos

- São 17 etapas (0 a 16), 6 portões de aprovação do dono e 3 travas de segurança. O trabalho interno corre sem perguntar. O agente para só no que sai de dentro do projeto: gastar, clonar voz ou mexer em rosto, entregar, publicar.
- Antes de qualquer cena, a [folha de rosto](02-folha-de-rosto.md). Antes de qualquer render, a [folha de storyboard](03-folha-de-storyboard.md) aprovada.
- Reprovou na conferência final? O agente corrige e refaz sem pedir aprovação ([capítulo 10](10-conferencia-e-entrega.md)). A versão vai primeiro só ao dono do vídeo.
- Aqui, um Reel de 2 a 3 minutos saiu do briefing à v1 em 2 h a 3 h 40, e os projetos que acompanhamos de perto foram aprovados entre a 3ª e a 7ª versão [testado].
- O tipo de projeto (talking head, Reel com motion, explicativo gerado, VSL, aula longa) decide quais etapas pesam. A tabela está em "O que muda por tipo de projeto".

<!-- diagrama:workflow -->

## A linha única

```
pedido (áudio + takes) → _bruto → transcrição + catálogo → ROSTO → [Decisões]
→ roteiro por blocos [Roteiro] → voz com tempo por palavra {Consentimento}
→ storyboard [Quadros e fala] → linha do tempo → composição [Prévia]
→ mix → render {Gasto} → finalização → conferência {Conferência}
→ entrega vN só ao dono [Entrega] → aprova ou reprova → vN+1
→ [Publicar] → agendamento → isca + automação comentário→DM (opcional) → registro
```

Colchetes são os 6 portões de aprovação: o trabalho espera uma decisão do dono. Chaves são as 3 travas de segurança: o agente para por conta própria até cumprir a condição. A seção "Portões e travas" abaixo detalha cada um.

## Papéis

| Papel | Quem | O que decide |
|---|---|---|
| Dono do vídeo | Criador ou cliente que assina o conteúdo | Estilo, voz, preço, prazo e vaga, "pode publicar" e o que sai para terceiros |
| Agente | Claude Code ou Codex, com subagentes em paralelo | Tudo que é interno: rascunho, análise, render, áudio de teste, arquivo novo |
| Operador | Pessoa que abre as sessões e dá feedback técnico | Padrões de edição, por exemplo aprovar um layout de tela dividida |
| Terceiros | Cliente final, sócio, equipe | Nada. Só recebem pelo dono, ou com o ok dele |

## As 17 etapas

Convenções: `<slug>` é o nome da pasta do projeto (`REEL-TEMA-AAAA-MM-DD`). A pasta fica com o dono do vídeo, nunca dentro da pasta das ferramentas. "Folha de contato" é uma imagem com um quadro a cada N segundos; ela aparece em três momentos (entrada, imagens geradas, final).

### Preparar (etapas 0 a 5)

| # | Etapa | Entrada | Saída | Ferramenta | Portão ou trava | Erro típico |
|---|---|---|---|---|---|---|
| 0 | Captar o pedido | Áudio de briefing, 9 a 18 takes e fotos, pelo canal do dono (WhatsApp, Drive, zip) | Pasta `<slug>/_bruto/` | API do WhatsApp que você usa, `gdown`, `yt-dlp` | Nenhum | Ler só uma conversa e perder as mídias que chegaram em outra [testado]. Nome de arquivo com emoji quebra o `gdown` [praticante] |
| 1 | Transcrever e catalogar | `_bruto/` | Transcrição do briefing; tabela arquivo / o que tem / uso, com os descartados; folha de contato do material | Whisper medium por palavra; ElevenLabs Scribe v2 quando precisa de fala literal | Nenhum | O Whisper ouviu "três vezes" onde a pessoa disse "em 3D": confira as falas-chave com uma segunda transcrição [testado]. O Whisper limpa gagueira, o Scribe v2 não [testado]. Cópia idêntica entra como "descartar" |
| 2 | Folha de rosto | Transcrição, catálogo, pesquisa sobre o negócio | `ROSTO.md` ([capítulo 02](02-folha-de-rosto.md)) | Agente, com pesquisa na web | **Portão Decisões**: o dono responde às perguntas abertas. Sem resposta, o agente segue o padrão proposto e registra | Falar com o público errado: uma v1 foi reprovada por se dirigir ao dono do negócio e não a quem vende a solução [testado] |
| 3 | Referência de estilo | Pedido de estilo ("documental", "tipo série de streaming") | Estilo escolhido e `CREDITOS.md` | [Coleção de referências de motion](09-escolhermotion.md), Pinterest, estudo de um Reel de referência | O dono escolhe entre as propostas | Paleta genérica e motion sem conceito foram recusados [testado]. Copiar marca, logo ou texto da referência |
| 4 | Roteiro por blocos | Rosto aprovado | `BLOCOS` (id e texto exato que a voz lê) e `ROTEIRO.md` do gancho ao CTA | Agente, no tom do dono; números e siglas por extenso | **Portão Roteiro**: obrigatório em VSL e material de cliente; em Reel curto segue junto com a v1 | Promessa, número ou "pilha de valor" sem fonte. Faixa de preço dita como fato quando era estimativa [testado] |
| 5 | Voz | Blocos e voz definida | `voz/bNN.mp3` e `bNN.json` com tempo por palavra | ElevenLabs com timestamps, OmniVoice local, Edge TTS ([voz local](05-voz-local.md)); dicionário de pronúncia | **Trava Consentimento**: o dono aprova cada voz nova uma vez, com teste curto. Clone de voz só com consentimento por escrito ([licenças e consentimento](11-licencas-e-consentimento.md)) | Modelo novo falou cerca de 15% mais devagar e o bloco deixou de caber no take [praticante]. Sigla lida errado. Voz real picotada sobre takes reprovou uma v1 [testado] |

### Montar (etapas 6 a 11)

| # | Etapa | Entrada | Saída | Ferramenta | Portão ou trava | Erro típico |
|---|---|---|---|---|---|---|
| 6 | Storyboard e imagens | Roteiro, tempos da voz, catálogo de takes | [Folha de storyboard](03-folha-de-storyboard.md); imagens geradas; clipes de banco; takes mapeados; folha de contato das imagens | Gerador de imagem (Codex `image_gen`) com foto real de referência; Pexels e Pixabay; ffmpeg | **Portão Quadros e fala**: a folha vai ao dono e espera o ok antes do render. Arte em etapas: gera, o dono escolhe, só então monta | Arte repetida sempre no mesmo enquadramento reprovou uma versão. Foto solta que não mostra o que a voz diz [testado]. O gerador inventa marca ou lugar reais; 4 gerações em paralelo travam [praticante] |
| 7 | Linha do tempo e motion | Voz com tempos e storyboard | `tempos.json`, `hf/index.html`, `caps.ass` (legenda), `events.json` (efeitos sonoros) | Script de linha do tempo, gerador de composição, HyperFrames com GSAP e Three.js locais ([motion](08-motion.md)) | **Portão Prévia**: em vídeo longo, prévia leve a 15 fps aprovada antes do render final | Cartão distribuído por régua e não pela fala; tela vazia por mais de 4 s; `tl.call()` não dispara no render; `<video>` sem `id` congela; biblioteca vinda de CDN derruba o render [testado] |
| 8 | Mix de áudio | Voz, trilha e efeitos | `mix.wav` a 48 kHz | Script de mix: voz nivelada por RMS, trilha baixa, duck forte (a trilha abaixa quando a voz entra) | Nenhum | Música alta: uma versão com a trilha cerca de 7 dB abaixo da voz foi reprovada; a seguinte, com cerca de 15 dB, passou [testado] |
| 9 | Render | Composição e `mix.wav` | `hf.mp4` (mudo) | HyperFrames local (cerca de 25 min num Reel de 2:50) ou [VM alugada](06-gpu-como-local.md) de 64 núcleos (3 a 6 min em outro Reel; não é a mesma render) [praticante] | **Trava Gasto**: confirmar antes de alugar; fixar um teto; destruir a máquina ao baixar | Oferta de VM com erro de GPU; `nohup` simples morre ao fechar o SSH [testado]. Limite de processos (no máximo 3 pedaços em paralelo); ffmpeg do conda sem libx264; emoji vira quadrado sem fonte de emoji [praticante] |
| 10 | Finalização | `hf.mp4`, `mix.wav`, `caps.ass` | `<slug>_vN.mp4`, `_vN_whats.mp4`, `_vN_post.mp4` | Script de finalização: legenda queimada, `loudnorm I=-14 TP=-1 LRA=11`, AAC 192k a 48 kHz; `_whats` em 720p, crf 26 | Nenhum | O render de vídeo descarta o áudio: sempre remuxe. Legenda fora da zona segura (y 1700) reprovou uma versão [testado] |
| 11 | Conferência | Master | `transcricao_final.txt`, quadros a cada 8 a 10 s, folha de contato final, `QA.md` | Whisper ou Scribe, `ffmpeg -v error -f null`, [`conferir_video.py`](10-conferencia-e-entrega.md), revisor independente | **Trava Conferência**: reprovou, o agente corrige e refaz sem pedir aprovação | Texto encostando no rosto de uma pessoa; voz do entrevistador sobrando no corte; fala diferente do roteiro [testado] |

### Entregar e publicar (etapas 12 a 16)

| # | Etapa | Entrada | Saída | Ferramenta | Portão ou trava | Erro típico |
|---|---|---|---|---|---|---|
| 12 | Entrega ao dono | `_whats` e um resumo | Mensagem com o vídeo, a versão e as perguntas | Canal combinado com o dono (WhatsApp) | **Portão Entrega**: só o dono recebe e aprova ou reprova | Marcar "enviado" com status "pendente" (a API só aceitou o pedido) [testado]. Mandar a terceiro antes do ok do dono é o que este portão existe para impedir |
| 13 | Iteração | Feedback do dono | vN+1 e `HANDOFF.md` com tabela de versões | O mesmo pipeline, com a versão como variável | O dono aprova ou reprova | Recomeçar do zero em vez de ajustar o formato aprovado [praticante]. Deixar um script sobrescrever a versão anterior [testado] |
| 14 | Postagem | `_post.mp4` e a legenda (arquivo com o mesmo nome) | Post agendado ou publicado, com collab | Sua ferramenta de agendamento | **Portão Publicar**: "pode publicar" explícito do dono | Duas sessões na mesma peça, uma publicando enquanto a outra ainda ajustava [testado] |
| 15 | Isca e automação comentário→DM (opcional) | Palavra do CTA, material e link | Página com o material, campanha (JSON), automação (palavra exata, DM com botão, resposta pública) e painel de leads | Hospedagem de página estática; sua ferramenta de automação de comentários | Regra fixa: post que pede "comenta PALAVRA" não sai sem a automação ativa e testada | Um post pediu comentário e saiu sem automação. Um deploy caiu num arquivo de configuração esquecido numa pasta acima. Erro intermitente de deploy: repetir resolveu [testado] |
| 16 | Registro | Tudo | Linha no `HANDOFF.md`; máquina destruída; segredos só no gerenciador de segredos | Gerenciador de segredos; CLI da máquina alugada | Nenhum | Instância "parada" em vez de destruída ainda pode cobrar armazenamento. `HANDOFF.md` desatualizado faz outra sessão repetir o trabalho [praticante] |

## Portões e travas

Seis portões esperam uma decisão do dono. Três travas fazem o agente parar por conta própria até cumprir uma condição. As skills do repositório também trazem seus portões obrigatórios por escrito; as três travas abaixo atravessam todas elas.

| Portão (aprovação do dono) | Etapa | Sem resposta |
|---|---|---|
| Decisões | 2 | Segue o padrão proposto e registra no campo 27 do rosto |
| Roteiro | 4 | VSL e material de cliente: espera. Reel curto: segue com a v1 |
| Quadros e fala | 6 | Espera. Não renderiza |
| Prévia | 7 | Espera (só em vídeo longo) |
| Entrega | 12 | Espera. Nada vai a terceiros |
| Publicar | 14 | Espera. Sem "pode publicar" nada sai |

| Trava (o agente para sozinho) | Etapa | Condição para seguir |
|---|---|---|
| Consentimento | 5, e onde houver rosto | Voz nova aprovada pelo dono com um teste curto. Clonar voz ou mexer no rosto de alguém só com consentimento por escrito de quem aparece ou fala |
| Gasto | 9 | Ok do dono com um teto, antes de alugar máquina ou gerar com serviço pago. Com teto e autorização permanente do dono, segue dentro do teto. Máquina destruída ao baixar |
| Conferência | 11 | Relatório sem falha. Reprovou: corrige e refaz, sem pedir aprovação |

## O que muda por tipo de projeto

| Etapa | Talking head (cortes, [capítulo 04](04-edicao-e-corte.md)) | Reel com motion (takes + voz) | Explicativo 100% gerado | VSL (cliente) | Aula longa |
|---|---|---|---|---|---|
| Entrada | Um bruto por corte; HDR de celular vira master SDR (tonemap, tags bt709) [testado] | 9 a 18 takes de WhatsApp e um áudio de briefing | Só roteiro e ideia, sem filmagem | Questionário, reuniões, perfil do cliente, concorrentes | Gravação de reunião ou live, de 1 h ou mais |
| Transcrição | Whisper por palavra; separar vozes por timbre se há entrevistador [testado] | Whisper medium; falas-chave conferidas duas vezes | Scribe ou faster-whisper sobre a voz gerada, ou o alinhamento do próprio TTS | Scribe v2 com falante; alinhamento do TTS | Scribe v2 com falante por palavra [praticante] |
| Rosto | Plano editorial: gancho, corpo, descartes [testado] | Mapa com tabela de material e roteiro por tempo [testado] | Roteiros em JSON e um README da série | Briefing estratégico longo, com fontes numeradas e marcas INFERÊNCIA e VERIFICAR [testado] | Tabela de candidatos a corte: nota, janela, gancho, cartão [testado] |
| Voz | A do próprio dono, sem clone | Clone por cima de takes mudos, ou a voz real em selfie | Voz gerada; clone só se pedido e autorizado | Voz de quem vende, real ou clonada com consentimento por escrito; teste de pronúncia; amostra limpa | Voz real de quem fala; se houver clone, só com termo escrito de quem fala |
| Imagem | Cartões de motion ancorados na fala (cerca de um a cada 5 s) [testado] | Takes inteiros na velocidade real, telas de sistema real, detecção real | Imagens geradas 2:3 (no máximo 2 em paralelo), sem logo real | Mistura de IA, banco, material real mudo e motion; piloto antes da versão longa [testado] | Layout remontado (tela e câmera), cartões de módulo e de dúvida |
| Portões | Mostrar antes de renderizar: gancho, cortes, frases dos cartões | Decisões e entrega da v1 | Quadros e fala; roteiro antes do render | Roteiro, storyboard e prévia do piloto, prévia da versão longa | Roteiro por tempo e lista de cortes |
| Render | Local | VM de 64 núcleos, pedaços de 8 a 10 s | Local, em pedaços de 60 s | Local com prévia a 15 fps e final em 2 blocos; ou VM | VM, dezenas de pedaços de 30 s, camada com alpha, junção por `-f concat` [praticante] |
| Conferência específica | Silêncio inicial, voz do entrevistador, cor, gancho sem eco, cobertura dos cartões [testado] | Transcrição do final, quadros, texto sobre rosto | `ffmpeg -f null` e pronúncia | Duas revisões independentes e lista de ressalvas de conformidade (regras de publicidade da área) antes de publicar [testado] | Privacidade: dúvida de participante vira cartão escrito, sem voz nem rosto [praticante] |
| Pós | Reel e legenda do post | Post, isca e automação de DM | Envio ao dono do vídeo | Página (HLS) publicada só com ok; anúncios | Master e versão WhatsApp |

## Tempos e custos observados

Os tempos de ciclo vêm dos carimbos de data dos arquivos, não de cronômetro. O pedido pode ter chegado antes da primeira transcrição.

| O que | Tempo ou custo | Selo |
|---|---|---|
| Reel de 2 a 3 min, do briefing à v1 | 2 h a 3 h 40, em duas produções | [testado] |
| Reel com 4 versões, da v1 à aprovada | cerca de 9 h | [testado] |
| VSL longa, do plano à entrega | cerca de 8 h | [testado] |
| Versões até a aprovação | de 3 a 7, em cinco projetos acompanhados de perto | [testado] |
| Render de um Reel de 2 a 3 min | cerca de 25 min no PC numa versão; 3 a 6 min em VM de 64 núcleos em outra (não é a mesma render) | [praticante] |
| Render de uma VSL curta em VM de 64 núcleos | cerca de 1 min para 5 min de vídeo | [praticante] |
| Aula longa reduzida a cerca de um terço, render em VM | cerca de 20 min, em dezenas de pedaços de 30 s | [praticante] |
| VM de 64 núcleos (Vast.ai) | US$ 0,54 por hora, visto em 01/11/2026 | [testado] |

## Regras que valem em qualquer etapa

| Regra | Efeito |
|---|---|
| Interno sem perguntar. Pare só no que sai para fora: terceiros, publicar, gastar, apagar, mexer em conta ou senha | Os portões chamam o dono; as travas param o agente em consentimento, gasto e conferência. O resto corre sozinho |
| O vídeo vai primeiro só ao dono. Para fora, só com o ok dele | A etapa 12 é sempre privada |
| A memória do PC é curta: no máximo 2 coisas pesadas por vez. Se faltar memória, peça ao dono antes de fechar qualquer programa dele | Render pesado vai para a VM; um render por vez no local |
| Relatório, folha e playbook ficam em pasta local, nunca em serviço de terceiros nem em conta de outra pessoa | `QA.md` e folhas ficam em `qa/` |
| Ao entregar, registre uma linha no `HANDOFF.md` | Etapa 16 |
| Confira a hora no sistema antes de dizer "ontem" ou "há pouco" | Datas exatas nos registros |

## O que deu errado aqui

- **Público errado na v1.** O pedido foi lido como "para o dono do negócio" e a versão foi reprovada. Solução: o campo 7 do rosto diz quem NÃO é o público, e o portão Decisões vem antes do roteiro [testado].
- **Voz real picotada sobre takes.** A fala do dono foi cortada em pedaços por cima de takes de apoio. Solução: take inteiro e mudo com voz gerada por cima, ou fala real contínua [testado].
- **Render que não renderiza.** `tl.call()` não dispara no render, `<video>` sem `id` congela e biblioteca de CDN derruba tudo. Solução: GSAP e Three.js locais, `id` em todo `<audio>` e `<video>`, animação só por tween [testado].
- **Música alta.** A trilha ficou cerca de 7 dB abaixo da voz. Solução: cerca de 15 dB abaixo, e medir o resultado com o `conferir_video.py` [testado].
- **Post com "comenta X" sem automação.** O comentário não gerou DM. Solução: a regra fixa da etapa 15, sem exceção [testado].
- **Duas sessões na mesma peça e versão sobrescrita.** Duas sessões trabalharam na mesma peça (uma publicando enquanto a outra ainda ajustava), e um script reescreveu duas versões. Solução: `HANDOFF.md` com a tabela de versões, `vN` no nome do arquivo e script que nunca sobrescreve [testado].
- **Processo morto ao fechar o SSH.** O render rodava com `nohup` simples. Rode dentro de `tmux` ou `screen` [praticante].

## Links

- [HyperFrames](https://github.com/heygen-com/hyperframes): HTML renderizado em vídeo, quadro a quadro; licença Apache-2.0 [oficial].
- [Folha de rosto](02-folha-de-rosto.md): o que escrever na etapa 2.
- [Voz local](05-voz-local.md), [GPU como local](06-gpu-como-local.md) e [Motion](08-motion.md): etapas 5, 9 e 7.
- [Licenças e consentimento](11-licencas-e-consentimento.md): a trava Consentimento.
- [Folha de storyboard](03-folha-de-storyboard.md): o que escrever na etapa 6.
- [Conferência e entrega](10-conferencia-e-entrega.md): etapas 11 a 14.
- [Modelo ROSTO.md](../modelos/ROSTO.md), [modelo STORYBOARD.md](../modelos/STORYBOARD.md) e [checklist de entrega](../modelos/CHECKLIST-ENTREGA.md): folhas em branco.
- [Skill estudio-workflow](../skills/estudio-workflow/SKILL.md): o agente que conduz este fluxo.
