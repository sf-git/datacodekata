import pathlib

from dck_problem1.models import CSVSpec, CSVSpecSchema, FWFSpec, FWFSpecSchema


def load_csv_spec_file(spec_path: pathlib.Path) -> CSVSpec:
    with open(spec_path, "r") as f:
        return load_csv_spec_json(f.read())


def load_csv_spec_json(spec_json: str) -> CSVSpec:
    """Loads CSV file spec from json string
       Uses marchmallow package to parse json

    Args:
        spec_json (str): json string

    Returns:
        CSVSpec: CSV file spec
    """
    schema = CSVSpecSchema(unknown="EXCLUDE")
    return schema.loads(spec_json)


def load_fwf_spec_file(spec_path: pathlib.Path) -> FWFSpec:
    with open(spec_path, "r") as f:
        return load_fwf_spec_json(f.read())


def load_fwf_spec_json(spec_json: str) -> FWFSpec:
    """Loads Fixed Width File spec from json string.
       Uses marchmallow package to parse json

    Args:
        spec_json (str): json string

    Returns:
        FWFSpec: Fixed width file spec
    """
    schema = FWFSpecSchema(unknown="EXCLUDE")
    return schema.loads(spec_json)
