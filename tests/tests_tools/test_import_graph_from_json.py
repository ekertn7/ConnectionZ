"""Tests of function `import_graph_from_json`"""

import os
import pytest
from connectionz import (
    DirectedGraph, UndirectedGraph,
    export_graph_to_json, import_graph_from_json)
from connectionz.exceptions import WrongFileExtensionException


@pytest.fixture(scope='function', autouse=False)
def prepare_environment(request):
    """Preparing environment
        - creating "graph.json" file before test
        - removing "graph.json" file after test
    """
    graph_class = request.param

    if os.path.exists('./graph.json'):
        os.remove('./graph.json')
    graph = graph_class()  # expected DirectedGraph or UndirectedGraph class
    graph.add_node('Aria')
    graph.add_node('Orlando')
    graph.add_edge('Orlando', 'Aria')
    export_graph_to_json(graph=graph, file_path='./graph.json')

    yield

    os.remove('./graph.json')


class TestsImportGraphFromJSON:
    """Tests of importing graph from JSON file"""

    def test_exception_wrong_file_extension(self):
        """Trying import graph from file with wrong extension"""
        with pytest.raises(WrongFileExtensionException):
            graph = import_graph_from_json(file_path='./graph.ololo')
        assert 'graph' not in globals() and 'graph' not in locals()


class TestsImportDirectedGraphFromJSON:
    """Tests of importing DirectedGraph from JSON file"""

    @pytest.mark.parametrize('prepare_environment', [DirectedGraph], indirect=True)
    @pytest.mark.usefixtures('prepare_environment')
    def test_create_right_graph_type(self):
        """Creating right graph type"""
        graph = import_graph_from_json(file_path='./graph.json')
        assert isinstance(graph, DirectedGraph)

    @pytest.mark.parametrize('prepare_environment', [DirectedGraph], indirect=True)
    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_neighbors_to_set(self):
        """Converting nodes attribute "neighbors" from list to set"""
        graph = import_graph_from_json(file_path='./graph.json')
        assert (graph.nodes['Aria']['neighbors'] == set()
            and graph.nodes['Orlando']['neighbors'] == {'Aria'})


class TestsImportUndirectedGraphFromJSON:
    """Tests of importing UndirectedGraph from JSON file"""

    @pytest.mark.parametrize('prepare_environment', [UndirectedGraph], indirect=True)
    @pytest.mark.usefixtures('prepare_environment')
    def test_create_right_graph_type(self):
        """Creating right graph type"""
        graph = import_graph_from_json(file_path='./graph.json')
        assert isinstance(graph, UndirectedGraph)

    @pytest.mark.parametrize('prepare_environment', [UndirectedGraph], indirect=True)
    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_neighbors_to_set(self):
        """Converting nodes attribute "neighbors" from list to set"""
        graph = import_graph_from_json(file_path='./graph.json')
        assert (graph.nodes['Aria']['neighbors'] == {'Orlando'}
            and graph.nodes['Orlando']['neighbors'] == {'Aria'})
