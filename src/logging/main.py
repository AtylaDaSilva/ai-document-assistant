import pprint
from typing import Any


def flog(
    obj: Any,
    indent: int = 1,
    width: int = 80,
    depth: int | None = None,
    compact: bool = False,
    sort_dicts: bool = True,
    underscore_numbers: bool = False
):
    """Returns a string of *obj* formatted for logging

    @see https://docs.python.org/3/library/pprint.html#pprint.PrettyPrinter for a list of parameters
    """
    pp = pprint.PrettyPrinter(
        indent=indent,
        width=width,
        depth=depth,
        compact=compact,
        sort_dicts=sort_dicts,
        underscore_numbers=underscore_numbers
    )
    return pp.pformat(obj)