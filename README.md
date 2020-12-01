
## Before Start
Install miniconda [link](https://docs.conda.io/en/latest/miniconda.html)

## Setup Environment
```bash
$ conda create -n traces python=3.6
$ conda install scapy cartopy
$ pip install geoip2
```

## Activate virtual env
```bash
$ conda activate traces
```

## Create the database
This command will create test.db case exist will overwrite it.

```bash
$ python database.py
```
## Run a trace

```bash
$ sudo python tracer.py www.example.com
```