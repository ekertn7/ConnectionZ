"""Functions for export graph to JSON"""

import uuid
import json
from datetime import date, datetime
from connectionz.core.nodes import Nodes
from connectionz.core.edges import Edges
from connectionz.core.graph import Graph
from connectionz.exceptions.wrong_file_extension_exception import (
    WrongFileExtensionException)


def _convert_nodes_for_json(nodes: Nodes) -> dict:
    for identifier, attributes in nodes.items():
        for attr_key, attr_value in attributes.items():
            if isinstance(attr_value, (tuple, set)):
                nodes[identifier][attr_key] = list(nodes[identifier][attr_key])
            if isinstance(attr_value, (date, datetime)):
                nodes[identifier][attr_key] = str(nodes[identifier][attr_key])
    return nodes


def _convert_edges_for_json(edges: Edges, delimiter: str) -> dict:
    edges = {
        delimiter.join((node_l, node_r)): multiples
        for (node_l, node_r), multiples in edges.items()}
    for couple, multiples in edges.items():
        for identifier, attributes in multiples.items():
            for attr_key, attr_value in attributes.items():
                if isinstance(attr_value, (tuple, set)):
                    edges[couple][identifier][attr_key] = list(edges[couple][identifier][attr_key])
                if isinstance(attr_value, (date, datetime)):
                    edges[couple][identifier][attr_key] = str(edges[couple][identifier][attr_key])
    return edges


def _generate_edges_delimiter() -> str:
    return f'~{uuid.uuid4().hex}~'


def export_graph_to_json(graph: Graph, file_path: str) -> None:
    """Export graph to JSON, convert nodes and edges attributes (from set and
    tuple to list, from date and datetime to str)

    Parameters
    ----------
    graph
        DirectedGraph or UndirectedGraph object
    file_path
        Path to JSON file
    """

    file_extension = file_path.split('.')[-1]
    if file_extension != 'json':
        raise WrongFileExtensionException(received=file_extension, required='json')

    graph.calc_degree()
    graph.find_neighbors()

    edges_delimiter = _generate_edges_delimiter()

    data = {
        'graph_type': graph.check_type(),
        'edges_delimiter': edges_delimiter,
        'nodes': _convert_nodes_for_json(graph.nodes),
        'edges': _convert_edges_for_json(graph.edges, edges_delimiter)
    }

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
