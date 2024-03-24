# Shed of Graphs

## Authors

Vincent Van Schependom  
Arne Claerhout

## Changelog

- 0.0 _(22/04/24)_
  - Project creation
- 1.0 _(22/04/24)_
  - Created `dev` branch
  - Added instructions in `README.md`
  - Started development
- 1.1 _(23/04/24)_
  - Created foundations for `filter_graphs.py`, `generate_graphs.py`
  - Added example `example_filter.json`
  - Updated `requirements.txt`
- 1.2 _(24/03/24)_
  - Added the compiling of plantri
  - Updated `generate_graphs.sh`

## Todo-list

- [ ] **Stage 1**: Filter implementation in Python
  - [ ] Bash script
  - [ ] Python script
- [ ] **Stage 2**: System history (history.txt)
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

Create a **new** virtual environment with the needed dependencies in the folder `hog-venv`, which is ignored by `.gitignore`:

> `python3 -m venv houseofgraphs ./hog-venv`

**Activate** the virtual environment:

> `source hog-venv/bin/activate`

Update dependencies in existing virtual environment

> `pip3 install --upgrade -r requirements.txt`

#### Conda

Create a **new** Conda environment with the needed dependencies:

> `conda create --name shedofgraphs --file requirements.txt`

Activating the environment:

> `conda activate shedofgraphs`

Update dependencies in **existing** Conda virtual environment:

> `conda install --name shedofgraphs --file requirements.txt`

### Installing plantri

Run the following command from within the project folder to compile the plantri file:

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

Run the bash script `generate_graphs.sh`, providing both the desired order of the graphs to be generated, as well as the YAML file that contains the filters to be applied:

> `./generate_graphs.sh <plantri_order> <filter_json>`

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
- `plantri`:
  A compiled C program for generating graphs.
- `example_filter.json`:
  A json file containing an example for how to use the filter format.
