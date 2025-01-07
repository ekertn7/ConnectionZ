"""Tests DirectedGraph and UndirectedGraph method `del_edge`

if (wrong type of node identifier):
    - raise WrongTypeOfNodeIdentifierException

if (wrong type of edge identifier):
    - raise WrongTypeOfEdgeIdentifierException

if (couple not exists):
    - raise CoupleIsNotExistsException

if (couple exists) and (edge not specified):
    - delete couple with all edges

if (couple exists) and (edge not exists):
    - raise EdgeIsNotExistsException

if (couple exists) and (edge exists):
    - delete edge

- recalculate calculated attributes (optional)
"""

import pytest
from connectionz import DirectedGraph, UndirectedGraph
from connectionz.exceptions import (
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfEdgeIdentifierException,
    CoupleIsNotExistsException,
    EdgeIsNotExistsException)


class TestsDirectedGraphMethodDelEdge:
    """Tests of DirectedGraph method `del_edge`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Deleting edge with wrong node identifiers type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = DirectedGraph()
        graph.add_edge('4325_134981', '8143_519358')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.del_edge('4325_134981', 8143_519358)  # wrong type of node identifier

    def test_exception_wrong_type_of_edge_identifier(self):
        """Deleting edge with wrong edge identifier type
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        graph = DirectedGraph()
        graph.add_edge('4325_134981', '8143_519358', '2159542')
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph.del_edge('4325_134981', '8143_519358', 2159542)  # wrong type of edge identifier

    def test_exception_couple_is_not_exists(self):
        """Deleting non-existent edge from non-existent couple
            - expected raise CoupleIsNotExistsException
        """
        graph = DirectedGraph()
        with pytest.raises(CoupleIsNotExistsException):
            graph.del_edge('Alice', 'Kaleb', 'c39a1a3')  # couple is not exists

    def test_exception_edge_is_not_exists(self):
        """Deleting non-existent edge from existing couple
            - expected raise EdgeIsNotExistsException
        """
        graph = DirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        with pytest.raises(EdgeIsNotExistsException):
            graph.del_edge('Alice', 'Kaleb', '3a6d3d6')  # edge is not exists

    def test_delete_couple_with_all_edges(self):
        """Deleting couple with all edges"""
        graph = DirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        graph.add_edge('Alice', 'Kaleb', '3a6d3d6')
        graph.add_edge('Alice', 'Kaleb', '6315593')
        graph.del_edge('Alice', 'Kaleb')
        assert (len(graph.nodes) == 2
            and 'Alice' in graph.nodes
            and 'Kaleb' in graph.nodes
            and len(graph.edges) == 0)

    def test_delete_selected_edge(self):
        """Deleting selected edge from couple"""
        graph = DirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        graph.add_edge('Alice', 'Kaleb', '3a6d3d6')
        graph.add_edge('Alice', 'Kaleb', '6315593')
        graph.del_edge('Alice', 'Kaleb', '3a6d3d6')
        assert (len(graph.nodes) == 2
            and 'Alice' in graph.nodes
            and 'Kaleb' in graph.nodes
            and len(graph.edges) == 1
            and len(graph.edges[('Alice', 'Kaleb')]) == 2
            and 'c39a1a3' in graph.edges[('Alice', 'Kaleb')]
            and '6315593' in graph.edges[('Alice', 'Kaleb')]
            and '3a6d3d6' not in graph.edges[('Alice', 'Kaleb')])

    def test_default_recalculate_calculated_attributes(self):
        """Deleting edge with automatically recalculation calculated attributes
        (default behavior)
        """
        graph = DirectedGraph(
            nodes=[
                'Steven',  # degree = 2, neighbors = {'Amina', 'Nicole'}
                'Nicole',  # degree = 1, neighbors is empty
                'Amina'],  # degree = 1, neighbors is empty
            edges=[
                ('Steven', 'Nicole'),
                ('Steven', 'Amina')] )
        graph.del_edge('Steven', 'Amina')
        assert (len(graph.nodes) == 3
            and 'Steven' in graph.nodes
            and 'Nicole' in graph.nodes
            and 'Amina' in graph.nodes
            and len(graph.edges) == 1
            and ('Steven', 'Nicole') in graph.edges
            and graph.nodes['Steven']['degree'] == 1
            and graph.nodes['Steven']['neighbors'] == {'Nicole'}
            and graph.nodes['Nicole']['degree'] == 1
            and graph.nodes['Nicole']['neighbors'] == set()
            and graph.nodes['Amina']['degree'] == 0
            and graph.nodes['Amina']['neighbors'] == set())

    def test_disable_recalculate_calculated_attributes(self):
        """Deleting edge with disabled automatically recalculation calculated
        attributes (custom behavior)
        """
        graph = DirectedGraph(
            nodes=[
                'Steven',  # degree = 2, neighbors = {'Amina', 'Nicole'}
                'Nicole',  # degree = 1, neighbors is empty
                'Amina'],  # degree = 1, neighbors is empty
            edges=[
                ('Steven', 'Nicole'),
                ('Steven', 'Amina')] )
        graph.del_edge('Steven', 'Amina', recalculate_calculated_attributes=False)
        assert (len(graph.nodes) == 3
            and 'Steven' in graph.nodes
            and 'Nicole' in graph.nodes
            and 'Amina' in graph.nodes
            and len(graph.edges) == 1
            and ('Steven', 'Nicole') in graph.edges
            and graph.nodes['Steven']['degree'] == 2
            and graph.nodes['Steven']['neighbors'] == {'Amina', 'Nicole'}
            and graph.nodes['Nicole']['degree'] == 1
            and graph.nodes['Nicole']['neighbors'] == set()
            and graph.nodes['Amina']['degree'] == 1
            and graph.nodes['Amina']['neighbors'] == set())


class TestsUndirectedGraphMethodDelEdge:
    """Tests of UndirectedGraph method `del_edge`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Deleting edge with wrong node identifiers type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = UndirectedGraph()
        graph.add_edge('4325_134981', '8143_519358')
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.del_edge('4325_134981', 8143_519358)  # wrong type of node identifier

    def test_exception_wrong_type_of_edge_identifier(self):
        """Deleting edge with wrong edge identifier type
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        graph = UndirectedGraph()
        graph.add_edge('4325_134981', '8143_519358', '2159542')
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph.del_edge('4325_134981', '8143_519358', 2159542)  # wrong type of edge identifier

    def test_exception_couple_is_not_exists(self):
        """Deleting non-existent edge from non-existent couple
            - expected raise CoupleIsNotExistsException
        """
        graph = UndirectedGraph()
        with pytest.raises(CoupleIsNotExistsException):
            graph.del_edge('Alice', 'Kaleb', 'c39a1a3')  # couple is not exists

    def test_exception_edge_is_not_exists(self):
        """Deleting non-existent edge from existing couple
            - expected raise EdgeIsNotExistsException
        """
        graph = UndirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        with pytest.raises(EdgeIsNotExistsException):
            graph.del_edge('Alice', 'Kaleb', '3a6d3d6')  # edge is not exists

    def test_delete_couple_with_all_edges(self):
        """Deleting couple with all edges"""
        graph = UndirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        graph.add_edge('Alice', 'Kaleb', '3a6d3d6')
        graph.add_edge('Alice', 'Kaleb', '6315593')
        graph.del_edge('Alice', 'Kaleb')
        assert (len(graph.nodes) == 2
            and 'Alice' in graph.nodes
            and 'Kaleb' in graph.nodes
            and len(graph.edges) == 0)

    def test_delete_selected_edge(self):
        """Deleting selected edge from couple"""
        graph = UndirectedGraph()
        graph.add_edge('Alice', 'Kaleb', 'c39a1a3')
        graph.add_edge('Alice', 'Kaleb', '3a6d3d6')
        graph.add_edge('Alice', 'Kaleb', '6315593')
        graph.del_edge('Alice', 'Kaleb', '3a6d3d6')
        assert (len(graph.nodes) == 2
            and 'Alice' in graph.nodes
            and 'Kaleb' in graph.nodes
            and len(graph.edges) == 1
            and len(graph.edges[tuple(sorted(('Alice', 'Kaleb')))]) == 2
            and 'c39a1a3' in graph.edges[tuple(sorted(('Alice', 'Kaleb')))]
            and '6315593' in graph.edges[tuple(sorted(('Alice', 'Kaleb')))]
            and '3a6d3d6' not in graph.edges[tuple(sorted(('Alice', 'Kaleb')))])

    def test_default_recalculate_calculated_attributes(self):
        """Deleting edge with automatically recalculation calculated attributes
        (default behavior)
        """
        graph = UndirectedGraph(
            nodes=[
                'Steven',  # degree = 2, neighbors = {'Amina', 'Nicole'}
                'Nicole',  # degree = 1, neighbors = {'Steven'}
                'Amina'],  # degree = 1, neighbors = {'Steven'}
            edges=[
                ('Steven', 'Nicole'),
                ('Steven', 'Amina')] )
        graph.del_edge('Steven', 'Amina')
        assert (len(graph.nodes) == 3
            and 'Steven' in graph.nodes
            and 'Nicole' in graph.nodes
            and 'Amina' in graph.nodes
            and len(graph.edges) == 1
            and tuple(sorted(('Steven', 'Nicole'))) in graph.edges
            and graph.nodes['Steven']['degree'] == 1
            and graph.nodes['Steven']['neighbors'] == {'Nicole'}
            and graph.nodes['Nicole']['degree'] == 1
            and graph.nodes['Nicole']['neighbors'] == {'Steven'}
            and graph.nodes['Amina']['degree'] == 0
            and graph.nodes['Amina']['neighbors'] == set())

    def test_disable_recalculate_calculated_attributes(self):
        """Deleting edge with disabled automatically recalculation calculated
        attributes (custom behavior)
        """
        graph = UndirectedGraph(
            nodes=[
                'Steven',  # degree = 2, neighbors = {'Amina', 'Nicole'}
                'Nicole',  # degree = 1, neighbors = {'Steven'}
                'Amina'],  # degree = 1, neighbors = {'Steven'}
            edges=[
                ('Steven', 'Nicole'),
                ('Steven', 'Amina')] )
        graph.del_edge('Steven', 'Amina', recalculate_calculated_attributes=False)
        assert (len(graph.nodes) == 3
            and 'Steven' in graph.nodes
            and 'Nicole' in graph.nodes
            and 'Amina' in graph.nodes
            and len(graph.edges) == 1
            and tuple(sorted(('Steven', 'Nicole'))) in graph.edges
            and graph.nodes['Steven']['degree'] == 2
            and graph.nodes['Steven']['neighbors'] == {'Amina', 'Nicole'}
            and graph.nodes['Nicole']['degree'] == 1
            and graph.nodes['Nicole']['neighbors'] == {'Steven'}
            and graph.nodes['Amina']['degree'] == 1
            and graph.nodes['Amina']['neighbors'] == {'Steven'})
