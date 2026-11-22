"""Autoteste da camada de decisão (codigo/decisao.py), só com assert.

Monta as matrizes de utilidade aqui mesmo, sem ler dados nem config/utilidade.json, e não grava nada.
Cobre: exemplo da apresentação, extremos, fronteiras c/400 e 1 - c/100, ausência da faixa de
análise manual, outra matriz, empates, ValueError e limiar fixo.

Uso: a partir da raiz do repositório,
  uv run python codigo/test_decisao.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decisao import ACOES, acao_duas, limiar, ordenar, utilidade_esperada  # noqa: E402


def matriz(c, perda=400):
    """Matriz demonstrativa com custo c da análise manual e perda ao aprovar um ruim."""
    return {"aprovar": {"bom": 100, "ruim": -perda}, "rejeitar": {"bom": 0, "ruim": 0}, "analise_manual": {"bom": 100 - c, "ruim": -c}}


def acao(p, u):
    return ordenar(p, u)[0]


grade = [i / 1000 for i in range(1001)]

# Exemplo da apresentação: p = 0,20.
assert abs(utilidade_esperada(0.2, matriz(40))["aprovar"] - 0) < 1e-9
assert abs(utilidade_esperada(0.2, matriz(40, perda=600))["aprovar"] - (-40)) < 1e-9

# Extremos e rejeitar sempre zero.
for c in [0, 20, 40, 60, 90, 100]:
    u = matriz(c)
    for a in ACOES:
        assert utilidade_esperada(0, u)[a] == u[a]["bom"]
        assert utilidade_esperada(1, u)[a] == u[a]["ruim"]
    assert all(utilidade_esperada(p, u)["rejeitar"] == 0 for p in grade)

# Fronteiras: aprovar abaixo de c/400, análise manual até 1 - c/100, rejeitar acima.
for c in [0, 20, 40, 60]:
    u, baixo, alto = matriz(c), c / 400, 1 - c / 100
    for p in grade:
        if abs(p - baixo) < 1e-9 or abs(p - alto) < 1e-9:
            esperado = "analise_manual"  # empate exato na fronteira
        elif p < baixo:
            esperado = "aprovar"
        elif p <= alto:
            esperado = "analise_manual"
        else:
            esperado = "rejeitar"
        assert acao(p, u) == esperado, (c, p, acao(p, u))

# Sem faixa de análise manual: corte aprovar/rejeitar em 0,20.
for c in [90, 100]:
    u = matriz(c)
    for p in grade:
        assert acao(p, u) != "analise_manual", (c, p)
        if abs(p - 0.2) > 1e-9:
            assert acao(p, u) == ("aprovar" if p < 0.2 else "rejeitar"), (c, p)

# Outra matriz: perda 600 e c = 40 dão fronteiras 40/600 e 0,60.
u = matriz(40, perda=600)
for p in grade:
    if abs(p - 40 / 600) < 1e-9 or abs(p - 0.6) < 1e-9:
        continue
    assert acao(p, u) == ("aprovar" if p < 40 / 600 else "analise_manual" if p < 0.6 else "rejeitar"), p
assert acao(40 / 600, u) == "analise_manual" and acao(0.6, u) == "analise_manual"

# Empates exatos seguem análise manual > rejeitar > aprovar.
assert ordenar(0.1, matriz(40))[:2] == ("analise_manual", "aprovar")
assert ordenar(0.6, matriz(40))[:2] == ("analise_manual", "rejeitar")
assert ordenar(0.2, matriz(100))[:2] == ("rejeitar", "aprovar")
assert all(ordenar(p, matriz(40))[2] >= 0 for p in grade)

# Probabilidade inválida.
for p in [-0.01, 1.01, float("nan")]:
    for f in [lambda x: utilidade_esperada(x, matriz(40)), lambda x: ordenar(x, matriz(40)), limiar]:
        levantou = False
        try:
            f(p)
        except ValueError:
            levantou = True
        assert levantou, p

# Limiar fixo.
assert limiar(0.4999) == "aprovar" and limiar(0.5) == "rejeitar" and limiar(0.7) == "rejeitar"

# Duas ações (UE só entre aprovar e rejeitar): o limiar vem da matriz.
# Com ganho igual à perda o limiar é 0,5 e a regra coincide com o corte fixo.
simetrica = {"aprovar": {"bom": 100, "ruim": -100}, "rejeitar": {"bom": 0, "ruim": 0}, "analise_manual": {"bom": 60, "ruim": -40}}
assert all(acao_duas(p, simetrica) == limiar(p) for p in grade)
# Matriz demonstrativa (G = 100, L = 400): aprova abaixo de G/(G + L) = 0,2; no empate, rejeita.
assert all(acao_duas(p, matriz(40)) == ("aprovar" if p < 0.2 else "rejeitar") for p in grade)
# Com L = 600 o limiar é 100/700; a análise manual não muda a regra de duas ações.
assert all(acao_duas(p, matriz(c, perda=600)) == ("aprovar" if p < 100 / 700 else "rejeitar") for p in grade for c in (0, 40, 90))
# A UE máxima com três ações nunca é menor que a máxima com duas.
for c in (0, 40, 90):
    for p in grade:
        ue = utilidade_esperada(p, matriz(c))
        assert max(ue.values()) >= max(ue["aprovar"], ue["rejeitar"])

print("test_decisao: todos os testes passaram")
