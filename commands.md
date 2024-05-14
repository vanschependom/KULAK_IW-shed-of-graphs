# Demo - verdediging project IW

Commando's

## Virtual environment

```bash
conda activate shedofgraphs
```

## Help file

```bash
python3 filter_graphs.py --help
```

## Manuele filtering

Basic voorbeeld (naar history weggeschreven):

```bash
./plantri -p -g 8 2>/dev/null | python3 filter_graphs.py --filter example_filter.json
```

### Exceptional cases

Geen filter

```bash
./plantri -p -g 10 2>/dev/null | python3 filter_graphs.py
```

Illegale filter

```bash
./plantri -p -g 10 2>/dev/null | python3 filter_graphs.py --filter illegal_filter.json
```

### Export naar pdf

```bash
./plantri -p -g 10 2>/dev/null | python3 filter_graphs.py --filter example_filter_2.json --export naamVanDeOutputFolder --format pdf
```

## Automatische generatie

### Exceptional cases

Geen datum

```bash
./plantri -p -g 10 2>/dev/null | python3 filter_graphs.py --automatic --date today
```

Geen thread nummer

```bash
./plantri -p -g 10 2>/dev/null | python3 filter_graphs.py --automatic --thread 2
```

### Legal cases

Simpel voorbeeld op 1 thread:

```bash
./generate_graphs.sh 11 example_filter_2.json
```

Voorbeeld met 4 threads:

```bash
./generate_graphs.sh 11 example_filter_2.json 5
```

## History

Backup maken:

```bash
./backup_history.sh
```

Restoren:

```bash
./restore_from_backup.sh
```

## Web Server

```bash
export FLASK_APP=webserver
```

```bash
flask run
```

Bvb: exact 4,5, amount 10

## Docker

Server @ [127.0.0.1:5000](http://127.0.0.1:5000/)

```bash
docker build -t webserver .
```

```bash
docker run -dp 127.0.0.1:5000:5000 webserver
```

```bash
docker ps
```

```bash
./stopdocker <ID>
```
