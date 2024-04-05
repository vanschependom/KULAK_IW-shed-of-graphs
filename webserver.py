import os
import subprocess
from flask import Flask, render_template, redirect, request, url_for
import sys

app = Flask(__name__)


@app.route('/')
def home():
    # redirect to the index page
    print('Redirecting to the index page...')
    return redirect(url_for('index'))


@app.route('/generate', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':

        order = request.form['order']
        filters = request.form['filter']

        # create a filter JSON file from filters variable
        with open('webserver_filters.json', 'w') as file:
            file.write(filters)
            
        # Export the passed graphs to the export_dir
        process = subprocess.Popen(
            [
                './generate_graphs.sh',
                order,
                'webserver_filters.json'
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()
        sys.stdout.buffer.write(stdout)
        sys.stderr.buffer.write(stderr)

        # delete the filter JSON file
        subprocess.run(['rm', 'webserver_filters.json'])

        return redirect(url_for('index'))


@app.route('/index')
def index():
    
    # We remove all the previously generated images so they don't stack up over time  
    for i in os.listdir("static/images"):
        try:
            if i != ".gitignore":
                os.remove("static/images/" + i)
        except:
            continue
            

    last_20 = []
    last_20_passed_graphs = []

    # If there is no history file, we exit
    # Read the last line from history.txt
    try:
        with open('history.txt', 'r') as file:
            lines = file.readlines()

            # loop over the last 20 lines backwards
            for i in range(1, len(lines)+1):

                split = lines[-i].strip().split("\t")
                graphs = split[4:]

                # loop over the graphs backwards
                for graph in reversed(graphs):
                    if len(last_20) == 20:
                        break
                    last_20.append([split[0], split[1], split[2], split[3], graph])
                    last_20_passed_graphs.append(graph)
    except FileNotFoundError:
        raise FileNotFoundError("No history file found, please generate some graphs or create a history file and try again.")

    # create a string of passed graphs, seperated by a end of line
    passed_graphs_string = "\n".join(last_20_passed_graphs)

    # Export the passed graphs to the export_dir
    process = subprocess.Popen(
        [
            'python3',
            'filter_graphs.py',
            '--export',
            'static/images',
            '--format',
            'svg'
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate(input=passed_graphs_string.encode())
    sys.stdout.buffer.write(stdout)
    sys.stderr.buffer.write(stderr)

    # Render the HTML template
    return render_template('index.html', last_20=last_20)


if __name__ == '__main__':
    app.run()
