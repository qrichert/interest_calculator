#!/usr/bin/env python3
"""
python loan.py 200_000 240 1.25

https://fr.wikipedia.org/wiki/Amortissement_(finance)

M = Mensualité
Mi = Part intérêts (intérêts payés sur la période)
Ma = Capital amorti (capital remboursé sur la période, hors intérêts)
K = Capital emprunté
Ki = Capital restant dû (à la i-ème période)
n = Nombre de périodes
r = Taux mensuel
T = Taux d'intérêt fixe annuel

    r = 12√(T+1) - 1
<=> r = (T+1)^(1/12) - 1

M = K * (r / (1 - (1+r)^-n))

Mi = (T/12) * Ki
Ma = M - Mi
"""

import sys
from decimal import Decimal

if len(sys.argv) < 4:
    K = Decimal("17500")  # 17 500 €
    n = 60  # 60 mois = 5 ans
    T = Decimal("0.59") / 100  # 0.59 %
else:
    K = Decimal(sys.argv[1])
    n = int(sys.argv[2])
    T = Decimal(sys.argv[3]) / 100

# K = Decimal("75500")  # 17 500 €
# n = 240  # 5 ans
# T = Decimal("1.25") / 100  # 0.59%

HEADER_p = "Rang"
HEADER_M = "Mensualité"
HEADER_Ma = "K amorti"
HEADER_Mi = "Intérêt"
HEADER_Ki = "Restant dû"


def dec2str(dec: Decimal) -> str:
    return str(dec.quantize(Decimal("0.01")))


def row2str(p, M, Ma, Mi, Ki) -> str:
    len_k = len(dec2str(K))
    p = str(p).rjust(max(len(str(n)), len(HEADER_p)))
    Ma = dec2str(Ma).rjust(max(len_k, len(HEADER_Ma)))
    Mi = dec2str(Mi).rjust(max(len_k, len(HEADER_Mi)))
    Ki = (dec2str(Ki) if Ki is not None else "").rjust(max(len_k, len(HEADER_Ki)))
    M = dec2str(M).rjust(max(len_k, len(HEADER_M)))
    return " ".join((p, M, Ma, Mi, Ki))


r = (T + 1) ** (Decimal(1) / 12) - 1
M = K * (r / (1 - ((1 + r) ** (-n))))

total_M = Decimal(0)
total_Ma = Decimal(0)
total_Mi = Decimal(0)
Ki = K
rows: list[list] = []
for i in range(n):
    p = i + 1
    Mi = (T / 12) * Ki
    Ma = M - Mi

    Ki = Ki * (1 + r) - M

    total_M += M
    total_Ma += Ma
    total_Mi += Mi

    rows.append([p, M, Ma, Mi, Ki])


print("Capital emprunté:", dec2str(K), "€")
print("Taux d'intérêt annuel fixe:", dec2str(T * 100), "%")
print("Durée:", n, "mois", f"({n//12} ans)")
print("=> Mensualités:", dec2str(M), "€")
print("=> Coût:", dec2str(total_Mi), "€")
print("=> Total:", dec2str(K + total_Mi), "€")
print(HEADER_p, HEADER_M, HEADER_Ma, HEADER_Mi, HEADER_Ki)
print(
    *[
        "-" * len(header)
        for header in [HEADER_p, HEADER_M, HEADER_Ma, HEADER_Mi, HEADER_Ki]
    ]
)
print(row2str(0, Decimal(), Decimal(), Decimal(), K))
rows[-1][-1] = Decimal(0)  # Last Ki = +0.00
print("\n".join([row2str(*row) for row in rows]))
totals: str = row2str("", total_M, total_Ma, total_Mi, None)
print("-" * len(totals))
print(totals)
