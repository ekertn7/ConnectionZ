"""Tests of `find_shortest_path` and `find_shortest_distance` functions"""

import pytest
from connectionz import (
    DirectedGraph, UndirectedGraph,
    find_shortest_path, find_shortest_distance)
from connectionz.exceptions import (
    NodeIsNotExistsException,
    EdgeAttributeIsNotExistsException,
    PathBetweenNodesIsNotExistsException,
    PathBetweenSameNodeCanNotExistException)


edges = [
    ('A', 'B', {'distance': 14}),
    ('A', 'B', {'distance': 6}),
    ('B', 'C', {'distance': 18}),
    ('B', 'C', {'distance': 11}),
    ('C', 'D', {'distance': 19}),
    ('B', 'E', {'distance': 7}),
    ('E', 'F', {'distance': 3}),
    ('G', 'F', {'distance': 12}),
    ('P', 'J', {'distance': 17})]


@pytest.fixture(scope='class', autouse=False, name='directed_graph')
def create_directed_graph():
    """
         14       18
         6        11       19
    [A] ===> [B] ===> [C] ---> [D]
              |                              17
              | 7                       [P] ---> [J]
              v
             [E] ---> [F] <--- [G]
                  3        12

    exists:
        A - B = AB   = 6
        A - C = ABC  = 17
        A - D = ABCD = 36
        A - E = ABE  = 13
        A - F = ABEF = 16
        B - C = BC   = 11
        B - D = BCD  = 30
        B - E = BE   = 7
        B - F = BEF  = 10
        C - D = CD   = 19
        E - F = EF   = 3
        G - F = GF   = 12
        P - J = PJ   = 17

    not exists:
        A - G   A - P   A - J
        B - A   B - G   B - P   B - J
        C - B   C - A   C - E   C - F   C - G   C - P   C - J
        D - C   D - B   D - A   D - E   D - F   D - G   D - P   D - J
        E - G   E - B   E - A   E - C   E - D   E - P   E - J
        F - G   F - E   F - B   F - A   F - C   F - D   F - P   F - J
        G - E   G - B   G - A   G - C   G - D   G - P   G - J
        P - A   P - B   P - C   P - D   P - E   P - F   P - G
        J - A   J - B   J - C   J - D   J - E   J - F   J - G
    """
    graph = DirectedGraph()

    for node_l, node_r, attributes in edges:
        graph.add_edge(node_l, node_r, **attributes)

    return graph


@pytest.fixture(scope='class', autouse=False, name='undirected_graph')
def create_undirected_graph():
    """
         14       18
         6        11       19
    [A] ==== [B] ==== [C] ---- [D]
              |                              17
              | 7                       [P] ---- [J]
              |
             [E] ---- [F] ---- [G]
                  3        12

    exists:
        A - B = AB     = 6
        A - C = ABC    = 17
        A - D = ABCD   = 36
        A - E = ABE    = 13
        A - F = ABEF   = 16
        A - G = ABEFG  = 28
        B - A = BA     = 6
        B - C = BC     = 11
        B - D = BCD    = 30
        B - E = BE     = 7
        B - F = BEF    = 10
        B - G = BEFG   = 22
        C - D = CD     = 19
        C - B = CB     = 11
        C - A = CBA    = 17
        C - E = CBE    = 18
        C - F = CBEF   = 21
        C - G = CBEFG  = 33
        D - C = DC     = 19
        D - B = DCB    = 30
        D - A = DCBA   = 36
        D - E = DCBE   = 37
        D - F = DCBEF  = 40
        D - G = DCBEFG = 52
        E - F = EF     = 3
        E - G = EFG    = 15
        E - B = EB     = 7
        E - A = EBA    = 13
        E - C = EBC    = 18
        E - D = EBCD   = 37
        F - G = FG     = 12
        F - E = FE     = 3
        F - B = FEB    = 10
        F - A = FEBA   = 16
        F - C = FEBC   = 21
        F - D = FEBCD  = 40
        G - F = GF     = 12
        G - E = GFE    = 15
        G - B = GFEB   = 22
        G - A = GFEBA  = 28
        G - C = GFEBC  = 33
        G - D = GFEBCD = 52
        P - J = PJ     = 17
        J - P = JP     = 17

    not exists:
        A - P   A - J
        B - P   B - J
        C - P   C - J
        D - P   D - J
        E - P   E - J
        F - P   F - J
        G - P   G - J
        P - A   P - B   P - C   P - D   P - E   P - F   P - G
        J - A   J - B   J - C   J - D   J - E   J - F   J - G
    """
    graph = UndirectedGraph()

    for node_l, node_r, attributes in edges:
        graph.add_edge(node_l, node_r, **attributes)

    return graph


@pytest.mark.usefixtures('directed_graph')
class TestsFindShortestPathInDirectedGraph:
    """Tests of `find_shortest_path` function on DirectedGraph"""

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'G'), ('A', 'P'), ('A', 'J'),
         ('B', 'A'), ('B', 'G'), ('B', 'P'), ('B', 'J'),
         ('C', 'B'), ('C', 'A'), ('C', 'E'), ('C', 'F'), ('C', 'G'), ('C', 'P'), ('C', 'J'),
         ('D', 'C'), ('D', 'B'), ('D', 'A'), ('D', 'E'), ('D', 'F'), ('D', 'G'), ('D', 'P'), ('D', 'J'),
         ('E', 'G'), ('E', 'B'), ('E', 'A'), ('E', 'C'), ('E', 'D'), ('E', 'P'), ('E', 'J'),
         ('F', 'G'), ('F', 'E'), ('F', 'B'), ('F', 'A'), ('F', 'C'), ('F', 'D'), ('F', 'P'), ('F', 'J'),
         ('G', 'E'), ('G', 'B'), ('G', 'A'), ('G', 'C'), ('G', 'D'), ('G', 'P'), ('G', 'J'),
         ('P', 'A'), ('P', 'B'), ('P', 'C'), ('P', 'D'), ('P', 'E'), ('P', 'F'), ('P', 'G'),
         ('J', 'A'), ('J', 'B'), ('J', 'C'), ('J', 'D'), ('J', 'E'), ('J', 'F'), ('J', 'G'),])
    def test_exception_path_between_nodes_is_not_exists(self, directed_graph, source, target):
        """Trying to find the shortest path if there is no path between nodes
            - expected raise PathBetweenNodesIsNotExistsException
        """
        with pytest.raises(PathBetweenNodesIsNotExistsException):
            find_shortest_path(directed_graph, source, target)

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
         ('F', 'F'), ('G', 'G'), ('P', 'P'), ('J', 'J'),])
    def test_exception_path_between_same_node_can_not_exist(self, directed_graph, source, target):
        """Trying to find the shortest path between the same node
            - expected raise PathBetweenSameNodeCanNotExistException
        """
        with pytest.raises(PathBetweenSameNodeCanNotExistException):
            find_shortest_path(directed_graph, source, target)

    def test_exception_node_is_not_exists(self, directed_graph):
        """Trying to find the shortest path if specified node is not exist
            - expected raise NodeIsNotExistsException
        """
        with pytest.raises(NodeIsNotExistsException):
            find_shortest_path(directed_graph, 'A', 'W')  # node "W" is not exists

    def test_exception_edge_attribute_is_not_exists(self, directed_graph):
        """Trying to find the shortest path if edge attribute passed
        in the "weight_key" parameter is not exist
            - expected raise EdgeAttributeIsNotExistsException
        """
        with pytest.raises(EdgeAttributeIsNotExistsException):
            find_shortest_path(
                directed_graph, 'A', 'D',
                weight_key='non_existent')  # edge attribute "non_existent" is not exists

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', ['A', 'B']),
         ('A', 'C', ['A', 'B', 'C']),
         ('A', 'D', ['A', 'B', 'C', 'D']),
         ('A', 'E', ['A', 'B', 'E']),
         ('A', 'F', ['A', 'B', 'E', 'F']),
         ('B', 'C', ['B', 'C']),
         ('B', 'D', ['B', 'C', 'D']),
         ('B', 'E', ['B', 'E']),
         ('B', 'F', ['B', 'E', 'F']),
         ('C', 'D', ['C', 'D']),
         ('E', 'F', ['E', 'F']),
         ('G', 'F', ['G', 'F']),
         ('P', 'J', ['P', 'J']),])
    def test_default(self, directed_graph, source, target, result):
        """Successful shortest path search"""
        assert (find_shortest_path(directed_graph, source, target) == result
            and find_shortest_path(directed_graph, source, target, weight_key='distance') == result)


@pytest.mark.usefixtures('undirected_graph')
class TestsFindShortestPathInUndirectedGraph:
    """Tests of `find_shortest_path` function on UndirectedGraph"""

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'P'), ('A', 'J'),
         ('B', 'P'), ('B', 'J'),
         ('C', 'P'), ('C', 'J'),
         ('D', 'P'), ('D', 'J'),
         ('E', 'P'), ('E', 'J'),
         ('F', 'P'), ('F', 'J'),
         ('G', 'P'), ('G', 'J'),
         ('P', 'A'), ('P', 'B'), ('P', 'C'), ('P', 'D'), ('P', 'E'), ('P', 'F'), ('P', 'G'),
         ('J', 'A'), ('J', 'B'), ('J', 'C'), ('J', 'D'), ('J', 'E'), ('J', 'F'), ('J', 'G'),])
    def test_exception_path_between_nodes_is_not_exists(self, undirected_graph, source, target):
        """Trying to find the shortest path if there is no path between nodes
            - expected raise PathBetweenNodesIsNotExistsException
        """
        with pytest.raises(PathBetweenNodesIsNotExistsException):
            find_shortest_path(undirected_graph, source, target)

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
         ('F', 'F'), ('G', 'G'), ('P', 'P'), ('J', 'J'),])
    def test_exception_path_between_same_node_can_not_exist(self, undirected_graph, source, target):
        """Trying to find the shortest path between the same node
            - expected raise PathBetweenSameNodeCanNotExistException
        """
        with pytest.raises(PathBetweenSameNodeCanNotExistException):
            find_shortest_path(undirected_graph, source, target)

    def test_exception_node_is_not_exists(self, undirected_graph):
        """Trying to find the shortest path if specified node is not exist
            - expected raise NodeIsNotExistsException
        """
        with pytest.raises(NodeIsNotExistsException):
            find_shortest_path(undirected_graph, 'A', 'W')  # node "W" is not exists

    def test_exception_edge_attribute_is_not_exists(self, undirected_graph):
        """Trying to find the shortest path if edge attribute passed
        in the "weight_key" parameter is not exist
            - expected raise EdgeAttributeIsNotExistsException
        """
        with pytest.raises(EdgeAttributeIsNotExistsException):
            find_shortest_path(
                undirected_graph, 'A', 'D',
                weight_key='non_existent')  # edge attribute "non_existent" is not exists

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', ['A', 'B']),
         ('A', 'C', ['A', 'B', 'C']),
         ('A', 'D', ['A', 'B', 'C', 'D']),
         ('A', 'E', ['A', 'B', 'E']),
         ('A', 'F', ['A', 'B', 'E', 'F']),
         ('A', 'G', ['A', 'B', 'E', 'F', 'G']),
         ('B', 'A', ['B', 'A']),
         ('B', 'C', ['B', 'C']),
         ('B', 'D', ['B', 'C', 'D']),
         ('B', 'E', ['B', 'E']),
         ('B', 'F', ['B', 'E', 'F']),
         ('B', 'G', ['B', 'E', 'F', 'G']),
         ('C', 'D', ['C', 'D']),
         ('C', 'B', ['C', 'B']),
         ('C', 'A', ['C', 'B', 'A']),
         ('C', 'E', ['C', 'B', 'E']),
         ('C', 'F', ['C', 'B', 'E', 'F']),
         ('C', 'G', ['C', 'B', 'E', 'F', 'G']),
         ('D', 'C', ['D', 'C']),
         ('D', 'B', ['D', 'C', 'B']),
         ('D', 'A', ['D', 'C', 'B', 'A']),
         ('D', 'E', ['D', 'C', 'B', 'E']),
         ('D', 'F', ['D', 'C', 'B', 'E', 'F']),
         ('D', 'G', ['D', 'C', 'B', 'E', 'F', 'G']),
         ('E', 'F', ['E', 'F']),
         ('E', 'G', ['E', 'F', 'G']),
         ('E', 'B', ['E', 'B']),
         ('E', 'A', ['E', 'B', 'A']),
         ('E', 'C', ['E', 'B', 'C']),
         ('E', 'D', ['E', 'B', 'C', 'D']),
         ('F', 'G', ['F', 'G']),
         ('F', 'E', ['F', 'E']),
         ('F', 'B', ['F', 'E', 'B']),
         ('F', 'A', ['F', 'E', 'B', 'A']),
         ('F', 'C', ['F', 'E', 'B', 'C']),
         ('F', 'D', ['F', 'E', 'B', 'C', 'D']),
         ('G', 'F', ['G', 'F']),
         ('G', 'E', ['G', 'F', 'E']),
         ('G', 'B', ['G', 'F', 'E', 'B']),
         ('G', 'A', ['G', 'F', 'E', 'B', 'A']),
         ('G', 'C', ['G', 'F', 'E', 'B', 'C']),
         ('G', 'D', ['G', 'F', 'E', 'B', 'C', 'D']),
         ('P', 'J', ['P', 'J']),
         ('J', 'P', ['J', 'P']),])
    def test_default(self, undirected_graph, source, target, result):
        """Successful shortest path search"""
        assert (find_shortest_path(undirected_graph, source, target) == result
            and find_shortest_path(undirected_graph, source, target, weight_key='distance') == result)


@pytest.mark.usefixtures('directed_graph')
class TestsFindShortestDistanceInDirectedGraph:
    """Tests of `find_shortest_distance` function on DirectedGraph"""

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'G'), ('A', 'P'), ('A', 'J'),
         ('B', 'A'), ('B', 'G'), ('B', 'P'), ('B', 'J'),
         ('C', 'B'), ('C', 'A'), ('C', 'E'), ('C', 'F'), ('C', 'G'), ('C', 'P'), ('C', 'J'),
         ('D', 'C'), ('D', 'B'), ('D', 'A'), ('D', 'E'), ('D', 'F'), ('D', 'G'), ('D', 'P'), ('D', 'J'),
         ('E', 'G'), ('E', 'B'), ('E', 'A'), ('E', 'C'), ('E', 'D'), ('E', 'P'), ('E', 'J'),
         ('F', 'G'), ('F', 'E'), ('F', 'B'), ('F', 'A'), ('F', 'C'), ('F', 'D'), ('F', 'P'), ('F', 'J'),
         ('G', 'E'), ('G', 'B'), ('G', 'A'), ('G', 'C'), ('G', 'D'), ('G', 'P'), ('G', 'J'),
         ('P', 'A'), ('P', 'B'), ('P', 'C'), ('P', 'D'), ('P', 'E'), ('P', 'F'), ('P', 'G'),
         ('J', 'A'), ('J', 'B'), ('J', 'C'), ('J', 'D'), ('J', 'E'), ('J', 'F'), ('J', 'G'),])
    def test_exception_path_between_nodes_is_not_exists(self, directed_graph, source, target):
        """Trying to find the shortest distance if there is no path between nodes
            - expected raise PathBetweenNodesIsNotExistsException
        """
        with pytest.raises(PathBetweenNodesIsNotExistsException):
            find_shortest_distance(directed_graph, source, target)

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
         ('F', 'F'), ('G', 'G'), ('P', 'P'), ('J', 'J'),])
    def test_exception_path_between_same_node_can_not_exist(self, directed_graph, source, target):
        """Trying to find the shortest distance between the same node
            - expected raise PathBetweenSameNodeCanNotExistException
        """
        with pytest.raises(PathBetweenSameNodeCanNotExistException):
            find_shortest_distance(directed_graph, source, target)

    def test_exception_node_is_not_exists(self, directed_graph):
        """Trying to find the shortest distance if specified node is not exist
            - expected raise NodeIsNotExistsException
        """
        with pytest.raises(NodeIsNotExistsException):
            find_shortest_distance(directed_graph, 'A', 'W')  # node "W" is not exists

    def test_exception_edge_attribute_is_not_exists(self, directed_graph):
        """Trying to find the shortest distance if edge attribute passed
        in the "weight_key" parameter is not exist
            - expected raise EdgeAttributeIsNotExistsException
        """
        with pytest.raises(EdgeAttributeIsNotExistsException):
            find_shortest_distance(
                directed_graph, 'A', 'D',
                weight_key='non_existent')  # edge attribute "non_existent" is not exists

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', 1),
         ('A', 'C', 2),
         ('A', 'D', 3),
         ('A', 'E', 2),
         ('A', 'F', 3),
         ('B', 'C', 1),
         ('B', 'D', 2),
         ('B', 'E', 1),
         ('B', 'F', 2),
         ('C', 'D', 1),
         ('E', 'F', 1),
         ('G', 'F', 1),
         ('P', 'J', 1),])
    def test_default_without_weight_key(self, directed_graph, source, target, result):
        """Successful shortest distance search without weight key"""
        assert find_shortest_distance(directed_graph, source, target) == result

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', 6),
         ('A', 'C', 17),
         ('A', 'D', 36),
         ('A', 'E', 13),
         ('A', 'F', 16),
         ('B', 'C', 11),
         ('B', 'D', 30),
         ('B', 'E', 7),
         ('B', 'F', 10),
         ('C', 'D', 19),
         ('E', 'F', 3),
         ('G', 'F', 12),
         ('P', 'J', 17),])
    def test_default_with_weight_key(self, directed_graph, source, target, result):
        """Successful shortest distance search with weight key"""
        assert find_shortest_distance(directed_graph, source, target, weight_key='distance') == result


@pytest.mark.usefixtures('undirected_graph')
class TestsFindShortestDistanceInUndirectedGraph:
    """Tests of `find_shortest_distance` function on UndirectedGraph"""

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'P'), ('A', 'J'),
         ('B', 'P'), ('B', 'J'),
         ('C', 'P'), ('C', 'J'),
         ('D', 'P'), ('D', 'J'),
         ('E', 'P'), ('E', 'J'),
         ('F', 'P'), ('F', 'J'),
         ('G', 'P'), ('G', 'J'),
         ('P', 'A'), ('P', 'B'), ('P', 'C'), ('P', 'D'), ('P', 'E'), ('P', 'F'), ('P', 'G'),
         ('J', 'A'), ('J', 'B'), ('J', 'C'), ('J', 'D'), ('J', 'E'), ('J', 'F'), ('J', 'G'),])
    def test_exception_path_between_nodes_is_not_exists(self, undirected_graph, source, target):
        """Trying to find the shortest distance if there is no path between nodes
            - expected raise PathBetweenNodesIsNotExistsException
        """
        with pytest.raises(PathBetweenNodesIsNotExistsException):
            find_shortest_distance(undirected_graph, source, target)

    @pytest.mark.parametrize(
        ['source', 'target'],
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
         ('F', 'F'), ('G', 'G'), ('P', 'P'), ('J', 'J'),])
    def test_exception_path_between_same_node_can_not_exist(self, undirected_graph, source, target):
        """Trying to find the shortest distance between the same node
            - expected raise PathBetweenSameNodeCanNotExistException
        """
        with pytest.raises(PathBetweenSameNodeCanNotExistException):
            find_shortest_distance(undirected_graph, source, target)

    def test_exception_node_is_not_exists(self, undirected_graph):
        """Trying to find the shortest distance if specified node is not exist
            - expected raise NodeIsNotExistsException
        """
        with pytest.raises(NodeIsNotExistsException):
            find_shortest_distance(undirected_graph, 'A', 'W')  # node "W" is not exists

    def test_exception_edge_attribute_is_not_exists(self, undirected_graph):
        """Trying to find the shortest distance if edge attribute passed
        in the "weight_key" parameter is not exist
            - expected raise EdgeAttributeIsNotExistsException
        """
        with pytest.raises(EdgeAttributeIsNotExistsException):
            find_shortest_distance(
                undirected_graph, 'A', 'D',
                weight_key='non_existent')  # edge attribute "non_existent" is not exists

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', 1),
         ('A', 'C', 2),
         ('A', 'D', 3),
         ('A', 'E', 2),
         ('A', 'F', 3),
         ('A', 'G', 4),
         ('B', 'A', 1),
         ('B', 'C', 1),
         ('B', 'D', 2),
         ('B', 'E', 1),
         ('B', 'F', 2),
         ('B', 'G', 3),
         ('C', 'D', 1),
         ('C', 'B', 1),
         ('C', 'A', 2),
         ('C', 'E', 2),
         ('C', 'F', 3),
         ('C', 'G', 4),
         ('D', 'C', 1),
         ('D', 'B', 2),
         ('D', 'A', 3),
         ('D', 'E', 3),
         ('D', 'F', 4),
         ('D', 'G', 5),
         ('E', 'F', 1),
         ('E', 'G', 2),
         ('E', 'B', 1),
         ('E', 'A', 2),
         ('E', 'C', 2),
         ('E', 'D', 3),
         ('F', 'G', 1),
         ('F', 'E', 1),
         ('F', 'B', 2),
         ('F', 'A', 3),
         ('F', 'C', 3),
         ('F', 'D', 4),
         ('G', 'F', 1),
         ('G', 'E', 2),
         ('G', 'B', 3),
         ('G', 'A', 4),
         ('G', 'C', 4),
         ('G', 'D', 5),
         ('P', 'J', 1),
         ('J', 'P', 1),])
    def test_default_without_weight_key(self, undirected_graph, source, target, result):
        """Successful shortest distance search without weight key"""
        assert find_shortest_distance(undirected_graph, source, target) == result

    @pytest.mark.parametrize(
        ['source', 'target', 'result'],
        [('A', 'B', 6),
         ('A', 'C', 17),
         ('A', 'D', 36),
         ('A', 'E', 13),
         ('A', 'F', 16),
         ('A', 'G', 28),
         ('B', 'A', 6),
         ('B', 'C', 11),
         ('B', 'D', 30),
         ('B', 'E', 7),
         ('B', 'F', 10),
         ('B', 'G', 22),
         ('C', 'D', 19),
         ('C', 'B', 11),
         ('C', 'A', 17),
         ('C', 'E', 18),
         ('C', 'F', 21),
         ('C', 'G', 33),
         ('D', 'C', 19),
         ('D', 'B', 30),
         ('D', 'A', 36),
         ('D', 'E', 37),
         ('D', 'F', 40),
         ('D', 'G', 52),
         ('E', 'F', 3),
         ('E', 'G', 15),
         ('E', 'B', 7),
         ('E', 'A', 13),
         ('E', 'C', 18),
         ('E', 'D', 37),
         ('F', 'G', 12),
         ('F', 'E', 3),
         ('F', 'B', 10),
         ('F', 'A', 16),
         ('F', 'C', 21),
         ('F', 'D', 40),
         ('G', 'F', 12),
         ('G', 'E', 15),
         ('G', 'B', 22),
         ('G', 'A', 28),
         ('G', 'C', 33),
         ('G', 'D', 52),
         ('P', 'J', 17),
         ('J', 'P', 17),])
    def test_default_with_weight_key(self, undirected_graph, source, target, result):
        """Successful shortest distance search with weight key"""
        assert find_shortest_distance(undirected_graph, source, target, weight_key='distance') == result
