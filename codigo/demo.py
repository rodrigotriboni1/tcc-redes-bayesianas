"""Mostra no terminal a decisão de crédito para um caso do dev.

Treina os três modelos nas 4 partições que não contêm o caso (como em predicoes_dev.csv)
e imprime as variáveis do caso, P(ruim) de cada modelo, a UE de cada ação para o modelo
escolhido, as fronteiras de risco da matriz de utilidade e a ação recomendada.

Entradas:
  dados/processados/dev.csv     o caso e as linhas de treino
  resultados/predicoes_dev.csv  partição (fold) de cada record_id
  config/utilidade.json         matriz de utilidade U(ação, estado)
Saída: só o terminal; nada é gravado.

Uso: a partir da raiz do repositório,
  uv run python codigo/demo.py <record_id> [--modelo nb|tan|logreg]
"""
import argparse
import sys
from itertools import combinations

import pandas as pd

import decisao
import modelos


def fronteiras(u):
    """Valores de p em que a ação de maior UE muda: cruzamentos das retas de UE no envelope superior."""
    pontos = []
    for a, b in combinations(decisao.ACOES, 2):
        # UE(a) - UE(b) = (bom_a - bom_b) + p·[(ruim_a - ruim_b) - (bom_a - bom_b)]
        db = u[a]["bom"] - u[b]["bom"]
        inclinacao = (u[a]["ruim"] - u[b]["ruim"]) - db
        if inclinacao == 0:
            continue
        p = -db / inclinacao
        if not 0 < p < 1:
            continue
        ue = decisao.utilidade_esperada(p, u)
        if ue[a] >= max(ue.values()) - decisao.TOLERANCIA:
            pontos.append((p, a, b))
    return sorted(pontos)


def main():
    parser = argparse.ArgumentParser(description="Demonstra a decisão para um caso do dev.")
    parser.add_argument("record_id")
    parser.add_argument("--modelo", choices=modelos.MODELOS, default="tan")
    args = parser.parse_args()

    dev = modelos.dev
    if args.record_id not in set(dev["record_id"]):
        sys.exit(f"ERRO: record_id {args.record_id} não está em dev.csv")
    fold = pd.read_csv(decisao.PREDICOES).set_index("record_id")["fold"]
    if args.record_id not in fold.index:
        sys.exit(f"ERRO: record_id {args.record_id} não está em predicoes_dev.csv")
    u = decisao.carregar_utilidade()

    folds = dev["record_id"].map(fold)
    treino = dev[folds != fold[args.record_id]]
    alvo = dev[dev["record_id"] == args.record_id].drop(columns="kredit")

    print(f"Caso {args.record_id} (partição {fold[args.record_id]})")
    for v in modelos.VARIAVEIS:
        print(f"  {v:10s} {alvo[v].iloc[0]}")

    print("\nP(ruim)")
    p = {m: float(modelos.prever(treino, alvo, m)[0]) for m in modelos.MODELOS}
    for m in modelos.MODELOS:
        print(f"  {m:10s} {p[m]:.6f}")

    print(f"\nUtilidade esperada ({args.modelo})")
    for a, ue in decisao.utilidade_esperada(p[args.modelo], u).items():
        print(f"  {a:15s} {ue:.2f}")

    print("\nFronteiras de risco")
    for x, a, b in fronteiras(u):
        print(f"  p = {x:.4f}: {a} / {b}")

    print(f"\nAção recomendada ({args.modelo}): {decisao.ordenar(p[args.modelo], u)[0]}")


if __name__ == "__main__":
    main()
