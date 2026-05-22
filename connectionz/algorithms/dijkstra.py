"""Dijkstra's algorithm implementation"""

from heapq import heappop, heappush
from connectionz.core.identifier import Identifier
from connectionz.core.graph import Graph
from connectionz.exceptions.object_isnot_exists_exceptions import (
    NodeIsNotExistsException,
    EdgeAttributeIsNotExistsException,
    PathBetweenNodesIsNotExistsException,
    PathBetweenSameNodeCanNotExistException)


def find_shortest_path(
        graph: Graph, source_node: Identifier, target_node: Identifier,
        weight_key: str = None) -> list[Identifier]:
    """Finding shortest path using Dijkstra's algorithm

    Parameters
    ----------
    graph
        DirectedGraph or UndirectedGraph object
    source_node
        Source node identifier
    target_node
        Target node identifier
    weight_key
        Weight key that is an edges identifier

    Returns
    -------
        List with node identifiers representing the shortest path between
        `source_node` and `target_node`

    Raises
    ------
    NodeIsNotExistsException
        If node is not exist in the graph
    EdgeAttributeIsNotExistsException
        If edge attribute passed in the `weight_key` parameter is not exist
    PathBetweenNodesIsNotExistsException
        If path between `source_node` and `target_node` is not exist
    PathBetweenSameNodeCanNotExistException
        If `source_node` and `target_node` are the same (have the same identifier)
    """

    visited_nodes, _ = _dijkstra(
        graph=graph, source_node=source_node, target_node=target_node,
        weight_key=weight_key)

    current_node = target_node
    result = []
    while current_node != source_node:
        result.append(current_node)
        try:
            current_node = visited_nodes[current_node]
        except KeyError:
            raise PathBetweenNodesIsNotExistsException(source_node, target_node) from None
    result.append(current_node)

    return result[::-1]


def find_shortest_distance(
        graph: Graph, source_node: Identifier, target_node: Identifier,
        weight_key: str = None) -> float:
    """Finding shortest distance using Dijkstra's algorithm

    Parameters
    ----------
    graph
        DirectedGraph or UndirectedGraph object
    source_node
        Source node identifier
    target_node
        Target node identifier
    weight_key
        Weight key that is an edges identifier

    Returns
    -------
        A number representing the shortest distance between `source_node` and
        `target_node`

    Raises
    ------
    NodeIsNotExistsException
        If node is not exist in the graph
    EdgeAttributeIsNotExistsException
        If edge attribute passed in the `weight_key` parameter is not exist
    PathBetweenNodesIsNotExistsException
        If path between `source_node` and `target_node` is not exist
    PathBetweenSameNodeCanNotExistException
        If `source_node` and `target_node` are the same (have the same identifier)
    """

    _, distance_to_nodes = _dijkstra(
        graph=graph, source_node=source_node, target_node=target_node,
        weight_key=weight_key)

    try:
        distance_to_target_node = distance_to_nodes[target_node]
    except KeyError:
        raise PathBetweenNodesIsNotExistsException(source_node, target_node) from None

    return distance_to_target_node


def _dijkstra(
        graph: Graph, source_node: Identifier, target_node: Identifier,
        weight_key: str
    ) -> tuple[dict[Identifier, Identifier | None], dict[Identifier, float]]:
    """Dijkstra's algorithm implementation

    Parameters
    ----------
    graph
        DirectedGraph or UndirectedGraph object
    source_node
        Source node identifier
    target_node
        Target node identifier
    weight_key
        Weight key that is an edges identifier

    Returns
    -------
        Tuple with:
            - Dict with:
                - keys: node identifier
                - values: nearest node identifier
            - Dict with:
                - keys: node identifier
                - values: number (int or float) representing the shortest
                  distance between current and nearest node
    """

    if not graph.has_node(source_node) or not graph.has_node(target_node):
        raise NodeIsNotExistsException()

    if source_node == target_node:
        raise PathBetweenSameNodeCanNotExistException()

    graph.find_neighbors()

    queue = []
    heappush(queue, (source_node, 0))
    distance_to_nodes = {source_node: 0}
    visited_nodes = {source_node: None}

    while queue:
        current_node, _ = heappop(queue)

        if current_node == target_node:
            break

        if weight_key is not None:
            # ['A', 'B'] -> [('A', 3), ('B', 5)]
            next_nodes = []
            for neighbor_node in graph.nodes[current_node]['neighbors']:
                try:
                    weight = min(
                        multiples[weight_key]
                        for multiples in graph.edges[
                            graph.couple_representation((current_node, neighbor_node))].values())
                except KeyError:
                    raise EdgeAttributeIsNotExistsException(attribute=weight_key) from None
                next_nodes.append((neighbor_node, weight))
        else:
            # ['A', 'B'] -> [('A', 1), ('B', 1)]
            next_nodes = [(node, 1) for node in graph.nodes[current_node]['neighbors']]

        for next_node in next_nodes:
            neighbor_node, neighbor_cost = next_node
            new_cost =  distance_to_nodes[current_node] + neighbor_cost
            if neighbor_node not in distance_to_nodes or \
                    new_cost < distance_to_nodes[neighbor_node]:
                heappush(queue, (neighbor_node, new_cost))
                distance_to_nodes[neighbor_node] = new_cost
                visited_nodes[neighbor_node] = current_node

    return visited_nodes, distance_to_nodes
