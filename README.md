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
  - Merged `stage5` with `main`
  - Created `stage6` branch
- 6.1 _(01/04/24)_
  - Created the multithreading functionality
  - Added an explanation to `README.md`

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
- [ ] **Stage 7**: Exporting graph drawings
- [ ] **Stage 8**: Web server
- [ ] **Stage 9**: Docker

## Features

### Graph filtering

Generates graphs of a given order, that comply with a provided set of filters. Click [here](#using-the-graph-filter) to skip to the usage instructions for generating graphs.

The underlying logic is as follows: the bash script `generate_graphs.sh` generates all graphs of the given order using _Plantri_. This script then pipes its output - a bunch of _Graph6_ encoded graphs - to the Python script `filter_graphs.py`, which filters all these graphs based on the given criteria in the `filter.json` file.

#### Multithreading

We also offer the ability to run the script multithreaded. Click [here](#multithreading-1) to skip to the instructions for multithreading,

### History

A history of all filtered graphs is kept in the `history.txt` file. For more information about this file, click [here](#history-1).

#### Backup

We have provided a script, `backup_history.sh`, that makes a backup of the `history.txt` file to the folder `~/.filtered-graphs`. To make this script run every hour, you must [configure it](#configuring-automatic-history-backup) in the cron table.

#### Restoring

If you have configured the history backup, you can also restore `history.txt` from a saved backup in `~/.filtered_graphs` by running `restore_from_backup.sh`. Click [here](#restoring-the-history-from-a-backup) for the instructions on restoring the history file.

## Usage

### Installing Python dependencies in virtual environment

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

Run the following command from within the project folder to compile the Plantri file:

```bash
cc -o plantri -O4 ./plantri54/plantri.c
```

### Graph filter

#### Defining filters

First, create a `filter.json` file, in which you specify which filters you want to apply to the graphs generated by _Plantri_. You can name this file anything you want, just make sure to enter the right name in a [later step](#running-the-script).

Filters have a name and one or two parameters. An overview of allowed filters is given below:

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

#### Running the script

Run the bash script `generate_graphs.sh`, providing both the desired order of the graphs to be generated, as well as the relative path to the `filter.json` file, that contains the filters to be applied:

```bash
./generate_graphs.sh <plantri_order> <path_to_filter>
```

An example is shown below:

```bash
./generate_graphs.sh 8 example_filter.json
```

##### Multithreading

To use multithreading, you have to make use of `generate_graphs.sh` inside of the `multithreaded` directory. This script takes an additional command line argument, where you can provide the desired number of threads.

The extended format now looks like this:

```bash
./multithreaded/generate_graphs.sh <plantri_order> <path_to_filter> <number_of_threads>
```

A multithreaded example, using 4 threads, is shown below:

```bash
./multithreaded/generate_graphs.sh 8 example_filter.json 4
```

### History

After running the bash script correctly for the first time, a `history.txt` file will be created. If the file already exists, the Python script will append entries at the end of this file.

Each entry represents 20 processed graphs using the following format:

> `<timestamp>\t<inputNumber>\t<outputNumber>\t<filter>\t<passedGraphList>`
>
> - `timestamp:` the current time in `%d/%m/%Y %H:%M:%S` format
> - `inputNumber:` the number of graphs generated of the given order by Plantri
> - `outputNumber:` the number of of graphs that passed the provided filter
> - `filter:` the provided JSON filter, parsed as a string
> - `passedGraphList:` a comma-seperated list of the Graph6 representations of graphs that passed the filter

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

<!-- ## Contents

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
- `example_filter.json` and `example_filter_2.json`:
  JSON files containing an example for how to use the filter format.
- `backup_history.sh`: A script for making a backup of the `history.txt` file.
- `restore_from_backup.sh`: A script for restoring the `history.txt` file from a backup in `~/.filtered-graphs` -->
