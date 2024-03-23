import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# Read data from standard input (generated graphs in Graph6 format)
data = sys.stdin.read()
# Get the path to the JSON file containing the filters
path_to_filter = sys.argv[1]

# Check if filter file exists
try:
    with open(path_to_filter) as json_file:
        filters = json.load(json_file)
except FileNotFoundError:
    print("The filter file was not found. Please provide a valid path.")
    sys.exit(1)

# Check if the output directory exists, if not create it
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


def apply_filters(graph, filters):
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


# Split the data (graphs) by new line
graphs = data.split('\n')

i = 0

# Iterate over the graphs and apply the filters
for graph in graphs:
    if i > 50:
        print("Processed 50 graphs. Exiting...")
        sys.exit(1)
    if graph:
        # Decode Graph6 format to a NetworkX graph
        G = nx.from_graph6_bytes(graph.encode())
        # Check if the graph matches the filters
        if apply_filters(G, filters):
            i += 1
            # Export the graph to the output folder
            output_path = os.path.join(output_dir, f"graph_{i}.png")
            nx.draw_planar(G, with_labels=True)  # draw the graph
            plt.savefig(output_path)  # save the graph
            plt.close()
            print(f"Graph {i} was saved as {output_path}")

if i == 0:
    print("No graphs matched the filters.")
