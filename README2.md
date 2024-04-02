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
  - Merged `stage5` with main
  - Merged `stage6` with main
  - Created `stage7` branch

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
- [ ] **Stage 8**: Web server
- [ ] **Stage 9**: Docker

## Features

### Graph filtering

The Python script `filter_graphs.py` takes graphs from the standard input and filters them based on the provided filter in JSON format.

Run `python3 filter_graphs.py --help` to view all required and optional arguments, or click [here]() to skip to the detailed instructions on using this script.

### Filtered graph history

Each time a batch of graphs is filtered by `filter_graphs.py`

### Automatic graph generation

We have provided a script, called `generate_graphs.sh`, that does two things:

1. Generate planar graphs of a given degree using _Plantri_
2. Filter these generated graphs with the above mentioned Python script, based on the JSON-format filter provided by the user.

Click [here]() to skip to the usage instructions for this bash script.

## Usage

### Graph filtering
