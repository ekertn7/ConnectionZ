"""Tests DirectedGraph and UndirectedGraph method `__len__`"""

from connectionz import DirectedGraph, UndirectedGraph


class TestsDirectedGraphMethodLen:
    """Tests of DirectedGraph method `__len__`"""

    def test_empty(self):
        """Using method `__len__`, empty case"""
        graph = DirectedGraph()
        assert len(graph) == len(graph.nodes) and len(graph) == 0

    def test_filled(self):
        """Using method `__len__`, filled case"""
        graph = DirectedGraph(['A', 'B', 'C', 'D', 'E'])
        assert len(graph) == len(graph.nodes) and len(graph) == 5


class TestsUndirectedGraphMethodLen:
    """Tests of UndirectedGraph method `__len__`"""

    def test_empty(self):
        """Using method `__len__`, empty case"""
        graph = UndirectedGraph()
        assert len(graph) == len(graph.nodes) and len(graph) == 0

    def test_filled(self):
        """Using method `__len__`, filled case"""
        graph = UndirectedGraph(['A', 'B', 'C', 'D', 'E'])
        assert len(graph) == len(graph.nodes) and len(graph) == 5
