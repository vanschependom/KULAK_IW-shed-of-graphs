import networkx as nx
from filter_graphs import *

# generate graphs suitable for testing the process_graphs method
test_graphs = [nx.complete_graph(
    5), nx.complete_graph(6), nx.complete_graph(7)]


def test_passed_filters_only():

    filters = {
        "only_degree": {
            "degree": 4
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False


def test_passed_filters_max():

    filters = {
        "max_degree": {
            "degree": 4,
            "amount": 1
        }
    }

    assert passed_filters(test_graphs[0], filters) == False
    assert passed_filters(test_graphs[1], filters) == True
    assert passed_filters(test_graphs[2], filters) == True


def test_passed_filters_min():

    filters = {
        "min_degree": {
            "degree": 4,
            "amount": 1
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False


def test_passed_filters_exact():

    filters = {
        "exact_degree": {
            "degree": 4,
            "amount": 5
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False

# TODO: add all tests
#
