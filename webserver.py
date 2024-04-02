import subprocess
from flask import Flask, render_template, redirect, url_for
import sys

app = Flask(__name__)


@app.route('/')
def home():
    # redirect to the index page
    print('Redirecting to the index page...')
    return redirect(url_for('index'))


@app.route('/index')
def index():

    last_20 = []
    last_20_passed_graphs = []

    # Read the last line from history.txt
    with open('history.txt', 'r') as file:
        lines = file.readlines()

        # loop over the last 20 lines backwards
        for i in range(1, len(lines)):

            split = lines[-i].strip().split("\t")
            graphs = split[4:]

            # loop over the graphs backwards
            for graph in reversed(graphs):
                if len(last_20) == 20:
                    break
                last_20.append([split[0], split[1], split[2], split[3], graph])
                last_20_passed_graphs.append(graph)

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
