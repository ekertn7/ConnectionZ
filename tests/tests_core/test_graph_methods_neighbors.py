"""Tests DirectedGraph and UndirectedGraph methods

- `clear_neighbors`
- `find_neighbors`
"""

from connectionz import DirectedGraph, UndirectedGraph


class TestsDirectedGraphMethodNeighbors:
    """Tests of DirectedGraph methods `clear_neighbors` and `find_neighbors`"""

    def test_clear_neighbors(self):
        """Setting neighbors value to empty set for all nodes in graph"""
        graph = DirectedGraph()
        graph.add_edge('Christopher', 'Eva', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Caroline', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Everly', recalculate_calculated_attributes=False)
        graph.clear_neighbors()
        assert (graph.nodes['Christopher']['neighbors'] == set()
            and graph.nodes['Eva']['neighbors'] == set()
            and graph.nodes['Santiago']['neighbors'] == set()
            and graph.nodes['Caroline']['neighbors'] == set()
            and graph.nodes['Everly']['neighbors'] == set())

    def test_find_neighbors(self):
        """Finding neighbors for all nodes in graph"""
        graph = DirectedGraph()
        graph.add_edge('Christopher', 'Eva', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Caroline', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Everly', recalculate_calculated_attributes=False)
        graph.find_neighbors()
        assert (graph.nodes['Christopher']['neighbors'] == {'Eva'}
            and graph.nodes['Eva']['neighbors'] == set()
            and graph.nodes['Santiago']['neighbors'] == {'Caroline', 'Everly'}
            and graph.nodes['Caroline']['neighbors'] == set()
            and graph.nodes['Everly']['neighbors'] == set())


class TestsUndirectedGraphMethodNeighbors:
    """Tests of UndirectedGraph methods `clear_neighbors` and `find_neighbors`"""

    def test_clear_neighbors(self):
        """Setting neighbors value to empty set for all nodes in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Christopher', 'Eva', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Caroline', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Everly', recalculate_calculated_attributes=False)
        graph.clear_neighbors()
        assert (graph.nodes['Christopher']['neighbors'] == set()
            and graph.nodes['Eva']['neighbors'] == set()
            and graph.nodes['Santiago']['neighbors'] == set()
            and graph.nodes['Caroline']['neighbors'] == set()
            and graph.nodes['Everly']['neighbors'] == set())

    def test_find_neighbors(self):
        """Finding neighbors for all nodes in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Christopher', 'Eva', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Caroline', recalculate_calculated_attributes=False)
        graph.add_edge('Santiago', 'Everly', recalculate_calculated_attributes=False)
        graph.find_neighbors()
        assert (graph.nodes['Christopher']['neighbors'] == {'Eva'}
            and graph.nodes['Eva']['neighbors'] == {'Christopher'}
            and graph.nodes['Santiago']['neighbors'] == {'Caroline', 'Everly'}
            and graph.nodes['Caroline']['neighbors'] == {'Santiago'}
            and graph.nodes['Everly']['neighbors'] == {'Santiago'})
