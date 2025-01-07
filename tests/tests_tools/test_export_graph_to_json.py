"""Tests of function `export_graph_to_json`"""

import os
import json
from datetime import date, datetime
import pytest
from connectionz import DirectedGraph, UndirectedGraph, export_graph_to_json
from connectionz.exceptions import WrongFileExtensionException


@pytest.fixture(scope='function', autouse=False)
def prepare_environment():
    """Preparing environment
        - removing "graph.json" file before and after test
    """
    if os.path.exists('./graph.json'):
        os.remove('./graph.json')

    yield

    os.remove('./graph.json')


class TestsExportDirectedGraphToJSON:
    """Tests of exporting DirectedGraph to JSON file"""

    def test_exception_wrong_file_extension(self):
        """Trying export graph to file with wrong extension"""
        graph = DirectedGraph()
        with pytest.raises(WrongFileExtensionException):
            export_graph_to_json(graph=graph, file_path='./graph.ololo')
        assert not os.path.exists('./graph.ololo')

    @pytest.mark.usefixtures('prepare_environment')
    def test_save_file(self):
        """Saving file"""
        graph = DirectedGraph()
        export_graph_to_json(graph=graph, file_path='./graph.json')
        assert os.path.exists('./graph.json')

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_nodes_attributes_from_tuple_and_set_to_list(self):
        """Converting nodes attributes from tuple and set to list"""
        graph = DirectedGraph()
        graph.add_node(
            'Aria',
            books=('Fluent Python', 'The Mystical Man-Month'),  # tuple -> list
            favorite_numbers={12, 33, 42, 69, 97})  # set -> list
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_nodes = json.load(file)['nodes']

        node_attr_books = saved_nodes['Aria']['books']
        node_attr_favorite_numbers = saved_nodes['Aria']['favorite_numbers']

        assert (isinstance(node_attr_books, list)
            and len(node_attr_books) == 2
            and 'Fluent Python' in node_attr_books
            and 'The Mystical Man-Month' in node_attr_books
            and isinstance(node_attr_favorite_numbers, list)
            and len(node_attr_favorite_numbers) == 5
            and 12 in node_attr_favorite_numbers
            and 33 in node_attr_favorite_numbers
            and 42 in node_attr_favorite_numbers
            and 69 in node_attr_favorite_numbers
            and 97 in node_attr_favorite_numbers)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_nodes_attributes_from_date_and_datetime_to_str(self):
        """Converting nodes attributes from date and datetime to str"""
        graph = DirectedGraph()
        graph.add_node(
            'Orlando',
            birth_datetime=datetime(1998, 11, 23, 8, 32, 54),  # datetime -> str
            wedding_date=date(2022, 8, 16))  # date -> str
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_nodes = json.load(file)['nodes']

        node_attr_birth_datetime = saved_nodes['Orlando']['birth_datetime']
        node_attr_wedding_date = saved_nodes['Orlando']['wedding_date']

        assert (isinstance(node_attr_birth_datetime, str)
            and node_attr_birth_datetime == '1998-11-23 08:32:54'
            and isinstance(node_attr_wedding_date, str)
            and node_attr_wedding_date == '2022-08-16')

    @pytest.mark.usefixtures('prepare_environment')
    def test_conver_couple_to_str_with_delimiter(self):
        """Converting couple of nodes to str with delimiter"""
        graph = DirectedGraph()
        graph.add_edge('Aria', 'Orlando', '6ecd0bf246924c6ab5c2a430691d7710')
        graph.add_edge('Mustafa', 'Ruby', '74f6e00d17f5486e96cb0de9eb439614')
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        assert (len(saved_edges) == 2
            and saved_edges_delimiter.join(('Aria', 'Orlando')) in saved_edges
            and saved_edges_delimiter.join(('Mustafa', 'Ruby')) in saved_edges)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_edges_attributes_from_tuple_and_set_to_list(self):
        """Converting edges attributes from tuple and set to list"""
        graph = DirectedGraph()
        graph.add_edge(
            'Aria', 'Orlando', '430691d77',
            papers=('How to Drive a Nuclear Reactor', 'Biomedical Informatics'),  # tuple -> list
            something={1, 2, 3})  # set -> list
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        couple = saved_edges_delimiter.join(('Aria', 'Orlando'))
        edge_attr_papers = saved_edges[couple]['430691d77']['papers']
        edge_attr_something = saved_edges[couple]['430691d77']['something']

        assert (isinstance(edge_attr_papers, list)
            and len(edge_attr_papers) == 2
            and 'How to Drive a Nuclear Reactor' in edge_attr_papers
            and 'Biomedical Informatics' in edge_attr_papers
            and isinstance(edge_attr_something, list)
            and len(edge_attr_something) == 3
            and 1 in edge_attr_something
            and 2 in edge_attr_something
            and 3 in edge_attr_something)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_edges_attributes_from_date_and_datetime_to_str(self):
        """Converting edges attributes from date and datetime to str"""
        graph = DirectedGraph()
        graph.add_edge(
            'Aria', 'Orlando', '430691d77',
            transaction_date=date(2024, 1, 17),  # date -> str
            transaction_datetime=datetime(2024, 1, 17, 18, 23, 21))  # datetime -> str
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        couple = saved_edges_delimiter.join(('Aria', 'Orlando'))
        edge_attr_transaction_date = saved_edges[couple]['430691d77']['transaction_date']
        edge_attr_transaction_datetime = saved_edges[couple]['430691d77']['transaction_datetime']

        assert (isinstance(edge_attr_transaction_date, str)
            and edge_attr_transaction_date == '2024-01-17'
            and isinstance(edge_attr_transaction_datetime, str)
            and edge_attr_transaction_datetime == '2024-01-17 18:23:21')


class TestsExportUndirectedGraphToJSON:
    """Tests of exporting UndirectedGraph to JSON file"""

    def test_exception_wrong_file_extension(self):
        """Trying export graph to file with wrong extension"""
        graph = UndirectedGraph()
        with pytest.raises(WrongFileExtensionException):
            export_graph_to_json(graph=graph, file_path='./graph.ololo')
        assert not os.path.exists('./graph.ololo')

    @pytest.mark.usefixtures('prepare_environment')
    def test_save_file(self):
        """Saving file"""
        graph = UndirectedGraph()
        export_graph_to_json(graph=graph, file_path='./graph.json')
        assert os.path.exists('./graph.json')

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_nodes_attributes_from_tuple_and_set_to_list(self):
        """Converting nodes attributes from tuple and set to list"""
        graph = UndirectedGraph()
        graph.add_node(
            'Aria',
            books=('Fluent Python', 'The Mystical Man-Month'),  # tuple -> list
            favorite_numbers={12, 33, 42, 69, 97})  # set -> list
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_nodes = json.load(file)['nodes']

        node_attr_books = saved_nodes['Aria']['books']
        node_attr_favorite_numbers = saved_nodes['Aria']['favorite_numbers']

        assert (isinstance(node_attr_books, list)
            and len(node_attr_books) == 2
            and 'Fluent Python' in node_attr_books
            and 'The Mystical Man-Month' in node_attr_books
            and isinstance(node_attr_favorite_numbers, list)
            and len(node_attr_favorite_numbers) == 5
            and 12 in node_attr_favorite_numbers
            and 33 in node_attr_favorite_numbers
            and 42 in node_attr_favorite_numbers
            and 69 in node_attr_favorite_numbers
            and 97 in node_attr_favorite_numbers)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_nodes_attributes_from_date_and_datetime_to_str(self):
        """Converting nodes attributes from date and datetime to str"""
        graph = UndirectedGraph()
        graph.add_node(
            'Orlando',
            birth_datetime=datetime(1998, 11, 23, 8, 32, 54),  # datetime -> str
            wedding_date=date(2022, 8, 16))  # date -> str
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_nodes = json.load(file)['nodes']

        node_attr_birth_datetime = saved_nodes['Orlando']['birth_datetime']
        node_attr_wedding_date = saved_nodes['Orlando']['wedding_date']

        assert (isinstance(node_attr_birth_datetime, str)
            and node_attr_birth_datetime == '1998-11-23 08:32:54'
            and isinstance(node_attr_wedding_date, str)
            and node_attr_wedding_date == '2022-08-16')

    @pytest.mark.usefixtures('prepare_environment')
    def test_conver_couple_to_str_with_delimiter(self):
        """Converting couple of nodes to str with delimiter"""
        graph = UndirectedGraph()
        graph.add_edge('Aria', 'Orlando', '6ecd0bf246924c6ab5c2a430691d7710')
        graph.add_edge('Mustafa', 'Ruby', '74f6e00d17f5486e96cb0de9eb439614')
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        assert (len(saved_edges) == 2
            and saved_edges_delimiter.join(tuple(sorted(('Aria', 'Orlando')))) in saved_edges
            and saved_edges_delimiter.join(tuple(sorted(('Mustafa', 'Ruby')))) in saved_edges)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_edges_attributes_from_tuple_and_set_to_list(self):
        """Converting edges attributes from tuple and set to list"""
        graph = UndirectedGraph()
        graph.add_edge(
            'Aria', 'Orlando', '430691d77',
            papers=('How to Drive a Nuclear Reactor', 'Biomedical Informatics'),  # tuple -> list
            something={1, 2, 3})  # set -> list
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        couple = saved_edges_delimiter.join(tuple(sorted(('Aria', 'Orlando'))))
        edge_attr_papers = saved_edges[couple]['430691d77']['papers']
        edge_attr_something = saved_edges[couple]['430691d77']['something']

        assert (isinstance(edge_attr_papers, list)
            and len(edge_attr_papers) == 2
            and 'How to Drive a Nuclear Reactor' in edge_attr_papers
            and 'Biomedical Informatics' in edge_attr_papers
            and isinstance(edge_attr_something, list)
            and len(edge_attr_something) == 3
            and 1 in edge_attr_something
            and 2 in edge_attr_something
            and 3 in edge_attr_something)

    @pytest.mark.usefixtures('prepare_environment')
    def test_convert_edges_attributes_from_date_and_datetime_to_str(self):
        """Converting edges attributes from date and datetime to str"""
        graph = UndirectedGraph()
        graph.add_edge(
            'Aria', 'Orlando', '430691d77',
            transaction_date=date(2024, 1, 17),  # date -> str
            transaction_datetime=datetime(2024, 1, 17, 18, 23, 21))  # datetime -> str
        export_graph_to_json(graph=graph, file_path='./graph.json')

        with open('./graph.json', 'r', encoding='utf-8') as file:
            saved_graph = json.load(file)
            saved_edges_delimiter = saved_graph['edges_delimiter']
            saved_edges = saved_graph['edges']

        couple = saved_edges_delimiter.join(tuple(sorted(('Aria', 'Orlando'))))
        edge_attr_transaction_date = saved_edges[couple]['430691d77']['transaction_date']
        edge_attr_transaction_datetime = saved_edges[couple]['430691d77']['transaction_datetime']

        assert (isinstance(edge_attr_transaction_date, str)
            and edge_attr_transaction_date == '2024-01-17'
            and isinstance(edge_attr_transaction_datetime, str)
            and edge_attr_transaction_datetime == '2024-01-17 18:23:21')
