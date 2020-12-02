
## Before Start
Install miniconda [link](https://docs.conda.io/en/latest/miniconda.html)

Download the geolite2 database [link](https://www.maxmind.com/en/geolite2/signup)

## Setup Environment
```bash
$ conda create -n traces python=3.6
$ conda activate traces
$ conda install scapy cartopy
$ pip install geoip2 dataclasses
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

The following command will create a file like this
*42bc99cb-8387-4918-ab49-5ab574a2b7ab*

```bash
$ sudo python tracer.py www.example.com
```

## Show Trace Map
create map takes two params 

first is the geomaplite.mmdb pathfile
sencod is the file created by tracer.py

```bash
$ python create_map.py /path/to/geolite2.mmdb 42bc99cb-8387-4918-ab49-5ab574a2b7ab

```