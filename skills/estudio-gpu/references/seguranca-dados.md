# Rosto e voz na nuvem: segurança e privacidade

Selos: `[oficial]` = norma ou documento do fabricante; `[fornecedor]` = o fornecedor diz, sem confirmação independente; `[praticante]` = nossa recomendação, sem medição; `[sem medição]` = não achamos documentação. Nada aqui é parecer jurídico.

## Por que é dado sensível

Por cautela, trate voz e rosto ligados a uma pessoa como dado pessoal sensível: a LGPD (Lei 13.709/2018) inclui o dado biométrico entre os sensíveis (art. 5, II), e o consentimento específico e destacado é uma das bases para tratá-lo (art. 11, I). Se a gravação de voz e o rosto em vídeo contam como biométrico é pergunta em aberto nas fontes que lemos. A transferência para fora do Brasil segue o art. 33 [oficial]. Mandar o vídeo ou o áudio de alguém para uma GPU fora do país provavelmente cai nessa regra: peça consentimento que cubra isso [praticante]. Isto não é parecer jurídico.

## Portão de consentimento

Antes de subir qualquer material com rosto ou voz de outra pessoa, o usuário tem de confirmar que existe consentimento escrito que diga:

- o que será feito (por exemplo, trocar a boca para acompanhar um áudio novo, ou clonar a voz);
- onde o resultado será publicado e por quanto tempo;
- que o processamento roda em nuvem, possivelmente fora do Brasil;
- como a pessoa revoga o consentimento e o que acontece com os arquivos nesse caso.

Sem isso, pare e diga ao usuário o que falta. Não prossiga "só para testar".

## Escolha do ambiente

| Ambiente | Para dado de terceiro? | Motivo |
|---|---|---|
| Vast, nível `datacenter=True` | Sim, com cuidados | A Vast diz que a Secure Cloud usa parceiros com ISO 27001 no mínimo e que a empresa tem SOC 2 Tipo 2 [fornecedor] |
| RunPod Secure Cloud | Sim, com cuidados | Parceiros T3 ou T4 com SOC 2, ISO 27001 e PCI DSS; os termos proíbem o host de inspecionar dados [fornecedor] |
| Lambda (VM) | Sim, com cuidados | Não achamos certificações documentadas [sem medição] |
| Vast em host de mercado, RunPod Community | Não | A Vast diz que "Provider security varies significantly" e que hosts individuais podem ter medidas menos formais [fornecedor] |
| Google Colab | Não | A FAQ lista "creating deepfakes" entre os usos proibidos e não define o termo [oficial] (https://research.google.com/colaboratory/faq.html, lida em 01/11/2026) |

Não achamos garantia documentada contra o administrador da máquina física, nem oferta de computação confidencial (GPU com dados cifrados em uso) na Vast, RunPod ou Lambda [sem medição]. O isolamento por contêiner protege de outros clientes, não necessariamente do dono do host [praticante]. Não lemos os termos de uso aceitável de Vast, RunPod e Lambda sobre rosto e voz: leia antes.

## Checklist de higiene

1. Mande só o necessário: áudio mono recortado, recortes do rosto, o trecho do teste, não a gravação inteira [praticante].
2. Cifre o que fica parado: `rclone crypt` cifra conteúdo e nomes de arquivo (XSalsa20 com Poly1305), mas não o tamanho nem a data de modificação [oficial]. A criptografia não protege o dado enquanto o modelo o lê na memória.
3. Use chave SSH, nunca senha. Não guarde credenciais dentro da máquina. Token de leitura só para o job, por variável de ambiente, e rotacione depois [fornecedor e praticante].
4. Não ponha chave em imagem, template ou script versionado. A RunPod guarda segredos cifrados e não os exibe depois de criados [oficial].
5. Prefira vida curta: crie, rode, baixe, destrua. Destruir, não parar; a própria Vast recomenda destruir a instância assim que terminar [fornecedor].
6. Nem Vast nem RunPod documentam apagamento seguro do disco [sem medição]. Não reaproveite volume entre clientes e anote data e hora da destruição.
7. Confirme a lista vazia (`scripts/lista_vazia.py`).
8. O resultado vai só ao dono do vídeo antes de qualquer publicação.

## Fontes

Páginas vistas em 01/11/2026.

- [Vast: FAQ de segurança](https://docs.vast.ai/guides/reference/faq/security.md): isolamento e recomendações.
- [Vast: conformidade](https://vast.ai/compliance): SOC 2 e nível Secure Cloud.
- [RunPod: segurança e conformidade](https://docs.runpod.io/references/security-and-compliance.md): Secure Cloud e certificações.
- [RunPod: segredos](https://docs.runpod.io/pods/templates/secrets.md): valor cifrado, não visível depois de criado.
- [rclone crypt](https://rclone.org/crypt/): criptografia do lado do cliente.
- [Colab: FAQ](https://research.google.com/colaboratory/faq.html): usos proibidos.
- [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm): Lei 13.709/2018, arts. 5, 11 e 33.
