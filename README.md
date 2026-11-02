# Estúdio de Vídeo com IA

O workflow completo de edição de vídeo com IA, aberto: do pedido solto ao post no ar, com folhas de projeto, skills para Claude Code e Codex, voz local, lip sync, GPU alugada, motion em código e os erros que custaram caro.

**Site:** https://estudio-video-ia.marcusforti2.workers.dev

## Instalar as skills

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.ps1 | iex
```

Linux e macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.sh | bash
```

O instalador copia as pastas para `~/.claude/skills` e `~/.codex/skills`. Skills com o mesmo nome são substituídas, e a versão antiga vai para `~/.estudio-video-ia-backup`. Abra uma sessão nova e chame `/estudio-workflow`.

## As skills

| Skill | Para quê |
|---|---|
| `estudio-workflow` | Conduz um projeto de vídeo do pedido à publicação e chama as outras skills |
| `estudio-folha-de-rosto` | Transforma um pedido solto na folha de rosto do projeto |
| `estudio-storyboard` | Escreve e valida a folha de storyboard, cena a cena |
| `estudio-corte` | Corta talking head em Reel legendado |
| `estudio-voz-local` | Clona voz com modelo aberto, com autorização por escrito |
| `estudio-gpu` | Conduz o ciclo de vida de uma GPU alugada, da criação à destruição conferida |
| `estudio-lipsync` | Escolhe e executa lip sync local ou pago, com o teste do pior plano |
| `estudio-motion` | Conduz a criação de motion em código |
| `estudio-escolher-motion` | Acha uma referência de motion e adapta o prompt à sua marca |
| `estudio-entrega` | Faz a conferência final do vídeo e gera as versões derivadas |

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `conhecimento/` | Os capítulos do manual, que também são a fonte do site |
| `modelos/` | Folhas em branco: rosto, storyboard, checklist, autorização |
| `skills/` | As skills, cada uma em sua pasta |
| `site/` | Gerador do site (`python site/build.py`) |

## Honestidade

Toda afirmação que não é óbvia leva um selo: testado aqui, fonte oficial, o fornecedor diz, medição independente, opinião de quem faz ou sem medição. Nessa área quase todo número de qualidade vem de quem vende, então os selos importam. Preços e versões foram conferidos em 01/11/2026.

Serviços pagos de lip sync não foram testados aqui. Os modelos citados têm licenças próprias: leia [Licenças e consentimento](conhecimento/11-licencas-e-consentimento.md) antes de usar comercialmente. Clonar voz ou mexer em rosto de outra pessoa exige autorização por escrito.

## Licença

Textos, skills e scripts sob [licença MIT](LICENSE). Ferramentas, modelos e marcas citados pertencem aos seus donos. Créditos em [NOTICE.md](NOTICE.md).
