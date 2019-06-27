# Economic Data Crawlers for CUTLER

This part of the repository gathers all the crawlers for economic data developed for CUTLER, as well as othere related software.

## Structure of the folder

There are folders created for some data sources, so the crawler and other related software, as well as instructions. 
The rest of the crawlers are files listed in this folder, mainly written in python or in R. There is a folder that contains the requirements for those python crawlers.

Description of the folders:

* [eurostat](eurostat/): crawler from eurostat databases
* [immoscoop.be](immoscoop.be/): crawler from immoscoop.be and indexing for elasticsearch, as well as instructions
* [maps.me](maps.me/): crawler from maps.me and indexing for elasticsearch, as well as instructions
* [spitogatos.gr](spitogatos.gr/): crawler from spitogatos.gr and indexing for elasticsearch, as well as instructions
* [requirements](requirements/): requiremenst for python crawlers listed 

Description of the crawlers:

Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.

|Crawler|Language|Origin|Credentials needed| Schedulling|Notes|
| ------------- | ------------- | ------------- | ------------- |------------- |------------|
| [OECD.R](OECD.R)| R |API|||OECD databases|
| [anta_eco_several_codes.py](anta_eco_several_codes.py)| python |EXCEL||||
| [antalya_econ_cityofantalya_city...pasengernumber_monthly.py](antalya_econ_cityofantalya_cityzonepuplictransportationpasengernumber_monthly.py)|  python |EXCEL ||||
| [antalya_econ_cityofantalya_shopsrentearn_year.py](antalya_econ_cityofantalya_shopsrentearn_year.py)|  python|EXCEL||||
| [cork_eco_visitors_daily.py](cork_eco_visitors_daily.py)|  python|EXCEL||||
| [thess_eco_thessalokini_municipality_budget.py](thess_eco_thessalokini_municipality_budget.py)|  python | from URL||Yes||
| [thess_eco_thessalokini_municipality_budget_batch.py](thess_eco_thessalokini_municipality_budget_batch.py)|  python | URL||||
| [thess_eco_thessaloniki_parking_data.py](thess_eco_thessaloniki_parking_data.py)|  python | EXCEL ||||
| [thess_eco_thessaloniki_traffic_fines.p](thess_eco_thessaloniki_traffic_fines.py)|  python | EXCEL ||||

## Python Crawlers
General instructions for python crawlers. Further instructions can be found under each data crawler folder
### Getting started with python
#### Prerequisites
You need to install python3, pip (python package manager) and a virtualenv (a tool to create virtual environments for python)

* For linux
  ```
  sudo apt-get install python3
  sudo apt-get install python3-pip
  sudo pip3 install virtualenv
  ```
* For windows
  * download the executable from [Python.org](https://www.python.org/downloads/) and run it
  * latest versions of python include pip; follow the instructions [here](https://packaging.python.org/tutorials/installing-packages/#id13) to check if it is installed and how to proceed if not
  * install virtualenv with pip
    ```
    pip install virtualenv
    ```
#### Installation
You need to create a virtual environment, activate it and install the corresponding requirements

* For linux 
  * Create and activate the virtual environment *myenv*
    ```
    virtualenv -p python3 myenv
    source myenv/bin/activate
    ```
    After you activate the environment, your command line will reflect the change
  * Install requirements 
    ```
    (myenv) $ pip3 install -r requirements/requirements.txt
    ```
     Corresponding requirements.txt can be found under corresponding  requirements folder.
* For windows
  * Create and activate the virtual environment *myenv* 
    ```
    cd my-project
    virtualenv --python python3 myenv
    .\myenv\Scripts\activate
    ```
    After you activate the environment, your command prompt will be modified to reflect the change
  * Install requirements 
    ```
    (myenv) C:\Path\To\my-project> pip3 install -r requirements/requirements.txt
    ```
     Corresponding requirements.txt can be found under corresponding  requirements folder.

### Running as stand alone

#### Prerequisites
Apart from those detailed in the [Installation](#installation) section, some scripts may need further prerequisites (e.g. certain file located in certain folder, or some credentials for accessing the data in a web page). That information can be found **in each script**. 

#### Run the script
All the python scrips run the same way

```
python3 name_of_the_script.py
```

### Deployment with Hadoop

We use Apache Flume to pass the data from local folder to HDFS of Hadoop cluster. More information at [HadoopDeployment](../HadoopDeployment/)

### Schedulling

Some scripts crawl data from sites that are updated periodically. Those scripts require a cron scheduler based on the corresponding acquisition frequency.

## R Crawlers

### Getting started with R
#### Prerequsites
You need to install [R](https://www.r-project.org/). 
Instructions can be found at [R project webpage](https://cran.r-project.org/doc/FAQ/R-FAQ.html#How-can-R-be-installed_003f). R can be downloaded from [any of these mirrors](https://cran.r-project.org/mirrors.html). Please, select first the mirror and then the correct distribution depending on you operating system.
* Note for linux: R is part of many Linux distributions, you should check with your Linux package management system in addition to the links found in the link above.

#### Installation
Packages can be installed with the R shell. 
```
> install.packages("package_name")
```
Needed packages can be found in each R script
### Running as stand alone

#### Prerequisites
Apart from those detailed in the [Installation](#installation-1) section, some scripts may need further prerequisites (e.g. certain file located in certain folder, or some credentials for accessing the data in a web page). That information can be found in each script. 

#### Run the script

```
Rscript name_of_the_script.R
```
