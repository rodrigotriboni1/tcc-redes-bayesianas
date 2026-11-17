# 08: Seleção aninhada do tamanho equivalente do prior

Depende das issues 01, 02 e 07 já no `main` e da §9 de `docs/plano-de-analise.md` (PR `docs/preregistro-selecao`) mergeada. Não roda em paralelo com outra issue que altere `modelos.py` ou `avaliar.py`.

Risco: médio/alto. Superfícies: `codigo/modelos.py`, `codigo/avaliar.py`.

## Objetivo

Acrescentar o modo `--selecao` a `modelos.py` e a `avaliar.py`, no molde do `--ocultar` da issue 03: validação cruzada aninhada que escolhe o tamanho equivalente do prior BDeu e a estrutura (Naive Bayes ou TAN) só com o treino de cada partição externa. Grade e regra de escolha: §9 de `docs/plano-de-analise.md`.

## Contexto

- Ler antes: `AGENTS.md`; `docs/plano-de-analise.md`, §9; issue 03 (molde de modo extra).
- Altera: `codigo/modelos.py`, `codigo/avaliar.py`. Nenhum script novo.
- Cria: `resultados/predicoes_selecao.csv`, `resultados/selecao_dev.csv`, `resultados/selecao_escolha.csv`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | Como na issue 01 |
| `resultados/predicoes_dev.csv`, `resultados/metricas_dev.csv` | Referência para as configurações `nb_ess5` e `tan_ess5` |

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `resultados/predicoes_selecao.csv` | 32.000 linhas: `config,record_id,fold_externo,fold_interno,p_ruim` |
| `resultados/selecao_dev.csv` | 9 linhas (8 configurações e `aninhado`), colunas de `metricas_dev.csv` |
| `resultados/selecao_escolha.csv` | 48 linhas: `fold_externo,config,log_loss_interno,escolhida` |

## Comportamento

1. `montar_rede` ganha o parâmetro `ess` (tamanho equivalente do BDeu). Sem ele, o valor é o de antes (5) e nada muda.
2. Grade fixa, exatamente a da §9: {nb, tan} × {1, 5, 10, 50}, ids `nb_ess1`, `nb_ess5`, `nb_ess10`, `nb_ess50`, `tan_ess1`, `tan_ess5`, `tan_ess10`, `tan_ess50`.
3. `modelos.py --selecao`, para cada partição externa (as 5 da issue 01) e cada configuração:
   - prevê a validação externa treinando no treino externo (`fold_interno = -1`);
   - divide o treino externo em 5 partições internas estratificadas (semente 2026) e, em cada uma, treina no treino interno, com cortes aprendidos nele, e prevê a validação interna.
4. `avaliar.py --selecao` não treina. Lê `predicoes_selecao.csv`; por partição externa (`fold_externo` 0 a 4), escolhe a configuração de menor log loss nas predições internas; no bloco `dev`, faz o mesmo sobre as predições externas. Grava `selecao_escolha.csv`. Grava `selecao_dev.csv`: uma linha por configuração, com as predições externas, e a linha `aninhado`, com a predição externa da configuração escolhida em cada partição.
5. Mede e imprime o tempo total de `modelos.py --selecao`.

## Critérios de aceitação

Os da seção 4, issue 08, de `docs/criterios-de-aceite.md` (itens 1 a 11), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

`--final`, calibração, faixas, seleção de variáveis, K2, hill climbing, outros valores de prior, outro critério de escolha.

## Decisões já tomadas (não perguntar, não mudar)

- Grade e critério de escolha são os da §9 de `docs/plano-de-analise.md`. Nenhum valor de prior além dos quatro aparece no código.
- Os comandos sem `--selecao` continuam gerando arquivos idênticos aos de antes.
- A configuração escolhida é resultado, qualquer que seja. A descrição do PR não comenta valores.

## Hipóteses a confirmar pelo autor

- O tempo de `--selecao` não foi estimado; é medido e registrado no PR.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`, `## Tempo medido`.
