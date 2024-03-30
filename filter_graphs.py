import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime

"""
A method for checking if the given filters are valid.

Parameters
----------
filters : dict
    A dictionary containing the filters in JSON format.

Returns
-------
bool
    True if the filters are valid, False otherwise.
"""


def are_valid_filters(filters):
    try:
        # Iterate over keys (filter types) and values (filter data) in the filters JSON file (dictionary structure)
        for filterType, filterData in filters.items():

            # Check if the filter type is 'only_degree' and if the type of degree is valid
            if filterType == 'only_degree' and \
                ((type(filterData['degree']) != int or type(filterData['degree']) != list)
                 or len(filterData) != 1):
                return False
            # Check if the filter type is a type not equal to 'only_degree' but still valid
            # and if the type of the degrees and amount are valid
            elif (filterType == 'max_degree' or filterType == 'min_degree' or filterType == 'exact_degree') \
                and ((type(filterData['degree']) != int or type(filterData['amount']) != int or type(filterData['degree']) != list)
                     or len(filterData) != 2):
                return False
            # If the type was not valid return False
            elif (filterType != 'max_degree' and filterType != 'min_degree' and filterType != 'exact_degree' and filterType != 'only_degree'):
                return False
            else:
                return True
    except:
        # If we get an error somewhere (because, for example, it does not exist), return False
        return False


"""
A method for emptying a given directory.

Parameters
----------
dir : str
    The path to the directory to empty.

Returns
-------
None
"""


def empty_directory(dir):

    # If the directory exists, empty it
    files = glob.glob(os.path.join(dir, '*'))
    for f in files:
        os.remove(f)


"""
A method for checking if a given graph passes the given filters.

Parameters
----------
graph : nx.Graph
    A NetworkX graph object.
filters : dict
    A dictionary containing the filters in JSON format.

Returns
-------
bool
    True if the graph passes the filters, False otherwise.
"""


def passed_filters(graph, filters):

    # Iterate over keys (filter types) and values (filter data) in the filters JSON file (dictionary structure)
    for filterType, filterData in filters.items():

        # Check if the filter type is 'only_degree'
        if filterType == 'only_degree':

            degree = filterData['degree']
            for node in graph.nodes:
                if type(degree) == int and graph.degree[node] != degree:
                    return False
                elif type(degree) == list and graph.degree[node] not in degree:
                    return False

        else:

            degree = filterData['degree']
            amount = filterData['amount']

            counter = 0

            for node in graph.nodes:
                if type(degree) == int and graph.degree[node] == degree:
                    counter += 1
                elif type(degree) == list and graph.degree[node] in degree:
                    counter += 1

            if filterType == 'min_degree' and counter < amount:
                return False
            elif filterType == 'max_degree' and counter > amount:
                return False
            elif filterType == 'exact_degree' and counter != amount:
                return False

    return True


"""
A method for exporting a given graph to an image file, in the given directory.

Parameters
----------
G : nx.Graph
    A NetworkX graph object.
index : int
    The index of the graph.
dir : str
    The path to the directory to export the graph image to.

Returns
-------
None
"""


def export_graph_image(G, index, dir):
    # Export the graph to the output folder
    output_path = os.path.join(dir, f"graph_{index}.png")
    nx.draw_planar(G, with_labels=True)  # draw the graph
    plt.savefig(output_path)  # save the graph
    plt.close()


"""
A method for processing a list of graphs, applying the given filters.

Parameters
----------
graphs : list[str]
    A list of graphs in Graph6 format.
filters : dict
    A dictionary containing the filters in JSON format.

Returns
-------
list[str]
    A list of Graph6 graphs that passed the filters.
"""


def process_graphs(graphs, filters):

    passed = []
    i = 0

    # Iterate over the graphs and apply the filters
    for graph in graphs:
        # Too many graphs
        if i >= 200:
            print("Processed 200 graphs. Exiting...")
            break
        if graph:
            # Decode Graph6 format to a NetworkX graph
            G = nx.from_graph6_bytes(graph.encode())
            # Check if the graph passes the filters
            if passed_filters(G, filters):
                # The output
                passed.append(graph)
                i += 1
                # export the graph image
                export_graph_image(G, i, output_dir)

    if i == 0:
        print("No graphs passed the filters.")
        return None
    else:
        print(f"{i} graphs passed the filters.")
        return passed


"""
A method for generating the contents of the history file.

Parameters
----------
inputNumber : int
    The number of input graphs.
passed : list[str]
    A list of Graph6 graphs that passed the filters.
filters : dict
    A dictionary containing the filters in JSON format.

Returns
-------
list[list[str]]
    A list of lists, where each inner list contains the contents of a history file entry.
"""


def generate_history(inputNumber, passed, filters):

    # The date for the history file
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # The filter for the history file
    jsonString = str(filters)

    # If graphs passed the filters, write them to the file
    if passed != None:
        output = []

        # The output and input numbers for the history file
        outputNumber = len(passed)

        i = 0
        graphsList20 = []

        # Loop over all passed graphs
        while i < outputNumber:
            if i % 20 == 0 and i != 0:
                output.append([date, str(inputNumber), str(outputNumber),
                               jsonString, ", ".join(graphsList20)])
                graphsList20 = []
            graphsList20.append(passed[i])
            i += 1

        # add the remaining graphs
        output.append([date, str(inputNumber), str(outputNumber),
                       jsonString, ", ".join(graphsList20)])

        return output

    # If no graphs passed the filters, write NA
    else:
        return [[date, str(inputNumber), "0", jsonString, "NA"]]


"""
A method for writing the history to the file history.txt.

Parameters
----------
history : list[list[str]]
    A list of lists, where each inner list contains the contents of a history file entry.

Returns
-------
None
"""


def write_history(history):
    # Check if the history file already exists
    try:
        # Make a new file with the name history.txt
        file = open("history.txt", "x+")
    except:
        # If the above code gives an error, (because the file already exists) append to the file
        file = open("history.txt", "a")

    # Write all the generated history
    for i in history:
        file.write(i[0] + "\t" + i[1] + "\t" + i[2] +
                   "\t" + i[3] + "\t" + i[4] + "\n")

    # Close the file
    file.close()


"""
The main method of the script.

Parameters
----------
None

Returns
-------
None
"""


if __name__ == "__main__":

    # Read data from standard input (graphs in Graph6 format, generated by plantri)
    data = sys.stdin.read()
    # Get the path to the JSON file containing the filters (passed as command line argument)
    path_to_filter = sys.argv[1]

    # Check if filter file exists
    try:
        # If it does, load the json data in variable <filters>
        with open(path_to_filter) as json_file:
            filters = json.load(json_file)
    except FileNotFoundError:
        # throw an error if the file doesn't exist
        raise ("The filter file does not exist. Please provide a valid filter.")
    except:
        # If we get a different error, this means that the json file is not valid
        raise (
            "The filter file doesn't have a valid format. Please provide a valid filter.")

    # Check if the filter is valid
    if not are_valid_filters(filters):
        # Raise an exception if it isn't
        raise ("The structure of the file is not valid. Please provide a valid filter.")

    # Check if the output directory exists, if not create it
    output_dir = "output"
    os.makedirs("output", exist_ok=True)

    # Empty the output directory
    empty_directory(output_dir)

    # Split the data (graphs) by new line
    graphs = data.split('\n')

    passedGraphs = process_graphs(graphs, filters)

    # Write history to history.txt
    write_history(generate_history(len(graphs), passedGraphs, filters))

    sys.exit(0)
