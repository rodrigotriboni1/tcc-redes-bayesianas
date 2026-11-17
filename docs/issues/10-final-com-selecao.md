# 10: Caminho do teste final com a configuração selecionada

Depende das issues 07 e 08 já no `main` (a 08 mergeada). Não roda em paralelo com outra issue que altere `modelos.py`, `avaliar.py` ou `decisao.py`.

## Objetivo

Fazer `modelos.py --final` gravar também `p_sel`: a configuração da linha `dev` escolhida em `selecao_escolha.csv`, treinada no dev inteiro. `avaliar.py --final` e `decisao.py --final` tratam `p_sel` como mais um modelo, rotulado secundário.

## Contexto

- Ler antes: `AGENTS.md`, regras duras 1 e 2; issues 07 e 08; `docs/plano-de-analise.md`, §9.
- Altera: `codigo/modelos.py`, `codigo/avaliar.py`, `codigo/decisao.py`.
- Não cria arquivo em `resultados/`.
- Tamanho: um PR só.

**Você não abre o arquivo de teste e não roda `--final` sobre ele.** O autoteste usa o arquivo falso da issue 07.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | Treino, o dev inteiro |
| `resultados/cortes.json` | Cortes das variáveis contínuas |
| `resultados/selecao_escolha.csv` | Configuração do bloco `dev` com `escolhida` verdadeira |
| Arquivo passado como argumento a `modelos.py --final` | Mesmas colunas do `dev.csv` |

## Saídas (geradas só quando o autor executar)

As da issue 07, com `p_sel` em `predicoes_teste.csv` e o modelo `sel`, rotulado secundário, nos arquivos de `avaliar.py --final` e `decisao.py --final`.

## Comportamento

1. `modelos.py --final` lê a configuração escolhida do bloco `dev` de `selecao_escolha.csv`; nenhum id de configuração fica fixo no caminho `--final`.
2. Treina essa configuração no dev inteiro, com os cortes de `cortes.json`, e grava `p_sel` ao lado de `p_nb`, `p_tan` e `p_logreg`.
3. `avaliar.py --final` e `decisao.py --final` incluem `sel` como mais um modelo, rotulado secundário.

## Critérios de aceitação

Os da seção 4, issue 10, de `docs/criterios-de-aceite.md` (itens 1 a 6), sem acréscimo, e os itens 07.2, 07.7 e 07.9 com `p_sel`. Valem também G1 a G9.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

Executar sobre o teste de verdade, refazer a seleção, escolher entre `p_sel` e os modelos principais, calibrar.

## Decisões já tomadas (não perguntar, não mudar)

- `p_sel` é secundário; os modelos principais continuam `nb`, `tan` e `logreg`.
- Nenhum arquivo `*_teste*` entra no PR.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
