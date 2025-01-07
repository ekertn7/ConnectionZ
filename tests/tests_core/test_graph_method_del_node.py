"""Tests DirectedGraph and UndirectedGraph method `del_node`

if (wrong type of node identifier):
    - raise WrongTypeOfNodeIdentifierException

if (node not exists):
    - raise NodeIsNotExistsException

if (node exists):
    - delete node
    - delete incident edges
    - recalculate calculated attributes (optional)
"""

import pytest
from connectionz import DirectedGraph, UndirectedGraph
from connectionz.exceptions import (
    WrongTypeOfNodeIdentifierException,
    NodeIsNotExistsException)


class TestsDirectedGraphMethodDelNode:
    """Tests of DirectedGraph method `del_node`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Deleting node with wrong identifier type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = DirectedGraph()
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.del_node(4217_092672)  # wrong type of node identifier

    def test_exception_node_is_not_exists(self):
        """Deleting non-existent node
            - expected raise NodeIsNotExistsException
        """
        graph = DirectedGraph()
        graph.add_node('Molly')
        with pytest.raises(NodeIsNotExistsException):
            graph.del_node('Layla')
        assert len(graph.nodes) == 1 and 'Molly' in graph.nodes

    def test_delete_node_and_incident_edges(self):
        """Deleting selected node with automatically deleting its incident edges"""
        graph = DirectedGraph(
            nodes=['Riley', 'Layla', 'Eliana', 'Stella'],
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana'),
                ('Stella', 'Eliana')] )
        graph.del_node('Riley')  # should delete ('Riley', 'Layla') and ('Riley', 'Eliana')
        assert (len(graph.nodes) == 3
            and 'Riley' not in graph.nodes
            and len(graph.edges) == 1
            and ('Riley', 'Layla') not in graph.edges
            and ('Riley', 'Eliana') not in graph.edges)

    def test_default_recalculate_calculated_attributes(self):
        """Deleting selected node with automatically recalculation calculated
        attributes (default behavior)
        """
        graph = DirectedGraph(
            nodes=[
                'Riley',    # degree = 2, neighbors = {'Eliana', 'Layla'}
                'Layla',    # degree = 1, neighbors is empty
                'Eliana'],  # degree = 1, neighbors is empty
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana')] )
        graph.del_node('Layla')
        assert (len(graph.nodes) == 2
            and 'Riley' in graph.nodes
            and 'Eliana' in graph.nodes
            and len(graph.edges) == 1
            and ('Riley', 'Eliana') in graph.edges
            and graph.nodes['Riley']['degree'] == 1
            and graph.nodes['Riley']['neighbors'] == {'Eliana'}
            and graph.nodes['Eliana']['degree'] == 1
            and graph.nodes['Eliana']['neighbors'] == set())

    def test_disable_recalculate_calculated_attributes(self):
        """Deleting selected node with disabled automatically recalculation
        calculated attributes (custom behavior)
        """
        graph = DirectedGraph(
            nodes=[
                'Riley',    # degree = 2, neighbors = {'Eliana', 'Layla'}
                'Layla',    # degree = 1, neighbors is empty
                'Eliana'],  # degree = 1, neighbors is empty
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana')] )
        graph.del_node('Layla', recalculate_calculated_attributes=False)
        assert (len(graph.nodes) == 2
            and 'Riley' in graph.nodes
            and 'Eliana' in graph.nodes
            and len(graph.edges) == 1
            and ('Riley', 'Eliana') in graph.edges
            and graph.nodes['Riley']['degree'] == 2
            and graph.nodes['Riley']['neighbors'] == {'Eliana', 'Layla'}
            and graph.nodes['Eliana']['degree'] == 1
            and graph.nodes['Eliana']['neighbors'] == set())


class TestsUndirectedGraphMethodDelNode:
    """Tests of UndirectedGraph method `del_node`"""

    def test_exception_wrong_type_of_node_identifier(self):
        """Deleting node with wrong identifier type
            - expected raise WrongTypeOfNodeIdentifierException
        """
        graph = UndirectedGraph()
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph.del_node(4217_092672)  # wrong type of node identifier

    def test_exception_node_is_not_exists(self):
        """Deleting non-existent node
            - expected raise NodeIsNotExistsException
        """
        graph = UndirectedGraph()
        graph.add_node('Molly')
        with pytest.raises(NodeIsNotExistsException):
            graph.del_node('Layla')
        assert len(graph.nodes) == 1 and 'Molly' in graph.nodes

    def test_delete_node_and_incident_edges(self):
        """Deleting selected node with automatically deleting its incident edges"""
        graph = UndirectedGraph(
            nodes=['Riley', 'Layla', 'Eliana', 'Stella'],
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana'),
                ('Stella', 'Eliana')] )
        graph.del_node('Riley')  # should delete ('Riley', 'Layla') and ('Riley', 'Eliana')
        assert (len(graph.nodes) == 3
            and 'Riley' not in graph.nodes
            and len(graph.edges) == 1
            and tuple(sorted(('Riley', 'Layla'))) not in graph.edges
            and tuple(sorted(('Riley', 'Eliana'))) not in graph.edges)

    def test_default_recalculate_calculated_attributes(self):
        """Deleting selected node with automatically recalculation calculated
        attributes (default behavior)
        """
        graph = UndirectedGraph(
            nodes=[
                'Riley',    # degree = 2, neighbors = {'Eliana', 'Layla'}
                'Layla',    # degree = 1, neighbors = {'Riley'}
                'Eliana'],  # degree = 1, neighbors = {'Riley'}
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana')] )
        graph.del_node('Layla')
        assert (len(graph.nodes) == 2
            and 'Riley' in graph.nodes
            and 'Eliana' in graph.nodes
            and len(graph.edges) == 1
            and tuple(sorted(('Riley', 'Eliana'))) in graph.edges
            and graph.nodes['Riley']['degree'] == 1
            and graph.nodes['Riley']['neighbors'] == {'Eliana'}
            and graph.nodes['Eliana']['degree'] == 1
            and graph.nodes['Eliana']['neighbors'] == {'Riley'})

    def test_disable_recalculate_calculated_attributes(self):
        """Deleting selected node with disabled automatically recalculation
        calculated attributes (custom behavior)
        """
        graph = UndirectedGraph(
            nodes=[
                'Riley',    # degree = 2, neighbors = {'Eliana', 'Layla'}
                'Layla',    # degree = 1, neighbors = {'Riley'}
                'Eliana'],  # degree = 1, neighbors = {'Riley'}
            edges=[
                ('Riley', 'Layla'),
                ('Riley', 'Eliana')] )
        graph.del_node('Layla', recalculate_calculated_attributes=False)
        assert (len(graph.nodes) == 2
            and 'Riley' in graph.nodes
            and 'Eliana' in graph.nodes
            and len(graph.edges) == 1
            and tuple(sorted(('Riley', 'Eliana'))) in graph.edges
            and graph.nodes['Riley']['degree'] == 2
            and graph.nodes['Riley']['neighbors'] == {'Eliana', 'Layla'}
            and graph.nodes['Eliana']['degree'] == 1
            and graph.nodes['Eliana']['neighbors'] == {'Riley'})
