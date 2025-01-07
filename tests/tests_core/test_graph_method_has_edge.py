"""Tests DirectedGraph and UndirectedGraph method `has_edge`"""

import pytest
from connectionz import DirectedGraph, UndirectedGraph
from connectionz.exceptions import (
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfEdgeIdentifierException)


class TestsDirectedGraphMethodHasEdge:
    """Tests of DirectedGraph method `has_edge`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Checking that edge is in graph with wrong node identifiers type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = DirectedGraph()
        graph.add_edge('4217 019234', '4325 845949')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.has_edge('4217 019234', 4325_845949)  # wrong type of node identifier

    def test_exception_wrong_type_of_edge_identifier(self):
        """Checking that edge is in graph with wrong edge identifier type
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        graph = DirectedGraph()
        graph.add_edge('Adalynn', 'Joshua', '3740572')
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph.has_edge('Adalynn', 'Joshua', 3740572)  # wrong type of edge identifier

    def test_couple_in_graph(self):
        """Checking that couple is in graph"""
        graph = DirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina')
        assert result is True

    def test_couple_not_in_graph(self):
        """Checking that couple is not in graph"""
        graph = DirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Robert', 'Sienna')
        assert result is False

    def test_edge_in_graph(self):
        """Checking that edge is in graph"""
        graph = DirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina', '0bac3283bf')
        assert result is True

    def test_edge_not_in_graph(self):
        """Checking that edge is not in graph"""
        graph = DirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina', '60fa4fa6bf')
        assert result is False


class TestsUndirectedGraphMethodHasEdge:
    """Tests of UndirectedGraph method `has_edge`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Checking that edge is in graph with wrong node identifiers type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = UndirectedGraph()
        graph.add_edge('4217 019234', '4325 845949')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.has_edge('4217 019234', 4325_845949)  # wrong type of node identifier

    def test_exception_wrong_type_of_edge_identifier(self):
        """Checking that edge is in graph with wrong edge identifier type
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        graph = UndirectedGraph()
        graph.add_edge('Adalynn', 'Joshua', '3740572')
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph.has_edge('Adalynn', 'Joshua', 3740572)  # wrong type of edge identifier

    def test_couple_in_graph(self):
        """Checking that couple is in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina')
        assert result is True

    def test_couple_not_in_graph(self):
        """Checking that couple is not in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Robert', 'Sienna')
        assert result is False

    def test_edge_in_graph(self):
        """Checking that edge is in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina', '0bac3283bf')
        assert result is True

    def test_edge_not_in_graph(self):
        """Checking that edge is not in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
        result = graph.has_edge('Jonathan', 'Alina', '60fa4fa6bf')
        assert result is False
