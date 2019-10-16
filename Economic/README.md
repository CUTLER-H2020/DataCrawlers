# Economic Data Crawlers for CUTLER

This part of the repository gathers all the crawlers for economic data developed for CUTLER, as well as othere related software.

## Structure of this folder

There are folders created for the crawlers of some data sources, that contain the crawler and other related software, as well as the corresponding instructions. 
The rest of the crawlers are files listed in this folder, mainly written in python or in R. There is a folder that contains the requirements for those python crawlers.

#### Description of the folders:

* [eurostat](eurostat/): crawler from eurostat databases
* [maps.me](maps.me/): crawler from maps.me and indexing for elasticsearch, as well as instructions
* [requirements](requirements/): requiremenst for python crawlers listed 

#### Description of the crawlers:

Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.

|Crawler|Description|Language|Origin|Credentials needed| Schedulling|Notes|
| ------------- |------------- | ------------- | ------------- | ------------- |------------- |------------|
| [OECD.R](OECD.R)|Collects data for the four pilots from OECD statistics related to employment, Labour Force, GDP, GVA and Regional Income| R |API|No|No||
| [anta_eco_several_codes.py](anta_eco_several_codes.py)| Parses economical data from Antalya related to the Dude Waterfall recreation area|python |EXCEL|No|No|Needs raw data in file (private)|
| [antalya_econ_cityofantalya_city...pasengernumber_monthly.py](antalya_econ_cityofantalya_cityzonepuplictransportationpasengernumber_monthly.py)|Parses data from Antalya related to public transportation |  python |EXCEL |No|No|Needs raw data in file (private)|
| [antalya_econ_cityofantalya_shopsrentearn_year.py](antalya_econ_cityofantalya_shopsrentearn_year.py)| Parses data from Antalya related to economical activity in Duden Waterfall Area |  python|EXCEL|No|No|Needs raw data in file (private)|
| [cork_eco_visitors_daily.py](cork_eco_visitors_daily.py)|Collects data related to visitors in the Camden Fort Meagher area|  python|EXCEL|||Needs raw data in file|
| [thess_eco_thessalokini_municipality_budget.py](thess_eco_thessalokini_municipality_budget.py)|Collects updated data from Thessaloniki municipal budget from https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php   |  python | URL|No|Yes||
| [thess_eco_thessalokini_municipality_budget_batch.py](thess_eco_thessalokini_municipality_budget_batch.py)|Collects historical data from Thessaloniki municipal budget from https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php|  python | URL|No|No||
| [thess_eco_thessaloniki_parking_data.py](thess_eco_thessaloniki_parking_data.py)|Collects data related to parking in Thessaloniki|  python | EXCEL |No|No|Needs raw data in file|
| [thess_eco_thessaloniki_traffic_fines.py](thess_eco_thessaloniki_traffic_fines.py)|Collects data related to traffic fines in Thessaloniki|  python | EXCEL |No|No|Needs raw data in file|
| [Eurostat Crawler](eurostat)| The Eurostat Crawler collects data from Eurostat for the four pilot cities, i.e. Antalya, Antwerp, Cork, and Thessaloniki. The data is used in the context of WP4 for economics-related analytics and data visualisations.  |  python | JSON | NO |||
| [Maps.me](maps.me)| The crawler collects data from maps.me app for the pilot cities of Thessaloniki, Antalya, Antwerp and Cork. |  python | NDJSON | NO |||

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
Apart from those detailed in the [Installation](#installation) section, some scripts **may need further prerequisites** (e.g. certain file located in certain folder, or some credentials for accessing the data in a web page). That information can be found **in each script**. 

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

#### Kafka integration with R
The script uses R package [rkafka] (https://cran.r-project.org/web/packages/rkafka/rkafka.pdf)that allows R developers to use the messaging functionalities provided by Apache Kafka. 

#### Run the script

```
Rscript name_of_the_script.R
```
