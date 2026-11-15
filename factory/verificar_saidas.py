"""Confere formato e consistência das saídas dos scripts do experimento.

É o juiz usado por factory/checks.sh. Cada bloco só roda se o arquivo que ele
confere existir. Nenhuma checagem exige valor de resultado: um modelo ruim, mas
programado corretamente, passa. Linhas "AVISO:" informam o autor e não reprovam.

Critérios em docs/criterios-de-aceite.md.

Uso:
  python factory/verificar_saidas.py <raiz>
onde <raiz> contém codigo/, config/, dados/processados/dev.csv e resultados/.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score

RAIZ = Path(sys.argv[1]).resolve()
RES = RAIZ / "resultados"
MODELOS = ["nb", "tan", "logreg"]
ACOES = ["aprovar", "rejeitar", "analise_manual"]
CORTES = {"laufzeit": [12.0, 24.0], "hoehe": [1553.0, 3384.0], "alter": [28.0, 38.0]}
PNG = b"\x89PNG\r\n\x1a\n"
erros = []


def exigir(condicao, mensagem):
    if not condicao:
        erros.append(mensagem)
    return bool(condicao)


def aviso(mensagem):
    print(f"AVISO: {mensagem}")


def perto(a, b, tol=1e-9):
    return bool(np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), rtol=0, atol=tol))


def colunas(df, esperadas, nome):
    return exigir(list(df.columns) == esperadas, f"{nome}: colunas {list(df.columns)}, esperado {esperadas}")


def e_png(nome):
    exigir((RES / nome).read_bytes()[:8] == PNG, f"{nome}: não é um PNG válido")


def probabilidades(serie, nome, estrito=True):
    v = serie.to_numpy(dtype=float)
    ok = np.isfinite(v).all() and ((v > 0) & (v < 1)).all() if estrito else np.isfinite(v).all() and ((v >= 0) & (v <= 1)).all()
    exigir(ok, f"{nome}: probabilidade vazia, não finita ou fora do intervalo")


def metricas_por_fold(y_ruim, p, fold):
    """Média e desvio amostral, entre as partições, de ROC-AUC, Brier, log loss e PR-AUC (nessa ordem)."""
    linhas = []
    for k in sorted(set(fold)):
        m = fold == k
        linhas.append([roc_auc_score(y_ruim[m], p[m]), brier_score_loss(y_ruim[m], p[m]), log_loss(y_ruim[m], p[m], labels=[0, 1]), average_precision_score(y_ruim[m], p[m])])
    linhas = np.array(linhas)
    return linhas.mean(axis=0), linhas.std(axis=0, ddof=1)


def escolher(p, u):
    """Ação de maior utilidade esperada; empate: análise manual, rejeitar, aprovar."""
    ue = {a: (1 - p) * u[a]["bom"] + p * u[a]["ruim"] for a in ACOES}
    melhor = max(ue.values())
    return next(a for a in ["analise_manual", "rejeitar", "aprovar"] if ue[a] >= melhor - 1e-9)


def ordenar(p, u):
    """(melhor, segunda, diferença de UE entre elas), com o desempate da D5."""
    ue = {a: (1 - p) * u[a]["bom"] + p * u[a]["ruim"] for a in ACOES}
    prioridade = ["analise_manual", "rejeitar", "aprovar"]
    primeira = next(a for a in prioridade if ue[a] >= max(ue.values()) - 1e-9)
    resto = [a for a in prioridade if a != primeira]
    segunda = next(a for a in resto if ue[a] >= max(ue[b] for b in resto) - 1e-9)
    return primeira, segunda, ue[primeira] - ue[segunda]


def rodar(*args):
    return subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True)


dev = pd.read_csv(RAIZ / "dados/processados/dev.csv")
variaveis = [c for c in dev.columns if c not in ("record_id", "kredit")]
pred = None
utilidade = None

# --- Issue 01 -------------------------------------------------------------
if (RES / "predicoes_dev.csv").exists():
    pred = pd.read_csv(RES / "predicoes_dev.csv")
    n = "predicoes_dev.csv"
    if colunas(pred, ["record_id", "kredit", "fold", "p_nb", "p_tan", "p_logreg"], n) and exigir(len(pred) == 800, f"{n}: {len(pred)} linhas, esperado 800"):
        exigir(list(pred["record_id"]) == list(dev["record_id"]), f"{n}: record_id fora da ordem do dev.csv")
        exigir(list(pred["kredit"]) == list(dev["kredit"]), f"{n}: kredit difere do dev.csv")
        exigir(sorted(pred["fold"].unique()) == [0, 1, 2, 3, 4], f"{n}: fold deve ir de 0 a 4")
        for k, parte in pred.groupby("fold"):
            exigir((len(parte), int((parte["kredit"] == 0).sum())) == (160, 48), f"{n}: partição {k} não tem 160 linhas e 48 ruins")
        for m in MODELOS:
            probabilidades(pred[f"p_{m}"], f"{n} p_{m}")
    else:
        pred = None
    cortes = json.loads((RES / "cortes.json").read_text()) if exigir((RES / "cortes.json").exists(), "cortes.json ausente") else None
    exigir(cortes == CORTES, f"cortes.json: {cortes}, esperado {CORTES}")
    if exigir((RES / "tan_arestas.csv").exists(), "tan_arestas.csv ausente"):
        arestas = pd.read_csv(RES / "tan_arestas.csv")
        n = "tan_arestas.csv"
        if colunas(arestas, ["fold", "origem", "destino"], n):
            exigir(sorted(arestas["fold"].unique()) == [0, 1, 2, 3, 4], f"{n}: fold deve ir de 0 a 4")
            exigir(arestas.equals(arestas.sort_values(["fold", "origem", "destino"]).reset_index(drop=True)), f"{n}: linhas fora de ordem (fold, origem, destino)")
            exigir(not arestas.duplicated().any(), f"{n}: aresta repetida")
            exigir(set(arestas["origem"]) | set(arestas["destino"]) <= set(variaveis) | {"kredit"}, f"{n}: nome que não é coluna do dev")
            for k, parte in arestas.groupby("fold"):
                exigir(set(parte.loc[parte["origem"] == "kredit", "destino"]) == set(variaveis), f"{n}: partição {k}: kredit deve apontar para as 20 variáveis")
                entre = parte[parte["origem"] != "kredit"]
                exigir(not entre["destino"].duplicated().any(), f"{n}: partição {k}: variável com mais de um pai entre as variáveis")

# --- Issue 02 -------------------------------------------------------------
metricas = None
if (RES / "metricas_dev.csv").exists() and pred is not None:
    metricas = pd.read_csv(RES / "metricas_dev.csv")
    n = "metricas_dev.csv"
    nomes = ["roc_auc", "pr_auc", "brier", "log_loss", "ece"]
    esperadas = ["modelo"] + [f"{m}_{s}" for m in nomes for s in ("media", "desvio")]
    if colunas(metricas, esperadas, n) and exigir(list(metricas["modelo"]) == MODELOS + ["taxa_base"], f"{n}: linhas devem ser nb, tan, logreg, taxa_base"):
        metricas = metricas.set_index("modelo")
        y, fold = (pred["kredit"] == 0).to_numpy().astype(int), pred["fold"].to_numpy()
        for m in MODELOS:
            media, desvio = metricas_por_fold(y, pred[f"p_{m}"].to_numpy(), fold)
            linha = metricas.loc[m]
            exigir(perto(linha[["roc_auc_media", "brier_media", "log_loss_media", "pr_auc_media"]], media), f"{n}: médias de {m} não batem com as predições")
            exigir(perto(linha[["roc_auc_desvio", "brier_desvio", "log_loss_desvio", "pr_auc_desvio"]], desvio), f"{n}: desvios de {m} não batem com as predições")
            exigir(0 <= linha["ece_media"] <= 1 and linha["ece_desvio"] >= 0, f"{n}: ece de {m} fora do intervalo")
        base = metricas.loc["taxa_base"]
        exigir(perto(base[["roc_auc_media", "brier_media", "log_loss_media", "ece_media", "pr_auc_media"]], [0.5, 0.21, 0.610864, 0.0, 0.30], 1e-6), f"{n}: linha taxa_base com valores errados")
        exigir(perto(base[[f"{m}_desvio" for m in nomes]], 0, 1e-6), f"{n}: desvios da taxa_base devem ser 0")
        for m in MODELOS:
            if metricas.loc[m, "brier_media"] >= base["brier_media"]:
                aviso(f"brier de {m} >= taxa_base")
            if metricas.loc[m, "roc_auc_media"] < 0.5:
                aviso(f"roc_auc de {m} < 0,5")
    else:
        metricas = None
    if exigir((RES / "calibracao_dev.png").exists(), "calibracao_dev.png ausente"):
        e_png("calibracao_dev.png")

# --- Issue 03 -------------------------------------------------------------
if (RES / "predicoes_dev_oculta.csv").exists() and pred is not None:
    oculta = pd.read_csv(RES / "predicoes_dev_oculta.csv")
    n = "predicoes_dev_oculta.csv"
    if colunas(oculta, ["record_id", "modelo", "variavel_oculta", "p_ruim"], n) and exigir(len(oculta) == 48000, f"{n}: {len(oculta)} linhas, esperado 48000"):
        exigir(set(oculta["modelo"]) == set(MODELOS) and set(oculta["variavel_oculta"]) == set(variaveis), f"{n}: modelos ou variáveis inesperados")
        probabilidades(oculta["p_ruim"], n, estrito=False)
        y, fold = (pred["kredit"] == 0).to_numpy().astype(int), pred["fold"].to_numpy()
        ids = list(pred["record_id"])
        resumo = {}
        for (m, v), parte in oculta.groupby(["modelo", "variavel_oculta"]):
            if not exigir(sorted(parte["record_id"]) == sorted(ids), f"{n}: par ({m}, {v}) não tem os 800 casos uma vez"):
                continue
            p = parte.set_index("record_id").loc[ids, "p_ruim"].to_numpy()
            if perto(p, pred[f"p_{m}"].to_numpy(), 0):
                aviso(f"esconder {v} não mudou nenhuma predição de {m}")
            resumo[(m, v)] = metricas_por_fold(y, p, fold)[0]
        if exigir((RES / "evidencia_incompleta.csv").exists(), "evidencia_incompleta.csv ausente") and metricas is not None:
            ev = pd.read_csv(RES / "evidencia_incompleta.csv")
            n = "evidencia_incompleta.csv"
            if colunas(ev, ["modelo", "variavel_oculta", "roc_auc", "brier", "delta_roc_auc", "delta_brier"], n) and exigir(len(ev) == 60, f"{n}: {len(ev)} linhas, esperado 60"):
                for _, r in ev.iterrows():
                    chave = (r["modelo"], r["variavel_oculta"])
                    if exigir(chave in resumo, f"{n}: par {chave} inesperado"):
                        exigir(perto([r["roc_auc"], r["brier"]], resumo[chave][:2]), f"{n}: métricas de {chave} não batem com as predições")
                        completo = metricas.loc[r["modelo"]]
                        exigir(perto([r["roc_auc"] - r["delta_roc_auc"], r["brier"] - r["delta_brier"]], [completo["roc_auc_media"], completo["brier_media"]]), f"{n}: delta de {chave} não bate com metricas_dev.csv")
                ev = ev.set_index(["modelo", "variavel_oculta"])
                for m in MODELOS:
                    if (m, "laufkont") in ev.index and ev.loc[(m, "laufkont"), "delta_brier"] <= ev.loc[(m, "telef"), "delta_brier"]:
                        aviso(f"ocultar laufkont não piorou mais que ocultar telef em {m}")

# --- Issue 04 -------------------------------------------------------------
if (RAIZ / "config/utilidade.json").exists():
    bruto = json.loads((RAIZ / "config/utilidade.json").read_text())
    acoes = bruto.get("acoes", {})
    ok = set(acoes) == set(ACOES) and all(set(acoes[a]) == {"bom", "ruim"} and all(isinstance(x, (int, float)) for x in acoes[a].values()) for a in acoes)
    if exigir(ok, "utilidade.json: esperado acoes.{aprovar,rejeitar,analise_manual}.{bom,ruim} numéricos"):
        utilidade = acoes
    exigir(isinstance(bruto.get("hipoteses"), str) and bruto["hipoteses"].strip(), "utilidade.json: campo hipoteses ausente ou vazio")

politicas = None
if (RES / "politicas_dev.csv").exists() and pred is not None and utilidade is not None:
    politicas = pd.read_csv(RES / "politicas_dev.csv")
    n = "politicas_dev.csv"
    cols = ["record_id", "kredit"] + [f"acao_{m}_{r}" for m in MODELOS for r in ("ue", "limiar")]
    novas = [f"{k}_{m}" for k in ("segunda", "dif_ue") for m in MODELOS]
    colunas_ok = exigir(list(politicas.columns[: len(cols)]) == cols and set(politicas.columns[len(cols):]) == set(novas) and len(politicas.columns) == len(cols) + len(novas), f"{n}: colunas {list(politicas.columns)}, esperado {cols} mais {novas}")
    if colunas_ok and exigir(len(politicas) == 800, f"{n}: {len(politicas)} linhas, esperado 800"):
        exigir(list(politicas["record_id"]) == list(pred["record_id"]) and list(politicas["kredit"]) == list(pred["kredit"]), f"{n}: record_id ou kredit diferem das predições")
        for m in MODELOS:
            p = pred[f"p_{m}"]
            exigir(list(politicas[f"acao_{m}_ue"]) == [escolher(x, utilidade) for x in p], f"{n}: acao_{m}_ue não é a de maior utilidade esperada")
            exigir(list(politicas[f"acao_{m}_limiar"]) == ["aprovar" if x < 0.5 else "rejeitar" for x in p], f"{n}: acao_{m}_limiar não segue o limiar 0,5")
            ordem = [ordenar(x, utilidade) for x in p]
            exigir(list(politicas[f"segunda_{m}"]) == [o[1] for o in ordem], f"{n}: segunda_{m} não é a ação de segunda maior utilidade esperada")
            exigir(perto(politicas[f"dif_ue_{m}"], [o[2] for o in ordem]) and (politicas[f"dif_ue_{m}"] >= -1e-9).all(), f"{n}: dif_ue_{m} não bate com a conta")
    else:
        politicas = None
    if exigir((RES / "resumo_politicas_dev.csv").exists(), "resumo_politicas_dev.csv ausente") and politicas is not None:
        resumo = pd.read_csv(RES / "resumo_politicas_dev.csv")
        n = "resumo_politicas_dev.csv"
        cols = ["modelo", "regra", "utilidade_media", "n_aprovar", "n_rejeitar", "n_analise_manual", "n_mudam_vs_outra_regra"]
        if colunas(resumo, cols, n) and exigir(sorted(zip(resumo["modelo"], resumo["regra"])) == sorted((m, r) for m in MODELOS for r in ("ue", "limiar")), f"{n}: esperado uma linha por modelo e regra"):
            estado = np.where(politicas["kredit"] == 0, "ruim", "bom")
            for _, r in resumo.iterrows():
                acao = politicas[f"acao_{r['modelo']}_{r['regra']}"]
                contagem = [int((acao == a).sum()) for a in ACOES]
                exigir([r["n_aprovar"], r["n_rejeitar"], r["n_analise_manual"]] == contagem, f"{n}: contagens de {r['modelo']}/{r['regra']} não batem com politicas_dev.csv")
                media = np.mean([utilidade[a][e] for a, e in zip(acao, estado)])
                exigir(perto(r["utilidade_media"], media), f"{n}: utilidade_media de {r['modelo']}/{r['regra']} não bate")
                mudam = int((politicas[f"acao_{r['modelo']}_ue"] != politicas[f"acao_{r['modelo']}_limiar"]).sum())
                exigir(r["n_mudam_vs_outra_regra"] == mudam, f"{n}: n_mudam_vs_outra_regra de {r['modelo']}/{r['regra']} não bate")
                if r["regra"] == "ue":
                    for a, c in zip(ACOES, contagem):
                        if c == 0:
                            aviso(f"a ação {a} não aparece em {r['modelo']}/ue")

# --- Issue 05 -------------------------------------------------------------
if (RES / "sensibilidade.csv").exists() and utilidade is not None:
    sens = pd.read_csv(RES / "sensibilidade.csv")
    n = "sensibilidade.csv"
    grade = [(float(l), float(c)) for l in (200, 400, 600, 800) for c in range(0, 101, 5)]
    if colunas(sens, ["perda", "custo_analise", "limiar_inferior", "limiar_superior"], n) and exigir(sorted(zip(sens["perda"].astype(float), sens["custo_analise"].astype(float))) == sorted(grade), f"{n}: grade diferente da combinada (84 linhas)"):
        g = utilidade["aprovar"]["bom"]
        for _, r in sens.iterrows():
            l, c = r["perda"], r["custo_analise"]
            esperado = [c / l, 1 - c / g] if c < g * l / (g + l) else [g / (g + l)] * 2
            exigir(perto([r["limiar_inferior"], r["limiar_superior"]], esperado), f"{n}: limiares errados para perda {l} e custo {c}")
    if exigir((RES / "sensibilidade.png").exists(), "sensibilidade.png ausente"):
        e_png("sensibilidade.png")

# --- Issue 06 -------------------------------------------------------------
if (RAIZ / "codigo/demo.py").exists() and pred is not None and politicas is not None:
    for k in (0, 1, 2):
        caso = pred[pred["fold"] == k].iloc[0]
        r = rodar("codigo/demo.py", caso["record_id"])
        if exigir(r.returncode == 0, f"demo.py {caso['record_id']}: saída {r.returncode}\n{r.stderr[-500:]}"):
            for m in MODELOS:
                exigir(f"{caso[f'p_{m}']:.6f}" in r.stdout, f"demo.py {caso['record_id']}: não mostra p_{m} = {caso[f'p_{m}']:.6f}")
            numeros = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", r.stdout)]
            for a in ACOES:
                ue = (1 - caso["p_tan"]) * utilidade[a]["bom"] + caso["p_tan"] * utilidade[a]["ruim"]
                exigir(any(abs(x - ue) <= 0.05 for x in numeros), f"demo.py {caso['record_id']}: não mostra a utilidade esperada de {a} ({ue:.2f}) para o tan")
            acao = politicas.loc[politicas["record_id"] == caso["record_id"], "acao_tan_ue"].iloc[0]
            exigir(acao in r.stdout, f"demo.py {caso['record_id']}: não mostra a ação {acao}")
            exigir(rodar("codigo/demo.py", caso["record_id"]).stdout == r.stdout, "demo.py: saída muda ao repetir")
    r = rodar("codigo/demo.py", "sgc-9999")
    exigir(r.returncode != 0 and "Traceback" not in r.stderr + r.stdout, "demo.py com caso inexistente deve falhar com mensagem, sem traceback")
    exigir(rodar("codigo/demo.py").returncode == 2, "demo.py sem argumento deve sair com 2")
    exigir(not list(RES.glob("*.pkl")) and not list(RES.glob("*.joblib")), "demo.py salvou modelo em arquivo")

# --- Issue 07 -------------------------------------------------------------
if (RAIZ / "codigo/modelos.py").exists() and "--final" in (RAIZ / "codigo/modelos.py").read_text() and pred is not None:
    antes = {f.name: f.read_bytes() for f in RES.iterdir()}
    exigir(rodar("codigo/modelos.py", "--final").returncode != 0 and not (RES / "predicoes_teste.csv").exists(), "modelos.py --final sem caminho deve falhar sem gravar")
    for script in ("avaliar.py", "decisao.py"):
        if "--final" in (RAIZ / "codigo" / script).read_text():
            exigir(rodar(f"codigo/{script}", "--final").returncode != 0, f"{script} --final sem predicoes_teste.csv deve falhar")
    with tempfile.TemporaryDirectory() as pasta:
        falso = Path(pasta) / "falso.csv"
        dev[(pred["fold"] == 0).to_numpy()].to_csv(falso, index=False)
        r = rodar("codigo/modelos.py", "--final", str(falso))
        if exigir(r.returncode == 0 and (RES / "predicoes_teste.csv").exists(), f"modelos.py --final falhou\n{r.stderr[-500:]}"):
            teste = pd.read_csv(RES / "predicoes_teste.csv")
            n = "predicoes_teste.csv"
            if colunas(teste, ["record_id", "kredit", "p_nb", "p_tan", "p_logreg"], n):
                exigir(list(teste["record_id"]) == list(pd.read_csv(falso)["record_id"]), f"{n}: linhas diferem do arquivo de entrada")
                for m in MODELOS:
                    probabilidades(teste[f"p_{m}"], f"{n} p_{m}")
            conteudo = (RES / "predicoes_teste.csv").read_bytes()
            r = rodar("codigo/modelos.py", "--final", str(falso))
            exigir(r.returncode != 0 and (RES / "predicoes_teste.csv").read_bytes() == conteudo, "modelos.py --final deve recusar sobrescrever predicoes_teste.csv")
            for script, saidas in (("avaliar.py", ["metricas_teste.csv", "calibracao_teste.png"]), ("decisao.py", ["politicas_teste.csv", "resumo_politicas_teste.csv", "diferenca_politicas_teste.csv"])):
                if "--final" in (RAIZ / "codigo" / script).read_text():
                    r = rodar(f"codigo/{script}", "--final")
                    exigir(r.returncode == 0 and all((RES / s).exists() for s in saidas), f"{script} --final falhou ou não gravou {saidas}\n{r.stderr[-500:]}")
            if (RES / "metricas_teste.csv").exists():
                mt = pd.read_csv(RES / "metricas_teste.csv")
                n = "metricas_teste.csv"
                if colunas(mt, ["modelo", "roc_auc", "roc_auc_ic_inf", "roc_auc_ic_sup", "pr_auc", "pr_auc_ic_inf", "pr_auc_ic_sup", "brier", "brier_ic_inf", "brier_ic_sup", "log_loss", "ece"], n):
                    exigir(list(mt["modelo"]) == MODELOS + ["taxa_base"], f"{n}: linhas devem ser nb, tan, logreg, taxa_base")
                    for nome in ("roc_auc", "pr_auc", "brier"):
                        dentro = (mt[f"{nome}_ic_inf"] <= mt[nome] + 1e-9) & (mt[nome] <= mt[f"{nome}_ic_sup"] + 1e-9)
                        exigir(dentro.all(), f"{n}: {nome} fora do próprio intervalo")
            if (RES / "resumo_politicas_teste.csv").exists() and (RES / "resumo_politicas_dev.csv").exists():
                rt = pd.read_csv(RES / "resumo_politicas_teste.csv")
                n = "resumo_politicas_teste.csv"
                if colunas(rt, list(pd.read_csv(RES / "resumo_politicas_dev.csv").columns) + ["utilidade_media_ic_inf", "utilidade_media_ic_sup"], n):
                    dentro = (rt["utilidade_media_ic_inf"] <= rt["utilidade_media"] + 1e-9) & (rt["utilidade_media"] <= rt["utilidade_media_ic_sup"] + 1e-9)
                    exigir(dentro.all(), f"{n}: utilidade_media fora do próprio intervalo")
                    if (RES / "diferenca_politicas_teste.csv").exists():
                        dif = pd.read_csv(RES / "diferenca_politicas_teste.csv")
                        n = "diferenca_politicas_teste.csv"
                        if colunas(dif, ["modelo", "dif_utilidade_media", "dif_ic_inf", "dif_ic_sup"], n) and exigir(sorted(dif["modelo"]) == sorted(MODELOS), f"{n}: uma linha por modelo"):
                            dentro = (dif["dif_ic_inf"] <= dif["dif_utilidade_media"] + 1e-9) & (dif["dif_utilidade_media"] <= dif["dif_ic_sup"] + 1e-9)
                            exigir(dentro.all(), f"{n}: diferença fora do próprio intervalo")
                            for _, r in dif.iterrows():
                                u = rt.set_index(["modelo", "regra"])["utilidade_media"]
                                exigir(perto(r["dif_utilidade_media"], u[(r["modelo"], "ue")] - u[(r["modelo"], "limiar")]), f"{n}: diferença de {r['modelo']} não bate com resumo_politicas_teste.csv")
            if (RES / "politicas_teste.csv").exists() and politicas is not None:
                exigir(list(pd.read_csv(RES / "politicas_teste.csv").columns) == list(politicas.columns), "politicas_teste.csv: colunas diferem de politicas_dev.csv")
    exigir(all(not f.exists() or f.read_bytes() == antes[f.name] for f in (RES / nome for nome in antes)), "--final alterou arquivo do dev")

if erros:
    print("\n".join(f"ERRO: {e}" for e in erros), file=sys.stderr)
    sys.exit(1)
print("saídas conferidas")
