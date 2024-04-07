# Shed of Graphs

## Authors

Vincent Van Schependom  
Arne Claerhout

## Changelog

<details>

  <summary>
    Click to expand
  </summary>

- 0.0 _(22/04/24)_
  - Project creation
- 1.0 _(22/04/24)_
  - Created `stage1` branch
  - Added instructions in `README.md`
  - Started development
- 1.1 _(23/04/24)_
  - Created foundations for `filter_graphs.py`, `generate_graphs.py`
  - Added example `example_filter.json`
  - Updated `requirements.txt`
- 1.2 _(24/03/24)_
  - Added the compiling of Plantri, since this is system-dependent and we can thus not include the compiled program on this repository.
- 2.0 _(25/03/24)_
  - Merged `stage1` with `main`
  - Created `stage2` branch
  - Added the history implementation
  - Added an explanation to `README.md` about the history of generated graphs
- 2.1 _(26/03/24)_
  - Refactored code in `filter_graphs.py`:
    - Added main method
    - Everything has its own function now; this will make unit testing easier
- 3.0 _(26/03/24)_
  - Merged `stage2` with `main`
  - Created `stage3` branch
- 3.1 _(26/03/24)_
  - Created first tests for `passed_filter()`
- 3.2 _(28/03/24)_
  - Split the history functionality into seperate methods `generate_history()` and `write_history()`
  - Added additional unit tests for filter and history functionality
- 4.0 _(28/03/24)_
  - Merged `stage3` with `main`
  - Created `stage4` branch
- 4.1 _(28/03/24)_
  - Added rule expansion
- 4.2 _(28/03/24)_
  - Added supplementary unit tests for the rule expansion
- 4.3 _(29/03/24)_
  - Added illegal filter detection and corresponding tests
- 4.4 _(30/03/24)_
  - Added docstrings to `filter_graphs.py`
  - Added supplementary illegal filter detection tests
- 5.0 _(30/03/24)_
  - Merged `stage4` with `main`
  - Created `stage5` branch
- 5.1 _(30/03/24)_
  - Added backup functionality (`history_backup.sh`)
  - Added restore functionality (`restore_from_backup.sh`)
  - Added instructions for all new features in `README.md`
- 6.0 _(01/04/24)_
  - Created `stage6` branch
- 6.1 _(01/04/24)_
  - Created the multithreading functionality in seperate folder
  - Added an explanation to `README.md`
- 6.2 _(01/04/24)_
  - Refactored multithreading
    - Removed seperate folder
    - Added optional 3rd command line argument for `generate_graphs.sh` to include the number of threads
    - Reworked the history functionality
  - Commented out the code responsible for exporting graphs
    - This will be added back in a later stage
- 7.0 _(02/04/24)_
  - Merged `stage5` with `main`
  - Merged `stage6` with `main`
  - Created `stage7` branch
- 7.1 _(02/04/24)_
  - Added export functionality
- 7.2 _(02/04/24)_
  - Reworked the `filter_graphs.py` structure
  - Fully revamped `README.md`
- 8.0 _(02/04/24)_
  - Merged `stage7` with `main`
  - Created `stage8` branch
- 8.1 _(02/04/24)_
  - Added basic webserver functionality
    - Added flask code to `webserver.py`
    - Added `index.html` to `/templates`
- 8.2 _(02/04/24)_
  - Extended web server functionality
    - Added `style.css` to `/static/css`
    - Added `/static/fonts`
    - Added feature for displaying images (not pretty yet!)
- 8.3 _(03/04/24)_
  - Improved user interface
  - Fixed bug where the first line in the history file wasn't properly processed
- 8.4 _(04/04/24)_
  - Image deletion over time
  - Minor fixes
- 9.0 _(06/04/24)_
  - Merged `stage8` with `main`
  - Created `stage9` branch
- 9.1 _(07/04/24)_
  - Added Docker container

</details>

## Todo-list

- [x] **Stage 1**: Filter implementation in Python
  - [x] Bash script
  - [x] Python script
- [x] **Stage 2**: System history (history.txt)
  - [x] History functionality
- [x] **Stage 3**: Unit testing
  - [x] Testing functionality
- [x] **Stage 4**: Rule expansion
- [x] **Stage 5**: History file backups
- [x] **Stage 6**: Bash script for multithreading
- [x] **Stage 7**: Exporting graph drawings
- [x] **Stage 8**: Web server
- [x] **Stage 9**: Docker

## Features

### Manual graph filtering

The Python script `filter_graphs.py` takes graphs from the standard input and filters them based on the provided filter in JSON format.

Run `python3 filter_graphs.py --help` to view all required and optional arguments, or click [here](#manual-graph-filtering-1) to skip to the detailed instructions on using this script.

### Automatic graph generation and filtering

We have provided a script, called `generate_graphs.sh`, that does two things:

1. Generate planar graphs of a given degree using _Plantri_
2. Filter these generated graphs with the above mentioned Python script, based on the JSON-format filter provided by the user.

Click [here](#automatic-graph-generation-and-filtering-1) to skip to the usage instructions for this bash script.

#### Multithreading

The automatic mode can also be run in multithreaded mode, to speed up graph generation. Click [here](#multithreading-1) to skip to the usage instructions,

### Filtered graph history

Each time a batch of graphs is filtered by `filter_graphs.py`, a history is kept of all graphs that passed the filter. This batch of graphs can either be manually piped to the Python script by the user themselves, or automatically by `generate_graphs.sh`.

Each entry represents 20 processed graphs using the following format:

> `<timestamp>\t<inputNumber>\t<outputNumber>\t<filter>\t<passedGraphList>`
>
> - `timestamp:` the current time in `%d/%m/%Y %H:%M:%S` format
> - `inputNumber:` the number of graphs generated of the given order by Plantri
> - `outputNumber:` the number of of graphs that passed the provided filter
> - `filter:` the provided JSON filter, parsed as a string
> - `passedGraphList:` a comma-seperated list of the Graph6 representations of graphs that passed the filter

#### (Automatic) history backup

We have provided a bash script, `backup_history.sh`, that makes a backup of the `history.txt` file to the folder `~/.filtered-graphs`.

Click [here](#running-the-backup-script) to skip to the command for running this script or [configure it in the cron table](#configuring-automatic-history-backup) to make it run every hour.

#### Backup restoration

After making a backup of the passed graph history, you can restore this to the `history.txt` file by running `restore_from_backup.sh`. Click [here](#restoring-the-history-from-a-backup) for the instructions on restoring the history file.

### Web server

We provide a web server that displays the 20 last processed graphs. Click [here](#starting-the-web-server) to skip to the instructions for starting the web server using _Flask_.

## Usage

### Installing Python dependencies in virtual environment

In order to run `filter_graphs.py`, you need to install some dependencies. We recommend to create a new virtual Python environment. This way, all required packages are installed at once, using `requirements.txt`.

Click on the package manager of your choice to expand the instructions:

#### Pip

<details>

  <summary>
    Click to expand
  </summary>

Create a **new** virtual environment with the needed dependencies in the folder `sog-venv`, which is ignored by `.gitignore`:

```bash
python3 -m venv shedofgraphs ./sog-venv
```

**Activate** the virtual environment:

```bash
source sog-venv/bin/activate
```

Update dependencies in existing virtual environment

```bash
pip3 install --upgrade -r requirements.txt
```

</details>

#### Conda

<details>

  <summary>
    Click to expand
  </summary>

Create a **new** Conda environment with the needed dependencies:

```bash
conda create --name shedofgraphs --file requirements.txt
```

Activating the environment:

```bash
conda activate shedofgraphs
```

Update dependencies in **existing** Conda virtual environment:

```bash
conda install --name shedofgraphs --file requirements.txt
```

</details>

### Installing Plantri

To use the `generate_graphs.sh` script for automatic planar graph generation and filtering, you will need to compile the Plantri C-program.

Run the following command from within the project folder to run the compilation:

```bash
cc -o plantri -O4 ./plantri54/plantri.c
```

### Defining graph filters

First, create a `filter.json` file, in which you specify which filters you want to apply. You can name this file anything you want, just make sure to enter the right name in a [later step]().

Filters have a name, as well as one or two arguments. An overview of allowed filters is given below:

- **only_degree**
  - The graph can **only** contain vertices with degree(s) _\<degree\>_
  - Arguments:
    - _degree_: either and integer or a list of integers
- **min_degree**
  - The graph must contain **at least** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_: either and integer or a list of integers
    - _amount_: an integer
- **max_degree**
  - The graph must contain **at most** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_: either and integer or a list of integers
    - _amount_: an integer
- **exact_degree**
  - The graph must contain **exactly** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_: either and integer or a list of integers
    - _amount_: an integer

An example for the filterfile in JSON-format is shown below:

> **example_filter.json**
>
> ```json
> {
>   "max_degree": {
>     "degree": 2,
>     "amount": 3
>   },
>   "min_degree": {
>     "degree": 4,
>     "amount": 5
>   }
> }
> ```

Another example - passing a list, instead of an integer, in the `degree` argument - is shown below:

> **example_filter_2.json**
>
> ```json
> {
>   "exact": {
>     "degree": [4, 5],
>     "amount": 10
>   }
> }
> ```

### Manual graph filtering

The Python script `graph_filter.py` filters graphs in Graph6 format - seperated by an end of line character (`\n`) - from the standard input.

This script has a few arguments - both required and optional - which you can consult by running:

```bash
python3 filter_graphs.py --help
```

The following arguments can be provided when running manually:

- `--filter <path_to_filter>`: The path to the JSON filter
- `--export <export_folder>`: The path to the folder, where you want the filtered graphs to be exported to.
- `--format <export_format>`: The format you want the exported graphs to be in. This can be either _jpg, jpeg, svg, png_ or _pdf_. If nothing is provided, the default format is _png_.

**Should not be used** when running `filter_graphs.py` manually:

- `--automatic`: This flag indicates that the script is run automatically by `generate_graphs.sh`.
- `--thread <thread_number>`: This indicates the thread number when running `generate_graphs.sh` multithreaded.
- `--date <generation_date>`: Provides a unique identifier for the output file of each thread.

The last three arguments should only be used by `generate_graphs.sh` - possibly running multithreaded.

#### Example usage

Assume `<command_generating_graph6_graphs>` spits out a series of Graph6 graphs seperated by an end of line character.

The command below saves all graphs that pass the `example_filter.json` filter to `/output_directory` in _.svg_ format:

```bash
<command_generating_graph6_graphs> | python3 filter_graphs.py --filter example_filter.json --export output_directory --format svg
```

### Automatic graph generation and filtering

To generate planar graphs and filter them automatically, run the bash script `generate_graphs.sh`, providing both the desired order of the graphs to be generated, as well as the relative path to the `filter.json` file, that contains the filters to be applied:

```bash
./generate_graphs.sh <plantri_order> <path_to_filter>
```

##### Multithreading

To enable multithreaded execution, you can simply provide a 3rd command line argument, in which you specify the desired number of threads:

```bash
./generate_graphs.sh <plantri_order> <path_to_filter> <number_of_threads>
```

##### Example

In the example below, planar graphs of order 8 are generated, using 4 threads.

```bash
./generate_graphs.sh 8 example_filter.json 4
```

### History

#### Running the backup script

Run the following command to make a backup of the current `history.txt` file:

```bash
./backup_history.sh
```

#### Configuring automatic history backup

Let's configure the hourly backup of the `history.txt` file. Start by editing the cron table using the following command:

```bash
crontab -e
```

Add the following line to the cron table:

```bash
0 * * * * /<working_dir>/backup_history.sh
```

In the command above, `<working_dir>` is the path to your current working directory of this project.

Save and exit the cron table. Afterwards, verify that the crontab was succesfully installed by running the following command:

```bash
crontab -l
```

If you can see the crontab we've just configured, you're all good!

#### Restoring the history from a backup

To restore the history from a saved backup in the `~/.filtered-graphs` folder, simply run:

```bash
./restore_from_backup.sh
```

All available backups will be listed and you will be prompted to select the one you wish to restore.

### Starting the web server

Start by specifying that _Flask_ must run the `webserver.py` script:

```bash
export FLASK_APP=webserver
```

Now start the web server by simply running:

```bash
flask run
```

Great job, you can now visit the web server at on your localhost ([127.0.0.1:5000/index](http://127.0.0.1:5000/index))!

### Running in a Docker container

You can run the webserver from a Docker container as well, by following the steps listed below.

#### 1. Install Docker

Install Docker from [the Docker website](https://www.docker.com/products/docker-desktop/).

#### 2. Create the container

Create the Docker container from `Dockerfile` by running:

```bash
docker build -t webserver .
```

#### 3. Run the container

Run the Docker container with the following command:

```bash
docker run -dp 127.0.0.1:5000:5000 webserver
```

#### 4. Done

Ensure the webserver is running by listing all active containers:

```bash
docker ps
```

If the webserver we have just initialized is listed by the command above, the server is running correctly at [127.0.0.1:5000](127.0.0.1:5000).

#### 5. Stopping the server

Run `docker ps` again to find out the container ID. Then run the command below, replacing `<containerID>` with the container ID from the `docker ps` command.

```bash
docker stop <containerID>
```

## Contents

- `/plantri54`:
  A folder containing the necessary files for compiling the Plantri C program.
- `/static`: A folder containing the necessary files for styling the web server index page.
- `/templates`: A folder containing the HTML template of the web server.
- `.gitignore`:
  A file containing rules about what not to push to the remote repository.
- `backup_history.sh`: A script for making a backup of the `history.txt` file.
- `Dockerfile`: A file for creating the Docker container for the webserver.
- `example_filter.json` and `example_filter_2.json`:
  JSON files containing an example for how to use the filter format.
- `filter_graphs.py`:
  A Python script for filtering graphs.
- `generate_graphs.sh`:
  A bash script for generating and filtering planar graphs.
- `README.md`:
  The file you're reading right now.
- `requirements.txt`:
  A file containing all Python dependencies that are required.
- `restore_from_backup.sh`: A script for restoring the `history.txt` file from a backup in `~/.filtered-graphs`
- `unit_tests.py`: A file containing all Pytest unit tests.
- `webserver.py`: A Python script with the necessary code for running the Flask webserver.
- `write_history.py`: A Python script for writing the history to memory.
