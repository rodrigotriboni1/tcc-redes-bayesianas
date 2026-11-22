"""Auditoria independente: refaz em NumPy as contas do experimento e compara com os arquivos gravados.

Não usa pgmpy, scikit-learn nem pandas. Recalcula:
  1. a divisão estratificada em 5 partições (semente 2026) e os cortes por tercis;
  2. a árvore do TAN de cada partição (informação mútua condicional à classe, árvore geradora máxima);
  3. a estimação com prior BDeu (tamanho equivalente 5) e a inferência exata de Naive Bayes e TAN,
     treinando nas outras 4 partições e prevendo cada partição do dev;
  4. Brier, log loss, erro de calibração (10 faixas), ROC-AUC e PR-AUC, sobre as predições gravadas
     do dev (por partição) e do teste (todas as linhas juntas);
  5. as ações e a utilidade média das políticas (3 ações, 2 ações e corte 0,5), no dev e no teste.

O teste só entra por resultados/predicoes_teste.csv; o arquivo de linhas do teste não é aberto.
Não treina nada sobre o teste e não grava arquivo. Mostra a maior diferença de cada conferência e
termina com código diferente de 0 se alguma passar de 1e-12 (números) ou diferir (ações e contagens).

Entradas: dados/processados/dev.csv, config/utilidade.json e, em resultados/: predicoes_dev.csv,
  predicoes_teste.csv, tan_arestas.csv, cortes.json, metricas_dev.csv, metricas_teste.csv,
  politicas_dev.csv, politicas_teste.csv, resumo_politicas_dev.csv, resumo_politicas_teste.csv,
  duas_acoes_teste.csv.
Saídas: nenhuma além do texto impresso.

Uso: a partir da raiz do repositório,
  uv run python codigo/auditoria_independente.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
SEMENTE = 2026
PARTICOES = 5
TAMANHO_EQUIVALENTE = 5
TOL = 1e-12  # diferença numérica máxima aceita
CONTINUAS = ["laufzeit", "hoehe", "alter"]
MODELOS = ["nb", "tan", "logreg"]
ACOES = ["aprovar", "rejeitar", "analise_manual"]
PRIORIDADE = ["analise_manual", "rejeitar", "aprovar"]  # empate de UE: a primeira vence
DUAS = ["rejeitar", "aprovar"]  # empate na política de duas ações: rejeitar
TOLERANCIA_UE = 1e-9
CORTE = 0.5
falhas = []


def ler(caminho):
    """CSV como dicionário coluna -> lista de textos. Termina com erro se o arquivo não existir."""
    if not caminho.exists():
        sys.exit(f"ERRO: arquivo ausente: {caminho.name}")
    with open(caminho, newline="") as f:
        linhas = list(csv.DictReader(f))
    return {c: [r[c] for r in linhas] for c in linhas[0]}


def numeros(tab, coluna):
    return np.array([float(v) for v in tab[coluna]])


def conferir(nome, diferenca, tolerancia=TOL):
    """Imprime a maior diferença e guarda a falha se passar da tolerância."""
    ok = diferenca <= tolerancia
    print(f"{'ok   ' if ok else 'FALHA'} {nome}: maior diferença {diferenca:.2e}")
    if not ok:
        falhas.append(nome)


def conferir_igual(nome, esperado, obtido):
    """Para ações, contagens e arestas: tem de ser exatamente igual."""
    diferentes = sum(a != b for a, b in zip(esperado, obtido)) + abs(len(esperado) - len(obtido))
    print(f"{'ok   ' if diferentes == 0 else 'FALHA'} {nome}: {diferentes} diferenças em {len(esperado)}")
    if diferentes:
        falhas.append(nome)


# ---------- dados e partições ----------

dev = ler(RAIZ / "dados/processados/dev.csv")
VARIAVEIS = [c for c in dev if c not in ("record_id", "kredit")]
CATEGORICAS = [c for c in VARIAVEIS if c not in CONTINUAS]
valores = {c: numeros(dev, c) for c in VARIAVEIS}
kredit = np.array([int(v) for v in dev["kredit"]])  # 0 = ruim, 1 = bom
N = len(kredit)
# estados de cada categórica = valores distintos do dev inteiro; contínuas viram 3 faixas (0, 1, 2)
ESTADOS = {c: np.unique(valores[c]) for c in CATEGORICAS}
CARD = {c: len(ESTADOS[c]) for c in CATEGORICAS} | {c: 3 for c in CONTINUAS} | {"kredit": 2}


def particoes(y):
    """Partição de cada linha: reimplementação do StratifiedKFold(5, shuffle=True, random_state=2026)."""
    classes, primeira, inverso = np.unique(y, return_index=True, return_inverse=True)
    codigo = np.argsort(np.argsort(primeira))[inverso]  # classes numeradas pela ordem da primeira aparição
    ordenado = np.sort(codigo)
    alocacao = np.array([np.bincount(ordenado[i::PARTICOES], minlength=len(classes)) for i in range(PARTICOES)])
    sorteio = np.random.RandomState(SEMENTE)
    folds = np.empty(len(y), dtype=int)
    for k in range(len(classes)):
        da_classe = np.arange(PARTICOES).repeat(alocacao[:, k])
        sorteio.shuffle(da_classe)
        folds[codigo == k] = da_classe
    return folds


def cortes(linhas):
    """Cortes dos tercis (interpolação linear) de cada contínua, calculados nas linhas dadas."""
    return {c: np.quantile(valores[c][linhas], [1 / 3, 2 / 3]) for c in CONTINUAS}


def codificar(linhas, corte):
    """Dicionário variável -> código inteiro (0, 1, ...) nas linhas dadas; contínuas pelas faixas dos cortes."""
    saida = {}
    for c in CATEGORICAS:
        saida[c] = np.searchsorted(ESTADOS[c], valores[c][linhas])
    for c in CONTINUAS:
        c1, c2 = corte[c]
        v = valores[c][linhas]
        saida[c] = np.where(v <= c1, 0, np.where(v <= c2, 1, 2))
    return saida


# ---------- árvore do TAN ----------

def info_mutua(a, b):
    """Informação mútua (em nats) entre dois vetores de códigos inteiros."""
    n = len(a)
    ka, kb = a.max() + 1, b.max() + 1
    p = np.bincount(a * kb + b, minlength=ka * kb).reshape(ka, kb) / n
    pa, pb = p.sum(axis=1, keepdims=True), p.sum(axis=0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log(p[nz] / (pa @ pb)[nz])).sum())


def arvore_tan(x, y):
    """Pai de cada variável na árvore do TAN (None na raiz), como o TreeSearch do pgmpy.

    1. Raiz: a coluna (kredit incluída) com maior soma de informação mútua com as demais.
    2. Peso de cada par de variáveis: informação mútua condicional à classe, soma sobre as classes
       de P(classe) vezes a informação mútua dentro da classe.
    3. Árvore geradora máxima por Kruskal (pares em ordem de coluna; empate: o primeiro vence).
    4. Arestas orientadas a partir da raiz.
    """
    todas = VARIAVEIS + ["kredit"]
    cod = dict(x, kredit=y)
    soma = np.array([sum(info_mutua(cod[u], cod[v]) for v in todas if v != u) for u in todas])
    if (soma == soma.max()).sum() != 1:
        sys.exit("ERRO: empate na escolha da raiz do TAN")
    raiz = todas[int(soma.argmax())]
    if raiz == "kredit":
        sys.exit("ERRO: a raiz do TAN seria a classe")
    n = len(y)
    pares = [(u, v) for i, u in enumerate(VARIAVEIS) for v in VARIAVEIS[i + 1:]]
    peso = {}
    for u, v in pares:
        peso[(u, v)] = sum((y == c).sum() / n * info_mutua(cod[u][y == c], cod[v][y == c]) for c in (0, 1))
    # Kruskal: ordena por peso decrescente (sort estável) e junta componentes
    componente = {v: v for v in VARIAVEIS}

    def achar(v):
        while componente[v] != v:
            v = componente[v]
        return v

    vizinhos = {v: [] for v in VARIAVEIS}
    for u, v in sorted((p for p in pares if peso[p] != 0), key=lambda p: peso[p], reverse=True):
        if achar(u) != achar(v):
            componente[achar(u)] = achar(v)
            vizinhos[u].append(v)
            vizinhos[v].append(u)
    pai, fila = {raiz: None}, [raiz]
    for u in fila:  # busca em largura a partir da raiz
        for v in vizinhos[u]:
            if v not in pai:
                pai[v] = u
                fila.append(v)
    if len(pai) != len(VARIAVEIS):
        sys.exit("ERRO: a árvore do TAN não liga todas as variáveis")
    return pai


# ---------- estimação BDeu e inferência exata ----------

def tabela_cpd(nome, pais, x, y):
    """P(nome | pais) com prior BDeu: (contagem + a) / (soma das contagens + a), a = N' / nº de células."""
    dims = [CARD[nome]] + [CARD[p] for p in pais]
    contagem = np.zeros(dims)
    col = {**x, "kredit": y}
    np.add.at(contagem, tuple(col[v] for v in [nome] + pais), 1)
    suave = contagem + TAMANHO_EQUIVALENTE / np.prod(dims)
    return suave / suave.sum(axis=0, keepdims=True)


def prever_rede(modelo, x_treino, y_treino, x_alvo):
    """P(ruim) de cada linha do alvo: rede treinada com BDeu, inferência exata com todas as variáveis observadas."""
    pais = {v: ["kredit"] for v in VARIAVEIS}
    if modelo == "tan":
        for filho, pai in arvore_tan(x_treino, y_treino).items():
            if pai is not None:
                pais[filho] = ["kredit", pai]
    prior = tabela_cpd("kredit", [], x_treino, y_treino)
    n = len(next(iter(x_alvo.values())))
    conjunta = []  # P(classe, evidência) para classe = 0 (ruim) e 1 (bom)
    for c in (0, 1):
        p = np.full(n, prior[c])
        for v in VARIAVEIS:
            indice = (x_alvo[v],) + tuple(np.full(n, c) if q == "kredit" else x_alvo[q] for q in pais[v])
            p = p * tabela_cpd(v, pais[v], x_treino, y_treino)[indice]
        conjunta.append(p)
    return conjunta[0] / (conjunta[0] + conjunta[1]), pais


# ---------- métricas ----------

def roc_auc(y, p):
    """Probabilidade de um ruim ter p maior que um bom, empates valendo 1/2 (postos médios)."""
    _, inverso, cont = np.unique(p, return_inverse=True, return_counts=True)
    posto = (np.cumsum(cont) - (cont - 1) / 2)[inverso]
    n1 = y.sum()
    return (posto[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


def pr_auc(y, p):
    """Precisão média: soma de (aumento da revocação) x precisão, um limiar por valor distinto de p."""
    _, inverso = np.unique(-p, return_inverse=True)  # grupos em ordem decrescente de p
    tp = np.cumsum(np.bincount(inverso, weights=y))
    total = np.cumsum(np.bincount(inverso))
    revocacao = tp / y.sum()
    return float(np.sum(np.diff(np.concatenate([[0.0], revocacao])) * tp / total))


def brier(y, p):
    return float(np.mean((p - y) ** 2))


def log_loss(y, p):
    if p.min() <= 1e-15 or p.max() >= 1 - 1e-15:
        sys.exit("ERRO: probabilidade colada em 0 ou 1; o log loss exigiria tratamento")
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def ece(y, p):
    """Média, ponderada pelo número de casos, de |média de p - fração de ruins| em 10 faixas de largura 0,1."""
    faixa = np.minimum(np.floor(p * 10).astype(int), 9)
    return sum((faixa == b).sum() * abs(p[faixa == b].mean() - y[faixa == b].mean()) for b in np.unique(faixa)) / len(p)


METRICAS = {"roc_auc": roc_auc, "pr_auc": pr_auc, "brier": brier, "log_loss": log_loss, "ece": ece}


# ---------- decisão ----------

utilidade = json.loads((RAIZ / "config/utilidade.json").read_text())["acoes"]


def utilidades(p):
    """UE de cada ação para P(ruim) = p: (1 - p) U(ação, bom) + p U(ação, ruim)."""
    return {a: (1 - p) * utilidade[a]["bom"] + p * utilidade[a]["ruim"] for a in ACOES}


def escolher(ue, ordem):
    """Ação de maior UE entre as de `ordem`; empate (tolerância 1e-9): a primeira de `ordem`."""
    melhor = max(ue[a] for a in ordem)
    return next(a for a in ordem if ue[a] >= melhor - TOLERANCIA_UE)


def acoes_das_regras(p):
    return {"ue": [escolher(utilidades(x), PRIORIDADE) for x in p],
            "ue2": [escolher(utilidades(x), DUAS) for x in p],
            "limiar": ["aprovar" if x < CORTE else "rejeitar" for x in p]}


def media_utilidade(acoes, y):
    return float(np.mean([utilidade[a]["ruim" if r == 1 else "bom"] for a, r in zip(acoes, y)]))


def conferir_tabela(rotulo, tabela, m, r, acoes, y):
    """Compara utilidade média e contagens da regra r do modelo m com a linha gravada em tabela."""
    i = next(j for j in range(len(tabela["modelo"])) if tabela["modelo"][j] == m and tabela["regra"][j] == r)
    conferir(f"{rotulo}: utilidade média {m}/{r}", abs(float(tabela["utilidade_media"][i]) - media_utilidade(acoes, y)))
    conferir_igual(f"{rotulo}: contagens {m}/{r}", [int(tabela[f"n_{a}"][i]) for a in ACOES], [acoes.count(a) for a in ACOES])


def conferir_politicas(rotulo, modelos, y, resumo, politicas, duas=None):
    """Compara ações por caso, utilidade média e contagens de cada regra com as tabelas gravadas."""
    for m, p in modelos.items():
        regras = acoes_das_regras(p)
        for r in ("ue", "limiar"):
            conferir_igual(f"{rotulo}: ações {m}/{r} (politicas)", politicas[f"acao_{m}_{r}"], regras[r])
            conferir_tabela(f"{rotulo} (resumo)", resumo, m, r, regras[r], y)
        if duas is not None:
            for r in ("ue", "ue2", "limiar"):
                conferir_tabela(f"{rotulo} (duas_acoes)", duas, m, r, regras[r], y)


def main():
    if sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/auditoria_independente.py")
    todas = np.arange(N)

    # 1. partições e cortes
    folds = particoes(kredit)
    gravado = ler(RES / "predicoes_dev.csv")
    if gravado["record_id"] != dev["record_id"] or [int(v) for v in gravado["kredit"]] != list(kredit):
        sys.exit("ERRO: predicoes_dev.csv não está na ordem de dev.csv")
    conferir_igual("partições (coluna fold de predicoes_dev.csv)", [int(v) for v in gravado["fold"]], list(folds))
    tamanhos = [int((folds == k).sum()) for k in range(PARTICOES)]
    ruins = [int(((folds == k) & (kredit == 0)).sum()) for k in range(PARTICOES)]
    print(f"     partições: casos {tamanhos}, ruins {ruins}")
    if tamanhos != [160] * PARTICOES or ruins != [48] * PARTICOES:
        falhas.append("tamanho das partições")
    gravados = json.loads((RES / "cortes.json").read_text())
    corte_dev = cortes(todas)
    conferir("cortes.json (tercis do dev inteiro)", max(abs(corte_dev[c][i] - gravados[c][i]) for c in CONTINUAS for i in range(2)))

    # 2 e 3. redes: treina nas outras 4 partições, prevê a partição
    prev = {m: np.zeros(N) for m in ("nb", "tan")}
    arestas = []
    for k in range(PARTICOES):
        treino, alvo = np.where(folds != k)[0], np.where(folds == k)[0]
        corte = cortes(treino)
        x_tr, x_al = codificar(treino, corte), codificar(alvo, corte)
        for m in ("nb", "tan"):
            prev[m][alvo], pais = prever_rede(m, x_tr, kredit[treino], x_al)
            if m == "tan":
                arestas += [(k, pai, filho) for filho, pai in sorted((f, q[1]) for f, q in pais.items() if len(q) == 2)]
                arestas += [(k, "kredit", v) for v in VARIAVEIS]
    for m in ("nb", "tan"):
        conferir(f"probabilidades p_{m} (BDeu N'={TAMANHO_EQUIVALENTE} e inferência exata)", np.abs(numeros(gravado, f"p_{m}") - prev[m]).max())
    esperado = sorted((int(f), o, d) for f, o, d in zip(*ler(RES / "tan_arestas.csv").values()))
    conferir_igual("arestas do TAN (tan_arestas.csv)", esperado, sorted(arestas))
    entre_variaveis = [{(o, d) for k, o, d in arestas if k == f and o != "kredit"} for f in range(PARTICOES)]
    print(f"     arestas entre variáveis por partição: {[len(e) for e in entre_variaveis]}; "
          f"iguais em todas as partições: {all(e == entre_variaveis[0] for e in entre_variaveis)}")

    # 4. métricas do dev, por partição (média e desvio amostral entre as 5)
    y = (kredit == 0).astype(float)  # 1 = ruim
    probs = {m: numeros(gravado, f"p_{m}") for m in MODELOS}
    base = np.zeros(N)
    for k in range(PARTICOES):
        base[folds == k] = y[folds != k].mean()
    probs["taxa_base"] = base
    tab = ler(RES / "metricas_dev.csv")
    for i, m in enumerate(tab["modelo"]):
        diferenca = 0.0
        for nome, f in METRICAS.items():
            por_fold = np.array([f(y[folds == k], probs[m][folds == k]) for k in range(PARTICOES)])
            diferenca = max(diferenca, abs(por_fold.mean() - float(tab[f"{nome}_media"][i])), abs(por_fold.std(ddof=1) - float(tab[f"{nome}_desvio"][i])))
        conferir(f"metricas_dev.csv: {m}", diferenca)

    # 4. métricas do teste, todas as linhas juntas
    teste = ler(RES / "predicoes_teste.csv")
    y_teste = (np.array([int(v) for v in teste["kredit"]]) == 0).astype(float)
    print(f"     teste: {len(y_teste)} linhas, {int(y_teste.sum())} ruins")
    probs_teste = {m: numeros(teste, f"p_{m}") for m in MODELOS}
    if "p_sel" in teste:
        probs_teste["sel"] = numeros(teste, "p_sel")
    probs_teste["taxa_base"] = np.full(len(y_teste), y.mean())
    tab = ler(RES / "metricas_teste.csv")
    for i, m in enumerate(tab["modelo"]):
        diferenca = max(abs(f(y_teste, probs_teste[m]) - float(tab[nome][i])) for nome, f in METRICAS.items())
        conferir(f"metricas_teste.csv: {m}", diferenca)

    # 5. políticas
    limiar_duas = utilidade["aprovar"]["bom"] - utilidade["rejeitar"]["bom"]
    limiar_duas = limiar_duas / (limiar_duas + utilidade["rejeitar"]["ruim"] - utilidade["aprovar"]["ruim"])
    print(f"     limiar da política de duas ações, derivado da matriz: {limiar_duas:.4f}; corte comparado: {CORTE}")
    conferir_politicas("dev", {m: probs[m] for m in MODELOS}, y, ler(RES / "resumo_politicas_dev.csv"), ler(RES / "politicas_dev.csv"))
    conferir_politicas("teste", {m: probs_teste[m] for m in probs_teste if m != "taxa_base"}, y_teste,
                       ler(RES / "resumo_politicas_teste.csv"), ler(RES / "politicas_teste.csv"), ler(RES / "duas_acoes_teste.csv"))

    if falhas:
        sys.exit(f"ERRO: {len(falhas)} conferências falharam: {', '.join(falhas)}")
    print("auditoria: ok")


if __name__ == "__main__":
    main()
