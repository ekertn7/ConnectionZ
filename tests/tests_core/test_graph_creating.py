"""Tests of validation functions when creating DirectedGraph and UndirectedGraph"""

import pytest
from connectionz import DirectedGraph, UndirectedGraph
from connectionz.exceptions import (
    WrongTypeOfNodesException,
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfNodeAttributesException,
    WrongTypeOfEdgesException,
    WrongTypeOfCoupleException,
    WrongLengthOfCoupleException,
    WrongTypeOfNodeIdentifierInCoupleException,
    WrongTypeOfMultipleEdgesException,
    WrongLengthOfMultipleEdgesException,
    WrongTypeOfEdgeIdentifierException,
    WrongTypeOfEdgeAttributesException,
    DuplicationInEdgeIdentifiersException)


class TestsDirectedGraphCreating:
    """Tests of creating DirectedGraph"""

    def test_without_values(self):
        """Creating empty DirectedGraph without values"""
        graph = DirectedGraph()
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 0
            and len(graph.edges) == 0)

    def test_from_none(self):
        """Creating empty DirectedGraph from None"""
        graph = DirectedGraph(nodes=None, edges=None)
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 0
            and len(graph.edges) == 0)

    def test_from_dict(self):
        """Creating DirectedGraph from dict"""
        graph = DirectedGraph(
            nodes={ 'A': {}, 'B': {} },
            edges={('A', 'B'): {'1b8a4be2281842179dddc5ddec629471': {}}} )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges)

    def test_from_list(self):
        """Creating DirectedGraph from list
            - nodes and edges should be converted into a dict
        """
        graph = DirectedGraph(
            nodes=['A', 'B'],
            edges=[('A', 'B')] )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_from_tuple(self):
        """Creating DirectedGraph from tuple
            - nodes and edges should be converted into a dict
        """
        graph = DirectedGraph(
            nodes=('A', 'B'),
            edges=(('A', 'B'),) )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_from_set(self):
        """Creating DirectedGraph from set
            - nodes and edges should be converted into a dict
        """
        graph = DirectedGraph(
            nodes={'A', 'B'},
            edges={('A', 'B')} )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_autocomplete_nodes(self):
        """Creating DirectedGraph with empty nodes
            - nodes should be added automatically based on edges
        """
        graph = DirectedGraph(
            nodes=None,
            edges={('A', 'B'): {'1b8a4be2281842179dddc5ddec629471': {}}} )
        assert (len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes)

    def test_exception_wrong_type_of_nodes(self):
        """Creating DirectedGraph with wrong type of nodes
            - graph should not be created
            - expected raise WrongTypeOfNodesException
        """
        nodes = 725  # wrong type of nodes
        with pytest.raises(WrongTypeOfNodesException):
            graph = DirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_identifier(self):
        """Creating DirectedGraph with wrong type of node identifier
            - graph should not be created
            - expected raise WrongTypeOfNodeIdentifierException
        """
        nodes = [
            '4217 386219',
            '4221 134809',
             4419_548391]  # wrong type of node identifier
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph = DirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_attributes(self):
        """Creating DirectedGraph with wrong type of node attributes
            - graph should not be created
            - expected raise WrongTypeOfNodeAttributesException
        """
        nodes = {
            'Alex': {'age': 20},
            'Boris': {'age': 19},
            'Clare': 21 }  # wrong type of node attributes
        with pytest.raises(WrongTypeOfNodeAttributesException):
            graph = DirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edges(self):
        """Creating DirectedGraph with wrong type of edges
            - graph should not be created
            - expected raise WrongTypeOfEdgesException
        """
        edges = 725_039  # wrong type of edges
        with pytest.raises(WrongTypeOfEdgesException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_couple(self):
        """Creating DirectedGraph with wrong type of couple
            - graph should not be created
            - expected raise WrongTypeOfCoupleException
        """
        edges = [
            ('Alex', 'Clare'),
            ('Alex', 'Eleanor'),
            ['Lucas', 'Nora'] ]  # wrong type of couple
        with pytest.raises(WrongTypeOfCoupleException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_length_of_couple(self):
        """Creating DirectedGraph with wrong length of couple
            - graph should not be created
            - expected raise WrongLengthOfCoupleException
        """
        edges = [
            ('Alex', 'Clare'),
            ('Alex', 'Eleanor'),
            ('Lucas', 'Nora', 'Stella') ]  # wrong length of couple
        with pytest.raises(WrongLengthOfCoupleException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_identifier_in_couple(self):
        """Creating DirectedGraph with wrong type of node identifier in couple
            - graph should not be created
            - expected raise WrongTypeOfNodeIdentifierInCoupleException
        """
        edges = [
            ('4217 386219', '4221 134809'),
            ('4221 134809', '4827 013841'),
            ('4419 548391',  4271_198493 ) ]  # wrong type of node identifier in couple
        with pytest.raises(WrongTypeOfNodeIdentifierInCoupleException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_multiple_edges(self):
        """Creating DirectedGraph with wrong type of multiple edges
            - graph should not be created
            - expected raise WrongTypeOfMultipleEdgesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): 1800 }  # wrong type of multiple edges
        with pytest.raises(WrongTypeOfMultipleEdgesException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_length_of_multiple_edges(self):
        """Creating DirectedGraph with wrong length of multiple edges
            - graph should not be created
            - expected raise WrongLengthOfMultipleEdgesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): {}}  # wrong length of multiple edges
        with pytest.raises(WrongLengthOfMultipleEdgesException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edge_identifier(self):
        """Creating DirectedGraph with wrong type of edge identifier
            - graph should not be created
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        edges = {
            ('Lucas', 'Nora'): {'1721692821': {'amount': 1500}},
            ('Nora', 'Stella'): {'1715817659': {'amount': 3200}},
            ('Alex', 'Clare'): {1731801694: {'amount': 1800}} }  # wrong type of edge identifier
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edge_attributes(self):
        """Creating DirectedGraph with wrong type of edge attributes
            - graph should not be created
            - expected raise WrongTypeOfEdgeAttributesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): {'2024-11-17': 1800} }  # wrong type of edge attributes
        with pytest.raises(WrongTypeOfEdgeAttributesException):
            graph = DirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

class TestsUndirectedGraphCreating:
    """Tests of creating UndirectedGraph"""

    def test_without_values(self):
        """Creating empty UndirectedGraph without values"""
        graph = UndirectedGraph()
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 0
            and len(graph.edges) == 0)

    def test_from_none(self):
        """Creating empty UndirectedGraph from None"""
        graph = UndirectedGraph(nodes=None, edges=None)
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 0
            and len(graph.edges) == 0)

    def test_from_dict(self):
        """Creating UndirectedGraph from dict"""
        graph = UndirectedGraph(
            nodes={ 'A': {}, 'B': {} },
            edges={ ('A', 'B'): {'1b8a4be2281842179dddc5ddec629471': {}} } )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges)

    def test_from_list(self):
        """Creating UndirectedGraph from list
            - nodes and edges should be converted into a dict
        """
        graph = UndirectedGraph(
            nodes=['A', 'B'],
            edges=[('A', 'B')] )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_from_tuple(self):
        """Creating UndirectedGraph from tuple
            - nodes and edges should be converted into a dict
        """
        graph = UndirectedGraph(
            nodes=('A', 'B'),
            edges=(('A', 'B'),) )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_from_set(self):
        """Creating UndirectedGraph from set
            - nodes and edges should be converted into a dict
        """
        graph = UndirectedGraph(
            nodes={'A', 'B'},
            edges={('A', 'B')} )
        assert (isinstance(graph.nodes, dict)
            and isinstance(graph.edges, dict)
            and len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes
            and len(graph.edges) == 1
            and ('A', 'B') in graph.edges
            and all(len(multiples) == 1 for multiples in graph.edges.values()))

    def test_autocomplete_nodes(self):
        """Creating UndirectedGraph with empty nodes
            - nodes should be added automatically based on edges
        """
        graph = UndirectedGraph(
            nodes=None,
            edges={ ('A', 'B'): {'1b8a4be2281842179dddc5ddec629471': {}} } )
        assert (len(graph.nodes) == 2
            and 'A' in graph.nodes
            and 'B' in graph.nodes)

    def test_exception_wrong_type_of_nodes(self):
        """Creating UndirectedGraph with wrong type of nodes
            - graph should not be created
            - expected raise WrongTypeOfNodesException
        """
        nodes = 725  # wrong type of nodes
        with pytest.raises(WrongTypeOfNodesException):
            graph = UndirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_identifier(self):
        """Creating UndirectedGraph with wrong type of node identifier
            - graph should not be created
            - expected raise WrongTypeOfNodeIdentifierException
        """
        nodes = [
            '4217 386219',
            '4221 134809',
             4419_548391 ]  # wrong type of node identifier
        with pytest.raises(WrongTypeOfNodeIdentifierException):
            graph = UndirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_attributes(self):
        """Creating UndirectedGraph with wrong type of node attributes
            - graph should not be created
            - expected raise WrongTypeOfNodeAttributesException
        """
        nodes = {
            'Alex': {'age': 20},
            'Boris': {'age': 19},
            'Clare': 21 }  # wrong type of node attributes
        with pytest.raises(WrongTypeOfNodeAttributesException):
            graph = UndirectedGraph(nodes=nodes)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edges(self):
        """Creating UndirectedGraph with wrong type of edges
            - graph should not be created
            - expected raise WrongTypeOfEdgesException
        """
        edges = 725_039  # wrong type of edges
        with pytest.raises(WrongTypeOfEdgesException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_couple(self):
        """Creating UndirectedGraph with wrong type of couple
            - graph should not be created
            - expected raise WrongTypeOfCoupleException
        """
        edges = [
            ('Alex', 'Clare'),
            ('Alex', 'Eleanor'),
            ['Lucas', 'Nora'] ]  # wrong type of couple
        with pytest.raises(WrongTypeOfCoupleException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_length_of_couple(self):
        """Creating UndirectedGraph with wrong length of couple
            - graph should not be created
            - expected raise WrongLengthOfCoupleException
        """
        edges = [
            ('Alex', 'Clare'),
            ('Alex', 'Eleanor'),
            ('Lucas', 'Nora', 'Stella') ]  # wrong length of couple
        with pytest.raises(WrongLengthOfCoupleException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_node_identifier_in_couple(self):
        """Creating UndirectedGraph with wrong type of node identifier in couple
            - graph should not be created
            - expected raise WrongTypeOfNodeIdentifierInCoupleException
        """
        edges = [
            ('4217 386219', '4221 134809'),
            ('4221 134809', '4827 013841'),
            ('4419 548391',  4271_198493 ) ]  # wrong type of node identifier in couple
        with pytest.raises(WrongTypeOfNodeIdentifierInCoupleException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_multiple_edges(self):
        """Creating UndirectedGraph with wrong type of multiple edges
            - graph should not be created
            - expected raise WrongTypeOfMultipleEdgesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): 1800 }  # wrong type of multiple edges
        with pytest.raises(WrongTypeOfMultipleEdgesException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_length_of_multiple_edges(self):
        """Creating UndirectedGraph with wrong length of multiple edges
            - graph should not be created
            - expected raise WrongLengthOfMultipleEdgesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): {} }  # wrong length of multiple edges
        with pytest.raises(WrongLengthOfMultipleEdgesException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edge_identifier(self):
        """Creating UndirectedGraph with wrong type of edge identifier
            - graph should not be created
            - expected raise WrongTypeOfEdgeIdentifierException
        """
        edges = {
            ('Lucas', 'Nora'): {'1721692821': {'amount': 1500}},
            ('Nora', 'Stella'): {'1715817659': {'amount': 3200}},
            ('Alex', 'Clare'): {1731801694: {'amount': 1800}} }  # wrong type of edge identifier
        with pytest.raises(WrongTypeOfEdgeIdentifierException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_wrong_type_of_edge_attributes(self):
        """Creating UndirectedGraph with wrong type of edge attributes
            - graph should not be created
            - expected raise WrongTypeOfEdgeAttributesException
        """
        edges = {
            ('Lucas', 'Nora'): {'2024-07-23': {'amount': 1500}},
            ('Nora', 'Stella'): {'2024-05-16': {'amount': 3200}},
            ('Alex', 'Clare'): {'2024-11-17': 1800} }  # wrong type of edge attributes
        with pytest.raises(WrongTypeOfEdgeAttributesException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()

    def test_exception_duplication_in_edge_identifiers(self):
        """Creating UndirectedGraph with duplication in edge identifiers
            - graph should not be created
            - expected raise DuplicationInEdgeIdentifiersException

        * possible only for UndirectedGraph
        """
        edges = {
            ('Nora', 'Stella'): {
                '2024-05-16': {'amount': 3200},
                '2024-08-03': {'amount': 2500}},
            ('Alex', 'Clare'): {
                '2024-11-17': {'amount': 1800}},
            ('Clare', 'Alex'): {
                '2024-11-17': {'amount': 1300}}, }  # duplication in edge identifiers
        with pytest.raises(DuplicationInEdgeIdentifiersException):
            graph = UndirectedGraph(edges=edges)
        assert 'graph' not in globals() and 'graph' not in locals()
