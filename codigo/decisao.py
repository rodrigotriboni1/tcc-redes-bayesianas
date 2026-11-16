"""Escolhe a ação de crédito por utilidade esperada e compara com o limiar fixo de 0,5.

Para cada caso e modelo, UE(a) = (1 - p)·U(a, bom) + p·U(a, ruim), com p = P(ruim).
A ação escolhida é a de maior UE; empate (tolerância 1e-9): análise manual, rejeitar, aprovar.
A regra de comparação aprova se p < 0,5 e rejeita caso contrário.

Com --final, faz o mesmo sobre predicoes_teste.csv, acrescenta ao resumo o intervalo de 95%
da utilidade média por bootstrap (2000 reamostras, semente 2026) e grava a diferença
UE − limiar com intervalo pareado nas mesmas reamostras. Rodado só pelo autor.

Entradas:
  resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
  resultados/predicoes_teste.csv record_id,kredit,p_nb,p_tan,p_logreg (só com --final)
  config/utilidade.json         matriz de utilidade U(ação, estado) e hipóteses
Saídas:
  resultados/politicas_dev.csv         ação de cada regra, segunda ação e diferença de UE por caso
  resultados/resumo_politicas_dev.csv  utilidade média e contagens por modelo e regra
  resultados/politicas_teste.csv, resumo_politicas_teste.csv  o mesmo no teste (só com --final)
  resultados/diferenca_politicas_teste.csv  modelo,dif_utilidade_media,dif_ic_inf,dif_ic_sup (só com --final)

Uso: a partir da raiz do repositório,
  uv run python codigo/decisao.py          grava as saídas do dev
  uv run python codigo/decisao.py --final  grava só as saídas do teste
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PREDICOES = RAIZ / "resultados/predicoes_dev.csv"
TESTE = RAIZ / "resultados/predicoes_teste.csv"
UTILIDADE = RAIZ / "config/utilidade.json"
SAIDA = RAIZ / "resultados"
MODELOS = ["nb", "tan", "logreg"]
ACOES = ["aprovar", "rejeitar", "analise_manual"]
# Ordem de desempate: a primeira vence quando as UE empatam.
PRIORIDADE = ["analise_manual", "rejeitar", "aprovar"]
TOLERANCIA = 1e-9
REAMOSTRAS = 2000
SEMENTE = 2026
PERCENTIS = [2.5, 97.5]


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


def main(entrada=PREDICOES, sufixo="dev"):
    """Grava politicas_<sufixo>.csv e resumo_politicas_<sufixo>.csv; no teste, também os intervalos."""
    u = carregar_utilidade()
    if not entrada.exists():
        sys.exit(f"ERRO: {entrada} não existe; rode codigo/modelos.py antes")
    pred = pd.read_csv(entrada)
    faltam = [c for c in ["record_id", "kredit"] + [f"p_{m}" for m in MODELOS] if c not in pred.columns]
    if faltam:
        sys.exit(f"ERRO: {entrada}: faltam as colunas {faltam}")
    if pred.empty:
        sys.exit(f"ERRO: {entrada}: arquivo sem linhas")
    for m in MODELOS:
        p = pd.to_numeric(pred[f"p_{m}"], errors="coerce")
        if p.isna().any() or ((p < 0) | (p > 1)).any():
            sys.exit(f"ERRO: {entrada}: p_{m} vazia, não numérica ou fora de [0, 1]")

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
    final = sufixo == "teste"
    if final:
        n = len(politicas)
        indices = np.random.default_rng(SEMENTE).integers(0, n, size=(REAMOSTRAS, n))
    linhas, por_linha, diferencas = [], {}, []
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
            if final:
                # utilidade realizada de cada caso; a média de cada reamostra dá o intervalo
                por_linha[regra] = np.array([u[a][e] for a, e in zip(acao, estado)])
                linhas[-1]["utilidade_media_ic_inf"], linhas[-1]["utilidade_media_ic_sup"] = np.percentile(por_linha[regra][indices].mean(axis=1), PERCENTIS)
        if final:
            dif = linhas[-2]["utilidade_media"] - linhas[-1]["utilidade_media"]
            inf, sup = np.percentile((por_linha["ue"] - por_linha["limiar"])[indices].mean(axis=1), PERCENTIS)
            diferencas.append({"modelo": m, "dif_utilidade_media": dif, "dif_ic_inf": inf, "dif_ic_sup": sup})

    politicas.to_csv(SAIDA / f"politicas_{sufixo}.csv", index=False)
    pd.DataFrame(linhas).to_csv(SAIDA / f"resumo_politicas_{sufixo}.csv", index=False)
    if final:
        pd.DataFrame(diferencas).to_csv(SAIDA / "diferenca_politicas_teste.csv", index=False)
    print(f"Gravados {SAIDA / f'politicas_{sufixo}.csv'} e {SAIDA / f'resumo_politicas_{sufixo}.csv'}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--final"]:
        main(TESTE, "teste")
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/decisao.py [--final]")
    else:
        main()
