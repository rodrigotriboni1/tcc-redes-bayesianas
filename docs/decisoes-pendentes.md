# Decisões pendentes

Lista do que **só o autor** pode decidir, antes ou durante o desenvolvimento. Nasce da revisão do repositório feita pelo opencode em 15/11/2026 (relatório `REVISAO.md`, que não está no git) e de conferências minhas.

Como usar: responda no campo **Decisão**; depois mova a linha para [decisoes.md](decisoes.md) com data e motivo. Nenhuma opção abaixo é recomendação baseada em métrica: ainda não existe resultado, e escolher por resultado é proibido (`AGENTS.md`, regra 3).

Cada item diz se a afirmação foi **conferida** por mim no repositório ou **só da revisão** (não verifiquei).

## 1. Resolvidas em 15/11/2026 (P1 a P7)

P1 a P7 foram decididas e estão registradas em [decisoes.md](decisoes.md), seção "Decidido depois da revisão do repositório". Ficam aqui só as demais.

## 2. Redação e método, sem código novo

| # | Questão | Sugestão da revisão | Conferido | Decisão |
|---|---|---|---|---|
| P8 | A tabela 2×2 chama a diferença de "efeito do modelo" e "efeito da regra", mas a regra fixa (0,5) só tem duas ações e a de utilidade tem três | Descrever como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal. Vale também para `docs/arquitetura.md` | Conferido | |
| P9 | Evidência incompleta: as redes removem a variável; a logística imputa mediana ou moda. A queda por variável não é comparável entre famílias | Separar a tabela por família ou escrever a ressalva na legenda | Só da revisão | |
| P10 | Os estados das variáveis são fixados no dev inteiro (critério 01.8), inclusive categorias que só aparecem na partição de validação | Dizer na seção de materiais e métodos que foi uma simplificação por estabilidade | Conferido | |
| P11 | O ECE do `baseline_logreg.py` é top-label; o novo é sobre P(ruim) | Se a monografia citar o ECE antigo, rotular como "top-label, protocolo anterior" ou recalcular | Conferido | |

## 3. Escopo da proposta que o plano não entrega

A proposta submetida pede coisas que não têm saída no plano. Para cada uma: entra, ou fica como corte registrado?

| # | Item da proposta | O que o plano tem hoje | Decisão |
|---|---|---|---|
| P12 | Etapa B: análise exploratória documentada | Só fatos soltos (categorias raras, 753 valores de `hoehe`); nenhum arquivo em `resultados/` | |
| P13 | Etapa D: registrar a segunda melhor ação e a diferença de utilidade | O demo imprime as utilidades, mas `politicas_dev.csv` não grava | |
| P14 | Etapa E: PR-AUC e custo esperado | Não aparecem; com 30% de ruins PR-AUC é pertinente | |
| P15 | Etapa F: justificativa da recomendação, evidência mais relevante, mudança em relação à prior | A issue 06 põe "explicação textual da decisão" fora do escopo | |
| P16 | Gravar as arestas do TAN por partição | A issue 01 admite que a estrutura muda entre partições, mas não grava o grafo; num TCC de redes bayesianas o grafo é resultado | |

As etapas B a F da proposta foram lidas pelo opencode no `.docx`; eu não as reconferi.

## 4. Mudanças em arquivos que a factory não pode tocar

| # | Questão | Onde | Conferido | Decisão |
|---|---|---|---|---|
| P17 | O gate não busca `clip`, que o `AGENTS.md` proíbe sobre probabilidades | `factory/checks.sh:55` | Só da revisão | |
| P18 | Depois da issue 04, incluir `config/utilidade.json` e `codigo/test_decisao.py` em `protected_paths`. Antes disso a issue 04 não consegue criá-los | `factory/config.json` | Só da revisão | |
| P19 | O critério 03.5 ("ao menos uma predição muda") é de presença de efeito, que os próprios critérios proíbem; o verificador o trata como falha | `docs/criterios-de-aceite.md:118`, `factory/verificar_saidas.py:146` | Só da revisão | |
| P20 | O verificador não cobre os valores das utilidades do demo nem as falhas esperadas do caminho `--final` (07.1 e 07.10) | `factory/verificar_saidas.py` | Só da revisão | |
| P21 | `AGENTS.md` diz "scripts só gravam em `resultados/`" e "nenhum outro arquivo de teste"; o `preparar_sgc.py` e o `test_decisao.py` são exceções. Editar depois do PR #8, que também mexe no arquivo | `AGENTS.md` | Conferido | |

## 5. Orientador e entregas

| # | Questão | Conferido | Decisão |
|---|---|---|---|
| P22 | Prazo de entrega e de defesa; modelo de documento da UFU; aceita a matriz demonstrativa (itens 11.1 a 11.3 do plano) | Conferido | |
| P23 | Avisar a troca de base (SGC) e de protótipo (terminal) (item 11.4) e **registrar também a mudança de alegação**: a proposta fala em "mais consistente e transparente"; o plano afirma derivar limiares dos custos | Conferido | |
| P24 | A folha de rosto da proposta traz "Supervisor: Prof. Dr. [Supervisor's Name]"; conferir se a versão submetida corrigiu | Só da revisão | |
| P25 | As contagens de categorias raras do `PLANO.md:65` (`bishkred`=4: 6; `verw`=8: 9; `verw`=4 e 10: 12) diferem das do dev (5, 7, 9, 9). Provavelmente são da base completa. Quem confere é o autor, no `sgc.csv`, e o plano passa a dizer "na base completa" ou "no dev" | Só da revisão (feita só no dev) | |

## 6. Referências e registros

| # | Questão | Conferido | Decisão |
|---|---|---|---|
| P26 | `russell2010`: o `.bib` mistura título e editora da tradução com ano de 2010. Escolher edição (original ou tradução) e ajustar título, editora, cidade e ano | Só da revisão | |
| P27 | Seção 2.5 do mapa de referências lista `platt1999` junto à regressão isotônica; Platt é sigmoide, a isotônica é de outros autores | Só da revisão | |
| P28 | Cinco entradas têm `% VERIFICAR` no `.bib` (`platt1999`, `gromping2019`, `kaufman2012`, `uci573`, `howard2005`), mas o mapa não mostra a marca, e o plano só fala nas 9 "A CONFERIR". O total a conferir é maior | Só da revisão | |
| P29 | O log de uso de IA (`docs/uso-de-ia.md`) está vazio, mas houve subagente em 15/11/2026, escrita assistida de documentos e revisão por outra IA | Conferido (a tabela está vazia) | |
| P30 | `README.md` tem sete linhas: sem índice da documentação e sem dizer que `factory/` e `.claude/` são processo, não experimento | Conferido | |

## O que já foi resolvido

- Divergências mecânicas de texto: PR #15.
- Erros nos meus documentos de docs: commits nos PRs #4, #5 e #7.
