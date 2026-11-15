# Arquitetura

Visão do experimento como o [PLANO.md](../PLANO.md) o define. Este documento não cria decisão nova: onde houver conflito, vale o plano. Os diagramas descrevem o desenho **previsto**; um script só passa a existir depois que a issue dele for mergeada.

## 1. Visão geral

O sistema não tem frontend, backend nem banco de dados. São scripts Python que leem CSV e gravam tabelas e figuras em `resultados/`. A ideia central do trabalho é separar duas coisas: **estimar o risco** (rede bayesiana) e **escolher a ação** (utilidade esperada).

```mermaid
flowchart LR
    D[(dev.csv<br/>800 casos)] --> M[modelos.py<br/>estima o risco p]
    M -->|p_ruim| U[decisao.py<br/>utilidade esperada]
    C[/config/utilidade.json<br/>matriz U/] --> U
    U --> A{{ação:<br/>aprovar, rejeitar<br/>ou análise manual}}
```

## 2. Scripts e arquivos trocados

Sete scripts depois das issues 01 a 07 (hoje existem `preparar_sgc.py` e o `baseline_logreg.py` herdado, que a issue 01 apaga). Cada seta é um arquivo em disco; nenhum modelo é salvo (sem `pickle` nem `joblib`).

```mermaid
flowchart TD
    BR[(dados/brutos)] --> PS[preparar_sgc.py]
    PS --> SGC[(sgc.csv)]
    PS --> DEV[(dev.csv)]
    PS --> TESTE[(teste.csv)]

    DEV --> MOD[modelos.py]
    MOD --> PRED[predicoes_dev.csv]
    MOD --> OCU[predicoes_dev_oculta.csv]
    MOD --> CORTES[cortes.json]

    PRED --> AV[avaliar.py]
    OCU --> AV
    AV --> MET[metricas_dev.csv<br/>calibracao_dev.png<br/>evidencia_incompleta.csv]

    PRED --> DEC[decisao.py]
    UTIL[/config/utilidade.json/] --> DEC
    DEC --> POL[politicas_dev.csv<br/>resumo_politicas_dev.csv]
    TDEC[test_decisao.py] -. confere a conta .-> DEC

    UTIL --> SENS[sensibilidade.py]
    SENS --> SCSV[sensibilidade.csv<br/>sensibilidade.png]

    DEV --> DEMO[demo.py]
    CORTES --> DEMO
    UTIL --> DEMO
    DEMO --> TERM[/texto no terminal/]

    TESTE -. só o autor, uma vez .-> FINAL[modelos.py --final]
```

Regras que o desenho impõe:

- `avaliar.py` nunca treina; só lê predições.
- `demo.py` treina de novo ao abrir, nas 4 partições que não contêm o caso pedido, para mostrar o mesmo risco de `predicoes_dev.csv`.
- O único arquivo de dados que o código lê é `dev.csv`. `teste.csv`, `sgc.csv` e `dados/brutos/` só são tocados por `preparar_sgc.py`.
- A linha pontilhada do teste final não é executada por agente: o caminho `--final` é escrito pela factory e testado com linhas do dev; quem roda sobre o teste é o autor, à mão, uma vez.

## 3. Dentro de `modelos.py`

```mermaid
flowchart TD
    DEV[(dev.csv)] --> SPLIT[5 partições estratificadas<br/>semente 2026]
    SPLIT --> LOOP{para cada partição}
    LOOP --> DISC[cortes por tercis<br/>aprendidos só no treino]
    DISC --> NB[Naive Bayes<br/>rede em estrela]
    DISC --> TAN[TAN<br/>TreeSearch]
    LOOP --> LR[Regressão logística<br/>variáveis contínuas brutas]
    NB --> FIT[fit com prior BDeu<br/>tamanho equivalente 5]
    TAN --> FIT
    FIT --> INF[predict_probability]
    LR --> P
    INF --> P[p_nb, p_tan, p_logreg<br/>probabilidade de RUIM]
    P --> OUT[predicoes_dev.csv<br/>800 linhas]
```

Pontos a lembrar na defesa:

- `kredit`: 0 = ruim, 1 = bom. A classe positiva é **ruim**; toda coluna `p_*` é probabilidade de ruim.
- A discretização em 3 faixas vale só para as redes. A regressão logística recebe as 3 contínuas (`laufzeit`, `hoehe`, `alter`) sem faixas.
- Os cortes são aprendidos no treino de cada partição, para o teste da partição não vazar na discretização.
- `record_id` sai antes de qualquer chamada ao `pgmpy`.

## 4. Camada de decisão

A rede entrega `p`, a probabilidade de o crédito ser ruim. A camada de decisão calcula a utilidade esperada de cada ação e escolhe a maior.

```mermaid
flowchart LR
    P[p = P ruim] --> UEA["UE aprovar<br/>(1-p)·100 + p·(-400)"]
    P --> UER["UE rejeitar<br/>0"]
    P --> UEM["UE análise manual<br/>(1-p)·(100-c) + p·(-c)"]
    UEA --> MAX{maior UE}
    UER --> MAX
    UEM --> MAX
    MAX --> ACAO[ação recomendada]
```

Os valores da matriz vêm de `config/utilidade.json`; os números acima são os da proposta demonstrativa do plano e não ficam escritos no código. Empate (tolerância 1e-9): análise manual, depois rejeitar, depois aprovar.

Como cada UE é uma reta em `p`, a política equivale a limiares sobre `p`. A contribuição do trabalho é **derivar esses limiares dos custos de forma explícita** e mostrar que isso exige probabilidade calibrada. Por isso a comparação é a tabela 2×2 (modelo × regra), e não "utilidade esperada contra limiar".

## 5. Como o código é construído

O código é escrito pela software factory, uma issue por PR, e o autor relê tudo antes do commit de congelamento.

```mermaid
flowchart TD
    I[issue com label factory] --> IN[intake<br/>ACCEPT, NEEDS-INFO ou REJECT]
    IN --> R[route<br/>escolhe revisores]
    R --> SP[spec-writer<br/>spec.md]
    SP --> B[builder<br/>commits e PR em rascunho]
    B --> G{gate<br/>factory/checks.sh}
    G -->|FAIL| B
    G -->|PASS| RV[reviewer-code]
    RV -->|CHANGES| B
    RV -->|PASS| AP[approver]
    AP -->|APPROVE| MG[merge automático]
    AP -->|ESCALATE| H[needs-human<br/>decide o autor]
```

No máximo 3 rodadas por issue; se acabarem sem passar, o job vai para `needs-human`.

## 6. Ordem de execução do experimento

```mermaid
flowchart LR
    P1[1 divisão] --> P3[3 predições dev]
    P3 --> P4[4 métricas]
    P3 --> P5[5 evidência incompleta]
    P3 --> P6[6 decisão]
    P6 --> P7[7 sensibilidade]
    P3 --> P8[8 demo]
    P4 --> P10
    P6 --> P10[10 teste final<br/>autor, à mão, uma vez]
    P10 --> P11[11 monografia]
```

O passo 2 (teste de fumaça do `pgmpy`) abre o `modelos.py` e o 9 (hill climbing) é opcional; ambos ficam fora do desenho acima. O que decide o autor, e não o código: qual modelo vai para a tabela 2×2, se a calibração entra, e os valores de custo.
