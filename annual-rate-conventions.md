# Annual rate conventions

The two conversions interpret the annual percentage differently:

- **Effective annual rate:** `r = (1 + T)^(1/12) - 1`, used by both
  scripts today.
- **Nominal annual rate:** `r = T / 12`, the standard French mortgage
  convention.
  [Crédit Agricole's mortgage formula](https://e-immobilier.credit-agricole.fr/conseils/marche/credit-immobilier-comprendre-votre-tableau-damortissement)

Here `T` is the annual rate as a decimal and `r` is the monthly rate. In
either case, use the same `r` for payments, balances, and interest:
`Mi = r * Ki`. Nominal and effective annual rates can describe the same
loan when converted consistently; entering the same percentage under
both definitions describes different loans.

For €200,000 over 240 months with `1.25` entered as the annual
percentage:

| Annual-rate interpretation       | Monthly payment | Total interest |
| -------------------------------- | --------------: | -------------: |
| Effective — current conversion   |         €941.62 |     €25,989.73 |
| Nominal — French bank convention |         €942.27 |     €26,144.19 |

These figures exclude fees and insurance. Totals use unrounded monthly
payments; rounding each installment to cents can change the final
installment and totals.

For French bank comparisons, the nominal conversion takes the quoted
**taux nominal / taux débiteur**. Both scripts currently interpret
annual rates as effective. For `loan.py`, convert a nominal quote before
entering it: `T_effective = (1 + T/12)^12 - 1`. This formula takes `T`
as a decimal rate (e.g. `0.0125`); the CLI takes a percentage, so enter
`100 * T_effective`.

**TAEG** includes additional costs, such as required insurance and fees;
it is not the borrowing rate to enter into these calculations.
[Crédit Agricole's explanation of TAEG](https://e-immobilier.credit-agricole.fr/conseils/financement/le-taux-annuel-effectif-global-taeg)

**Colombia and Peru are concrete examples of effective annual rates
being used for loans:**

- **Colombia:** Bancolombia publishes mortgage rates as _efectiva anual_
  alongside equivalent monthly rates. Conversion uses
  `r = (1 + T)^(1/12) - 1`.
  [Bancolombia](https://www.bancolombia.com/personas/creditos/vivienda/credito-hipotecario-para-comprar-vivienda)
- **Peru:** Banco GNB quotes _Tasa Efectiva Anual_ (TEA) and calculates
  the period rate as `(1 + T)^(days/360) - 1`. For 30 days this equals
  the effective monthly formula above; actual payment dates can change
  the interest charged.
  [Banco GNB's mortgage formulas](https://www.bancognb.com.pe/web/files/peru/banca_personas/FORMULAS-CREDITO-HIPOTECARIO.pdf)

Choose the conversion from the rate definition on the bank's quote;
practices can vary by product and lender.
