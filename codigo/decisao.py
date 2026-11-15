"""Escolhe a ação de crédito por utilidade esperada e compara com o limiar fixo de 0,5.

Para cada caso e modelo, UE(a) = (1 - p)·U(a, bom) + p·U(a, ruim), com p = P(ruim).
A ação escolhida é a de maior UE; empate (tolerância 1e-9): análise manual, rejeitar, aprovar.
A regra de comparação aprova se p < 0,5 e rejeita caso contrário.

Entradas:
  resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
  config/utilidade.json         matriz de utilidade U(ação, estado) e hipóteses
Saídas:
  resultados/politicas_dev.csv         ação de cada regra, segunda ação e diferença de UE por caso
  resultados/resumo_politicas_dev.csv  utilidade média e contagens por modelo e regra

Uso: a partir da raiz do repositório,
  uv run python codigo/decisao.py
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PREDICOES = RAIZ / "resultados/predicoes_dev.csv"
UTILIDADE = RAIZ / "config/utilidade.json"
SAIDA = RAIZ / "resultados"
MODELOS = ["nb", "tan", "logreg"]
ACOES = ["aprovar", "rejeitar", "analise_manual"]
# Ordem de desempate: a primeira vence quando as UE empatam.
PRIORIDADE = ["analise_manual", "rejeitar", "aprovar"]
TOLERANCIA = 1e-9


def carregar_utilidade(caminho=UTILIDADE):
    """Lê a matriz de utilidade do JSON e confere as três ações com bom/ruim numéricos."""
    acoes = json.loads(Path(caminho).read_text())["acoes"]
    ok = set(acoes) == set(ACOES) and all(
        set(acoes[a]) == {"bom", "ruim"} and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in acoes[a].values())
        for a in ACOES
    )
    if not ok:
        sys.exit(f"ERRO: {caminho}: esperado acoes.{{aprovar,rejeitar,analise_manual}}.{{bom,ruim}} numéricos")
    return acoes


def conferir_p(p):
    if math.isnan(p) or p < 0 or p > 1:
        raise ValueError(f"probabilidade fora de [0, 1]: {p}")


def utilidade_esperada(p, u):
    """UE de cada ação para P(ruim) = p e matriz u."""
    conferir_p(p)
    return {a: (1 - p) * u[a]["bom"] + p * u[a]["ruim"] for a in ACOES}


def ordenar(p, u):
    """(primeira ação, segunda ação, diferença de UE entre elas), com o desempate da prioridade."""
    ue = utilidade_esperada(p, u)
    primeira = next(a for a in PRIORIDADE if ue[a] >= max(ue.values()) - TOLERANCIA)
    resto = [a for a in PRIORIDADE if a != primeira]
    segunda = next(a for a in resto if ue[a] >= max(ue[b] for b in resto) - TOLERANCIA)
    return primeira, segunda, ue[primeira] - ue[segunda]


def limiar(p):
    """Regra de comparação: aprova se p < 0,5, senão rejeita."""
    conferir_p(p)
    return "aprovar" if p < 0.5 else "rejeitar"


def main():
    u = carregar_utilidade()
    if not PREDICOES.exists():
        sys.exit(f"ERRO: {PREDICOES} não existe; rode codigo/modelos.py antes")
    pred = pd.read_csv(PREDICOES)
    faltam = [c for c in ["record_id", "kredit"] + [f"p_{m}" for m in MODELOS] if c not in pred.columns]
    if faltam:
        sys.exit(f"ERRO: {PREDICOES}: faltam as colunas {faltam}")
    if pred.empty:
        sys.exit(f"ERRO: {PREDICOES}: arquivo sem linhas")
    for m in MODELOS:
        p = pd.to_numeric(pred[f"p_{m}"], errors="coerce")
        if p.isna().any() or ((p < 0) | (p > 1)).any():
            sys.exit(f"ERRO: {PREDICOES}: p_{m} vazia, não numérica ou fora de [0, 1]")

    politicas = pred[["record_id", "kredit"]].copy()
    segunda, dif = {}, {}
    for m in MODELOS:
        ordem = [ordenar(x, u) for x in pred[f"p_{m}"]]
        politicas[f"acao_{m}_ue"] = [o[0] for o in ordem]
        politicas[f"acao_{m}_limiar"] = [limiar(x) for x in pred[f"p_{m}"]]
        segunda[f"segunda_{m}"] = [o[1] for o in ordem]
        dif[f"dif_ue_{m}"] = [o[2] for o in ordem]
    politicas = politicas.assign(**segunda, **dif)

    # kredit: 0 = ruim, 1 = bom
    estado = ["ruim" if k == 0 else "bom" for k in politicas["kredit"]]
    linhas = []
    for m in MODELOS:
        mudam = int((politicas[f"acao_{m}_ue"] != politicas[f"acao_{m}_limiar"]).sum())
        for regra, possiveis in [("ue", ACOES), ("limiar", ["aprovar", "rejeitar"])]:
            acao = politicas[f"acao_{m}_{regra}"]
            contagem = {f"n_{a}": int((acao == a).sum()) for a in ACOES}
            for a in possiveis:
                if contagem[f"n_{a}"] == 0:
                    print(f"AVISO: a ação {a} não aparece em {m}/{regra}")
            media = sum(u[a][e] for a, e in zip(acao, estado)) / len(acao)
            linhas.append({"modelo": m, "regra": regra, "utilidade_media": media, **contagem, "n_mudam_vs_outra_regra": mudam})

    politicas.to_csv(SAIDA / "politicas_dev.csv", index=False)
    pd.DataFrame(linhas).to_csv(SAIDA / "resumo_politicas_dev.csv", index=False)
    print(f"Gravados {SAIDA / 'politicas_dev.csv'} e {SAIDA / 'resumo_politicas_dev.csv'}")


if __name__ == "__main__":
    main()
