import codecs
import dataclasses
from itertools import accumulate
from typing import ClassVar, List

from marshmallow import Schema, ValidationError, fields, post_load, validate, validates_schema
from marshmallow.decorators import validates


@dataclasses.dataclass
class FWFColumnSpec:
    """Fixed Width File Column specification"""

    name: str
    offset: int
    length: int
    dtype: str = "str"


@dataclasses.dataclass
class FWFSpec:
    """Fixed Width File specification"""

    columns: List[FWFColumnSpec]
    header: bool
    encoding: str


@dataclasses.dataclass
class CSVSpec:
    """CSV file specification"""

    column_names: List[str]
    header: bool
    encoding: str
    delimiter: str = ","
    quotechar = '"'


class FWFSpecSchema(Schema):
    __COLUMN_NAMES_MAX_LEN: ClassVar[int] = 128
    __OFFSETS_MAX_LEN: ClassVar[int] = 128
    __COLUMN_MAX_LEN: ClassVar[int] = 128

    header = fields.Boolean(data_key="IncludeHeader", required=True)

    encoding = fields.Str(data_key="FixedWidthEncoding", required=True)

    column_lengths = fields.List(
        fields.Int(validate=validate.Range(min=1, max=__COLUMN_MAX_LEN)),
        data_key="Offsets",
        required=True,
        validate=validate.Length(min=1, max=__OFFSETS_MAX_LEN),
    )

    column_names = fields.List(
        fields.Str(),
        data_key="ColumnNames",
        required=True,
        validate=validate.Length(min=1, max=__COLUMN_NAMES_MAX_LEN),
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if len(data["column_names"]) != len(data["column_lengths"]):
            raise ValidationError("Offsets length must be the same as ColumnNames length")

    @validates("encoding")
    def validate_encoding(self, encoding, **kwargs):
        try:
            codecs.lookup(encoding)
        except LookupError:
            raise ValidationError(f"Encoding {encoding} not found")

    @post_load
    def make_fwf_spec(self, data, **kwargs):
        # calculate collumn offsets, starts with 0
        column_offsets = [0] + list(accumulate(data["column_lengths"]))[:-1]
        # convert into a list of FixedWidthColumnSpec
        spec_values = zip(data["column_names"], column_offsets, data["column_lengths"])
        columns = [FWFColumnSpec(*col) for col in spec_values]
        return FWFSpec(header=data["header"], encoding=data["encoding"], columns=columns)


class CSVSpecSchema(Schema):
    __COLUMN_NAMES_MAX_LEN: ClassVar[int] = 128
    header = fields.Boolean(data_key="IncludeHeader", required=True)
    encoding = fields.Str(data_key="DelimitedEncoding", required=True)
    column_names = fields.List(
        fields.Str(),
        data_key="ColumnNames",
        required=True,
        validate=validate.Length(min=1, max=__COLUMN_NAMES_MAX_LEN),
    )

    @validates("encoding")
    def validate_encoding(self, encoding, **kwargs):
        try:
            codecs.lookup(encoding)
        except LookupError:
            raise ValidationError(f"Encoding {encoding} not found")

    @post_load
    def make_csv_spec(self, data, **kwargs):
        return CSVSpec(**data)
