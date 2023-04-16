from decimal import Decimal
from numbers import Number


def rdec(dec):
    return dec.quantize(Decimal("0.02"))


def dict_of_lists_to_list_of_dicts(dict_of_lists: dict[str, list]) -> list[dict]:
    if not dict_of_lists:
        return []
    return [dict(zip(dict_of_lists, t)) for t in zip(*dict_of_lists.values())]


def is_number(value) -> bool:
    return isinstance(value, Number) and not isinstance(value, bool)


def dict_of_lists_as_table(
    dict_: dict[str, list],
    max_length: int = 7,
) -> str:
    cols_alignment: dict[str, str] = {}
    for col, row in dict_.items():
        align: str = "l"  # Left by default.
        for value in row:
            if value is None:  # Ignore null values.
                continue
            if is_number(value):
                align = "r"  # Numbers are aligned right.
            break
        cols_alignment[col] = align

    cols: list[str] = [str(x) for x in dict_]
    rows: list[dict] = dict_of_lists_to_list_of_dicts(dict_)

    if max_length != -1 and len(rows) > max_length:
        start: int = max_length // 2
        end: int = -max_length // 2
        placeholder: list[dict] = [{col: "..." for col in cols}]
        rows = rows[:start] + placeholder + rows[end:]

    cols_width: dict[str, int] = {col: len(str(col)) for col in cols}
    for row in rows:
        for col, value in row.items():
            cols_width[col] = max(cols_width[col], len(str(value)))

    out: str = ""

    def format_val(val, width: int, justify: str) -> str:
        if val is None:
            val = "n/a"
        if justify == "l":
            val = str(val).ljust(width)
        else:
            val = str(val).rjust(width)
        return " " + val + " "

    for col in cols:
        out += format_val(col, cols_width[col], cols_alignment[col])
    out += "\n"

    for col in cols:
        line = ""
        for letter in format_val(col, cols_width[col], cols_alignment[col]):
            line += " " if letter == " " else "-"
        out += line
    out += "\n"

    for row in rows:
        for col in cols:
            out += format_val(row[col], cols_width[col], cols_alignment[col])
        out += "\n"

    return str(out).rstrip()
