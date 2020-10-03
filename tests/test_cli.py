# import pytest
import random as rnd
import string
import sys

import dck_problem1.csv_cli as csv_cli
import dck_problem1.fwf_cli as fwf_cli


def __rnd_filename(ext, length=10) -> str:
    return "".join(rnd.choice(string.ascii_lowercase) for _ in range(length)) + ext


def test_fwf_cli(tmp_path) -> None:
    # given
    fwf_file = tmp_path / __rnd_filename(".txt")
    number_of_lines = 10
    sys.argv[1:] = [
        "--spec_file",
        "tests/resources/spec.json",
        "--fwf_file",
        str(fwf_file),
        "-n",
        str(number_of_lines),
    ]

    # when
    fwf_cli.main()

    # then
    with open(fwf_file) as f:
        lines = f.readlines()
    # number of lines + header
    assert len(lines) == number_of_lines + 1


def test_csv_cli(tmp_path) -> None:
    # given
    csv_file = tmp_path / __rnd_filename(".csv")
    sys.argv[1:] = [
        "--spec_file",
        "tests/resources/spec.json",
        "--fwf_file",
        "tests/resources/test_fwf.txt",
        "--csv_file",
        str(csv_file),
    ]

    # when
    csv_cli.main()

    # then
    with open(csv_file) as f:
        lines = f.readlines()
    assert len(lines) == 3
