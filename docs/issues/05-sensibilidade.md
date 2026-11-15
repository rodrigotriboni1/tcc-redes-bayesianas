# 05: Mostrar como as fronteiras de decisão mudam com os custos

Onda 3. Depende da issue 04 já no `main`. Pode rodar em paralelo com a 03 e a 06.

## Objetivo

Criar `codigo/sensibilidade.py`, que calcula e desenha as fronteiras entre aprovar, análise manual e rejeitar para vários valores de perda e de custo da análise. Passo 7 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, item 5 (matriz e fronteiras).
- Cria: `codigo/sensibilidade.py`, `resultados/sensibilidade.csv`, `resultados/sensibilidade.png`.
- Não altera `decisao.py` nem `config/utilidade.json`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `config/utilidade.json` | Ganho de aprovar um caso bom |

O script é analítico: não lê predições nem dados.

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `resultados/sensibilidade.csv` | 84 linhas: `perda,custo_analise,limiar_inferior,limiar_superior` |
| `resultados/sensibilidade.png` | Custo da análise no eixo x, risco no eixo y, uma curva ou painel por perda, regiões nomeadas |

## Comportamento

1. Monta a grade: perda em {200, 400, 600, 800} e custo da análise em {0, 5, …, 100}.
2. Para cada ponto, calcula os dois limiares de risco: abaixo do inferior aprova, entre os dois vai para análise manual, acima do superior rejeita. Quando a análise manual nunca compensa, os dois limiares coincidem.
3. Usa a função de utilidade esperada de `decisao.py`; não repete a conta.
4. Grava a tabela e o gráfico.
5. No modo `--verificar`, confere em cada ponto da grade que a ação escolhida por `decisao.py` muda exatamente nos limiares calculados.

## Critérios de aceitação

Os da seção 4, issue 05, de `docs/criterios-de-aceite.md` (itens 1 a 7), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

Sensibilidade com dados (distribuição das ações no dev), variar o ganho, gráfico interativo, comparar modelos, mudar `decisao.py` ou o JSON.

## Decisões já tomadas (não perguntar, não mudar)

- A grade é a do item 1.
- A hipótese da análise manual é a do plano: o analista acerta e custa `c`.

## Hipóteses a confirmar pelo autor

- Forma do gráfico: uma curva por perda no mesmo painel ou um painel por perda.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
