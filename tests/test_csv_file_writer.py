# import pytest
import random as rnd
import string

import pytest

from dck_problem1.csv_file_writer import write_csv_file
from dck_problem1.models import CSVSpec


def __rnd_filename(ext, length=10) -> str:
    return "".join(rnd.choice(string.ascii_lowercase) for _ in range(length)) + ext


@pytest.mark.parametrize(
    "header,output",
    [
        (
            False,
            """sssss,sssss\nsssss,sssss\nsssss,sssss\nsssss,sssss\n""",
        ),
        (
            True,
            """f1,f2\nsssss,sssss\nsssss,sssss\nsssss,sssss\nsssss,sssss\n""",
        ),
    ],
    ids=["test_write_csv_file_no_header", "test_write_csv_file_with_header"],
)
def test_write_csv_file(header, output, tmp_path) -> None:
    # given
    output_file = tmp_path / __rnd_filename(".txt")
    spec = CSVSpec(["f1", "f2"], header, "utf-8")
    lines = (("s" * 5 for _ in range(2)) for _ in range(4))

    # when
    write_csv_file(spec, lines, output_file)

    # then
    with open(output_file) as f:
        csv_output = f.read()
    assert csv_output == output
