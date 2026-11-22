"""Escolhe a ação de crédito por utilidade esperada e compara com o limiar fixo de 0,5.

Para cada caso e modelo, UE(a) = (1 - p)·U(a, bom) + p·U(a, ruim), com p = P(ruim).
A ação escolhida é a de maior UE; empate (tolerância 1e-9): análise manual, rejeitar, aprovar.
A regra de comparação aprova se p < 0,5 e rejeita caso contrário.

Com --final, faz o mesmo sobre predicoes_teste.csv, acrescenta ao resumo o intervalo de 95%
da utilidade média por bootstrap (2000 reamostras, semente 2026) e grava a diferença
UE − limiar com intervalo pareado nas mesmas reamostras. Se predicoes_teste.csv tem p_sel
(modelo secundário escolhido pela seleção), sel entra como quarto modelo: colunas ao final de
politicas_teste.csv e linhas depois das de logreg no resumo e na diferença. Rodado só pelo autor.

Com --final, grava também a política de utilidade esperada restrita a aprovar e rejeitar (ue2), cujo
limiar vem da matriz, ao lado de ue (três ações) e do corte 0,5: utilidade média por regra e as
diferenças pareadas ue − limiar, ue − ue2 e ue2 − limiar, nas mesmas reamostras do bootstrap.
Análise exploratória posterior ao teste: não substitui a comparação principal.

Entradas:
  resultados/predicoes_dev.csv  record_id,kredit,fold,p_nb,p_tan,p_logreg
  resultados/predicoes_teste.csv record_id,kredit,p_nb,p_tan,p_logreg[,p_sel] (só com --final)
  config/utilidade.json         matriz de utilidade U(ação, estado) e hipóteses
Saídas:
  resultados/politicas_dev.csv         ação de cada regra, segunda ação e diferença de UE por caso
  resultados/resumo_politicas_dev.csv  utilidade média e contagens por modelo e regra
  resultados/politicas_teste.csv, resumo_politicas_teste.csv  o mesmo no teste (só com --final)
  resultados/diferenca_politicas_teste.csv  modelo,dif_utilidade_media,dif_ic_inf,dif_ic_sup (só com --final)
  com p_sel, as três tabelas do teste ganham sel (colunas ou linhas)
  resultados/duas_acoes_teste.csv           modelo,regra,utilidade_media,n_*,IC por regra: ue, ue2, limiar (só com --final)
  resultados/diferenca_duas_acoes_teste.csv modelo,comparacao,dif_utilidade_media,dif_ic_inf,dif_ic_sup,n_acao_diferente (só com --final)

Uso: a partir da raiz do repositório,
  uv run python codigo/decisao.py          grava as saídas do dev
  uv run python codigo/decisao.py --final  grava só as saídas do teste
  uv run python codigo/decisao.py --verificar  roda os autotestes e não grava nada
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
# Desempate entre aprovar e rejeitar na política de duas ações: rejeitar vence, como na PRIORIDADE.
DUAS = ["rejeitar", "aprovar"]
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


def acao_duas(p, u):
    """Ação de maior UE só entre rejeitar e aprovar; empate (tolerância 1e-9): rejeitar.
    Equivale a um limiar sobre p derivado da matriz, sem número escrito aqui."""
    ue = utilidade_esperada(p, u)
    return next(a for a in DUAS if ue[a] >= max(ue[b] for b in DUAS) - TOLERANCIA)


def calcular_duas_acoes(pred, u):
    """(resumo, diferencas) das regras ue (três ações), ue2 (UE com duas ações) e limiar (corte 0,5).
    Bootstrap com as mesmas reamostras de calcular(), então ue − limiar reproduz diferenca_politicas_teste.csv."""
    modelos = MODELOS + ["sel"] * ("p_sel" in pred.columns)
    estado = ["ruim" if k == 0 else "bom" for k in pred["kredit"]]  # kredit: 0 = ruim, 1 = bom
    n = len(pred)
    indices = np.random.default_rng(SEMENTE).integers(0, n, size=(REAMOSTRAS, n))
    linhas, diferencas = [], []
    for m in modelos:
        p = pred[f"p_{m}"]
        acoes = {"ue": [ordenar(x, u)[0] for x in p], "ue2": [acao_duas(x, u) for x in p], "limiar": [limiar(x) for x in p]}
        ganho = {r: np.array([u[a][e] for a, e in zip(acoes[r], estado)]) for r in acoes}
        media = {r: sum(ganho[r].tolist()) / n for r in acoes}
        for r in acoes:
            contagem = {f"n_{a}": acoes[r].count(a) for a in ACOES}
            if r == "ue2":
                for a in DUAS:
                    if contagem[f"n_{a}"] == 0:
                        print(f"AVISO: a ação {a} não aparece em {m}/{r}")
            inf, sup = np.percentile(ganho[r][indices].mean(axis=1), PERCENTIS)
            linhas.append({"modelo": m, "regra": r, "utilidade_media": media[r], **contagem, "utilidade_media_ic_inf": inf, "utilidade_media_ic_sup": sup})
        for a, b in [("ue", "limiar"), ("ue", "ue2"), ("ue2", "limiar")]:
            inf, sup = np.percentile((ganho[a] - ganho[b])[indices].mean(axis=1), PERCENTIS)
            diferencas.append({"modelo": m, "comparacao": f"{a} - {b}", "dif_utilidade_media": media[a] - media[b], "dif_ic_inf": inf, "dif_ic_sup": sup,
                               "n_acao_diferente": sum(x != y for x, y in zip(acoes[a], acoes[b]))})
    return pd.DataFrame(linhas), pd.DataFrame(diferencas)


def ler(entrada, final=False):
    """Lê as predições e termina com erro se faltar coluna, não houver linhas ou alguma p_* for inválida."""
    if not entrada.exists():
        sys.exit(f"ERRO: {entrada} não existe; rode codigo/modelos.py antes")
    pred = pd.read_csv(entrada)
    faltam = [c for c in ["record_id", "kredit"] + [f"p_{m}" for m in MODELOS] if c not in pred.columns]
    if faltam:
        sys.exit(f"ERRO: {entrada}: faltam as colunas {faltam}")
    if pred.empty:
        sys.exit(f"ERRO: {entrada}: arquivo sem linhas")
    for m in MODELOS + ["sel"] * (final and "p_sel" in pred.columns):
        p = pd.to_numeric(pred[f"p_{m}"], errors="coerce")
        if p.isna().any() or ((p < 0) | (p > 1)).any():
            sys.exit(f"ERRO: {entrada}: p_{m} vazia, não numérica ou fora de [0, 1]")
    return pred


def calcular(pred, u, final):
    """(politicas, resumo, diferencas); no teste, sel entra como quarto modelo se houver p_sel."""
    politicas = pred[["record_id", "kredit"]].copy()
    segunda, dif = {}, {}
    for m in MODELOS:
        ordem = [ordenar(x, u) for x in pred[f"p_{m}"]]
        politicas[f"acao_{m}_ue"] = [o[0] for o in ordem]
        politicas[f"acao_{m}_limiar"] = [limiar(x) for x in pred[f"p_{m}"]]
        segunda[f"segunda_{m}"] = [o[1] for o in ordem]
        dif[f"dif_ue_{m}"] = [o[2] for o in ordem]
    politicas = politicas.assign(**segunda, **dif)
    modelos = MODELOS
    if final and "p_sel" in pred.columns:
        modelos = MODELOS + ["sel"]
        ordem = [ordenar(x, u) for x in pred["p_sel"]]
        politicas["acao_sel_ue"] = [o[0] for o in ordem]
        politicas["acao_sel_limiar"] = [limiar(x) for x in pred["p_sel"]]
        politicas["segunda_sel"] = [o[1] for o in ordem]
        politicas["dif_ue_sel"] = [o[2] for o in ordem]

    # kredit: 0 = ruim, 1 = bom
    estado = ["ruim" if k == 0 else "bom" for k in politicas["kredit"]]
    if final:
        n = len(politicas)
        indices = np.random.default_rng(SEMENTE).integers(0, n, size=(REAMOSTRAS, n))
    linhas, por_linha, diferencas = [], {}, []
    for m in modelos:
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
    return politicas, pd.DataFrame(linhas), pd.DataFrame(diferencas)


def main(entrada=PREDICOES, sufixo="dev"):
    """Grava politicas_<sufixo>.csv e resumo_politicas_<sufixo>.csv; no teste, também os intervalos."""
    u = carregar_utilidade()
    final = sufixo == "teste"
    pred = ler(entrada, final)
    politicas, resumo, diferencas = calcular(pred, u, final)
    politicas.to_csv(SAIDA / f"politicas_{sufixo}.csv", index=False)
    resumo.to_csv(SAIDA / f"resumo_politicas_{sufixo}.csv", index=False)
    if final:
        diferencas.to_csv(SAIDA / "diferenca_politicas_teste.csv", index=False)
        duas, dif_duas = calcular_duas_acoes(pred, u)
        duas.to_csv(SAIDA / "duas_acoes_teste.csv", index=False)
        dif_duas.to_csv(SAIDA / "diferenca_duas_acoes_teste.csv", index=False)
    print(f"Gravados {SAIDA / f'politicas_{sufixo}.csv'} e {SAIDA / f'resumo_politicas_{sufixo}.csv'}")
    if final:
        print(f"Gravados também {SAIDA / 'duas_acoes_teste.csv'} e {SAIDA / 'diferenca_duas_acoes_teste.csv'}")


def verificar():
    """Autoteste do --final com arquivo falso montado do dev, com e sem p_sel; não grava nada."""
    u = carregar_utilidade()
    falso = ler(PREDICOES)[["record_id", "kredit"] + [f"p_{m}" for m in MODELOS]]
    sem = calcular(falso, u, True)
    com = calcular(falso.assign(p_sel=falso["p_tan"]), u, True)
    novas = ["acao_sel_ue", "acao_sel_limiar", "segunda_sel", "dif_ue_sel"]
    assert list(com[0].columns) == list(sem[0].columns) + novas
    assert com[0][sem[0].columns].equals(sem[0])
    for c, t in zip(com[1:], sem[1:]):
        assert c[c["modelo"] != "sel"].equals(t)
    assert list(com[1]["modelo"])[-2:] == ["sel", "sel"] and list(com[1]["regra"])[-2:] == ["ue", "limiar"]
    assert list(com[2]["modelo"]) == MODELOS + ["sel"]
    # o dev não ganha sel, mesmo com p_sel
    assert list(calcular(falso.assign(p_sel=falso["p_tan"]), u, False)[0].columns) == list(calcular(falso, u, False)[0].columns)
    # duas ações: reproduz ue e limiar de calcular(), fecha a conta da diferença e deriva o limiar da matriz
    duas, dif_duas = calcular_duas_acoes(falso, u)
    for m in MODELOS:
        for r in ("ue", "limiar"):
            a, b = duas[(duas["modelo"] == m) & (duas["regra"] == r)].iloc[0], sem[1][(sem[1]["modelo"] == m) & (sem[1]["regra"] == r)].iloc[0]
            assert all(np.isclose(a[c], b[c]) for c in ["utilidade_media", "utilidade_media_ic_inf", "utilidade_media_ic_sup"])
        d = dif_duas[dif_duas["modelo"] == m].set_index("comparacao")
        ref = sem[2][sem[2]["modelo"] == m].iloc[0]
        assert all(np.isclose(d.loc["ue - limiar", c], ref[k]) for c, k in [("dif_utilidade_media", "dif_utilidade_media"), ("dif_ic_inf", "dif_ic_inf"), ("dif_ic_sup", "dif_ic_sup")])
        assert np.isclose(d.loc["ue - limiar", "dif_utilidade_media"], d.loc["ue - ue2", "dif_utilidade_media"] + d.loc["ue2 - limiar", "dif_utilidade_media"])
    assert list(dif_duas["comparacao"][:3]) == ["ue - limiar", "ue - ue2", "ue2 - limiar"]
    g, r = u["aprovar"], u["rejeitar"]
    pstar = (g["bom"] - r["bom"]) / ((g["bom"] - r["bom"]) + (r["ruim"] - g["ruim"]))
    assert acao_duas(pstar - 0.01, u) == "aprovar" and acao_duas(pstar + 0.01, u) == "rejeitar"
    print("verificar: ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--final"]:
        main(TESTE, "teste")
    elif sys.argv[1:] == ["--verificar"]:
        verificar()
    elif sys.argv[1:]:
        sys.exit("Uso: uv run python codigo/decisao.py [--final | --verificar]")
    else:
        main()
