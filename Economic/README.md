# Economic Data Crawlers for CUTLER

This part of the repository gathers all the crawlers for economic data developed for CUTLER, as well as othere related software.

## Structure of the folder

There are folders created for some data sources, so the crawler and other related software, as well as instructions.
The rest of the crawlers are files listed in this folder, mainly written in python or in R.

Description of the folders:

* [eurostat](eurostat/): crawler from eurostat databases
* [immoscoop.be](immoscoop.be/): crawler from immoscoop.be and indexing for elasticsearch, as well as instructions
* [maps.me](maps.me/): crawler from maps.me and indexing for elasticsearch, as well as instructions
* [spitogatos.gr](spitogatos.gr/): crawler from spitogatos.gr and indexing for elasticsearch, as well as instructions

Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.

## Python Crawlers

### Getting started
#### Installation
### Running as stand alone

#### Prerequisites
Apart from those detailed in the [Installation](####Installation) section, some scripts may need further prerequisites (e.g. certain file located in certain folder, or some credentials for accessing the data in a web page). That information can be found in each script. 

#### Run the script
All the python scrips run the same way
```
py name_of_the_script.py
```

### Deployment with Hadoop

## R Crawlers

### Getting started
#### Installation
### Running as stand alone

#### Prerequisites
Apart from those detailed in the [Installation](####Installation) section, some scripts may need further prerequisites (e.g. certain file located in certain folder, or some credentials for accessing the data in a web page). That information can be found in each script. 

#### Run the script

```
OEDC.R
```
