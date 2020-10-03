#!/usr/bin/env python3

import argparse
import pathlib
import sys

from exitstatus import ExitStatus

from dck_problem1.fixed_width_file_helper import generate_fwf_file
from dck_problem1.spec_file_loader import load_fwf_spec_file


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gererates fixed width file based on given spec and number of lines.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--spec_file", type=pathlib.Path, required=True, help="Fixed width spec file path"
    )
    parser.add_argument(
        "--fwf_file", type=pathlib.Path, required=True, help="Output fixed width file path"
    )
    parser.add_argument("-n", type=int, required=True, help="Number of lines")
    return parser.parse_args()


def main() -> ExitStatus:
    """Accept arguments from the user, compute generate CSV file, and display the results."""
    args = parse_args()

    fwf_spec = load_fwf_spec_file(args.spec_file)
    generate_fwf_file(fwf_spec, args.n, args.fwf_file)

    print(f"Fixed width file is generated : {args.fwf_file}")
    return ExitStatus.success


# Allow the script to be run standalone (useful during development in PyCharm).
if __name__ == "__main__":
    sys.exit(main())
