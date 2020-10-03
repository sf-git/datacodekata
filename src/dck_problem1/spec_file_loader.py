import pathlib

from dck_problem1.models import CSVSpec, CSVSpecSchema, FWFSpec, FWFSpecSchema


def load_csv_spec_file(spec_path: pathlib.Path) -> CSVSpec:
    with open(spec_path, "r") as f:
        return load_csv_spec_json(f.read())


def load_csv_spec_json(spec_json: str) -> CSVSpec:
    schema = CSVSpecSchema(unknown="EXCLUDE")
    return schema.loads(spec_json)


def load_fwf_spec_file(spec_path: pathlib.Path) -> FWFSpec:
    with open(spec_path, "r") as f:
        return load_fwf_spec_json(f.read())


def load_fwf_spec_json(spec_json: str) -> FWFSpec:
    schema = FWFSpecSchema(unknown="EXCLUDE")
    return schema.loads(spec_json)
