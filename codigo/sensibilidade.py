"""Mostra como os limiares de decisão mudam com a perda e com o custo da análise manual.

Para cada perda L e custo c da grade, a matriz do ponto é: aprovar (G, -L),
rejeitar (0, 0), análise manual (G - c, -c), com G = ganho de aprovar um bom.
Pela forma fechada, se c < G·L/(G + L) aprova-se com p < c/L, rejeita-se com
p > 1 - c/G e entre os dois vai para análise manual; senão os dois limiares
valem G/(G + L) e a análise manual nunca é escolhida. Não lê dados nem predições.

Entrada: config/utilidade.json  o ganho G = acoes.aprovar.bom e a linha acoes.rejeitar
Saídas:
  resultados/sensibilidade.csv  perda,custo_analise,limiar_inferior,limiar_superior (84 linhas)
  resultados/sensibilidade.png  um painel por perda com as regiões de cada ação

Uso: a partir da raiz do repositório,
  uv run python codigo/sensibilidade.py              grava as saídas
  uv run python codigo/sensibilidade.py --verificar  roda os autotestes e não grava nada
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import decisao

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "resultados"
# Grade da decisão D7.
PERDAS = [200, 400, 600, 800]
CUSTOS = list(range(0, 101, 5))


def matriz(g, rejeitar, perda, custo):
    return {"aprovar": {"bom": g, "ruim": -perda}, "rejeitar": rejeitar, "analise_manual": {"bom": g - custo, "ruim": -custo}}


def limiares(g, perda, custo):
    """(inferior, superior): aprova abaixo do inferior, rejeita acima do superior."""
    if custo < g * perda / (g + perda):
        return custo / perda, 1 - custo / g
    return g / (g + perda), g / (g + perda)


def tabela(g):
    linhas = [(l, c, *limiares(g, l, c)) for l in PERDAS for c in CUSTOS]
    return pd.DataFrame(linhas, columns=["perda", "custo_analise", "limiar_inferior", "limiar_superior"])


def desenhar(t):
    fig, eixos = plt.subplots(1, len(PERDAS), figsize=(16, 4.5), sharey=True)
    for ax, l in zip(eixos, PERDAS):
        r = t[t["perda"] == l]
        x, inf, sup = r["custo_analise"], r["limiar_inferior"], r["limiar_superior"]
        ax.fill_between(x, 0, inf, color="tab:green", alpha=0.3, label="aprovar")
        ax.fill_between(x, inf, sup, color="tab:orange", alpha=0.3, label="análise manual")
        ax.fill_between(x, sup, 1, color="tab:red", alpha=0.3, label="rejeitar")
        ax.plot(x, inf, "k-", label="limiar inferior")
        ax.plot(x, sup, "k--", label="limiar superior")
        ax.set_title(f"perda = {l}")
        ax.set_xlabel("custo da análise")
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1)
    eixos[0].set_ylabel("risco P(ruim)")
    eixos[0].legend(loc="upper right", fontsize=8)
    fig.suptitle("Ação escolhida por utilidade esperada em função da perda e do custo da análise")
    fig.tight_layout()
    fig.savefig(SAIDA / "sensibilidade.png", dpi=100)
    plt.close(fig)


def main():
    g = decisao.carregar_utilidade()["aprovar"]["bom"]
    t = tabela(g)
    t.to_csv(SAIDA / "sensibilidade.csv", index=False)
    desenhar(t)
    print(f"Gravados {SAIDA / 'sensibilidade.csv'} e {SAIDA / 'sensibilidade.png'}")


def verificar():
    acoes = decisao.carregar_utilidade()
    g = acoes["aprovar"]["bom"]
    for l in PERDAS:
        for c in CUSTOS:
            inf, sup = limiares(g, l, c)
            u = matriz(g, acoes["rejeitar"], l, c)
            if inf > 0:
                assert decisao.ordenar(inf - 1e-6, u)[0] == "aprovar", (l, c)
            if inf < sup:
                assert decisao.ordenar((inf + sup) / 2, u)[0] == "analise_manual", (l, c)
            if sup < 1:
                assert decisao.ordenar(sup + 1e-6, u)[0] == "rejeitar", (l, c)
    # linhas conhecidas com G = 100
    for (l, c), esperado in {(400, 40): (0.1, 0.6), (400, 80): (0.2, 0.2), (400, 100): (0.2, 0.2)}.items():
        assert all(abs(a - b) < 1e-9 for a, b in zip(limiares(100, l, c), esperado)), (l, c)
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/sensibilidade.py [--verificar]")
    else:
        main()
