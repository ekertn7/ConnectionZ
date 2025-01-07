"""Tests DirectedGraph and UndirectedGraph method `has_node`"""

import pytest
from connectionz import DirectedGraph, UndirectedGraph
from connectionz.exceptions import WrongTypeOfNodeIdentifierException


class TestsDirectedGraphMethodHasNode:
    """Tests of DirectedGraph method `has_node`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Checking that node is in graph with wrong node identifier type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = DirectedGraph()
        graph.add_node('4217 014533')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.has_node(4217_014533)  # wrong type of node identifier

    def test_node_in_graph(self):
        """Checking that node is in graph"""
        graph = DirectedGraph()
        graph.add_node('Freya')
        result = graph.has_node('Freya')
        assert result is True

    def test_node_not_in_graph(self):
        """Checking that node is not in graph"""
        graph = DirectedGraph()
        graph.add_node('Freya')
        result = graph.has_node('Margaret')
        assert result is False


class TestsUndirectedGraphMethodHasNode:
    """Tests of UndirectedGraph method `has_node`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Checking that node is in graph with wrong node identifier type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = UndirectedGraph()
        graph.add_node('4217 014533')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.has_node(4217_014533)  # wrong type of node identifier

    def test_node_in_graph(self):
        """Checking that node is in graph"""
        graph = UndirectedGraph()
        graph.add_node('Freya')
        result = graph.has_node('Freya')
        assert result is True

    def test_node_not_in_graph(self):
        """Checking that node is not in graph"""
        graph = UndirectedGraph()
        graph.add_node('Freya')
        result = graph.has_node('Margaret')
        assert result is False
