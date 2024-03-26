# Shed of Graphs

## Authors

Vincent Van Schependom  
Arne Claerhout

## Changelog

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
  - Created `stage2` branch
  - Added the history implementation
  - Added an explantation to `README.md` about the history of generated graphs

## Todo-list

- [x] **Stage 1**: Filter implementation in Python
  - [x] Bash script
  - [x] Python script
- [ ] **Stage 2**: System history (history.txt)
  - [x] History script
- [ ] **Stage 3**: Unit testing
- [ ] **Stage 4**: Rule expansion
- [ ] **Stage 5**: History file backups
- [ ] **Stage 6**: Bash script for multithreading
- [ ] **Stage 7**: Exporting graph drawings
- [ ] **Stage 8**: Web server
- [ ] **Stage 9**: Docker

## Features

### Graph generation

Generates graphs of a given order, that comply with a provided set of filters. Click [here](#using-the-graph-filter) to skip to the usage instructions for generating graphs.

The underlying logic is as follows: the bash script `generate_graphs.sh` generates all graphs of the given order using _Plantri_. This script then pipes its output - a bunch of _Graph6_ encoded graphs - to the Python script `filter_graphs.py`, which filters all these graphs based on the given criteria in the `filter.json` file.

## Usage

### Installing Python dependencies in virtual environment

#### Pip

Create a **new** virtual environment with the needed dependencies in the folder `sog-venv`, which is ignored by `.gitignore`:

> `python3 -m venv shedofgraphs ./sog-venv`

**Activate** the virtual environment:

> `source sog-venv/bin/activate`

Update dependencies in existing virtual environment

> `pip3 install --upgrade -r requirements.txt`

#### Conda

Create a **new** Conda environment with the needed dependencies:

> `conda create --name shedofgraphs --file requirements.txt`

Activating the environment:

> `conda activate shedofgraphs`

Update dependencies in **existing** Conda virtual environment:

> `conda install --name shedofgraphs --file requirements.txt`

### Installing Plantri

Run the following command from within the project folder to compile the Plantri file:

> `cc -o plantri -O4 ./plantri54/plantri.c`

### Using the graph filter

#### Defining filters

First, create a `filter.json` file, in which you specify which filters you want to apply to the graphs generated by _Plantri_.

Filters have a name and one or two parameters. An overview of allowed filters is given below:

- **only_degree**
  - The graph can **only** contain vertices with degree _\<degree\>_
  - Arguments:
    - _degree_
- **min_degree**
  - The graph must contain **at least** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_
    - _amount_
- **max_degree**
  - The graph must contain **at most** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_
    - _amount_
- **exact_degree**
  - The graph must contain **exactly** _\<amount\>_ vertices with degree _\<degree\>_
  - Arguments:
    - _degree_
    - _amount_

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

#### Running the script

Run the bash script `generate_graphs.sh`, providing both the desired order of the graphs to be generated, as well as the JSON file that contains the filters to be applied:

> `./generate_graphs.sh <plantri_order> <filter_json>`

#### Viewing history

After running the bash script with an accepted filter, a file with the name history.txt will be created, if it doesn't exist already. If the file already exists, we will append entries at the end of the file.
Each entry represents 20 processed graphs and will have the following format:

> `<timestamp>\t<inputNumber>\t<outputNumber>\t<filter>\t<passedGraphList>`
>
> - `timestamp` is the current time in `%d/%m/%Y %H:%M:%S` format
> - `inputNumber` is the number of graphs generated of the given order by Plantri
> - `outputNumber` is the number of of graphs that passed the provided filter
> - `filter` is the JSON filter, parsed as a string
> - `passedGraphList` is a comma-seperated list of the Graph6 representations of graphs that passed the filter

## Contents

- `requirements.txt`:
  A file containing all Python dependencies that are required, used by the Python virtual environment.
- `README.md`:
  The file you're reading right now.
- `.gitignore`:
  A file containing rules about what not to push to the remote repository.
- `generate_graphs.sh`:
  A bash script for generating graphs.
- `filter_graphs.py`:
  A Python script for filtering graphs. This file is ran by the bash script that generates graphs.
- `/plantri54`:
  A folder containing the necessary files for compiling the Plantri C program.
- `example_filter.json`:
  A json file containing an example for how to use the filter format.
