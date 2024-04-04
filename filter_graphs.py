import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime
import argparse
from write_history import generate_history, write_history

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
                ((type(filterData['degree']) != int and type(filterData['degree']) != list)
                 or len(filterData) != 1):
                return False

            # Check if the filter type is a type not equal to 'only_degree' but still valid
            # and if the type of the degrees and amount are valid

            elif (filterType in ['max_degree', 'min_degree', 'exact_degree']) \
                and (len(filterData) != 2
                     or (type(filterData['degree']) != int and type(filterData['degree']) != list)
                     or type(filterData['amount']) != int):
                return False

            # If the type was not valid return False
            elif (filterType not in ['max_degree', 'min_degree', 'exact_degree', 'only_degree']):
                return False

        # Only return true if all filters passed!!
        else:
            return True

    except Exception as e:

        # If we get an error somewhere (because, for example, it does not exist), return False
        print(e)
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
        if os.path.isdir(f):
            empty_directory(f)
            os.rmdir(f)
        else:
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


def export_graph_image(G, name, dir, image_format):
    if image_format not in ["png", "jpg", "jpeg", "pdf", "svg"]:
        image_format = "png"
    # Export the graph to the output folder
    output_path = os.path.join(dir, f"{name}.{image_format}")
    nx.draw_planar(G, with_labels=True, node_color="#00BDFF",
                   # draw the graph
                   node_size=500, width=1, edge_color="#161b22", font_color="#161b22", font_weight="bold")
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
thread : int
    The number of the thread.
output_dir : str
    The path to the output directory.
image_format : str
    The format for the exported images.

Returns
-------
list[str]
    A list of Graph6 graphs that passed the filters.
"""


def process_graphs(graphs, filters, thread, output_dir=None, image_format="png"):

    passed = []
    i = 0

    # Iterate over the graphs and apply the filters
    for graph in graphs:

        # Check if the graph is not empty
        if graph:

            # strip the graph of any whitespace
            graph = graph.strip()

            # Decode Graph6 format to a NetworkX graph
            G = nx.from_graph6_bytes(graph.strip().encode())

            # Check if the graph passes the filters
            if passed_filters(G, filters):

                # Append graph to passed graph list
                passed.append(graph)
                # Increment the counter of passed graphs
                i += 1

                # Check if the --export flag is provided
                if output_dir != None:
                    # export the graph image
                    export_graph_image(G, graph, output_dir, image_format)

    # Print the number of graphs that passed the filters
    if i == 0:
        print(f"No graphs passed the filters on tread {thread}.")
        return None
    else:
        print(f"{i} graphs passed the filters on tread {thread}.")
        return passed


"""
A method for writing the passed graphs for this thread to the file <date>.txt.
The date is used as a unique identifier for the generation of multithreaded graphs.

Parameters
----------
passed_graphs : list[str]
    A list of Graph6 graphs that passed the filters.
inputNumber : int
    The number of input graphs.
output_file : str
    The path to the output file.

Returns
-------
None
"""


def thread_report(passed_graphs, inputNumber, output_file):

    try:

        # If the file already exists, append to the file
        file = open(output_file, "a")

    except:

        # If the above code gives an error, (because the file doesn't exist) create the file
        file = open(output_file, "x+")

    # Write the number of input graphs
    file.write(str(inputNumber))

    if passed_graphs != None:
        # Write the passed graphs list
        for i in passed_graphs:
            file.write("\t" + i)

    # Close the file
    file.close()


"""
A method for getting the command line arguments.

Parameters
----------
None

Returns
-------
argparse.Namespace
    An object containing the command line arguments.
"""


def get_command_line_arguments():

    parser = argparse.ArgumentParser(
        description="A script for filtering Graph6 graphs from standard input.")

    # Optional arguments
    parser.add_argument("--filter", type=str,
                        help="Path to the JSON filter (required)")
    parser.add_argument(
        "--export", type=str, help="Path to the export folder, if you want to export the graphs.")
    parser.add_argument(
        "--format", type=str, help="Format for exported graphs. Can be 'png', 'jpg', 'jpeg', 'pdf', 'svg'. Default is 'png'.")
    parser.add_argument(
        "--thread", type=str, help="Thread number, only used for multithreaded graph generation with generate_graphs.sh.")
    parser.add_argument(
        "--date", type=str, help="The unique identifier for the generation of multithreaded graphs using generate_graphs.sh.")
    parser.add_argument(
        "--automatic", action="store_true", help="Flag for automatic mode, used for multithreaded graph generation with generate_graphs.sh.")

    args = parser.parse_args()

    return args


"""
A method for loading the filters from the given path.

Parameters
----------
path_to_filter : str
    The path to the filter file.

Returns
-------
dict
    A dictionary containing the filters in JSON format.
"""


def load_filters(path_to_filter):

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

    return filters


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

    # Get the command line arguments
    cmdln_args = get_command_line_arguments()

    # Read data from standard input (graphs in Graph6 format, generated by plantri)
    data = sys.stdin.read()

    # Split the data (graphs) by new line
    graphs = data.split('\n')

    # Check illegal combinations of arguments
    if (cmdln_args.automatic == True and (cmdln_args.date == None or cmdln_args.thread == None)):
        raise Exception(
            "Please provide the date and thread number when running in automatic mode.")
    if (cmdln_args.filter == None and cmdln_args.export == None):
        raise Exception(
            "Please provide a filter file.")

    # If --threads flag was provided, use it as the thread number
    if cmdln_args.thread:
        thread = cmdln_args.thread
    else:
        thread = 0

    # If filters are provided, load them
    if cmdln_args.filter:
        # Load the filters
        filters = load_filters(cmdln_args.filter)
    else:
        filters = {}

    # Check if --export flag is provided
    if cmdln_args.export:

        # Create the export directory if it doesn't exist and empty it
        os.makedirs(cmdln_args.export, exist_ok=True)
        # empty_directory(cmdln_args.export)

        # Process the graphs and apply the filters, exporting the images
        passedGraphs = process_graphs(
            graphs, filters, thread, cmdln_args.export, cmdln_args.format)

    # The --export flag is not provided
    else:

        # Process the graphs and apply the filters without exporting the images
        passedGraphs = process_graphs(graphs, filters, thread)

    # If running in automatic mode (generate_graphs.sh), write the passed graphs to the output file
    if cmdln_args.automatic == True:

        output_file_name = cmdln_args.date + f"_thread{thread}.txt"

        # write the passed graphs to the output file
        # this is used for multithreaded graph generation
        thread_report(passedGraphs, len(graphs), output_file_name)

    # If running in manual mode, generate the history file only if the --filter flag is provided
    elif cmdln_args.filter:

        history = generate_history(inputNumber=len(
            graphs), passed=passedGraphs, filters=filters)
        write_history(history)

    sys.exit(0)
