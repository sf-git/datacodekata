#!/usr/bin/env python3

import argparse
import pathlib
import sys

from exitstatus import ExitStatus

from dck_problem1.csv_file_writer import write_csv_file
from dck_problem1.fixed_width_file_helper import parse_fwf_file
from dck_problem1.spec_file_loader import load_csv_spec_file, load_fwf_spec_file


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gererates CSV file based on given Fixed width file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--spec_file", type=pathlib.Path, required=True, help="Fixed width and CSV spec file path"
    )
    parser.add_argument(
        "--fwf_file", type=pathlib.Path, required=True, help="Fixed width data file path"
    )
    parser.add_argument(
        "--csv_file", type=pathlib.Path, required=True, help="Output CSV file path"
    )
    return parser.parse_args()


def main() -> ExitStatus:
    """Accept arguments from the user, compute generate CSV file, and display the results."""
    args = parse_args()

    fwf_spec = load_fwf_spec_file(args.spec_file)
    csv_spec = load_csv_spec_file(args.spec_file)
    lines = parse_fwf_file(fwf_spec, args.fwf_file)
    write_csv_file(csv_spec, lines, args.csv_file)

    print(f"CSV file is generated : {args.csv_file}")

    return ExitStatus.success


# Allow the script to be run standalone (useful during development in PyCharm).
if __name__ == "__main__":
    sys.exit(main())
