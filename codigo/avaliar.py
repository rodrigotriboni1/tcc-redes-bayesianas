"""Calcula as métricas dos três modelos no dev e desenha o diagrama de calibração.

Lê as predições da validação cruzada e, para cada modelo e cada partição, calcula
ROC-AUC, PR-AUC, Brier, log loss e erro de calibração (10 faixas de P(ruim)).
A linha taxa_base prevê, em cada partição, a proporção de ruins nas outras 4.
Classe positiva: ruim (kredit == 0). Não treina nenhum modelo.

Entrada: resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
Saídas:
  resultados/metricas_dev.csv   média e desvio amostral, entre as 5 partições, de cada métrica
  resultados/calibracao_dev.png diagrama de calibração com as 800 predições juntas

Uso: a partir da raiz do repositório,
  uv run python codigo/avaliar.py              grava as saídas
  uv run python codigo/avaliar.py --verificar  roda os autotestes e não grava nada
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
MODELOS = ["nb", "tan", "logreg"]
COLUNAS = ["kredit", "fold"] + [f"p_{m}" for m in MODELOS]
METRICAS = ["roc_auc", "pr_auc", "brier", "log_loss", "ece"]


def faixas(p):
    """Índice da faixa (0 a 9) de cada probabilidade; a última faixa inclui o 1,0."""
    return np.minimum((p * 10).astype(int), 9)


def ece(y, p):
    """Média, ponderada pelo número de casos, de |média de p - fração de ruins| em cada faixa."""
    f = faixas(p)
    return sum((f == b).sum() * abs(p[f == b].mean() - y[f == b].mean()) for b in np.unique(f)) / len(p)


def metricas(y, p):
    return [roc_auc_score(y, p), average_precision_score(y, p), brier_score_loss(y, p), log_loss(y, p, labels=[0, 1]), ece(y, p)]


def ler():
    """Lê predicoes_dev.csv e termina com erro se faltar coluna, houver vazio ou p fora de [0, 1]."""
    pred = pd.read_csv(PREDICOES)
    faltando = [c for c in COLUNAS if c not in pred.columns]
    if faltando:
        sys.exit(f"ERRO: colunas ausentes em {PREDICOES.name}: {', '.join(faltando)}")
    if pred[COLUNAS].isna().any().any():
        sys.exit(f"ERRO: valor vazio em {PREDICOES.name}")
    for m in MODELOS:
        if not pred[f"p_{m}"].between(0, 1).all():
            sys.exit(f"ERRO: p_{m} fora de [0, 1] em {PREDICOES.name}")
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


def desenhar(pred):
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
    ax.set_title("Diagrama de calibração no dev (10 faixas)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.savefig(SAIDA / "calibracao_dev.png", dpi=100)
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


def verificar():
    # tudo 0,8 sem nenhum ruim: erro de calibração 0,8
    assert abs(ece(np.zeros(10), np.full(10, 0.8)) - 0.8) < 1e-12
    # tudo 0,3 com 30% de ruins: erro de calibração 0
    assert abs(ece(np.array([1] * 3 + [0] * 7), np.full(10, 0.3))) < 1e-12
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/avaliar.py [--verificar]")
    else:
        main()
