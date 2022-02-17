## Prerequisites
```
pip install jugaad-data
pip install nsetools
```

## Initial DB Setup
```
psql -U postgres -c "DROP DATABASE IF EXISTS stocks;"
psql -U postgres -c "CREATE DATABASE stocks;"
cd setupFiles/
python setup.py
```

## Initial Data Setup
` python generateAllFiles.py -s <start-year> -e <end-year> -n <legacy-stock-code>`
```
python generateAllFiles.py -s 2020 -e 2022 -n ICICIBANK
python loadTables.py
```

## Day to Day Data Loading
` python generateAllFiles.py -y <current-year> -m <current-month> -d <day> -n <legacy-stock-code>`
```
python generateAllFiles.py -y 2022 -m 2 -d 1 -n ICICIBANK
python loadTables.py
```

## Querying DB
```
./stocks.sh
```

## Useful Queries
> queries.sql
