# Comece aqui

Este é o manual de como a gente edita vídeo com IA em produção: do pedido solto até o post no ar. Foi escrito para quem usa agentes de código, como Claude Code e Codex, sabe rodar um comando e quer um processo que aguente trabalho de verdade.

## Resumo em 30 segundos

- Todo projeto nasce em duas folhas: a [folha de rosto](02-folha-de-rosto.md) e a [folha de storyboard](03-folha-de-storyboard.md). Render só depois.
- O [workflow](01-workflow-completo.md) tem 17 etapas e 6 portões. Os portões seguram o que custa caro: público errado, voz errada, publicar sem ok.
- O agente faz o trabalho interno sozinho. O dono decide o que sai para fora.
- Quando precisa de força, alugue uma [GPU como se fosse seu PC](06-gpu-como-local.md) e destrua a máquina ao terminar.
- Modelo aberto não quer dizer uso livre. Confira a licença e tenha [autorização por escrito](11-licencas-e-consentimento.md) antes de mexer em voz ou rosto de alguém.

## O caminho mais curto

1. Instale as skills:

```powershell
irm https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.ps1 | iex
```

2. Abra uma sessão nova do Claude Code ou do Codex na pasta do seu projeto.
3. Chame `/estudio-workflow` e descreva o vídeo como descreveria para um editor.
4. Responda às perguntas de bloqueio. O resto fica registrado na folha de rosto como padrão adotado.

## Por onde ler, conforme o que você precisa

| Você quer | Comece por |
|---|---|
| Entender o processo inteiro | [Workflow completo](01-workflow-completo.md) |
| Organizar um projeto hoje | [Folha de rosto](02-folha-de-rosto.md) e [storyboard](03-folha-de-storyboard.md) |
| Cortar talking head para Reel | [Edição e corte](04-edicao-e-corte.md) |
| Clonar voz com modelo aberto | [Voz local](05-voz-local.md) |
| Rodar modelo pesado sem GPU em casa | [GPU como local](06-gpu-como-local.md) |
| Sincronizar boca com áudio novo | [Lip sync](07-lip-sync.md) |
| Fazer motion em código | [Motion](08-motion.md) |
| Achar referência de animação | [/escolhermotion](09-escolhermotion.md) |
| Conferir antes de mandar | [Conferência e entrega](10-conferencia-e-entrega.md) |
| Saber o que pode usar | [Licenças e consentimento](11-licencas-e-consentimento.md) |
| Ver as fontes de tudo | [Pesquisa completa](12-pesquisa-estado-da-arte.md) |
| Ver como os assuntos se ligam | [Análise do grafo](13-grafo.md) |

## Como ler os selos

Cada afirmação que não é óbvia leva um selo dizendo de onde veio. Isso importa porque, nessa área, quase todo número de qualidade vem de quem vende.

| Selo | Quer dizer |
|---|---|
| [testado] | Rodamos em projeto real |
| [oficial] | Documento oficial do fabricante, plataforma ou norma |
| [fornecedor] | O fabricante diz, sem confirmação independente |
| [independente] | Medição de terceiro sem interesse comercial |
| [praticante] | Opinião de quem faz, sem medição |
| [sem medição] | Não existe número confiável, ou ninguém mediu |

## O que você precisa ter

| Item | Para quê | Obrigatório? |
|---|---|---|
| Claude Code ou Codex | Rodar as skills | Sim |
| Python 3.10+ | Scripts das skills | Sim |
| FFmpeg | Corte, conferência, folha de contato | Sim |
| Node.js 22+ | Motion com HyperFrames | Só para motion |
| Conta em serviço de GPU | Voz local, lip sync, render pesado | Só quando precisar |

Preços e versões foram conferidos em 01/11/2026. Essa área muda rápido, então confira de novo antes de gastar.

## Links

- [Repositório no GitHub](https://github.com/marcusforti/estudio-video-ia): skills, modelos e código deste site.
- [Página de download das skills](/skills/): instalação em uma linha, zip e lista completa.
