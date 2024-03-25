import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime

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

# If the directory exists empty it
files = glob.glob(os.path.join(output_dir, '*'))
for f in files:
    os.remove(f)


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

# Variables for the loop
outputData = []
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
            # The output
            outputData.append(graph)
            
            i += 1
            # Export the graph to the output folder
            output_path = os.path.join(output_dir, f"graph_{i}.png")
            nx.draw_planar(G, with_labels=True)  # draw the graph
            plt.savefig(output_path)  # save the graph
            plt.close()
            print(f"Graph {i} was saved as {output_path}")

if i == 0:
    print("No graphs matched the filters.")
    
    
# HISTORY   
inputNumber = data.count("\n") + 1
outputNumber = i                                        # The output and input numbers for the history file

date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")     # The date for the history file
filterJson = str(filters)                               # The filter for the history file

try:
    file = open("history.txt", "x+")                    # Make a new file with the name history.txt
except:
    file = open("history.txt", "r")                     # If the above code gives an error, (because the file already exists) read the file
history = file.read().splitlines()                      # Split all the lines of all the old history  
                             
w = open("history.txt", "w")
for j in range((i//20)+1):
    w.write(date + "\t" + str(inputNumber) + "\t" + str(outputNumber) + "\t" + filterJson + "\t" + ",".join(outputData[j:j+20]) + "\n")
    # Write the new line and delete an old line
    if len(history) >= 20-j:
        history.pop(0)   
          
for j in history:
    w.write(j + "\n")                                   # Write all the old history back

file.close()
w.close()


