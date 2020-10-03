from typing import List

import marshmallow
import pytest

from dck_problem1.spec_file_loader import load_csv_spec_json, load_fwf_spec_json


@pytest.mark.parametrize(
    "spec_json,colum_names,column_lengths,column_offsets,header,encoding",
    [
        (
            """{"ColumnNames":["f1","f2"],
             "Offsets":[3,4],
             "IncludeHeader":"True",
             "FixedWidthEncoding":"windows-1252"}""",
            ["f1", "f2"],
            [3, 4],
            [0, 3],
            True,
            "windows-1252",
        ),
        (
            """{"ColumnNames":["f1"],
             "Offsets":[5],
             "IncludeHeader":"False",
             "FixedWidthEncoding":"windows-1252"}""",
            ["f1"],
            [5],
            [0],
            False,
            "windows-1252",
        ),
    ],
)
def test_valid_fwf_spec(
    spec_json: str,
    colum_names: List[str],
    column_lengths: List[int],
    column_offsets: List[int],
    header: bool,
    encoding: str,
) -> None:
    # when spec parser is called
    spec = load_fwf_spec_json(spec_json)

    # then
    assert [col.name for col in spec.columns] == colum_names, "column names should match"
    assert [col.length for col in spec.columns] == column_lengths, "column lengths should match"
    assert [
        col.offset for col in spec.columns
    ] == column_offsets, "column offsets should be calculated correctly"
    assert spec.header == header, "headers should match"
    assert spec.encoding == encoding, "encodings should match"


@pytest.mark.parametrize(
    "spec_json,message",
    [
        (
            """{"ColumnNames":["f1","f2"],
                "Offsets":[3,4],
                "FixedWidthEncoding":"windows-1252"}""",
            r".*?Missing data for required field.*",
        ),
        (
            """{"ColumnNames":["f1"],
                 "Offsets":[5],
                 "IncludeHeader":"True"}""",
            r".*?Missing data for required field.*",
        ),
        (
            """{"ColumnNames":[],
                 "Offsets":[5],
                 "IncludeHeader":"True",
                 "FixedWidthEncoding":"windows-1252"}""",
            r".*?Length must be between 1 and 128.*?",
        ),
        (
            """{"ColumnNames":["f1"],
                 "Offsets":[],
                 "IncludeHeader":"True",
                 "FixedWidthEncoding":"windows-1252"}""",
            r".*?Length must be between 1 and 128.*",
        ),
        (
            """{"ColumnNames":["f1"],
                 "Offsets":[3,5],
                 "IncludeHeader":"True",
                 "FixedWidthEncoding":"windows-1252"} """,
            r".*?Offsets length must be the same as ColumnNames length.*",
        ),
        (
            """{"ColumnNames":["f1"],
              "Offsets":[3],
              "IncludeHeader":"True",
              "FixedWidthEncoding":"HHH"}""",
            r".*?Encoding HHH not found.*",
        ),
    ],
    ids=[
        'test missing "IncludeHeader"',
        'test missing "FixedWidthEncoding"',
        'test empty "ColumnNames"',
        'test empty "Offsets"',
        'test "ColumnNames" "Offsets" length mistmatch',
        'test incorrect "FixedWidthEncoding"',
    ],
)
def test_invalid_fwf_spec(spec_json: str, message: str) -> None:
    # then ValidattionError with message is expected
    with pytest.raises(marshmallow.ValidationError, match=message):
        # when parser is called
        load_fwf_spec_json(spec_json)


@pytest.mark.parametrize(
    "spec_json,colum_names,header,encoding",
    [
        (
            """{"ColumnNames":["f1","f2"],
             "IncludeHeader":"True",
             "DelimitedEncoding":"windows-1252"}""",
            ["f1", "f2"],
            True,
            "windows-1252",
        ),
        (
            """{"ColumnNames":["f1"],
             "IncludeHeader":"False",
             "DelimitedEncoding":"windows-1252"}""",
            ["f1"],
            False,
            "windows-1252",
        ),
    ],
)
def test_valid_csv_spec(
    spec_json: str,
    colum_names: List[str],
    header: bool,
    encoding: str,
) -> None:
    # when spec parser is called
    spec = load_csv_spec_json(spec_json)

    # then
    assert spec.column_names == colum_names, "column names should match"
    assert spec.header == header, "headers should match"
    assert spec.encoding == encoding, "encodings should match"


@pytest.mark.parametrize(
    "spec_json,message",
    [
        (
            """{"ColumnNames":["f1","f2"],
                "DelimitedEncoding":"windows-1252"}""",
            r".*?Missing data for required field.*",
        ),
        (
            """{"ColumnNames":["f1"],
                 "IncludeHeader":"True"}""",
            r".*?Missing data for required field.*",
        ),
        (
            """{"ColumnNames":[],
                 "IncludeHeader":"True",
                 "DelimitedEncoding":"windows-1252"}""",
            r".*?Length must be between 1 and 128.*?",
        ),
        (
            """{"ColumnNames":["f1"],
              "IncludeHeader":"True",
              "DelimitedEncoding":"HHH"}""",
            r".*?Encoding HHH not found.*",
        ),
    ],
    ids=[
        'test missing "IncludeHeader"',
        'test missing "DelimitedEncoding"',
        'test empty "ColumnNames"',
        'test incorrect "DelimitedEncoding"',
    ],
)
def test_invalid_csv_spec(spec_json: str, message: str) -> None:
    # then ValidattionError with message is expected
    with pytest.raises(marshmallow.ValidationError, match=message):
        # when parser is called
        load_csv_spec_json(spec_json)
