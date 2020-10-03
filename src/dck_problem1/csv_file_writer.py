import csv
import pathlib
from typing import Any, Iterator

from dck_problem1.models import CSVSpec


def write_csv_file(spec: CSVSpec, lines: Iterator[Iterator[Any]], csv_output_file: pathlib.Path):
    if csv_output_file.parent:
        csv_output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_output_file, "w", newline="", encoding=spec.encoding) as f:
        writer = csv.writer(f, delimiter=spec.delimiter, quotechar=spec.quotechar)
        writer.writerows(lines)
