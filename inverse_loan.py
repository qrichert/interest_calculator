#!/usr/bin/env python3
"""
python inverse_loan.py 800.00

    r = 12√(T+1) - 1
<=> r = (T+1)^(1/12) - 1

    M = K * (r / (1 - (1+r)^-n))
<=> K = M / (r / (1 - (1+r)^-n))
"""

import sys
from collections import defaultdict
from decimal import Decimal

from utils import dict_of_lists_as_table, rdec

if len(sys.argv) < 2:
    M = Decimal("800")  # 800 €
else:
    M = Decimal(sys.argv[1])


n = 60  # 60 mois = 5 ans
T = Decimal("0.59") / 100  # 0.59 %


table = defaultdict(list)
for n in (5, 10, 15, 20, 25, 30):
    years = n
    n *= 12
    for T in [x / 100 for x in range(50, 425, 25)]:
        T = Decimal(T) / 100

        r = (T + 1) ** (Decimal(1) / 12) - 1
        K = M / (r / (1 - ((1 + r) ** (-n))))

        total_Mi = Decimal(0)
        Ki = K
        for i in range(n):
            p = i + 1
            Mi = (T / 12) * Ki

            Ki = Ki * (1 + r) - M

            total_Mi += Mi

        table["Ans"].append(years)
        table["Mois"].append(n)
        table["Taux"].append(rdec(T * 100))
        table["Capital"].append(rdec(K))
        table["Mensualité"].append(rdec(M))
        table["Intérêts"].append(rdec(total_Mi))
        table["Total"].append(rdec(K + total_Mi))

    if years != 30:
        table["Ans"].append("-")
        table["Mois"].append("-")
        table["Taux"].append("-")
        table["Capital"].append("-")
        table["Mensualité"].append("-")
        table["Intérêts"].append("-")
        table["Total"].append("-")

r = (T + 1) ** (Decimal(1) / 12) - 1
K = M / (r / (1 - ((1 + r) ** (-n))))

print(dict_of_lists_as_table(table, -1))
