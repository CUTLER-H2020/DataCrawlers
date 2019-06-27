# Environmantal Data Crawlers for CUTLER

This part of the repository gathers all the crawlers for environmental data developed for CUTLER, as well as othere related software.

## Structure of the folder

There are folders created for some data sources, so the crawler and other related software, as well as instructions. 
The rest of the crawlers are files listed in this folder, mainly written in python or in R. There is a folder that contains the requirements for those python crawlers.

Description of the folders:

* [IMEC Data Crawler](ANT_ENV_IMEC/): java based crawler that gets data from API
* [requirements](requirements/): requiremenst for python crawlers listed


Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.


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
  * Install requirements (corresponding requirements.txt can be found under requirements folder)
    ```
    (myenv) C:\Path\To\my-project> pip3 install -r requirements/requirements.txt
    ```


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

## Java Crawlers
More information under the correponding folder
* [IMEC Data Crawler](ANT_ENV_IMEC/)

## Javascript Crawlers

### Deployment with ElasticSearch
