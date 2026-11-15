"""Prepara a base: SouthGermanCredit.asc -> sgc.csv -> dev.csv (800) e teste.csv (200).

Não altera o arquivo bruto. Uso, a partir da raiz do repositório:
  uv run python codigo/preparar_sgc.py

Depois de gerado, teste.csv só é lido no teste final (PLANO.md, passo 10).
"""
import csv
import hashlib
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "dados/brutos/SouthGermanCredit.asc"
SAIDA = RAIZ / "dados/processados"
SEMENTE = 2026
CONTINUAS = ["laufzeit", "hoehe", "alter"]


def converter():
    rows = [line.split() for line in BRUTO.read_text(encoding="ascii").splitlines() if line.strip()]
    header, body = rows[0], rows[1:]
    assert len(body) == 1000 and all(len(r) == len(header) for r in body), "base inesperada"
    SAIDA.mkdir(parents=True, exist_ok=True)
    with open(SAIDA / "sgc.csv", "w", newline="", encoding="utf-8") as handle:
        w = csv.writer(handle)
        w.writerow(["record_id"] + header)
        for i, r in enumerate(body):
            w.writerow(["sgc-{:04d}".format(i)] + r)


def dividir():
    base = pd.read_csv(SAIDA / "sgc.csv")
    dev, teste = train_test_split(base, test_size=0.2, stratify=base["kredit"], random_state=SEMENTE)
    dev, teste = dev.sort_index(), teste.sort_index()

    # kredit: 0 = ruim, 1 = bom
    assert (len(dev), len(teste)) == (800, 200)
    assert ((dev["kredit"] == 0).sum(), (teste["kredit"] == 0).sum()) == (240, 60)
    assert not set(dev["record_id"]) & set(teste["record_id"]), "registro nos dois conjuntos"
    for col in base.columns.drop(["record_id", "kredit"] + CONTINUAS):
        fora = set(teste[col]) - set(dev[col])
        assert not fora, f"{col}: categoria {fora} aparece no teste e não no dev"

    dev.to_csv(SAIDA / "dev.csv", index=False)
    teste.to_csv(SAIDA / "teste.csv", index=False)


def main():
    converter()
    dividir()
    linhas = [
        f"{hashlib.sha256((SAIDA / nome).read_bytes()).hexdigest()}  {nome}"
        for nome in ("sgc.csv", "dev.csv", "teste.csv")
    ]
    (SAIDA / "SHA256SUMS").write_text("\n".join(linhas) + "\n")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
