"""Tests DirectedGraph and UndirectedGraph methods

- `check_type`
- `check_is_complete`
- `check_is_pseudo`
- `check_is_multi`
"""

from connectionz import DirectedGraph, UndirectedGraph


class TestsGraphMethodCheckType:
    """Tests of DirectedGraph and UndirectedGraph method `check_type`"""

    def test_directed_graph(self):
        """Checks type of DirectedGraph object"""
        graph = DirectedGraph()
        assert graph.check_type() == 'DirectedGraph'

    def test_undirected_graph(self):
        """Checks type of UndirectedGraph object"""
        graph = UndirectedGraph()
        assert graph.check_type() == 'UndirectedGraph'


class TestsDirectedGraphMethodCheckIsComplete:
    """Tests of DirectedGraph method `check_is_complete`"""

    def test_not_complete(self):
        """Checks that graph is not complete

        Graph illustration
        ------------------
            A - B
            | x |
            D - C
        """
        graph = DirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[
                ('A', 'B'), ('A', 'C'), ('A', 'D'),
                ('B', 'C'), ('B', 'D'),
                ('C', 'D')])
        assert graph.check_is_complete() is False

    def test_not_complete_empty(self):
        """Checks that empty graph is not complete"""
        graph = DirectedGraph()
        assert graph.check_is_complete() is False

    def test_not_complete_with_one_node(self):
        """Checks that graph with one node and without edges is not complete"""
        graph = DirectedGraph()
        graph.add_node('Vivian')
        assert graph.check_is_complete() is False

    def test_not_complete_with_loops(self):
        """Checks that graph with correct number of edges but with loops is not
        complete

        Graph illustration
        ------------------
            ∩
            A - B
            ‖ x ‖
            D = C
        """
        graph = DirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[
                ('A', 'A'), ('A', 'C'), ('A', 'D'),  # A - A is loop
                ('B', 'A'), ('B', 'C'), ('B', 'D'),
                ('C', 'A'), ('C', 'B'), ('C', 'D'),
                ('D', 'A'), ('D', 'B'), ('D', 'C')])
        assert graph.check_is_complete() is False

    def test_complete(self):
        """Checks that graph is complete

        Graph illustration
        ------------------
            A = B
            ‖ x ‖
            D = C
        """
        graph = DirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[
                ('A', 'B'), ('A', 'C'), ('A', 'D'),
                ('B', 'A'), ('B', 'C'), ('B', 'D'),
                ('C', 'A'), ('C', 'B'), ('C', 'D'),
                ('D', 'A'), ('D', 'B'), ('D', 'C')])
        assert graph.check_is_complete() is True


class TestsUndirectedGraphMethodCheckIsComplete:
    """Tests of UndirectedGraph method `check_is_complete`"""

    def test_not_complete(self):
        """Checks that graph is not complete

        Graph illustration
        ------------------
            A - B - C - D
        """
        graph = UndirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[('A', 'B'), ('B', 'C'), ('C', 'D')])
        assert graph.check_is_complete() is False

    def test_not_complete_empty(self):
        """Checks that empty graph is not complete"""
        graph = UndirectedGraph()
        assert graph.check_is_complete() is False

    def test_not_complete_with_one_node(self):
        """Checks that graph with one node and without edges is not complete"""
        graph = UndirectedGraph()
        graph.add_node('Vivian')
        assert graph.check_is_complete() is False

    def test_not_complete_with_loops(self):
        """Checks that graph with correct number of edges but with loops is not
        complete

        Graph illustration
        ------------------
            ∩
            A   B
            | x |
            D - C
        """
        graph = UndirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[
                ('A', 'A'), ('A', 'C'), ('A', 'D'),  # A - A is loop
                ('B', 'C'), ('B', 'D'),
                ('C', 'D')])
        assert graph.check_is_complete() is False

    def test_complete(self):
        """Checks that graph is complete

        Graph illustration
        ------------------
            A - B
            | x |
            D - C
        """
        graph = UndirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[
                ('A', 'B'), ('A', 'C'), ('A', 'D'),
                ('B', 'C'), ('B', 'D'),
                ('C', 'D')])
        assert graph.check_is_complete() is True


class TestsDirectedGraphMethodCheckIsPseudo:
    """Tests of DirectedGraph method `check_is_pseudo`"""

    def test_not_pseudo(self):
        """Checks that graph not contains any loops (and is not a pseudograph)"""
        graph = DirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[('A', 'B'), ('B', 'C'), ('C', 'D')])
        assert graph.check_is_pseudo() is False

    def test_pseudo(self):
        """Checks that graph contains at least one loop (and is a pseudograph)"""
        graph = DirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[('A', 'A'), ('B', 'C'), ('C', 'D')])  # A - A is loop
        assert graph.check_is_pseudo() is True


class TestsUndirectedGraphMethodCheckIsPseudo:
    """Tests of UndirectedGraph method `check_is_pseudo`"""

    def test_not_pseudo(self):
        """Checks that graph not contains any loops (and is not a pseudograph)"""
        graph = UndirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[('A', 'B'), ('B', 'C'), ('C', 'D')])
        assert graph.check_is_pseudo() is False

    def test_pseudo(self):
        """Checks that graph contains at least one loop (and is a pseudograph)"""
        graph = UndirectedGraph(
            nodes=['A', 'B', 'C', 'D'],
            edges=[('A', 'A'), ('B', 'C'), ('C', 'D')])  # A - A is loop
        assert graph.check_is_pseudo() is True


class TestsDirectedGraphMethodCheckIsMulti:
    """Tests of DirectedGraph method `check_is_multi`"""

    def test_not_multi(self):
        """Checks that graph contains only one edge between a couple of nodes
        (and is not a multigraph)

        Graph illustration
        ------------------
            A - B - C
        """
        graph = DirectedGraph(nodes=['A', 'B', 'C'])
        graph.add_edge('A', 'B', weight=146)
        graph.add_edge('B', 'C', weight=237)
        assert graph.check_is_multi() is False

    def test_multi(self):
        """Checks that graph contains more than one edge between a couple of
        nodes (and is a multigraph)

        Graph illustration
        ------------------
            A - B = C
        """
        graph = DirectedGraph(nodes=['A', 'B', 'C'])
        graph.add_edge('A', 'B', weight=146)
        graph.add_edge('B', 'C', weight=237)
        graph.add_edge('B', 'C', weight=524)
        assert graph.check_is_multi() is True


class TestsUndirectedGraphMethodCheckIsMulti:
    """Tests of UndirectedGraph method `check_is_multi`"""

    def test_not_multi(self):
        """Checks that graph contains only one edge between a couple of nodes
        (and is not a multigraph)

        Graph illustration
        ------------------
            A - B - C
        """
        graph = UndirectedGraph(nodes=['A', 'B', 'C'])
        graph.add_edge('A', 'B', weight=146)
        graph.add_edge('B', 'C', weight=237)
        assert graph.check_is_multi() is False

    def test_multi(self):
        """Checks that graph contains more than one edge between a couple of
        nodes (and is a multigraph)

        Graph illustration
        ------------------
            A - B = C
        """
        graph = UndirectedGraph(nodes=['A', 'B', 'C'])
        graph.add_edge('A', 'B', weight=146)
        graph.add_edge('B', 'C', weight=237)
        graph.add_edge('B', 'C', weight=524)
        assert graph.check_is_multi() is True
