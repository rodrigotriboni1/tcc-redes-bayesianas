# APÊNDICES

<!-- rascunho de 18/11/2026. Fontes: docs/reproduzir.md (A), docs/uso-de-ia.md (B), cap. 4 (C), docs/plano-de-analise.md (D). Trechos entre colchetes e comentários "confirmar" são do autor. -->

## APÊNDICE A – Como reproduzir os resultados

Todos os arquivos de `resultados/` são gerados por sete scripts Python que leem CSV e gravam tabelas e figuras, sem servidor, banco de dados nem modelo salvo em arquivo [fonte: PLANO.md §3 e §7]. Os comandos abaixo partem da raiz do repositório, rodam sem interação e usam Python 3.12 com as dependências travadas pelo `uv`, inclusive o `pgmpy` 1.1.2 [fonte: docs/reproduzir.md §1].

### A.1 Ambiente

```bash
uv sync --frozen
```

A opção `--frozen` instala exatamente as versões do `uv.lock`. A versão do `pgmpy` não deve ser atualizada, porque a interface da biblioteca mudou entre as versões 1.0 e 1.1.2 [fonte: PLANO.md §3].

### A.2 Ordem de execução

Cada script grava apenas em `resultados/`; a exceção é `preparar_sgc.py`, que grava em `dados/processados/`. Toda fonte de aleatoriedade usa a semente 2026, e rodar o mesmo comando duas vezes gera arquivos CSV e JSON idênticos byte a byte [fonte: AGENTS.md, seção "Reprodutibilidade"]. As figuras PNG não foram comparadas byte a byte entre execuções [fonte: docs/reproduzir.md §4].

**Quadro A.1** – Comandos, em ordem, e arquivos gravados [fonte: docs/reproduzir.md §2]

| Passo | Comando | Grava |
|---|---|---|
| Divisão desenvolvimento/teste | `uv run python codigo/preparar_sgc.py` | `dados/processados/sgc.csv`, `dev.csv`, `teste.csv`, `SHA256SUMS` |
| Predições no desenvolvimento | `uv run python codigo/modelos.py` | `predicoes_dev.csv`, `cortes.json`, `tan_arestas.csv` |
| Métricas e calibração | `uv run python codigo/avaliar.py` | `metricas_dev.csv`, `calibracao_dev.png` |
| Evidência incompleta | `uv run python codigo/modelos.py --ocultar`, depois `uv run python codigo/avaliar.py --ocultar` | `predicoes_dev_oculta.csv`, `evidencia_incompleta.csv` |
| Camada de decisão | `uv run python codigo/decisao.py` | `politicas_dev.csv`, `resumo_politicas_dev.csv` |
| Sensibilidade | `uv run python codigo/sensibilidade.py` | `sensibilidade.csv`, `sensibilidade.png` |
| Estudo de seleção (secundário) | `uv run python codigo/modelos.py --selecao`, depois `uv run python codigo/avaliar.py --selecao` | `predicoes_selecao.csv`, `selecao_dev.csv`, `selecao_escolha.csv` |
| Demonstração | `uv run python codigo/demo.py <record_id> [--modelo nb\|tan\|logreg]` | nada; imprime no terminal |

### A.3 Autotestes e conferência

Os scripts `modelos.py`, `avaliar.py` e `sensibilidade.py` têm o modo `--verificar`, que confere contas com resposta conhecida e não grava nada; `test_decisao.py` usa apenas `assert` e inclui o exemplo da apresentação de 15/10/2026 (com p = 0,20, ganho de 100 e perda de 400, a utilidade esperada de aprovar é 0; com perda de 600, é −40) [fonte: docs/reproduzir.md §3].

```bash
uv run python codigo/modelos.py --verificar
uv run python codigo/avaliar.py --verificar
uv run python codigo/sensibilidade.py --verificar
uv run python codigo/test_decisao.py
```

Os arquivos gerados são versionados junto com o código. Depois de rodar tudo, a reprodução é confirmada se o comando abaixo não imprimir nada e terminar com código 0:

```bash
git diff --exit-code -- 'resultados/*.csv' 'resultados/*.json'
```

Esse teste confere que os arquivos são idênticos aos publicados, não que o modelo é bom [fonte: docs/reproduzir.md §6].

### A.4 Teste final

O conjunto de teste foi usado uma única vez, em 17/11/2026, sobre o commit de congelamento `49d77ff`. A decisão original era que o autor rodasse os comandos à mão; na prática, eles foram executados por um agente Claude (o orquestrador), a pedido explícito do autor, todos com código de saída 0, e o agente não leu o arquivo de teste (apenas o script o leu) [fonte: docs/decisoes.md, registro de 17/11/2026; docs/reproduzir.md §5]. Os comandos, na ordem, foram:

```bash
uv run python codigo/modelos.py --final <arquivo do teste>
uv run python codigo/avaliar.py --final
uv run python codigo/decisao.py --final
```

Eles gravam `predicoes_teste.csv`, `metricas_teste.csv`, `calibracao_teste.png`, `politicas_teste.csv`, `resumo_politicas_teste.csv` e `diferenca_politicas_teste.csv`; os intervalos usam bootstrap com 2000 reamostras e semente 2026. O primeiro comando exige o caminho do arquivo de teste como argumento e recusa sobrescrever `predicoes_teste.csv` se ele já existir [fonte: docs/reproduzir.md §5].

Quem reproduz sem o arquivo de teste obtém todos os resultados de desenvolvimento, mas não os `*_teste*`: a divisão é determinística (semente 2026) e sai de `dados/brutos/`, que não acompanha a descrição do código [fonte: docs/reproduzir.md §6].
<!-- confirmar: se os dados brutos (UCI) e o `teste.csv` entram no repositório entregue à banca; hoje a regra do projeto é que nenhum agente os lê -->

---

## APÊNDICE B – Declaração de uso de inteligência artificial

O autor recebeu do orientador, em 19/10/2026, autorização para usar inteligência artificial como apoio ao trabalho, com o objetivo de otimizar o tempo [fonte: docs/uso-de-ia.md, "Acordo de trabalho"]. Esta declaração descreve os usos, o que foi aproveitado e como cada um foi validado. O registro completo, linha a linha, está em `docs/uso-de-ia.md`. A IA não foi usada como comprovação de resultado: os números do texto apontam para arquivos de `resultados/`, gerados pelo código.

**Quadro B.1** – Usos de IA no trabalho [fonte: docs/uso-de-ia.md, "Registro de uso"]

| Uso | Ferramenta | O que foi aproveitado | Como foi validado |
|---|---|---|---|
| Código dos sete scripts e arquivos de `resultados/` | Software factory de agentes Claude (intake, especificação, construção, revisão e aprovação), com roteamento de modelos por risco | O código de `codigo/` | Gate automático (`factory/checks.sh`: autotestes `--verificar`, execução do zero, comparação com `resultados/`); leitura de cada PR pelo autor depois do merge; releitura de todo o código antes do commit de congelamento |
| Critérios de aceite, issues, plano de análise e documentos de apoio (`docs/`) | Claude Code (Sonnet 5.5 e Fable 5.2) e subagentes Claude | O texto dos documentos, depois de decisões do autor | Conferência contra `PLANO.md` e critérios; decisões do autor registradas em `docs/decisoes.md`. Não conferidos: tradução das variáveis do glossário (feita de memória) e diagramas Mermaid (não renderizados) |
| Revisão do repositório | opencode v2.3.0 com o modelo DeepSeek 4.1 flash (informado pelo autor) | Lista de pendências | Cinco achados reconferidos no repositório; os demais registrados como "só da revisão" |
| Pesquisa das normas do curso | Claude Code com busca web e leitura de PDFs | Estrutura exigida e regras de formatação | PDFs oficiais da FEELT lidos diretamente; vigência para o curso ainda a confirmar com a coordenação |
| Referências bibliográficas | Claude Code | Sugestão e conferência de entradas de `monografia/referencias.bib` | Conferência contra Crossref, páginas de editoras e catálogos (`docs/conferencia-referencias.md`); referências não abertas no original permanecem marcadas no texto e só entram na versão final depois da confirmação do autor |
| Rascunho dos capítulos 1 a 6, do resumo e destes apêndices | Subagentes Claude Code e Claude Code | Rascunhos a partir de `PLANO.md`, `docs/` e `resultados/` | Cada número aponta para o arquivo de origem; leitura e correção pelo autor [confirmar] |

<!-- confirmar com o autor antes de entregar:
  1. `docs/uso-de-ia.md` não tem linha para o rascunho dos capítulos (PRs #52 a #63) nem para o resumo e referências; a última linha do Quadro B.1 foi inferida do histórico do git. Acrescentar ao registro, com modelo e validação, e corrigir aqui se for diferente.
  2. As linhas "Agentes avulsos" e "decisões por delegação" de 17/11/2026 (PRs #43 e #47) estão marcadas no registro como "não conferido pelo autor". Se continuarem assim na entrega, a declaração tem de dizer isso.
  3. O orientador ainda não confirmou quais usos aceita nem como devem ser declarados (fim de docs/uso-de-ia.md). -->

Limites declarados: a IA pode produzir referências inexistentes e afirmações incorretas; por isso nenhuma referência foi tratada como real sem conferência na fonte, e nenhum resultado numérico depende de texto gerado por IA. As escolhas que dependem de um número (modelo principal, calibração, valores de utilidade) são do autor e estão em `docs/decisoes.md`; as tomadas por delegação, com o autor ausente, estão marcadas ali como "a rever pelo autor".

---

## APÊNDICE C – Resultados dos três modelos

Os três modelos (Naive Bayes, TAN e regressão logística) aparecem lado a lado nas Tabelas 4.1, 4.3, 4.5, 4.6 e 4.7 do capítulo 4; o TAN é o modelo da comparação principal por decisão de 15/11/2026, tomada antes de qualquer métrica [fonte: PLANO.md §5]. Por isso este apêndice não repete as tabelas. Se o formato do curso exigir os três modelos fora do corpo do texto, as Tabelas 4.3, 4.6 e 4.7 passam para cá, com as linhas `nb` e `logreg` no apêndice e `tan` no capítulo.
<!-- decidir: manter as tabelas completas no capítulo 4 (como está) ou mover as linhas nb/logreg para este apêndice, como previa o PLANO.md §5 -->

## APÊNDICE D – Plano de análise

O plano de análise, fixado antes da abertura do conjunto de teste, é o documento `docs/plano-de-analise.md` do repositório e entra aqui na íntegra na versão final [fonte: monografia/esqueleto.md, Apêndices].
<!-- pendente: copiar o conteúdo de docs/plano-de-analise.md quando o formato do curso for definido -->
