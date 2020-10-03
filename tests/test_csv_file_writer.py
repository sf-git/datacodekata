# import pytest
import random as rnd
import string

from dck_problem1.csv_file_writer import write_csv_file
from dck_problem1.models import CSVSpec


def __rnd_filename(ext, length=10) -> str:
    return "".join(rnd.choice(string.ascii_lowercase) for _ in range(length)) + ext


def test_write_csv_file(tmp_path) -> None:
    # given
    output_file = tmp_path / __rnd_filename(".txt")
    spec = CSVSpec(["f1", "f2"], True, "utf-8")
    lines = (("s" * 5 for _ in range(2)) for _ in range(4))

    # when
    write_csv_file(spec, lines, output_file)

    # then
    with open(output_file) as f:
        output = f.read()
    assert """sssss,sssss\nsssss,sssss\nsssss,sssss\nsssss,sssss\n""" == output
