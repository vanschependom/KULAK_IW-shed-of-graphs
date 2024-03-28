import networkx as nx
from filter_graphs import *

# generate graphs suitable for testing the process_graphs method
test_graphs = [nx.complete_graph(4), nx.complete_graph(
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


def test_history_1():
    test_graphs = ["HtuIZoM", "HspZhCr", "HspYhCr", "HspZ`Cr", "HspZHCr", "HspZhCp", "H~eMO[L", "HsvJ`Cr", "H{d`gsF", "HtuKI\w"]
    
    filters = {
        "exact_degree": {
            "degree": 4,
            "amount": 5
        }
    }
    
    assert generate_history(10, test_graphs, filters) == [[datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                          10, len(test_graphs), str(filters),
                                                          ", ".join(test_graphs)]]
    
def test_history_2():
    test_graphs = ["HtuIZoM", "HspZhCr", "HspYhCr", "HspZ`Cr", "HspZHCr", "HspZhCp", "H~eMO[L", "HsvJ`Cr", "H{d`gsF", "HtuKI\w"]
    
    filters = {
        "min_degree": {
            "degree": 32,
            "amount": 75
        }
    }
    
    assert generate_history(85, test_graphs, filters) == [[datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                          85, len(test_graphs), str(filters),
                                                          ", ".join(test_graphs)]]
    
def test_history_3():
    test_graphs = ["HtuIZoM", "HspZhCr", "HspYhCr", "HspZ`Cr", "HspZHCr", "HspZhCp", "H~eMO[L", "HsvJ`Cr", "H{d`gsF", "HtuKI\w",
                "HtbAZSx", "HtmMMDk", "Hte]BCf", "H~aI?sN", "Hte\MDb", "H{eIbcM", "HtdBHKX", "H{dBGk[", "HsvI`Cr", "Hut@HKT",
                "HtuK]Tw", "HteMAL|", "H|eKKNx", "HteMMD{", "HteMMDs", "HteMMDk", "HtfKMDw", "HtfKMLw", "HteEI\w", "HtfAYCx",
                   "HtpIHcT", "H|`ooSF", "HteAI\w", "Hs`Iz_p", "Ht`BgwL", "HsfAZCx", "H{``gsL", "HttIXoJ", "H|aMjC]", "HtfAZSp"]

    filters = {
        "max_degree": {
            "degree": 10,
            "amount": 6
        }
    }

    assert generate_history(120, test_graphs, filters) == [[datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                            120, len(test_graphs), str(filters),
                                                            ", ".join(test_graphs[:20])], 
                                                         [datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                            120, len(test_graphs), str(filters),
                                                            ", ".join(test_graphs[20:])]]
    