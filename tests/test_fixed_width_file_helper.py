import random as rnd
import string

import pytest

from dck_problem1.fixed_width_file_helper import (
    generate_fwf_file,
    generate_fwf_lines,
    parse_fwf_file,
)
from dck_problem1.models import FWFColumnSpec, FWFSpec


def __rnd_filename(ext, length=10) -> str:
    return "".join(rnd.choice(string.ascii_lowercase) for _ in range(length)) + ext


def test_generate_fwf_lines_line_length() -> None:
    # given number of lines and spec with header=False
    number_of_lines = 1
    spec = FWFSpec(
        [FWFColumnSpec("a", 0, 4), FWFColumnSpec("b", 4, 5), FWFColumnSpec("c", 9, 6)],
        False,
        "utf-8",
    )
    # when
    lines = list(generate_fwf_lines(spec, number_of_lines))

    # then
    assert len(lines) == number_of_lines, "number of lines should be correct"
    assert len(lines[0]) == 15, "lines length should be equal to a total length of all columns"


def test_generate_fwf_lines_header() -> None:
    # given number of lines and spec with header=True
    number_of_lines = 1
    spec = FWFSpec(
        [FWFColumnSpec("a", 0, 4), FWFColumnSpec("b", 4, 5), FWFColumnSpec("c", 9, 6)],
        True,
        "utf-8",
    )

    # when lines generator is called
    lines = list(generate_fwf_lines(spec, number_of_lines))

    # then
    assert len(lines) == number_of_lines + 1, "number of lines should be correct"
    assert lines[0] == "a   b    c     ", "header should be present"


def test_generate_fwf_lines() -> None:
    # given number of lines and spec with header=True
    number_of_lines = 2
    spec = FWFSpec(
        [FWFColumnSpec("a", 0, 4), FWFColumnSpec("b", 4, 5), FWFColumnSpec("c", 9, 6)],
        False,
        "utf-8",
    )

    def values_generator(col: FWFColumnSpec):
        # return first letter of a column names col.length times
        return col.name[0] * col.length

    # when lines generator is called
    lines = list(generate_fwf_lines(spec, number_of_lines, values_generator))

    # then
    assert len(lines) == number_of_lines, "number of lines should be correct"
    assert lines[0] == "aaaabbbbbcccccc", "values in the line should be correct"
    assert lines[1] == "aaaabbbbbcccccc", "values in the line should be correct"


def test_generate_fwf_file(tmp_path) -> None:
    # given
    output_file = tmp_path / __rnd_filename(".txt")
    spec = FWFSpec([FWFColumnSpec("a", 0, 10)], False, "utf-8")

    # when
    generate_fwf_file(spec, 4, output_file, lambda col: "s" * col.length)

    # then
    with open(output_file) as f:
        lines = f.read()
    assert """ssssssssss\nssssssssss\nssssssssss\nssssssssss\n""" == lines


def test_generate_fwf_file_invalid_encoding(tmp_path) -> None:
    # given
    output_file = tmp_path / __rnd_filename(".txt")

    spec = FWFSpec([FWFColumnSpec("a", 0, 5)], False, "windows-1252")

    # then expect an excpetion
    with pytest.raises(UnicodeEncodeError):
        # when
        # windows-1252 unsupported character
        generate_fwf_file(spec, 1, output_file, lambda col: "Mořic")


def test_parser_fwf_file_utf_8(tmp_path) -> None:
    # given
    number_of_lines = 10
    fwf_file = tmp_path / __rnd_filename(".txt")
    with open(fwf_file, "w") as f:
        f.writelines(("aaa bbbb ccccc    ddddd   eeee\n" for _ in range(number_of_lines)))
    spec = FWFSpec(
        [
            FWFColumnSpec("a", 0, 4),
            FWFColumnSpec("b", 4, 5),
            FWFColumnSpec("c", 9, 9),
            FWFColumnSpec("d", 18, 8),
            FWFColumnSpec("e", 26, 4),
        ],
        False,
        "utf-8",
    )
    # when
    lines = list(parse_fwf_file(spec, fwf_file))

    # then
    assert len(lines) == number_of_lines
    assert list(lines[0]) == ["aaa", "bbbb", "ccccc", "ddddd", "eeee"]
    assert list(lines[1]) == ["aaa", "bbbb", "ccccc", "ddddd", "eeee"]


def test_pasrse_fwf_file_utf_16(tmp_path) -> None:
    # given
    number_of_lines = 1
    fwf_file = tmp_path / __rnd_filename(".txt")
    with open(fwf_file, "w", encoding="utf-16") as f:
        f.writelines(("wyjście bbbb\n" for _ in range(number_of_lines)))
    spec = FWFSpec(
        [FWFColumnSpec("a", 0, 8), FWFColumnSpec("b", 8, 4)],
        False,
        "utf-16",
    )
    # when
    lines = list(parse_fwf_file(spec, fwf_file))

    # then
    assert len(lines) == number_of_lines
    assert list(lines[0]) == ["wyjście", "bbbb"]
