# O teste de 10 a 15 s no pior plano

Não existe benchmark independente nem teste em português para nenhum modelo ou serviço (`[sem medição]`). Os números dos fornecedores e dos autores são deles. O teste abaixo é a única evidência que vale para o seu material.

## 1. Escolha o plano

O pior plano do seu vídeo: perfil, mão ou microfone perto da boca, dentes à mostra, barba, pouca luz, fala rápida, rosto pequeno no quadro. Se passar nele, passa nos outros. Corte de 10 a 15 s com a pessoa falando.

## 2. Escolha a fala

Use a voz final do projeto, em português do Brasil, e uma frase que tenha:

- lábios que se fecham: pão, bom, mamãe (p, b, m);
- vogais nasais: não, mão, põe;
- vogais arredondadas: o, u;
- um trecho de fala rápida.

Esta escolha é nossa: nenhum benchmark cobre o português (`[praticante]`).

## 3. Prepare e rode

Nos comandos, `<skill>` é a pasta desta skill.

```bash
python <skill>/scripts/preparar_teste.py --video bruto.mp4 --inicio 83 --duracao 12 --audio voz_nova.wav --saida teste
```

O script gera `original_trecho.mp4` (com áudio, para comparar), `base_25fps.mp4` (25 fps constantes, sem áudio, 0,5 s mais longo) e `voz_16k_mono.wav` (mono, 16 kHz, com 0,5 s de silêncio no fim). Sem `--audio`, ele usa o áudio do próprio trecho. Entregue o mesmo par `base_25fps.mp4` + `voz_16k_mono.wav` a cada candidato.

Custo do teste de 12 s a preço de tabela de 01/11/2026: LatentSync na fal US$ 0,20; lipsync-2-pro US$ 1,00; sync-3 US$ 1,60; modelo aberto numa A100 alugada, centavos de máquina mais a montagem. Planos com mensalidade somam à parte.

## 4. Compare

```bash
python <skill>/scripts/comparar_lado_a_lado.py --original teste/original_trecho.mp4 --resultado saida_a.mp4 saida_b.mp4 saida_c.mp4 --saida teste/comparacao.mp4
```

Os painéis aparecem na ordem dada (o script imprime a ordem). O áudio vem do primeiro resultado; mude com `--audio-de`. Veja com som e também em câmera lenta na boca.

## 5. As sete perguntas

Marque sim ou não para cada candidato.

| # | Pergunta | A | B | C |
|---|---|---|---|---|
| 1 | Os lábios fecham em p, b, m? | | | |
| 2 | As vogais nasais (não, mão) abrem certo? | | | |
| 3 | Os dentes parecem dentes? | | | |
| 4 | Há remendo ou borda em volta da boca? (sim é ruim) | | | |
| 5 | Cor e nitidez da boca batem com o rosto? | | | |
| 6 | Há tremor entre quadros? (sim é ruim) | | | |
| 7 | A última palavra saiu inteira, e a pessoa continua parecendo ela mesma? | | | |

Registre também: custo, minutos de máquina, segundos de máquina por segundo de vídeo na placa que você alugou. Os tempos publicados de um mesmo modelo variam de minutos a horas conforme a configuração, então o seu número vale mais que o do README.

## 6. Decida

- Escolha o mais barato que passa no pior plano.
- Se nenhum passar, refilme o plano (de frente, microfone fora da boca, mais luz) antes de trocar de ferramenta.
- O dono do vídeo dá o veredito final, com som.
- Guarde a ficha preenchida no projeto, sem arquivos de rosto ou voz de terceiros no repositório.

## Quando o teste dá errado

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Nenhuma boca se mexe | Trecho sem fala no vídeo-base, ou áudio mudo | Confira com o `ffprobe` e use um trecho com a pessoa falando |
| Última palavra cortada | Áudio mais longo que o vídeo | Refaça o preparo com `--folga 1.0` |
| Sincronia deslocada o vídeo todo | fps diferente de 25 | Confira que a base está em 25 fps constantes |
| "Face not detected" | Duas pessoas, rosto pequeno ou perfil | Recorte o quadro no rosto de quem fala |
| Falha só em RTX 50 | LatentSync fixa PyTorch 2.5.1 | Use Ampere, Ada ou Hopper (A100, RTX 4090, L40S) |
