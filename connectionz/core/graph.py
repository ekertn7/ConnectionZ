"""Graph implementation"""

from typing import Iterable
from abc import ABC, abstractmethod
from connectionz.core.identifier import Identifier, generate_identifier
from connectionz.core.nodes import Nodes
from connectionz.core.edges import Edges
from connectionz.exceptions.cannot_delete_basic_elements_exceptions import (
    CanNotDeleteNodesException,
    CanNotDeleteEdgesException)
from connectionz.exceptions.object_already_exists_exceptions import (
    NodeAlreadyExistsException,
    EdgeAlreadyExistsException)
from connectionz.exceptions.object_isnot_exists_exceptions import (
    NodeIsNotExistsException,
    CoupleIsNotExistsException,
    EdgeIsNotExistsException)
from connectionz.exceptions.validation_exceptions import (
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


class Graph(ABC):
    """Graph implementation"""

    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        self.nodes = nodes
        self.edges = edges

        self.calc_degree()
        self.find_neighbors()

    def __repr__(self):
        description = self.describe()

        # graph type
        graph_type = description['type'].replace('Graph', ' Graph')

        if description['multi_graph'] is True:
            graph_type = f'Multi {graph_type}'

        if description['pseudo_graph'] is True:
            graph_type = f'Pseudo {graph_type}'

        if description['complete_graph'] is True:
            graph_type = f'Complete {graph_type}'

        # number of nodes
        nodes_number = description['number_of_nodes']
        if nodes_number == 0:
            nodes_message = 'without nodes'
        elif nodes_number == 1:
            nodes_message = f'with {nodes_number} node'
        else:
            nodes_message = f'with {nodes_number} nodes'

        # number of couples
        couples_number = description['number_of_couples']
        if couples_number == 0 and nodes_number == 0:
            couples_message = 'couples'
        elif couples_number == 0:
            couples_message = 'without couples'
        elif couples_number == 1:
            couples_message = f'{couples_number} couple'
        else:
            couples_message = f'{couples_number} couples'

        # number of edges
        edges_number = description['number_of_edges']
        if edges_number == 0:
            edges_message = 'edges'
        elif edges_number == 1:
            edges_message = f'{edges_number} edge'
        else:
            edges_message = f'{edges_number} edges'

        # message
        message = (
            f'{graph_type} {nodes_message}, {couples_message} and '
            f'{edges_message}')

        return message

    @property
    def nodes(self):
        """Nodes getter"""
        return self.__nodes

    @nodes.setter
    def nodes(self, new_nodes: Nodes):
        """Nodes setter"""
        self.__nodes = {}
        self._nodes_validation(new_nodes)

    @nodes.deleter
    def nodes(self):
        """Nodes deleter"""
        raise CanNotDeleteNodesException()

    def _nodes_validation(self, nodes) -> Nodes:
        """Validation function for nodes"""

        def check_node_identifier_type() -> None:
            """Checks that type of node identifier is Identifier"""
            if not all(isinstance(identifier, Identifier) for identifier in nodes):
                raise WrongTypeOfNodeIdentifierException()

        def check_node_attributes_type() -> None:
            """Checks that type of node attributes is dict"""
            if not all(isinstance(attrs, dict) for attrs in nodes.values()):
                raise WrongTypeOfNodeAttributesException()

        if nodes is None:
            return

        if isinstance(nodes, dict):
            check_node_identifier_type()
            check_node_attributes_type()
            for identifier, attributes in nodes.items():
                self.add_node(identifier=identifier, **attributes)
        elif isinstance(nodes, (list, set, tuple)):
            check_node_identifier_type()
            for identifier in nodes:
                self.add_node(identifier=identifier, replace=True)
        else:
            raise WrongTypeOfNodesException()

    @property
    def edges(self):
        """Edges getter"""
        return self.__edges

    @edges.setter
    def edges(self, new_edges: Edges):
        """Edges setter"""
        self.__edges = {}
        self._edges_validation(new_edges)

    @edges.deleter
    def edges(self):
        """Edges deleter"""
        raise CanNotDeleteEdgesException()

    def _edges_validation(self, edges) -> Edges:
        """Validation function for directed edges"""

        def check_couple_type() -> None:
            """Checks that type of couple is tuple"""
            if not all(isinstance(couple, tuple) for couple in edges):
                raise WrongTypeOfCoupleException()

        def check_couple_len() -> None:
            """Checks that length of couple == 2"""
            if not all(len(couple) == 2 for couple in edges):
                raise WrongLengthOfCoupleException()

        def check_node_identifier_type() -> None:
            """Checks that type of node identifier in couple is Identifier"""
            if not all(
                    isinstance(node_l, Identifier) and isinstance(node_r, Identifier)
                    for (node_l, node_r) in edges):
                raise WrongTypeOfNodeIdentifierInCoupleException()

        def check_multiples_type() -> None:
            """Checks that type of multiple edges is dict"""
            if not all(isinstance(multiples, dict) for multiples in edges.values()):
                raise WrongTypeOfMultipleEdgesException()

        def check_multiples_len() -> None:
            """Checks that length of multiple edges more than 0"""
            if not all(len(multiples) > 0 for multiples in edges.values()):
                raise WrongLengthOfMultipleEdgesException()

        def check_edge_identifier_type():
            """Checks that type of edge identifier is Identifier"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_identifier, Identifier)
                        for edge_identifier in multiples):
                    raise WrongTypeOfEdgeIdentifierException()

        def check_edge_attributes_type():
            """Checks that type of edge attributes is dict"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_attributes, dict)
                        for edge_attributes in multiples.values()):
                    raise WrongTypeOfEdgeAttributesException()

        if edges is None:
            return

        if isinstance(edges, dict):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            check_multiples_type()
            check_multiples_len()
            check_edge_identifier_type()
            check_edge_attributes_type()
            for (node_l, node_r), multiples in edges.items():
                if len(multiples) == 0:
                    self.add_edge(
                        node_l=node_l, node_r=node_r,
                        recalculate_calculated_attributes=False)
                else:
                    for identifier, attributes in multiples.items():
                        try:
                            self.add_edge(
                                node_l=node_l, node_r=node_r,
                                identifier=identifier,
                                recalculate_calculated_attributes=False,
                                **attributes)
                        except EdgeAlreadyExistsException:
                            raise DuplicationInEdgeIdentifiersException(node_l, node_r) from None
        elif isinstance(edges, (list, set, tuple)):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            for (node_l, node_r) in edges:
                self.add_edge(
                    node_l=node_l, node_r=node_r,
                    recalculate_calculated_attributes=False)
        else:
            raise WrongTypeOfEdgesException()

    def __eq__(self, other):
        """Equal (==) dunder method

        Explanation
        -----------
            - try self.__eq__(other)
            - if it returns NotImplemented, try other.__eq__(self)
            - if it returns NotImplemented, return self is other
        """
        if not isinstance(other, self.__class__.__bases__):
            return NotImplemented
        return type(self) is type(other) and \
            self.nodes == other.nodes and \
            self.edges == other.edges

    def __ne__(self, other):
        """Not equal (!=) dunder method

        Explanation
        -----------
            - try self.__eq__(other)
            - if it returns NotImplemented, return NotImplemented
            - if it returns value, return not value
        """
        equal = self.__eq__(other)
        if equal == NotImplemented:
            return NotImplemented
        return not equal

    def __len__(self):
        """Returns the number of nodes in the graph"""
        return len(self.nodes)

    def add_node(
        self, identifier: Identifier = None, replace: bool = False,
        **attributes) -> Identifier:
        """Adds node to the graph

        Parameters
        ----------
        identifier, optional
            Node identifier
                - None (default): assigned an automatically generated identifier
                - ...: assigned selected identifier, raise
                    WrongTypeOfNodeIdentifierException if wrong type of node
                    identifier specified
        replace, optional
            Replace existing node
                - True: replace existing node by new
                - False (default): raise NodeAlreadyExistsException if node exists
        attributes, optional
            Node attributes

        Returns
        -------
            Node identifier
        """

        # validate identifier
        if identifier is None:
            identifier = generate_identifier()
        else:
            if not isinstance(identifier, Identifier):
                raise WrongTypeOfNodeIdentifierException()

        # actions if (node exists)
        if self.nodes.get(identifier) is not None:
            if replace is False:
                raise NodeAlreadyExistsException()
            if replace is True:
                replaceable_node_degree = self.nodes[identifier].get('degree')
                if replaceable_node_degree is not None:
                    attributes['degree'] = replaceable_node_degree
                replaceable_node_neighbors = self.nodes[identifier].get('neighbors')
                if replaceable_node_neighbors is not None:
                    attributes['neighbors'] = replaceable_node_neighbors
        # actions if (node not exists)
        self.nodes[identifier] = attributes

        return identifier

    def del_node(
            self, identifier: Identifier,
            recalculate_calculated_attributes: bool = True) -> None:
        """Removes node and its incident edges from the graph

        Parameters
        ----------
        identifier
            Node identifier
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, find_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when removing a small number of nodes
                - False: do nothing (best performance)
                    * use it when removing a large number of nodes,
                      then recalculate calculated attributes
        """

        if not isinstance(identifier, Identifier):
            raise WrongTypeOfNodeIdentifierException()

        if self.nodes.get(identifier) is None:
            raise NodeIsNotExistsException()

        # delete incident edges
        incident_edges = [
            couple for couple in self.edges if identifier in couple]
        for couple in incident_edges:
            self.del_edge(*couple, recalculate_calculated_attributes=False)

        # delete node
        del self.nodes[identifier]

        # recalculate calculated attributes
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.find_neighbors()

    def has_node(self, identifier: Identifier) -> bool:
        """Checks that node is in graph"""

        # node validation
        if not isinstance(identifier, Identifier):
            raise WrongTypeOfNodeIdentifierException()

        return identifier in self.nodes

    def clear_nodes(self) -> None:
        """Removes all nodes from the graph"""
        self.nodes = {}
        self.edges = {}

    @abstractmethod
    def _couple_representation(
            self, couple: tuple[Identifier, Identifier]
            ) -> tuple[Identifier, Identifier]:
        """Couple representation for different graph types"""

    def add_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None, replace: bool = False,
            recalculate_calculated_attributes: bool = True,
            **attributes) -> Identifier:
        """Adds an edge and its incident non-existing nodes to the graph

        Parameters
        ----------
        node_l
            Left node identifier
        node_r
            Right node identifier
        identifier, optional
            Edge identifier
                - None (default): assigned an automatically generated identifier
                - ...: assigned selected identifier, raise
                    WrongTypeOfEdgeIdentifierException if wrong type of edge
                    identifier specified
        replace, optional
            Replace existing edge
                - True: replace existing edge by new
                - False (default): raise EdgeAlreadyExistsException if edge exists
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, find_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when adding a small number of edges
                - False: do nothing (best performance)
                    * use it when adding a large number of edges,
                      then recalculate calculated attributes

        Returns
        -------
            Edge identifier
        """

        # validate node identifiers
        if not (isinstance(node_l, Identifier) and isinstance(node_r, Identifier)):
            raise WrongTypeOfNodeIdentifierException()

        # couple representation
        couple = self._couple_representation((node_l, node_r))

        # validate identifier
        if identifier is None:
            identifier = generate_identifier()
        else:
            if not isinstance(identifier, Identifier):
                raise WrongTypeOfEdgeIdentifierException()

        # actions if (edge exists) and (replace is False)
        if self.edges.get(couple) is not None and \
                self.edges.get(couple).get(identifier) is not None:
            if replace is False:
                raise EdgeAlreadyExistsException()
        # actions if (edge not exists) or (edge exists and replace is True)
        self.edges[couple] = self.edges.get(couple) or {}
        self.edges[couple][identifier] = attributes

        # add non-existent incident nodes
        try:
            self.add_node(node_l, replace=False)
        except NodeAlreadyExistsException:
            pass
        try:
            self.add_node(node_r, replace=False)
        except NodeAlreadyExistsException:
            pass

        # recalculate calculated values
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.find_neighbors()

        return identifier

    def del_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None,
            recalculate_calculated_attributes: bool = True) -> None:
        """Removes an edge from the graph

        Parameters
        ----------
        node_l
            Left node identifier
        node_r
            Right node identifier
        identifier
            Edge identifier
                - None (default): removes all edges incident with source and target nodes
                - ...: removes selected edge, raise
                    WrongTypeOfEdgeIdentifierException if wrong type of edge
                    identifier specified, raise EdgeIsNotExistsException if
                    selected edge not exists
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, find_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when removing a small number of edges
                - False: do nothing (best performance)
                    * use it when removing a large number of edges,
                      then recalculate calculated attributes
        """

        # nodes validation
        if not (isinstance(node_l, Identifier) and isinstance(node_r, Identifier)):
            raise WrongTypeOfNodeIdentifierException()

        # couple representation
        couple = self._couple_representation((node_l, node_r))

        # couple validation
        if self.edges.get(couple) is None:
            raise CoupleIsNotExistsException()

        # delete couple
        if identifier is None:
            del self.edges[couple]
        else:
            # edge validation
            if not isinstance(identifier, Identifier):
                raise WrongTypeOfEdgeIdentifierException()
            if self.edges.get(couple).get(identifier) is None:
                raise EdgeIsNotExistsException()
            # delete edge
            del self.edges[couple][identifier]

        # clear calculated attributes
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.find_neighbors()

    def has_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None) -> bool:
        """Checks that couple and edge is in graph"""

        # nodes validation
        if not (isinstance(node_l, Identifier) and isinstance(node_r, Identifier)):
            raise WrongTypeOfNodeIdentifierException()

        # couple representation
        couple = self._couple_representation((node_l, node_r))

        if identifier is None:
            return couple in self.edges
        # edge validation
        if not isinstance(identifier, Identifier):
            raise WrongTypeOfEdgeIdentifierException()
        if couple in self.edges:
            return identifier in self.edges[couple]
        return False

    def clear_edges(self) -> None:
        """Removes all edges from the graph"""
        self.edges = {}

        self.clear_degree()
        self.clear_neighbors()

    def get_subgraph(
            self, selected_nodes: Iterable[Identifier],
            include_adjacent_nodes: bool = False):
        """Returns subgraph with selected nodes

        Parameters
        ----------
        selected_nodes
            Iterable object with node identifiers
        include_adjacent_nodes, optional
            Include nodes adjacent to nodes from selected nodes
                - True: include adjacent nodes
                - False (default): include nodes only from selected nodes

        Returns
        -------
            Subgraph
        """

        # intersection of selected nodes and existing nodes
        selected_nodes = set(selected_nodes) & set(self.nodes)

        # initialise subgraph
        subgraph = self.__class__()

        def _condition(include_adjacent_nodes, node_l, node_r):
            if include_adjacent_nodes is True:
                return (node_l in selected_nodes) or (node_r in selected_nodes)
            return (node_l in selected_nodes) and (node_r in selected_nodes)

        # fill subgraph by nodes and edges
        for (node_l, node_r), multiples in self.edges.items():
            if _condition(include_adjacent_nodes, node_l, node_r):
                for edge_identifier, edge_attributes in multiples.items():
                    try:
                        subgraph.add_node(
                            identifier=node_l, replace=False, **self.nodes[node_l])
                    except NodeAlreadyExistsException:
                        pass
                    try:
                        subgraph.add_node(
                            identifier=node_r, replace=False, **self.nodes[node_r])
                    except NodeAlreadyExistsException:
                        pass
                    subgraph.add_edge(
                        node_l=node_l, node_r=node_r,
                        identifier=edge_identifier,
                        recalculate_calculated_attributes=False,
                        **edge_attributes)

        # recalculate calculated attributes
        subgraph.calc_degree()
        subgraph.find_neighbors()

        return subgraph

    def clear_degree(self):
        """Set degree value to 0 for each node in graph"""
        for node in self.nodes:
            self.nodes[node]['degree'] = 0

    def calc_degree(self):
        """Calculates degree for each node in graph"""
        self.clear_degree()

        for (node_l, node_r), multiples in self.edges.items():
            self.nodes[node_l]['degree'] += len(multiples)
            self.nodes[node_r]['degree'] += len(multiples)

    def clear_neighbors(self):
        """Set neighbors value to empty set for each node in graph"""
        for node in self.nodes:
            self.nodes[node]['neighbors'] = set()

    @abstractmethod
    def find_neighbors(self):
        """Finds neighbors for each node in graph"""

    def find_loops(self):
        """Finds loops in a graph (when an edge incident to one node)"""
        for (node_l, node_r) in self.edges:
            if node_l == node_r:
                yield (node_l, node_r)

    def check_type(self) -> str:
        """Checks graph type"""
        return self.__class__.__name__

    @abstractmethod
    def check_is_complete(self):
        """Checks that graph is complete"""

    def check_is_pseudo(self):
        """Checks that graph contains at least one loop (and is a pseudograph)"""
        return any(self.find_loops())

    def check_is_multi(self):
        """Checks that graph contains more than one edge between a couple of
        nodes (and is a multigraph)"""
        return any(len(multiples) > 1 for multiples in self.edges.values())

    def describe(self):
        """Returns information about graph"""
        self.calc_degree()
        self.find_neighbors()
        return {
            'type': self.check_type(),
            'number_of_nodes': len(self.nodes),
            'number_of_couples': len(self.edges),
            'number_of_edges': sum(len(multiples) for multiples in self.edges.values()),
            'multi_graph': self.check_is_multi(),
            'pseudo_graph': self.check_is_pseudo(),
            'complete_graph': self.check_is_complete(),
        }
