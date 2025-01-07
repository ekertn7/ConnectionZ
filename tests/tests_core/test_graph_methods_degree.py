"""Tests DirectedGraph and UndirectedGraph methods

- `clear_degree`
- `calc_degree`
"""

from connectionz import DirectedGraph, UndirectedGraph


class TestsDirectedGraphMethodDegree:
    """Tests of DirectedGraph methods `clear_degree` and `calc_degree`"""

    def test_clear_degree(self):
        """Setting degree value to 0 for all nodes in graph"""
        graph = DirectedGraph()
        graph.add_edge('Logan', 'Violet', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Grace', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Riley', recalculate_calculated_attributes=False)
        graph.clear_degree()
        assert (graph.nodes['Logan']['degree'] == 0
            and graph.nodes['Violet']['degree'] == 0
            and graph.nodes['Jacob']['degree'] == 0
            and graph.nodes['Grace']['degree'] == 0
            and graph.nodes['Riley']['degree'] == 0)

    def test_calc_degree(self):
        """Calculating degree value for all nodes in graph"""
        graph = DirectedGraph()
        graph.add_edge('Logan', 'Violet', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Grace', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Riley', recalculate_calculated_attributes=False)
        graph.calc_degree()
        assert (graph.nodes['Logan']['degree'] == 1
            and graph.nodes['Violet']['degree'] == 1
            and graph.nodes['Jacob']['degree'] == 2
            and graph.nodes['Grace']['degree'] == 1
            and graph.nodes['Riley']['degree'] == 1)


class TestsUndirectedGraphMethodDegree:
    """Tests of UndirectedGraph methods `clear_degree` and `calc_degree`"""

    def test_clear_degree(self):
        """Setting degree value to 0 for all nodes in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Logan', 'Violet', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Grace', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Riley', recalculate_calculated_attributes=False)
        graph.clear_degree()
        assert (graph.nodes['Logan']['degree'] == 0
            and graph.nodes['Violet']['degree'] == 0
            and graph.nodes['Jacob']['degree'] == 0
            and graph.nodes['Grace']['degree'] == 0
            and graph.nodes['Riley']['degree'] == 0)

    def test_calc_degree(self):
        """Calculating degree value for all nodes in graph"""
        graph = UndirectedGraph()
        graph.add_edge('Logan', 'Violet', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Grace', recalculate_calculated_attributes=False)
        graph.add_edge('Jacob', 'Riley', recalculate_calculated_attributes=False)
        graph.calc_degree()
        assert (graph.nodes['Logan']['degree'] == 1
            and graph.nodes['Violet']['degree'] == 1
            and graph.nodes['Jacob']['degree'] == 2
            and graph.nodes['Grace']['degree'] == 1
            and graph.nodes['Riley']['degree'] == 1)
