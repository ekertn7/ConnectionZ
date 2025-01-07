"""UndirectedGraph implementation"""

from connectionz.core.identifier import Identifier
from connectionz.core.nodes import Nodes
from connectionz.core.edges import Edges
from connectionz.core.graph import Graph


class UndirectedGraph(Graph):

    """UndirectedGraph implementation

    Nodes representation
    --------------------

    Nodes representation is a dict with:
        - node identifier
        - node attributes

    Nodes representation example:
        {
            'Elizabeth': {'age': 19, 'sex': False},
            'Sebastian': {'age': 21, 'sex': True},
        }

    Edges representation
    --------------------

    Edges representation is a dict with:
        - couple - a sorted tuple with:
            - left node identifier
            - right node identifier
        - multiples (same as in DirectedGraph) - a dict with:
            - edge identifier
            - edge attributes

    Edges representation example:
        {
            ('Elizabeth', 'Sebastian'): {
                '46f893e': {'amount': 1400, 'date': '2024-03-08'},
                '206ij5s': {'amount': 2700, 'date': '2024-07-23'},
                '239af58': {'amount': 1900, 'date': '2024-04-16'},
            },
        }
    """

    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        super().__init__(nodes=nodes, edges=edges)

    def _couple_representation(
            self, couple: tuple[Identifier, Identifier]
            ) -> tuple[Identifier, Identifier]:
        """Couple representation for directed graph"""
        return tuple(sorted(couple))

    def find_neighbors(self):
        """Finds neighbors for each node in graph"""
        self.clear_neighbors()

        for (node_l, node_r) in self.edges:
            self.nodes[node_l]['neighbors'].add(node_r)
            self.nodes[node_r]['neighbors'].add(node_l)

    def check_is_complete(self):
        """Checks that graph is complete

                                                        nodes count * (nodes count - 1)
        Max edges length in complete undirected graph = -------------------------------
                                                                       2
        """
        if len(self.edges) == 0:
            return False
        edges_length = len({
            self._couple_representation((node_l, node_r))
            for (node_l, node_r) in self.edges
            if node_l != node_r})
        max_edges_length = (len(self.nodes) * (len(self.nodes) - 1)) / 2
        return edges_length == max_edges_length
