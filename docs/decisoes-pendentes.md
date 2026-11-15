# Decisões pendentes

Lista do que **só o autor** pode decidir, antes ou durante o desenvolvimento. Nasce da revisão do repositório feita pelo opencode em 15/11/2026 (relatório `REVISAO.md`, que não está no git) e de conferências minhas.

Como usar: responda no campo **Decisão**; depois mova a linha para [decisoes.md](decisoes.md) com data e motivo. Nenhuma opção abaixo é recomendação baseada em métrica: ainda não existe resultado, e escolher por resultado é proibido (`AGENTS.md`, regra 3).

Cada item diz se a afirmação foi **conferida** por mim no repositório ou **só da revisão** (não verifiquei).

## 1. Resolvidas em 15/11/2026 (P1 a P7)

P1 a P7 foram decididas e estão registradas em [decisoes.md](decisoes.md), seção "Decidido depois da revisão do repositório". Ficam aqui só as demais.

## 2. Resolvidas em 15/11/2026 (P8 a P11)

Registradas em [decisoes.md](decisoes.md), na mesma seção.

## 3. Resolvidas em 15/11/2026 (P12 a P16)

Registradas em [decisoes.md](decisoes.md), na seção "Decidido depois da revisão do repositório". As etapas B a F da proposta foram lidas pelo opencode no `.docx`; eu não as reconferi.

## 4. Mudanças em arquivos que a factory não pode tocar

P17, P19, P20 e P21 foram decididas e aplicadas em 15/11/2026 (registro em [decisoes.md](decisoes.md)). Resta a P18.

| # | Questão | Onde | Conferido | Decisão |
|---|---|---|---|---|
| P18 | Depois da issue 04, incluir `config/utilidade.json` e `codigo/test_decisao.py` em `protected_paths`. Antes disso a issue 04 não consegue criá-los | `factory/config.json` | Só da revisão | |

## 5. Orientador e entregas

P22 a P25 foram tratadas em 15/11/2026 (registro em [decisoes.md](decisoes.md)); ficam em aberto o prazo (entrega ou defesa), o aceite da matriz pelo orientador e o modelo do Colegiado. Ver a seção 6 de `decisoes.md`.

| # | Questão | Conferido | Decisão |
|---|---|---|---|

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
