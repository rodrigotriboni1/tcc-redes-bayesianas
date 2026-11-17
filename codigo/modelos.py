"""Gera as predições dos três modelos no dev por validação cruzada em 5 partições.

Modelos: Naive Bayes (rede em estrela), TAN (rede em árvore) e regressão logística.
Para cada caso do dev, P(ruim) vem do modelo treinado nas outras 4 partições.

Entrada: dados/processados/dev.csv (800 linhas).
Saídas:
  resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
  resultados/tan_arestas.csv    fold,origem,destino (grafo do TAN de cada partição)
  resultados/cortes.json        cortes dos tercis das contínuas no dev inteiro
  resultados/predicoes_dev_oculta.csv  record_id,modelo,variavel_oculta,p_ruim (só com --ocultar)
  resultados/predicoes_teste.csv       record_id,kredit,p_nb,p_tan,p_logreg (só com --final)
  resultados/predicoes_selecao.csv     config,record_id,fold_externo,fold_interno,p_ruim (só com --selecao)

Com --ocultar, os modelos são treinados com as 20 variáveis e cada variável é escondida,
uma por vez, só na previsão: as redes ficam sem aquela evidência e a regressão logística
recebe a mediana (contínuas) ou a moda (categóricas) do treino da partição.

Com --final <arquivo>, os três modelos são treinados no dev inteiro (redes com os cortes de
resultados/cortes.json) e preveem cada linha do arquivo, que precisa ter as colunas do dev.
Recusa sobrescrever predicoes_teste.csv. Esse modo é rodado só pelo autor, uma única vez.

Com --selecao, faz a validação cruzada aninhada da grade de redes (NB e TAN com prior BDeu de
tamanho equivalente 1, 5, 10 e 50). Em cada partição externa, cada rede é treinada no treino
externo e prevê a partição (fold_interno = -1); o treino externo é dividido de novo em 5
partições internas, e cada rede treinada no treino interno prevê a validação interna.
Imprime o tempo total, em segundos.

Uso: a partir da raiz do repositório,
  uv run python codigo/modelos.py              grava as saídas
  uv run python codigo/modelos.py --verificar  roda os autotestes e não grava nada
  uv run python codigo/modelos.py --ocultar    grava só predicoes_dev_oculta.csv
  uv run python codigo/modelos.py --final <arquivo>  grava só predicoes_teste.csv
  uv run python codigo/modelos.py --selecao    grava só predicoes_selecao.csv
"""
import json
import sys
import tempfile
import time
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
# grade da seleção aninhada (§9 do plano de análise), na ordem de desempate
GRADE = {
    "nb_ess1": ("nb", 1), "nb_ess5": ("nb", 5), "nb_ess10": ("nb", 10), "nb_ess50": ("nb", 50),
    "tan_ess1": ("tan", 1), "tan_ess5": ("tan", 5), "tan_ess10": ("tan", 10), "tan_ess50": ("tan", 50),
}

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


def montar_rede(treino, modelo, ess=5):
    """Rede treinada (com BDeu) sobre o treino já discretizado e sem record_id."""
    if modelo == "nb":
        rede = DiscreteBayesianNetwork([("kredit", f) for f in VARIAVEIS])
    else:
        dag = TreeSearch(treino).estimate(estimator_type="tan", class_node="kredit", show_progress=False)
        rede = DiscreteBayesianNetwork(dag.edges())
    estimador = DiscreteBayesianEstimator(state_names=ESTADOS, prior_type="BDeu", equivalent_sample_size=ess)
    rede.fit(treino, estimator=estimador)
    return rede


def preparar_rede(treino, modelo, ess=5):
    """Discretiza com cortes do treino e treina a rede. Devolve (rede, cortes)."""
    c = cortes(treino)
    treino = discretizar(treino.drop(columns="record_id"), c)
    return montar_rede(treino, modelo, ess), c


def treinar(treino, modelo, ess=5):
    """Regressão logística treinada ou (rede, cortes)."""
    if modelo == "logreg":
        return build(CONTINUAS, CATEGORICAS).fit(treino[VARIAVEIS], treino["kredit"])
    return preparar_rede(treino, modelo, ess)


def preencher(treino, alvo, ocultar):
    """Regra D2: a coluna escondida recebe a mediana (contínua) ou a moda (categórica) do treino; empate na moda fica com o menor valor."""
    x = alvo[VARIAVEIS].copy()
    x[ocultar] = treino[ocultar].median() if ocultar in CONTINUAS else treino[ocultar].mode().iloc[0]
    return x


def aplicar(treinado, treino, alvo, modelo, ocultar=None):
    """P(ruim) de alvo com um modelo já treinado, opcionalmente sem a variável ocultar."""
    if modelo == "logreg":
        x = alvo[VARIAVEIS] if ocultar is None else preencher(treino, alvo, ocultar)
        return treinado.predict_proba(x)[:, list(treinado.classes_).index(0)]
    rede, c = treinado
    x = discretizar(alvo[VARIAVEIS], c)
    if ocultar is not None:
        # sem a coluna, a rede soma sobre os valores da variável escondida
        x = x.drop(columns=ocultar)
    return rede.predict_probability(x)["kredit_0"].to_numpy()


def prever(treino, alvo, modelo, ocultar=None, ess=5):
    """P(ruim) para cada linha de alvo, na ordem de alvo. Tudo é aprendido só em treino."""
    if modelo not in MODELOS:
        sys.exit(f"ERRO: modelo desconhecido: {modelo}")
    if ocultar is not None and ocultar not in VARIAVEIS:
        sys.exit(f"ERRO: variável desconhecida para ocultar: {ocultar}")
    return aplicar(treinar(treino, modelo, ess), treino, alvo, modelo, ocultar)


def particoes():
    folds = np.zeros(len(dev), dtype=int)
    for k, (_, va) in enumerate(StratifiedKFold(5, shuffle=True, random_state=2026).split(dev, dev["kredit"])):
        folds[va] = k
    return folds


def calcular():
    """Validação cruzada: devolve a tabela de predições e as arestas do TAN de cada partição."""
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
    return saida, pd.DataFrame(sorted(arestas), columns=["fold", "origem", "destino"])


def calcular_oculta():
    """Validação cruzada com cada variável escondida. Devolve a tabela e os pares em que nada mudou."""
    folds = particoes()
    completo = {m: np.zeros(len(dev)) for m in MODELOS}
    oculta = {(m, v): np.zeros(len(dev)) for m in MODELOS for v in VARIAVEIS}
    for k in range(5):
        treino, alvo = dev[folds != k], dev[folds == k].drop(columns="kredit")
        for m in MODELOS:
            # um treino por partição e modelo, reaproveitado nas 20 variáveis
            treinado = treinar(treino, m)
            completo[m][folds == k] = aplicar(treinado, treino, alvo, m)
            for v in VARIAVEIS:
                oculta[(m, v)][folds == k] = aplicar(treinado, treino, alvo, m, v)
    partes = [pd.DataFrame({"record_id": dev["record_id"], "modelo": m, "variavel_oculta": v, "p_ruim": p}) for (m, v), p in oculta.items()]
    iguais = [(m, v) for (m, v), p in oculta.items() if np.array_equal(p, completo[m])]
    return pd.concat(partes, ignore_index=True), iguais


def main_oculta():
    tabela, iguais = calcular_oculta()
    for m, v in iguais:
        print(f"AVISO: esconder {v} não mudou nenhuma predição de {m}")
    SAIDA.mkdir(exist_ok=True)
    tabela.to_csv(SAIDA / "predicoes_dev_oculta.csv", index=False)


def selecao_particao(k, folds):
    """Predições da grade na partição externa k (fold_interno = -1) e nas 5 validações internas do treino externo."""
    treino, alvo = dev[folds != k], dev[folds == k]
    internos = np.zeros(len(treino), dtype=int)
    for j, (_, va) in enumerate(StratifiedKFold(5, shuffle=True, random_state=2026).split(treino, treino["kredit"])):
        internos[va] = j
    partes = []
    for config, (m, ess) in GRADE.items():
        pares = [(-1, treino, alvo)] + [(j, treino[internos != j], treino[internos == j]) for j in range(5)]
        for j, tr, va in pares:
            partes.append(pd.DataFrame({"config": config, "record_id": va["record_id"].to_numpy(), "fold_externo": k,
                                        "fold_interno": j, "p_ruim": prever(tr, va, m, ess=ess)}))
    return pd.concat(partes, ignore_index=True)


def main_selecao():
    inicio = time.perf_counter()
    folds = particoes()
    tabela = pd.concat([selecao_particao(k, folds) for k in range(5)], ignore_index=True)
    SAIDA.mkdir(exist_ok=True)
    tabela.to_csv(SAIDA / "predicoes_selecao.csv", index=False)
    print(f"tempo total de --selecao: {time.perf_counter() - inicio:.1f} s")


def main():
    saida, arestas = calcular()
    SAIDA.mkdir(exist_ok=True)
    saida.to_csv(SAIDA / "predicoes_dev.csv", index=False)
    arestas.to_csv(SAIDA / "tan_arestas.csv", index=False)
    (SAIDA / "cortes.json").write_text(json.dumps(cortes(dev)) + "\n")


def final(entrada, pasta):
    """Treina no dev inteiro com os cortes de pasta/cortes.json e grava pasta/predicoes_teste.csv."""
    entrada, destino = Path(entrada), Path(pasta) / "predicoes_teste.csv"
    if not entrada.exists():
        sys.exit(f"ERRO: arquivo ausente: {entrada}")
    alvo = pd.read_csv(entrada)
    faltando = [c for c in dev.columns if c not in alvo.columns]
    if faltando:
        sys.exit(f"ERRO: colunas ausentes em {entrada.name}: {', '.join(faltando)}")
    if destino.exists():
        sys.exit(f"ERRO: {destino.name} já existe; não sobrescrevo")
    c = json.loads((Path(pasta) / "cortes.json").read_text())
    treino = discretizar(dev.drop(columns="record_id"), c)
    x = alvo.drop(columns="kredit")
    saida = alvo[["record_id", "kredit"]].copy()
    for m in ("nb", "tan"):
        saida[f"p_{m}"] = montar_rede(treino, m).predict_probability(discretizar(x[VARIAVEIS], c))["kredit_0"].to_numpy()
    saida["p_logreg"] = prever(dev, x, "logreg")
    saida.to_csv(destino, index=False)


def verificar():
    folds = particoes()
    gravado, _ = calcular()
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

    for m in ("nb", "tan"):
        rede, c = preparar_rede(treino0, m)
        x = discretizar(linhas[VARIAVEIS], c)
        ve = VariableElimination(rede)
        cpds = {cpd.variable: cpd for cpd in rede.get_cpds()}
        for v in VARIAVEIS:
            p_oculta = prever(treino0, linhas, m, ocultar=v)
            for i in range(5):
                # 8b: igual a VariableElimination.query com a evidência sem a variável escondida
                evid = {u: int(x.iloc[i][u]) for u in VARIAVEIS if u != v}
                assert abs(p_oculta[i] - ve.query(["kredit"], evidence=evid).values[0]) < 1e-9, (m, v, i)
                # 8a: no NB, produto normalizado das tabelas sem o fator da variável escondida
                if m == "nb":
                    p = cpds["kredit"].values.copy()
                    for u in VARIAVEIS:
                        if u != v:
                            p = p * cpds[u].values[cpds[u].state_names[u].index(int(x.iloc[i][u]))]
                    assert abs(p[0] / p.sum() - p_oculta[i]) < 1e-9, (v, i)

    # 8c: na regressão, ocultar é igual a prever sem ocultar com a coluna preenchida pela regra D2
    for v in VARIAVEIS:
        preenchido = linhas.copy()
        preenchido[v] = treino0[v].median() if v in CONTINUAS else treino0[v].mode().iloc[0]
        assert np.abs(prever(treino0, linhas, "logreg", ocultar=v) - prever(treino0, preenchido, "logreg")).max() < 1e-12, v

    # 08.3: P(ruim) sem evidência = (192 + s/2)/(640 + s) para cada prior da grade
    for m, ess in GRADE.values():
        rede, _ = preparar_rede(treino0, m, ess)
        assert abs(VariableElimination(rede).query(["kredit"]).values[0] - (192 + ess / 2) / (640 + ess)) < 1e-9, (m, ess)

    sel0 = selecao_particao(0, folds)
    # 08.4: guarda de vazamento: a validação interna 0 vem de uma rede treinada só no treino interno
    internos = np.zeros(len(treino0), dtype=int)
    for j, (_, va) in enumerate(StratifiedKFold(5, shuffle=True, random_state=2026).split(treino0, treino0["kredit"])):
        internos[va] = j
    tr, va = treino0[internos != 0], treino0[internos == 0].iloc[:5]
    for config, (m, ess) in GRADE.items():
        p = sel0[(sel0["config"] == config) & (sel0["fold_interno"] == 0)].set_index("record_id").loc[va["record_id"], "p_ruim"]
        assert np.abs(p.to_numpy() - prever(tr, va, m, ess=ess)).max() < 1e-12, config
    # 08.5: nb_ess5 e tan_ess5 na partição externa 0 iguais a p_nb e p_tan de calcular()
    for m in ("nb", "tan"):
        p = sel0[(sel0["config"] == f"{m}_ess5") & (sel0["fold_interno"] == -1)]["p_ruim"].to_numpy()
        assert np.abs(p - gravado.loc[folds == 0, f"p_{m}"].to_numpy()).max() < 1e-12, m

    # 07: --final com um arquivo falso feito da partição 0 do dev, gravado numa pasta temporária
    with tempfile.TemporaryDirectory() as pasta:
        # cortes.json gravado como em main(); o gate confere byte a byte que o commitado é este
        (Path(pasta) / "cortes.json").write_text(json.dumps(cortes(dev)) + "\n")
        falso = dev[folds == 0]
        falso.to_csv(Path(pasta) / "falso.csv", index=False)
        final(Path(pasta) / "falso.csv", pasta)
        teste = pd.read_csv(Path(pasta) / "predicoes_teste.csv")
        assert len(teste) == 160 and list(teste["record_id"]) == list(falso["record_id"])
        for m in MODELOS:
            assert np.abs(teste[f"p_{m}"].to_numpy() - prever(dev, falso.drop(columns="kredit"), m)).max() < 1e-12, m
        # a recusa acontece antes de qualquer treino
        try:
            final(Path(pasta) / "falso.csv", pasta)
            assert False, "--final sobrescreveu predicoes_teste.csv"
        except SystemExit:
            pass
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:] == ["--ocultar"]:
        main_oculta()
    elif sys.argv[1:] == ["--selecao"]:
        main_selecao()
    elif sys.argv[1:2] == ["--final"] and len(sys.argv) == 3:
        final(sys.argv[2], SAIDA)
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/modelos.py [--verificar | --ocultar | --selecao | --final <arquivo>]")
    else:
        main()
