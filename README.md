# Shed of Graphs

## Authors

Vincent Van Schependom  
Arne Claerhout

## Version history

- 0.0 _(22/04/24)_
  - Project creation

## Features todo-list

- [ ] **Stage 1**: filter implementation in Python
- [ ] **Stage 2**: system history (history.txt)
- [ ] **Stage 3**: unit testing
- [ ] **Stage 4**: rule expansion
- [ ] **Stage 5**: history file backups
- [ ] **Stage 6**: bash script for multithreading
- [ ] **Stage 7**: exporting graph drawings
- [ ] **Stage 8**: web server
- [ ] **Stage 9**: Docker

## Usage

### Install Python dependencies in virtual environment

#### Pip

Create a **new** virtual environment with the needed dependencies in the folder `hog-venv`, which is ignored by `.gitignore`:

> `python3 -m venv houseofgraphs ./hog-venv`

**Activate** the virtual environment:

> `source hog-venv/bin/activate`

Update dependencies in existing virtual environment

> `pip3 install --upgrade -r requirements.txt`

#### Conda

Create a **new** Conda environment with the needed dependencies:

> `conda conda create --name shedofgraphs --file requirements.txt`

Update dependencies in **existing** Conda virtual environment:

> `conda install --name shedofgraphs --file requirements.txt`

## Contents

- `requirements.txt`:  
  A file containing all Python dependencies that are required, used by the Python virtual environment.
- `README.md`:  
  The file you're reading right now.
- `.gitignore`:  
  A file containing rules about what not to push to the remote repository.
