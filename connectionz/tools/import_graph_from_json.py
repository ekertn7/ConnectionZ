"""Functions for import graph from JSON"""

import sys
import json
from connectionz.core.nodes import Nodes
from connectionz.core.edges import Edges
from connectionz.core.graph import Graph
from connectionz.exceptions.wrong_file_extension_exception import (
    WrongFileExtensionException)


def _convert_nodes_from_json(nodes: dict) -> Nodes:
    for identifier, attributes in nodes.items():
        for attr_key, attr_value in attributes.items():
            if isinstance(attr_value, (list)) and attr_key == 'neighbors':
                nodes[identifier][attr_key] = set(nodes[identifier][attr_key])
    return nodes


def _convert_edges_from_json(edges: dict, delimiter: str) -> Edges:
    edges = {
        tuple(couple.split(delimiter)): multiples
        for couple, multiples in edges.items()}
    return edges


def import_graph_from_json(file_path: str) -> Graph:
    """Import graph from JSON, convert node attribute neighbors from list to set

    Parameters
    ----------
    file_path
        Path to JSON file

    Returns
    -------
        DirectedGraph or UndirectedGraph object
    """

    file_extension = file_path.split('.')[-1]
    if file_extension != 'json':
        raise WrongFileExtensionException(received=file_extension, required='json')

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    graph = getattr(sys.modules['connectionz.core'], data['graph_type'])

    return graph(
        nodes = _convert_nodes_from_json(data['nodes']),
        edges = _convert_edges_from_json(data['edges'], data['edges_delimiter']))
