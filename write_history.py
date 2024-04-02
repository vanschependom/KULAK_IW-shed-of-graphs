
import sys
from datetime import datetime
import json
import os

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


if __name__ == "__main__":

    # Get the date, the unique identifier for the generation of multithreaded graphs
    generation_date = sys.argv[1]

    # Get the filters
    path_to_filter = sys.argv[2]

    # get the number of threads
    thread_number = sys.argv[3]

    with open(path_to_filter) as json_file:
        filters = json.load(json_file)

    # The total number of input graphs
    totalInputNumber = 0

    # The total number of output graphs
    totalOutputNumber = 0

    # The list of passed graphs
    passedGraphs = []

    # loop over all the output files
    for i in range(1, int(thread_number)+1):

        # read the data of the output file, characterised by the generation date
        passed_graph_file = open(f"{generation_date}_thread{i}.txt", "r")

        # get the first line of the file
        first_line = passed_graph_file.readline()

        # Split the first line into the input number and the passed graphs
        threadInputNumber, * \
            threadPassedGraphs = first_line.split("\t")

        # remove the last element of the list, because it is empty
        threadPassedGraphs = threadPassedGraphs[:-1]

        # Add the input number to the total input number
        totalInputNumber += int(threadInputNumber)

        if threadPassedGraphs != None:
            # Add the passed graphs to the total list of passed graphs
            passedGraphs += threadPassedGraphs

        # Add the number of passed graphs to the total output number
        totalOutputNumber += len(threadPassedGraphs)

        # close the file
        passed_graph_file.close()

        # delete the output file
        os.remove(f"{generation_date}_thread{i}.txt")

    # Write the history to the file history.txt
    history = generate_history(totalInputNumber, passedGraphs, filters)

    write_history(history)
