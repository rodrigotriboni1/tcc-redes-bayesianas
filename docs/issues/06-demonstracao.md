# 06: Demonstrar um caso no terminal

Onda 3. Depende das issues 01 e 04 já no `main`. Pode rodar em paralelo com a 03 e a 05.

## Objetivo

Criar `codigo/demo.py`, que recebe um `record_id` do dev e mostra o risco estimado, a utilidade esperada de cada ação e a ação recomendada. É a demonstração usada na defesa. Passo 8 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, item 7 (notas sobre `demo.py`).
- Cria: `codigo/demo.py`.
- Não altera `modelos.py` nem `decisao.py`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | O caso pedido e os dados de treino |
| `resultados/predicoes_dev.csv` | Coluna `fold`, para saber em que partição o caso está |
| `config/utilidade.json` | Matriz de utilidade |

## Saídas

Só texto no terminal. Nenhum arquivo.

## Comportamento

1. Recebe `<record_id>` e, opcionalmente, `--modelo nb|tan|logreg` (padrão `tan`).
2. Treina os três modelos nas 4 partições que não contêm o caso, com `modelos.prever`.
3. Imprime, nesta ordem: as 20 variáveis do caso; a probabilidade de ruim nos três modelos, com 6 casas; a utilidade esperada de cada ação para o modelo escolhido; as fronteiras de risco; a ação recomendada.
4. `record_id` inexistente ou fora do dev: uma linha de mensagem em português e saída diferente de 0, sem traceback.
5. Sem argumento: mensagem de uso e saída 2.

## Critérios de aceitação

Os da seção 4, issue 06, de `docs/criterios-de-aceite.md` (itens 1 a 7), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

Digitar um caso novo, esconder variável, interface web, cores ou bibliotecas de terminal, explicação textual da decisão, casos do teste.

## Decisões já tomadas (não perguntar, não mudar)

- Treinar nas 4 partições sem o caso faz o número da tela ser o mesmo de `predicoes_dev.csv`, que é o da monografia.
- Não existe modelo salvo em arquivo; o treino é refeito a cada execução.
- Usa as funções de `modelos.py` e `decisao.py`; não repete contas.

## Hipóteses a confirmar pelo autor

- Mostrar as variáveis com o nome alemão da base. A tradução fica para a monografia.
- Formato exato do texto impresso fica a critério do construtor, desde que os itens do passo 3 apareçam na ordem.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
