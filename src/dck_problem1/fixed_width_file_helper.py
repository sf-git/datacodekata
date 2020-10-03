from itertools import chain
import pathlib
from typing import Any, Callable, Iterator

from dck_problem1.models import FWFColumnSpec, FWFSpec
from dck_problem1.random_values_generator import rnd_fwf_value


def __create_fwf_header(spec: FWFSpec) -> str:
    header = ""
    for col in spec.columns:
        header += col.name.ljust(col.length, " ")
    return header


def __generate_fwf_lines(
    spec: FWFSpec, number_of_lines: int, rnd_value_generator: Callable[[FWFColumnSpec], str]
) -> Iterator[str]:
    for _ in range(number_of_lines):
        line = ""
        for col in spec.columns:
            line += rnd_value_generator(col)
        yield line


def generate_fwf_lines(
    spec: FWFSpec,
    number_of_lines: int,
    rnd_value_generator: Callable[[FWFColumnSpec], str] = rnd_fwf_value,
) -> Iterator[str]:
    if number_of_lines <= 0:
        raise ValueError("number_of_lines should be > 0")
    rows_generator = __generate_fwf_lines(spec, number_of_lines, rnd_value_generator)
    if spec.header:
        return chain([__create_fwf_header(spec)], rows_generator)
    else:
        return rows_generator


def generate_fwf_file(
    spec: FWFSpec,
    number_of_lines: int,
    output_file: pathlib.Path,
    rnd_value_generator: Callable[[FWFColumnSpec], str] = rnd_fwf_value,
) -> None:
    if output_file.parent:
        output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", 1024, encoding=spec.encoding, newline="") as f:
        lines = generate_fwf_lines(spec, number_of_lines, rnd_value_generator)
        f.writelines((line + "\n" for line in lines))


def parse_fwf_file(
    spec: FWFSpec,
    input_file: pathlib.Path,
) -> Iterator[Iterator[Any]]:
    slices = [slice(col.offset, col.offset + col.length, None) for col in spec.columns]
    with open(input_file, "r", 1024, encoding=spec.encoding) as f:
        for line in f:
            yield (line[s].strip() for s in slices)
