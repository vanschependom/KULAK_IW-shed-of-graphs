import subprocess
from flask import Flask, render_template, redirect, url_for
import filter_graphs
import sys

app = Flask(__name__)


@app.route('/')
def home():
    # redirect to the index page
    print('Redirecting to the index page...')
    return redirect(url_for('index'))


@app.route('/index')
def index():

    # Read the last line from history.txt
    with open('history.txt', 'r') as file:
        lines = file.readlines()

        # no history
        if len(lines) == 0:
            return render_template('index.html', timestamp='', input_number='', output_number='', filter_str='', passed_graphs=[])

        # last line = 20 last graphs
        last_line = lines[-1].strip().split('\t')

    # Extract information from the last line (20 last graphs)
    timestamp = last_line[0]
    input_number = last_line[1]
    output_number = last_line[2]
    filter_str = last_line[3]
    passed_graphs = last_line[4:]

    # create a string of passed graphs, seperated by a end of line
    passed_graphs_string = "\n".join(last_line[4:])

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
    return render_template('index.html', timestamp=timestamp, input_number=input_number, output_number=output_number, filter_str=filter_str, passed_graphs=passed_graphs)


if __name__ == '__main__':
    app.run()
