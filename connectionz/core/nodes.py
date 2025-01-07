"""Type alias for nodes"""

from typing import TypeAlias, Any
from connectionz.core.identifier import Identifier


Nodes: TypeAlias = dict[Identifier, Any]
