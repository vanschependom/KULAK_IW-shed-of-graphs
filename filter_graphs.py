import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime


# A method for emptying a given folder
def empty_folder(dir):

    # If the directory exists, empty it
    files = glob.glob(os.path.join(dir, '*'))
    for f in files:
        os.remove(f)


# A method for applying a given set of filters to a given graph
#   @returns True if the graph passes the filter
def passes_filters(graph, filters):
    # Iterate over keys (filter types) and values (filter data) in the filters JSON file (dictionary structure)
    for filterType, filterData in filters.items():
        if filterType == 'only_degree':
            degree = filterData['degree']
            if not all(graph.degree[node] == degree for node in graph.nodes):
                return False
        elif filterType == 'max_degree':
            degree = filterData['degree']
            amount = filterData['amount']
            if sum(1 for node in graph.nodes if graph.degree[node] == degree) > amount:
                return False
        elif filterType == 'min_degree':
            degree = filterData['degree']
            amount = filterData['amount']
            if sum(1 for node in graph.nodes if graph.degree[node] == degree) < amount:
                return False
        elif filterType == 'exact_degree':
            degree = filterData['degree']
            amount = filterData['amount']
            if sum(1 for node in graph.nodes if graph.degree[node] == degree) != amount:
                return False
    return True


# A method for exporting a graph as an image to a given directory, with a given index for the image name
def export_graph_image(graph, index, dir):
    # Export the graph to the output folder
    output_path = os.path.join(dir, f"graph_{index}.png")
    nx.draw_planar(graph, with_labels=True)  # draw the graph
    plt.savefig(output_path)  # save the graph
    plt.close()
    print(f"Graph {index} was saved as {output_path}")


# A method for processing graphs based on a given set of filters in JSON fomrat
def process_graphs(graphs, filters):

    outputData = []
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
            if passes_filters(G, filters):
                # The output
                outputData.append(graph)
                i += 1
                # export the graph image
                export_graph_image(G, i, output_dir)

    if i == 0:
        return None
    else:
        return outputData


# A method for writing the history file
def write_history(inputNumber, passed, filters):

    # The output and input numbers for the history file
    outputNumber = len(passed)

    # The date for the history file
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # The filter for the history file
    jsonString = str(filters)

    # Check if the history file already exists
    try:
        # Make a new file with the name history.txt
        file = open("history.txt", "x+")
    except:
        # If the above code gives an error, (because the file already exists) append to the file
        file = open("history.txt", "a")

    i = 0
    graphsList20 = []

    # Loop over all passed graphs
    while i < outputNumber:
        if i % 20 == 0 and i != 0:
            file.write(date + "\t" + str(inputNumber) + "\t" + str(outputNumber) +
                       "\t" + jsonString + "\t" + ", ".join(graphsList20) + "\n")
            graphsList20 = []
        graphsList20.append(passed[i])
        i += 1

    # Write the remaining graphs
    file.write(date + "\t" + str(inputNumber) + "\t" + str(outputNumber) +
               "\t" + jsonString + "\t" + ", ".join(graphsList20) + "\n")

    # Close the file
    file.close()


if __name__ == "__main__":

    # Read data from standard input (graphs in Graph6 format, generated by plantri)
    data = sys.stdin.read()
    # Get the path to the JSON file containing the filters (passed as command line argument)
    path_to_filter = sys.argv[1]

    # Check if filter file exists
    # If it does, load the json data in variable <filters>
    try:
        with open(path_to_filter) as json_file:
            filters = json.load(json_file)
    # The file doesn't exist yet.
    # Print error to the user.
    except FileNotFoundError:
        print("The filter file was not found. Please provide a valid path.")
        sys.exit(1)

    # Check if the output directory exists, if not create it
    output_dir = "output"
    os.makedirs("output", exist_ok=True)

    # Empty the output directory
    empty_folder(output_dir)

    # Split the data (graphs) by new line
    graphs = data.split('\n')

    passedGraphs = process_graphs(graphs, filters)

    # Write history to history.txt
    write_history(len(graphs), passedGraphs, filters)
