import contextlib
import io
import runpy
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch


class LoanAccountingTests(unittest.TestCase):
    def test_forward_schedule_conserves_principal_and_interest(self):
        tolerance = Decimal("1e-18")
        for args in ((), ("200000", "240", "1.25"), ("220000", "240", "3.5")):
            with self.subTest(args=args):
                loan = run_script("loan.py", *args)
                self.assertAlmostEqual(loan["total_Ma"], loan["K"], delta=tolerance)
                self.assertAlmostEqual(
                    loan["total_Mi"], loan["total_M"] - loan["K"], delta=tolerance
                )
                self.assertAlmostEqual(loan["Ki"], Decimal(0), delta=tolerance)

                balance = loan["K"]
                for period, payment, principal, interest, remaining in loan["rows"]:
                    self.assertAlmostEqual(
                        balance - remaining, principal, delta=tolerance, msg=period
                    )
                    self.assertAlmostEqual(
                        payment, principal + interest, delta=tolerance, msg=period
                    )
                    balance = remaining

    def test_known_payments_and_interest_totals(self):
        for args, payment, interest in (
            (("200000", "240", "1.25"), "942.27", "26144.19"),
            (("220000", "240", "3.5"), "1275.91", "86218.73"),
        ):
            with self.subTest(args=args):
                loan = run_script("loan.py", *args)
                self.assertEqual(loan["M"].quantize(Decimal("0.01")), Decimal(payment))
                self.assertEqual(
                    loan["total_Mi"].quantize(Decimal("0.01")), Decimal(interest)
                )

    def test_inverse_totals_equal_monthly_payments(self):
        for args in ((), ("1234.56",)):
            with self.subTest(args=args):
                table = run_script("inverse_loan.py", *args)["table"]
                checked = 0
                for values in zip(*table.values()):
                    row = dict(zip(table, values))
                    if row["Ans"] == "-":
                        continue
                    total_payments = row["Mois"] * row["Mensualité"]
                    self.assertAlmostEqual(
                        row["Total"], total_payments, delta=Decimal("0.01"), msg=row
                    )
                    self.assertAlmostEqual(
                        row["Capital"] + row["Intérêts"],
                        total_payments,
                        delta=Decimal("0.01"),
                        msg=row,
                    )
                    checked += 1
                self.assertEqual(checked, 90)


def run_script(filename, *args):
    path = Path(__file__).parent / filename
    with patch.object(sys, "argv", [str(path), *args]):
        with contextlib.redirect_stdout(io.StringIO()):
            return runpy.run_path(str(path))


if __name__ == "__main__":
    unittest.main()
