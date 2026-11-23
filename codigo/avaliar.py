"""Calcula as métricas dos três modelos no dev e desenha o diagrama de calibração.

Lê as predições da validação cruzada e, para cada modelo e cada partição, calcula
ROC-AUC, PR-AUC, Brier, log loss e erro de calibração (10 faixas de P(ruim)).
A linha taxa_base prevê, em cada partição, a proporção de ruins nas outras 4.
Classe positiva: ruim (kredit == 0). Não treina nenhum modelo.

Com --ocultar, calcula ROC-AUC e Brier de cada modelo com cada variável escondida
(média das 5 partições) e a diferença para o desempenho com todas as variáveis.

Com --final, calcula as métricas sobre predicoes_teste.csv (todas as linhas juntas), com
intervalo de 95% por bootstrap (2000 reamostras, semente 2026) para ROC-AUC, PR-AUC e Brier.
A taxa_base prevê para toda linha a proporção de ruins do dev. Se o arquivo tem p_sel (modelo
secundário escolhido pela seleção), a linha sel entra por último, nas mesmas reamostras. Rodado só pelo autor.

Com --selecao, resume a validação cruzada aninhada da grade de redes. Em cada partição externa,
o log_loss_interno de cada configuração é a média do log loss das 5 partições internas; no bloco
dev, é o log loss das 800 predições externas juntas. A escolhida de cada bloco é a primeira, na
ordem da grade, com log_loss_interno até 1e-9 acima do menor. Em selecao_dev.csv, cada configuração
e a linha aninhado (em cada partição externa, a configuração escolhida naquele bloco) têm as
métricas das partições externas resumidas como em metricas_dev.csv.

Com --calibrada, mede as predições calibradas por Platt (análise secundária) do mesmo jeito
que o modo sem opção mede as originais. Não ajusta nada.

Entradas:
  resultados/predicoes_dev.csv         record_id,kredit,fold,p_nb,p_tan,p_logreg
  resultados/predicoes_dev_oculta.csv  record_id,modelo,variavel_oculta,p_ruim (só com --ocultar)
  resultados/metricas_dev.csv          desempenho com todas as variáveis (só com --ocultar)
  resultados/predicoes_teste.csv       record_id,kredit,p_nb,p_tan,p_logreg[,p_sel] (só com --final)
  resultados/predicoes_selecao.csv     config,record_id,fold_externo,fold_interno,p_ruim (só com --selecao)
  resultados/predicoes_calibradas_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg (só com --calibrada)
  dados/processados/dev.csv            proporção de ruins do dev para a taxa_base (só com --final)
Saídas:
  resultados/metricas_dev.csv   média e desvio amostral, entre as 5 partições, de cada métrica
  resultados/calibracao_dev.png diagrama de calibração com as 800 predições juntas
  resultados/evidencia_incompleta.csv  modelo,variavel_oculta,roc_auc,brier,delta_roc_auc,delta_brier (só com --ocultar)
  resultados/metricas_teste.csv   valor e intervalo de cada métrica no teste; linha sel se houver p_sel (só com --final)
  resultados/calibracao_teste.png diagrama de calibração no teste (só com --final)
  resultados/selecao_escolha.csv  fold_externo,config,log_loss_interno,escolhida (só com --selecao)
  resultados/selecao_dev.csv      métricas de cada configuração e do aninhado, colunas de metricas_dev.csv (só com --selecao)
  resultados/metricas_calibradas_dev.csv  colunas de metricas_dev.csv, para p calibrada (só com --calibrada)
  resultados/calibracao_calibrada_dev.png diagrama de calibração da p calibrada (só com --calibrada)

Uso: a partir da raiz do repositório,
  uv run python codigo/avaliar.py              grava as saídas
  uv run python codigo/avaliar.py --verificar  roda os autotestes e não grava nada
  uv run python codigo/avaliar.py --ocultar    grava só evidencia_incompleta.csv
  uv run python codigo/avaliar.py --final      grava só metricas_teste.csv e calibracao_teste.png
  uv run python codigo/avaliar.py --selecao    grava só selecao_escolha.csv e selecao_dev.csv
  uv run python codigo/avaliar.py --calibrada  grava só metricas_calibradas_dev.csv e calibracao_calibrada_dev.png
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "resultados"
PREDICOES = SAIDA / "predicoes_dev.csv"
OCULTA = SAIDA / "predicoes_dev_oculta.csv"
TESTE = SAIDA / "predicoes_teste.csv"
SELECAO = SAIDA / "predicoes_selecao.csv"
CALIBRADAS = SAIDA / "predicoes_calibradas_dev.csv"
# mesma grade e ordem de desempate de modelos.py
CONFIGS = ["nb_ess1", "nb_ess5", "nb_ess10", "nb_ess50", "tan_ess1", "tan_ess5", "tan_ess10", "tan_ess50"]
DEV = RAIZ / "dados/processados/dev.csv"
MODELOS = ["nb", "tan", "logreg"]
COLUNAS = ["kredit", "fold"] + [f"p_{m}" for m in MODELOS]
METRICAS = ["roc_auc", "pr_auc", "brier", "log_loss", "ece"]
COM_INTERVALO = ["roc_auc", "pr_auc", "brier"]
REAMOSTRAS = 2000
SEMENTE = 2026
PERCENTIS = [2.5, 97.5]


def faixas(p):
    """Índice da faixa (0 a 9) de cada probabilidade; a última faixa inclui o 1,0."""
    return np.minimum((p * 10).astype(int), 9)


def ece(y, p):
    """Média, ponderada pelo número de casos, de |média de p - fração de ruins| em cada faixa."""
    f = faixas(p)
    return sum((f == b).sum() * abs(p[f == b].mean() - y[f == b].mean()) for b in np.unique(f)) / len(p)


def metricas(y, p):
    return [roc_auc_score(y, p), average_precision_score(y, p), brier_score_loss(y, p), log_loss(y, p, labels=[0, 1]), ece(y, p)]


def ler_csv(caminho, colunas):
    """Lê um CSV e termina com erro se o arquivo não existir, faltar coluna ou houver vazio."""
    if not caminho.exists():
        sys.exit(f"ERRO: arquivo ausente: {caminho.name}")
    df = pd.read_csv(caminho)
    faltando = [c for c in colunas if c not in df.columns]
    if faltando:
        sys.exit(f"ERRO: colunas ausentes em {caminho.name}: {', '.join(faltando)}")
    if df[colunas].isna().any().any():
        sys.exit(f"ERRO: valor vazio em {caminho.name}")
    return df


def ler(caminho=PREDICOES, colunas=COLUNAS):
    """Lê as predições e termina com erro se faltar coluna, houver vazio ou p fora de [0, 1]."""
    pred = ler_csv(caminho, colunas)
    for m in MODELOS:
        if not pred[f"p_{m}"].between(0, 1).all():
            sys.exit(f"ERRO: p_{m} fora de [0, 1] em {caminho.name}")
    return pred


def calcular(pred):
    """Tabela com média e desvio (ddof=1) de cada métrica entre as partições, uma linha por modelo."""
    y, fold = (pred["kredit"] == 0).to_numpy().astype(int), pred["fold"].to_numpy()
    base = np.zeros(len(pred))
    for k in np.unique(fold):
        base[fold == k] = y[fold != k].mean()
    probs = {m: pred[f"p_{m}"].to_numpy() for m in MODELOS}
    probs["taxa_base"] = base
    linhas = []
    for nome, p in probs.items():
        por_fold = np.array([metricas(y[fold == k], p[fold == k]) for k in np.unique(fold)])
        linha = {"modelo": nome}
        for i, met in enumerate(METRICAS):
            linha[f"{met}_media"] = por_fold[:, i].mean()
            linha[f"{met}_desvio"] = por_fold[:, i].std(ddof=1)
        linhas.append(linha)
    return pd.DataFrame(linhas)


def desenhar(pred, arquivo="calibracao_dev.png", onde="no dev"):
    y = (pred["kredit"] == 0).to_numpy().astype(int)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([0, 1], [0, 1], "k--", label="calibração perfeita")
    for m in MODELOS:
        p = pred[f"p_{m}"].to_numpy()
        f = faixas(p)
        usadas = np.unique(f)
        ax.plot([p[f == b].mean() for b in usadas], [y[f == b].mean() for b in usadas], "o-", label=m)
    ax.set_xlabel("P(ruim) prevista (média da faixa)")
    ax.set_ylabel("Fração observada de ruins")
    ax.set_title(f"Diagrama de calibração {onde} (10 faixas)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.savefig(SAIDA / arquivo, dpi=100)
    plt.close(fig)


def main():
    pred = ler()
    tabela = calcular(pred)
    base = tabela.set_index("modelo").loc["taxa_base"]
    for _, r in tabela[tabela["modelo"] != "taxa_base"].iterrows():
        if r["brier_media"] >= base["brier_media"]:
            print(f"AVISO: brier de {r['modelo']} >= taxa_base")
        if r["roc_auc_media"] < 0.5:
            print(f"AVISO: roc_auc de {r['modelo']} < 0,5")
    tabela.to_csv(SAIDA / "metricas_dev.csv", index=False)
    desenhar(pred)


def calcular_final(pred, taxa_dev):
    """Uma linha por modelo: métricas em todas as linhas e intervalo por bootstrap nas mesmas reamostras."""
    y = (pred["kredit"] == 0).to_numpy().astype(int)
    n = len(y)
    indices = np.random.default_rng(SEMENTE).integers(0, n, size=(REAMOSTRAS, n))
    probs = {m: pred[f"p_{m}"].to_numpy() for m in MODELOS}
    probs["taxa_base"] = np.full(n, taxa_dev)
    if "p_sel" in pred.columns:
        probs["sel"] = pred["p_sel"].to_numpy()
    linhas = []
    for nome, p in probs.items():
        valores = dict(zip(METRICAS, metricas(y, p)))
        reamostras = np.array([metricas(y[i], p[i])[:len(COM_INTERVALO)] for i in indices])
        linha = {"modelo": nome}
        for j, met in enumerate(METRICAS):
            linha[met] = valores[met]
            if met in COM_INTERVALO:
                linha[f"{met}_ic_inf"], linha[f"{met}_ic_sup"] = np.percentile(reamostras[:, j], PERCENTIS)
        linhas.append(linha)
    return pd.DataFrame(linhas)


def main_final():
    pred = ler(TESTE, ["kredit"] + [f"p_{m}" for m in MODELOS])
    if "p_sel" in pred.columns and (pred["p_sel"].isna().any() or not pred["p_sel"].between(0, 1).all()):
        sys.exit(f"ERRO: p_sel vazia ou fora de [0, 1] em {TESTE.name}")
    taxa_dev = (pd.read_csv(DEV)["kredit"] == 0).mean()
    calcular_final(pred, taxa_dev).to_csv(SAIDA / "metricas_teste.csv", index=False)
    desenhar(pred, "calibracao_teste.png", "no teste")


def calcular_oculta(oculta, pred, completo):
    """ROC-AUC e Brier médios de cada par (modelo, variável) e a diferença para o modelo completo."""
    if not oculta["p_ruim"].between(0, 1).all():
        sys.exit(f"ERRO: p_ruim fora de [0, 1] em {OCULTA.name}")
    y, fold = (pred["kredit"] == 0).to_numpy().astype(int), pred["fold"].to_numpy()
    ids = list(pred["record_id"])
    linhas = []
    for m in MODELOS:
        for v in oculta["variavel_oculta"].unique():
            parte = oculta[(oculta["modelo"] == m) & (oculta["variavel_oculta"] == v)]
            if sorted(parte["record_id"]) != sorted(ids):
                sys.exit(f"ERRO: par ({m}, {v}) não tem os {len(ids)} casos uma vez em {OCULTA.name}")
            p = parte.set_index("record_id").loc[ids, "p_ruim"].to_numpy()
            por_fold = np.array([metricas(y[fold == k], p[fold == k]) for k in np.unique(fold)])
            roc, brier = por_fold[:, METRICAS.index("roc_auc")].mean(), por_fold[:, METRICAS.index("brier")].mean()
            linhas.append({"modelo": m, "variavel_oculta": v, "roc_auc": roc, "brier": brier,
                           "delta_roc_auc": roc - completo.loc[m, "roc_auc_media"], "delta_brier": brier - completo.loc[m, "brier_media"]})
    return pd.DataFrame(linhas)


def main_oculta():
    pred = ler()
    oculta = ler_csv(OCULTA, ["record_id", "modelo", "variavel_oculta", "p_ruim"])
    completo = ler_csv(SAIDA / "metricas_dev.csv", ["modelo", "roc_auc_media", "brier_media"]).set_index("modelo")
    tabela = calcular_oculta(oculta, pred, completo)
    delta = tabela.set_index(["modelo", "variavel_oculta"])["delta_brier"]
    for m in MODELOS:
        if delta[(m, "laufkont")] <= delta[(m, "telef")]:
            print(f"AVISO: ocultar laufkont não piorou mais que ocultar telef em {m}")
    tabela.to_csv(SAIDA / "evidencia_incompleta.csv", index=False)


def resumo(nome, y, p, fold):
    """Linha com média e desvio (ddof=1) de cada métrica entre as partições, como em calcular."""
    por_fold = np.array([metricas(y[fold == k], p[fold == k]) for k in np.unique(fold)])
    linha = {"modelo": nome}
    for i, met in enumerate(METRICAS):
        linha[f"{met}_media"] = por_fold[:, i].mean()
        linha[f"{met}_desvio"] = por_fold[:, i].std(ddof=1)
    return linha


def escolher(perdas):
    """Índice da primeira perda, na ordem dada, até 1e-9 acima da menor."""
    return next(i for i, v in enumerate(perdas) if v <= min(perdas) + 1e-9)


def calcular_selecao(sel, pred):
    """Devolve (selecao_escolha, selecao_dev)."""
    if not sel["p_ruim"].between(0, 1).all():
        sys.exit(f"ERRO: p_ruim fora de [0, 1] em {SELECAO.name}")
    sel = sel.merge(pred[["record_id", "kredit"]], on="record_id", how="left")
    if sel["kredit"].isna().any():
        sys.exit(f"ERRO: record_id de {SELECAO.name} ausente em {PREDICOES.name}")
    sel["ruim"] = (sel["kredit"] == 0).astype(int)
    externas = sel[sel["fold_interno"] == -1]
    escolha, escolhidas = [], {}
    for b in [0, 1, 2, 3, 4, "dev"]:
        perdas = []
        for c in CONFIGS:
            if b == "dev":
                q = externas[externas["config"] == c]
                perdas.append(log_loss(q["ruim"], q["p_ruim"], labels=[0, 1]))
            else:
                q = sel[(sel["config"] == c) & (sel["fold_externo"] == b) & (sel["fold_interno"] >= 0)]
                perdas.append(np.mean([log_loss(g["ruim"], g["p_ruim"], labels=[0, 1]) for _, g in q.groupby("fold_interno")]))
        i = escolher(perdas)
        escolhidas[b] = CONFIGS[i]
        escolha += [{"fold_externo": b, "config": c, "log_loss_interno": v, "escolhida": j == i} for j, (c, v) in enumerate(zip(CONFIGS, perdas))]
    linhas = []
    for c in CONFIGS:
        q = externas[externas["config"] == c].sort_values(["fold_externo", "record_id"])
        linhas.append(resumo(c, q["ruim"].to_numpy(), q["p_ruim"].to_numpy(), q["fold_externo"].to_numpy()))
    q = pd.concat([externas[(externas["config"] == escolhidas[k]) & (externas["fold_externo"] == k)] for k in range(5)])
    linhas.append(resumo("aninhado", q["ruim"].to_numpy(), q["p_ruim"].to_numpy(), q["fold_externo"].to_numpy()))
    return pd.DataFrame(escolha), pd.DataFrame(linhas)


def main_selecao():
    pred = ler()
    sel = ler_csv(SELECAO, ["config", "record_id", "fold_externo", "fold_interno", "p_ruim"])
    escolha, tabela = calcular_selecao(sel, pred)
    escolha.to_csv(SAIDA / "selecao_escolha.csv", index=False)
    tabela.to_csv(SAIDA / "selecao_dev.csv", index=False)


def main_calibrada():
    pred = ler(CALIBRADAS, COLUNAS)
    calcular(pred).to_csv(SAIDA / "metricas_calibradas_dev.csv", index=False)
    desenhar(pred, "calibracao_calibrada_dev.png", "no dev, p calibrado por Platt")


def verificar():
    # tudo 0,8 sem nenhum ruim: erro de calibração 0,8
    assert abs(ece(np.zeros(10), np.full(10, 0.8)) - 0.8) < 1e-12
    # tudo 0,3 com 30% de ruins: erro de calibração 0
    assert abs(ece(np.array([1] * 3 + [0] * 7), np.full(10, 0.3))) < 1e-12
    # 08.8: desempate pela ordem da grade, num caso feito à mão
    assert escolher([0.6, 0.5, 0.5 + 1e-10, 0.7]) == 1
    assert escolher([0.5 + 1e-10, 0.5, 0.7]) == 0
    # 08.8: nb_ess5 e tan_ess5 batem com nb e tan de metricas_dev.csv; numa execução do zero
    # (factory/checks.sh) este autoteste roda antes de --selecao, então só confere se os arquivos já existem
    if SELECAO.exists() and (SAIDA / "metricas_dev.csv").exists():
        _, tabela = calcular_selecao(ler_csv(SELECAO, ["config", "record_id", "fold_externo", "fold_interno", "p_ruim"]), ler())
        tabela, dev = tabela.set_index("modelo"), ler_csv(SAIDA / "metricas_dev.csv", ["modelo"]).set_index("modelo")
        for m in ("nb", "tan"):
            assert np.abs(tabela.loc[f"{m}_ess5", dev.columns].to_numpy() - dev.loc[m].to_numpy()).max() < 1e-9, m
    # 11: --final com arquivo falso montado do dev; sem p_sel, a tabela é a de antes; com p_sel, sel é a última linha
    falso = ler()[["kredit"] + [f"p_{m}" for m in MODELOS]]
    sem = calcular_final(falso, 0.3)
    com = calcular_final(falso.assign(p_sel=falso["p_tan"]), 0.3)
    assert list(sem["modelo"]) == MODELOS + ["taxa_base"]
    assert list(com["modelo"]) == MODELOS + ["taxa_base", "sel"]
    assert com.iloc[:-1].equals(sem)
    assert not com.iloc[-1].isna().any()
    assert ((falso["p_tan"] > 0) & (falso["p_tan"] < 1)).all()
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:] == ["--ocultar"]:
        main_oculta()
    elif sys.argv[1:] == ["--selecao"]:
        main_selecao()
    elif sys.argv[1:] == ["--calibrada"]:
        main_calibrada()
    elif sys.argv[1:] == ["--final"]:
        main_final()
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/avaliar.py [--verificar | --ocultar | --selecao | --calibrada | --final]")
    else:
        main()
