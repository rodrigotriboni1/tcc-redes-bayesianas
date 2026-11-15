"""Gera as predições dos três modelos no dev por validação cruzada em 5 partições.

Modelos: Naive Bayes (rede em estrela), TAN (rede em árvore) e regressão logística.
Para cada caso do dev, P(ruim) vem do modelo treinado nas outras 4 partições.

Entrada: dados/processados/dev.csv (800 linhas).
Saídas:
  resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
  resultados/tan_arestas.csv    fold,origem,destino (grafo do TAN de cada partição)
  resultados/cortes.json        cortes dos tercis das contínuas no dev inteiro

Uso, a partir da raiz do repositório:
  uv run python codigo/modelos.py              grava as saídas
  uv run python codigo/modelos.py --verificar  roda os autotestes e não grava nada
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pgmpy.estimators import TreeSearch
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteBayesianEstimator
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAIZ = Path(__file__).resolve().parent.parent
DEV = RAIZ / "dados/processados/dev.csv"
SAIDA = RAIZ / "resultados"
CONTINUAS = ["laufzeit", "hoehe", "alter"]
MODELOS = ["nb", "tan", "logreg"]

# kredit: 0 = ruim, 1 = bom
dev = pd.read_csv(DEV)
VARIAVEIS = [c for c in dev.columns if c not in ("record_id", "kredit")]
CATEGORICAS = [c for c in VARIAVEIS if c not in CONTINUAS]
# Estados fixos: tudo que aparece no dev inteiro, para que categoria ausente no treino não quebre a inferência.
ESTADOS = {c: sorted(int(v) for v in dev[c].unique()) for c in CATEGORICAS}
ESTADOS.update({c: [0, 1, 2] for c in CONTINUAS})
ESTADOS["kredit"] = [0, 1]


def build(numeric, categorical):
    # shortcut: colunas não listadas em --numeric são tratadas como categóricas; revisar o dicionário da base.
    pre = ColumnTransformer(
        [("num", StandardScaler(), numeric), ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)]
    )
    return make_pipeline(pre, LogisticRegression(max_iter=1000))


def cortes(treino):
    return {c: [float(v) for v in treino[c].quantile([1 / 3, 2 / 3])] for c in CONTINUAS}


def discretizar(df, cortes_treino):
    df = df.copy()
    for c, (c1, c2) in cortes_treino.items():
        df[c] = np.where(df[c] <= c1, 0, np.where(df[c] <= c2, 1, 2))
    return df


def montar_rede(treino, modelo):
    """Rede treinada (com BDeu) sobre o treino já discretizado e sem record_id."""
    if modelo == "nb":
        rede = DiscreteBayesianNetwork([("kredit", f) for f in VARIAVEIS])
    else:
        dag = TreeSearch(treino).estimate(estimator_type="tan", class_node="kredit", show_progress=False)
        rede = DiscreteBayesianNetwork(dag.edges())
    estimador = DiscreteBayesianEstimator(state_names=ESTADOS, prior_type="BDeu", equivalent_sample_size=5)
    rede.fit(treino, estimator=estimador)
    return rede


def preparar_rede(treino, modelo):
    """Discretiza com cortes do treino e treina a rede. Devolve (rede, cortes)."""
    c = cortes(treino)
    treino = discretizar(treino.drop(columns="record_id"), c)
    return montar_rede(treino, modelo), c


def prever(treino, alvo, modelo, ocultar=None):
    """P(ruim) para cada linha de alvo, na ordem de alvo. Tudo é aprendido só em treino."""
    if ocultar is not None:
        sys.exit("ERRO: ocultar ainda não é suportado")
    if modelo not in MODELOS:
        sys.exit(f"ERRO: modelo desconhecido: {modelo}")
    if modelo == "logreg":
        m = build(CONTINUAS, CATEGORICAS).fit(treino[VARIAVEIS], treino["kredit"])
        return m.predict_proba(alvo[VARIAVEIS])[:, list(m.classes_).index(0)]
    rede, c = preparar_rede(treino, modelo)
    x = discretizar(alvo[VARIAVEIS], c)
    return rede.predict_probability(x)["kredit_0"].to_numpy()


def particoes():
    folds = np.zeros(len(dev), dtype=int)
    for k, (_, va) in enumerate(StratifiedKFold(5, shuffle=True, random_state=2026).split(dev, dev["kredit"])):
        folds[va] = k
    return folds


def main():
    folds = particoes()
    saida = dev[["record_id", "kredit"]].copy()
    saida["fold"] = folds
    for m in MODELOS:
        saida[f"p_{m}"] = np.nan
    arestas = []
    for k in range(5):
        treino, alvo = dev[folds != k], dev[folds == k].drop(columns="kredit")
        for m in ("nb", "logreg"):
            saida.loc[folds == k, f"p_{m}"] = prever(treino, alvo, m)
        # TAN montado aqui para gravar o mesmo grafo que gera as predições
        rede, c = preparar_rede(treino, "tan")
        saida.loc[folds == k, "p_tan"] = rede.predict_probability(discretizar(alvo[VARIAVEIS], c))["kredit_0"].to_numpy()
        arestas += [(k, o, d) for o, d in rede.edges()]
    SAIDA.mkdir(exist_ok=True)
    saida.to_csv(SAIDA / "predicoes_dev.csv", index=False)
    pd.DataFrame(sorted(arestas), columns=["fold", "origem", "destino"]).to_csv(SAIDA / "tan_arestas.csv", index=False)
    (SAIDA / "cortes.json").write_text(json.dumps(cortes(dev)) + "\n")


def verificar():
    folds = particoes()
    gravado = pd.read_csv(SAIDA / "predicoes_dev.csv")
    assert (gravado["fold"].to_numpy() == folds).all()
    treino0, alvo0 = dev[folds != 0], dev[folds == 0].drop(columns="kredit")
    linhas = alvo0.iloc[:5]

    # 5a: prever um conjunto é igual a prever linha por linha
    for m in MODELOS:
        juntos = prever(treino0, linhas, m)
        for i in range(5):
            assert abs(juntos[i] - prever(treino0, linhas.iloc[[i]], m)[0]) < 1e-12, (m, i)

    # 5b: a coluna gravada é igual a prever(dev[fold != k], dev[fold == k])
    for k in range(5):
        treino, alvo = dev[folds != k], dev[folds == k].drop(columns="kredit")
        for m in MODELOS:
            assert np.abs(gravado.loc[folds == k, f"p_{m}"].to_numpy() - prever(treino, alvo, m)).max() < 1e-12, (k, m)

    # 5c: cortes por tercis do treino e faixas 0, 1, 2
    c = cortes(treino0)
    for col in CONTINUAS:
        assert c[col] == [float(v) for v in treino0[col].quantile([1 / 3, 2 / 3])]
        c1, c2 = c[col]
        assert discretizar(pd.DataFrame({col: [c1, c1 + 0.5, c2, c2 + 0.5]}), {col: c[col]})[col].tolist() == [0, 1, 1, 2]

    for m in ("nb", "tan"):
        rede, c = preparar_rede(treino0, m)
        x = discretizar(linhas[VARIAVEIS], c)
        prob = rede.predict_probability(x)
        # 6a: P(ruim) sem evidência = (192 + 2,5)/(640 + 5)
        assert abs(VariableElimination(rede).query(["kredit"]).values[0] - 0.3015503876) < 1e-9, m
        # 6d: as duas colunas somam 1
        assert np.abs(prob["kredit_0"] + prob["kredit_1"] - 1).max() < 1e-9, m
        # 6c: igual a VariableElimination.query
        ve = VariableElimination(rede)
        for i in range(5):
            evid = {v: int(x.iloc[i][v]) for v in VARIAVEIS}
            assert abs(prob["kredit_0"].iloc[i] - ve.query(["kredit"], evidence=evid).values[0]) < 1e-9, (m, i)
        # 6b: no NB, produto normalizado das tabelas de get_cpds()
        if m == "nb":
            cpds = {cpd.variable: cpd for cpd in rede.get_cpds()}
            for i in range(5):
                p = cpds["kredit"].values.copy()
                for v in VARIAVEIS:
                    p = p * cpds[v].values[cpds[v].state_names[v].index(int(x.iloc[i][v]))]
                assert abs(p[0] / p.sum() - prob["kredit_0"].iloc[i]) < 1e-9, i

    # 6e: na regressão, a coluna usada é a da classe 0 (ruim)
    m = build(CONTINUAS, CATEGORICAS).fit(treino0[VARIAVEIS], treino0["kredit"])
    assert list(m.classes_) == [0, 1]
    assert np.abs(m.predict_proba(linhas[VARIAVEIS])[:, 0] - prever(treino0, linhas, "logreg")).max() < 1e-12
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/modelos.py [--verificar]")
    else:
        main()
