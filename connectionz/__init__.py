"""Main init"""

from . core import (
    # identifier
    Identifier, generate_identifier,
    # nodes and edges type alias
    Nodes, Edges,
    # abstract class
    Graph,
    # classes
    DirectedGraph,
    UndirectedGraph)
from . algorithms import *
from . tools import (
    # graph to/from json
    export_graph_to_json,
    import_graph_from_json)
from . exceptions import (
    # object already exists exceptions
    NodeAlreadyExistsException,
    EdgeAlreadyExistsException,
    # object is not exists exceptions
    NodeIsNotExistsException,
    CoupleIsNotExistsException,
    EdgeIsNotExistsException,
    # can not delete basic elements exceptions
    CanNotDeleteNodesException,
    CanNotDeleteEdgesException,
    # validation exceptions
    WrongTypeOfNodesException,
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfNodeAttributesException,
    WrongTypeOfEdgesException,
    WrongTypeOfCoupleException,
    WrongLengthOfCoupleException,
    WrongTypeOfNodeIdentifierInCoupleException,
    WrongTypeOfMultipleEdgesException,
    WrongLengthOfMultipleEdgesException,
    WrongTypeOfEdgeIdentifierException,
    WrongTypeOfEdgeAttributesException,
    DuplicationInEdgeIdentifiersException,
    # wrong file extension exception
    WrongFileExtensionException,)
