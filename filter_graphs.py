import sys
import networkx
import json

# read data from standard in (generated graphs in Graph6 format)
data = sys.stdin.read()
# get the path to the JSON file containing the filters
pathToFilter = sys.argv[1]

print(data)

# check if file exists
try:
    with open(pathToFilter) as json_file:
        filter = json.load(json_file)
except FileNotFoundError:
    print("The filter file was not found. Please provide a valid path.")
    sys.exit(1)

# print the JSON file
print(filter)
# TODO: implement the filters
