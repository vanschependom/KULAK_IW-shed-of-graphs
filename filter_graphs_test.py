import networkx as nx
from filter_graphs import passed_filters, write_history
import matplotlib.pyplot as plt

# generate graphs suitable for testing the process_graphs method
test_graphs = [nx.complete_graph(
    5), nx.complete_graph(6), nx.complete_graph(7)]


def test_passed_graphs():

    filters = {
        "only_degree": {
            "degree": 4
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False

    filters = {
        "max_degree": {
            "degree": 4,
            "amount": 1
        }
    }

    assert passed_filters(test_graphs[0], filters) == False
    assert passed_filters(test_graphs[1], filters) == True
    assert passed_filters(test_graphs[2], filters) == True

    filters = {
        "min_degree": {
            "degree": 4,
            "amount": 1
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False

    filters = {
        "min_degree": {
            "degree": 4,
            "amount": 5
        },
        "exact_degree": {
            "degree": 4,
            "amount": 5
        }
    }

    assert passed_filters(test_graphs[0], filters) == True
    assert passed_filters(test_graphs[1], filters) == False
    assert passed_filters(test_graphs[2], filters) == False


if __name__ == "__main__":
    test_passed_graphs()
    # todo test_write_history()
    # todo test_process_graphs()
    print("All tests passed.")
    # exit
    exit(0)
