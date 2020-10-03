import random as rnd
import string

from dck_problem1.models import FWFColumnSpec


def __rnd_str(length=1) -> str:
    return "".join(rnd.choice(string.ascii_lowercase) for _ in range(length))


def __rnd_fwf_str(column_spec: FWFColumnSpec) -> str:
    return __rnd_str(column_spec.length)


__RND_VALUES_GENERATOR_BY_TYPE = {
    "str": __rnd_fwf_str,
}


def __unexpected_data_type(column_spec: FWFColumnSpec):
    raise ValueError(f"Unexpected datatype {column_spec.dtype} for column {column_spec.name}")


def rnd_fwf_value(column_spec: FWFColumnSpec) -> str:
    """Generates random value according to fixed width column spec

    Args:
        column_spec (FWFColumnSpec): columns spec

    Returns:
        str: random string
    """
    rnd_generator = __RND_VALUES_GENERATOR_BY_TYPE.get(column_spec.dtype, __unexpected_data_type)
    return rnd_generator(column_spec)
