"""Tests DirectedGraph and UndirectedGraph method `get_subgraph`"""

from connectionz import DirectedGraph, UndirectedGraph


class TestsDirectedGraphMethodGetSubgraph:
    """Tests of DirectedGraph method `get_subgraph`"""

    def test_only_selected_nodes(self):
        """Getting subgraph including nodes only from selected nodes"""
        graph = DirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'])
        assert (len(subgraph.nodes) == 2
            and 'Milani' in subgraph.nodes
            and 'Adrian' in subgraph.nodes
            and len(subgraph.edges) == 1
            and ('Adrian', 'Milani') in subgraph.edges)

    def test_include_adjacent_nodes(self):
        """Getting subgraph including adjacent nodes"""
        graph = DirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'], include_adjacent_nodes=True)
        assert (len(subgraph.nodes) == 4
            and 'Milani' in subgraph.nodes
            and 'Adrian' in subgraph.nodes
            and 'Diana' in subgraph.nodes
            and 'Presley' in subgraph.nodes
            and len(subgraph.edges) == 3
            and ('Adrian', 'Milani') in subgraph.edges
            and ('Adrian', 'Diana') in subgraph.edges
            and ('Presley', 'Adrian') in subgraph.edges)

    def test_recalculate_calculated_attributes(self):
        """Getting subgraph with automatically recalculation calculated
        attributes (default behavior)
        """
        graph = DirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'])
        assert (subgraph.nodes['Milani']['degree'] == 1
            and subgraph.nodes['Milani']['neighbors'] == set()
            and subgraph.nodes['Adrian']['degree'] == 1
            and subgraph.nodes['Adrian']['neighbors'] == {'Milani'})


class TestsUndirectedGraphMethodGetSubgraph:
    """Tests of UndirectedGraph method `get_subgraph`"""

    def test_only_selected_nodes(self):
        """Getting subgraph including nodes only from selected nodes"""
        graph = UndirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'])
        assert (len(subgraph.nodes) == 2
            and 'Milani' in subgraph.nodes
            and 'Adrian' in subgraph.nodes
            and len(subgraph.edges) == 1
            and tuple(sorted(('Adrian', 'Milani'))) in subgraph.edges)

    def test_include_adjacent_nodes(self):
        """Getting subgraph including adjacent nodes"""
        graph = UndirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'], include_adjacent_nodes=True)
        assert (len(subgraph.nodes) == 4
            and 'Milani' in subgraph.nodes
            and 'Adrian' in subgraph.nodes
            and 'Diana' in subgraph.nodes
            and 'Presley' in subgraph.nodes
            and len(subgraph.edges) == 3
            and tuple(sorted(('Adrian', 'Milani'))) in subgraph.edges
            and tuple(sorted(('Adrian', 'Diana'))) in subgraph.edges
            and tuple(sorted(('Presley', 'Adrian'))) in subgraph.edges)

    def test_recalculate_calculated_attributes(self):
        """Getting subgraph with automatically recalculation calculated
        attributes (default behavior)
        """
        graph = UndirectedGraph()
        graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
        graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
        graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
        graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
        subgraph = graph.get_subgraph(['Milani', 'Adrian'])
        assert (subgraph.nodes['Milani']['degree'] == 1
            and subgraph.nodes['Milani']['neighbors'] == {'Adrian'}
            and subgraph.nodes['Adrian']['degree'] == 1
            and subgraph.nodes['Adrian']['neighbors'] == {'Milani'})
