"""Type alias for idetifier"""

from uuid import uuid4
from typing import TypeAlias


Identifier: TypeAlias = str


def generate_identifier() -> Identifier:
    """Returns uuid in fixed format"""
    return uuid4().hex
