# Environmental Data Crawlers for CUTLER

This part of the repository gathers all the crawlers for environmental data developed for CUTLER, as well as othere related software.

## Structure of the folder

There are folders created for some data sources, so the crawler and other related software, as well as instructions.
The rest of the crawlers are files listed in this folder, mainly written in python or in R. There is a folder that contains the requirements for those python crawlers.

Description of the folders:

- [IMEC Data Crawler](ANT_ENV_IMEC/): java based crawler that gets data from API
- [requirements](requirements/): requiremenst for python crawlers listed

Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.

| Crawler                                                                                                                | Language   | Origin    | Credentials needed | Schedulling | Notes                |
| ---------------------------------------------------------------------------------------------------------------------- | ---------- | --------- | ------------------ | ----------- | -------------------- |
| [CORK*ENV* MARINEINSTITUTE1_DAILY_1.py](CORK_ENV_%20MARINEINSTITUTE1_DAILY_1.py)                                       | python     | URL       | -                  | -           | -                    |
| [CORK*ENV* MARINEINSTITUTE2_DAILY_1.py](CORK_ENV_%20MARINEINSTITUTE2_DAILY_1.py)                                       | python     | URL       | -                  | -           | -                    |
| [CORK*ENV* MARINEINSTITUTE2_DAILY_2.py](CORK_ENV_%20MARINEINSTITUTE2_DAILY_2.py)                                       | python     | URL       | -                  | -           | -                    |
| [CORK*ENV* MARINEINSTITUTE2_DAILY_3.py](CORK_ENV_%20MARINEINSTITUTE2_DAILY_3.py)                                       | python     | URL       | -                  | -           | -                    |
| [CORK*ENV* MARINEINSTITUTE2_DAILY_4.py](CORK_ENV_%20MARINEINSTITUTE2_DAILY_4.py)                                       | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_IDO_DAILY_1.py](CORK_ENV_IDO_DAILY_1.py)                                                                     | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_IDO_DAILY_2.py](CORK_ENV_IDO_DAILY_2.py)                                                                     | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_MET_HOURLY_1.py](CORK_ENV_MET_HOURLY%20_1.py)                                                                | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_MET_W_DAILY.py](CORK_ENV_MET_W_DAILY.py)                                                                     | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_NMCI Hourly_3.py](CORK_ENV_NMCI%20_Hourly_3.py)                                                              | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_OPW_EPA_DAILY_1.py](CORK_ENV_OPW_EPA_DAILY_1.py)                                                             | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_OPW_EPA_DAILY_2.py](CORK_ENV_OPW_EPA_DAILY_2.py)                                                             | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_OPW_EPA_DAILY_3.py](CORK_ENV_OPW_EPA_DAILY_3.py)                                                             | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_OPW_MINUTE_1.py](CORK_ENV_OPW_MINUTE_1.py)                                                                   | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_OPW_WL_15min.js](CORK_ENV_OPW_WL_15min.js)                                                                   | javascript | -         | -                  | -           | -                    |
| [CORK_ENV_OPW_WL_15min.py](CORK_ENV_OPW_WL_15min.py)                                                                   | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_SEAI_DAILY_1_1.py](CORK_ENV_SEAI_DAILY_1_1.py)                                                               | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_SEAI_DAILY_1_2.py](CORK_ENV_SEAI_DAILY_1_2.py)                                                               | python     | URL       | -                  | -           | -                    |
| [CORK_ENV_SEAI_DAILY_1_3.py](CORK_ENV_SEAI_DAILY_1_3.py)                                                               | python     | URL       | -                  | -           | -                    |
| [SHAPE_FILE_TO_GEOJSON_CORK&ANTWERP.py](SHAPE_FILE_TO_GEOJSON_CORK&ANTWERP.py)                                         | python     | SHP FILE  |                    |             | shapefile to GeoJSON |  |
| [ant_env_cityofant_gwl.py](ant_env_cityofant_gwl.py)                                                                   | python     | EXCEL     | -                  | -           | -                    | - |
| [ant*env_cityofant_gwl*(draxis).js](<ant_env_cityofant_gwl_(draxis).js>)                                               | javascript | -         | -                  | -           | -                    |
| [ant_env_cityofant_histprec.py](ant_env_cityofant_histprec.py)                                                         | python     | EXCEL     | -                  | -           | -                    |
| [anta*env_airquality_envmin_hourly*(DRAXIS).js](<anta_env_airquality_envmin_hourly_(DRAXIS).js>)                       | javascript | -         | -                  | -           | -                    |
| [anta_env_cityofantalya2_monthly.py](anta_env_cityofantalya2_monthly.py)                                               | python     | EXCEL     | -                  | -           | -                    |
| [anta_env_waterqualityflow_cityofantalya_monthly.py](anta_env_waterqualityflow_cityofantalya_monthly.py)               | python     | EXCEL     | -                  | -           | -                    |
| [anta_env_waterqualityflow_cityofantalya_monthly_draxis.js](anta_env_waterqualityflow_cityofantalya_monthly_draxis.js) | javascript | -         | -                  | -           | -                    |
| [anta_soc_visitors_monthly_draxis.js](anta_soc_visitors_monthly_draxis.js)                                             | javascript | -         | -                  | -           | -                    |
| [antalya_env_cityofantalya_perminute.py](antalya_env_cityofantalya_perminute.py)                                       | python     | URL       | -                  | Yes         | -                    |
| [antalya_env_cityofantalya_perminute_batch.py](antalya_env_cityofantalya_perminute_batch.py)                           | python     | URL       | -                  | -           | -                    |
| [cork_env_met_w_daily_draxis.js](cork_env_met_w_daily_draxis.js)                                                       | javascript | -         | -                  | -           | -                    |
| [cork_soc_visitors_daily_draxis.js](cork_soc_visitors_daily_draxis.js)                                                 | javascript | -         | -                  | -           | -                    |
| [cutler_thess_speedmeasurements_draxis.js](cutler_thess_speedmeasurements_draxis.js)                                   | javascript | -         | -                  | -           | -                    |
| [stations_crawler.js](stations_crawler.js)                                                                             | javascript | -         | -                  | -           | -                    |
| [thess_env_cityofthess_dailyyearly.py](thess_env_cityofthess_dailyyearly.py)                                           | python     | URL+EXCEL | -                  | -           | -                    |
| [thess_env_imet_speed_15min.py](thess_env_imet_speed_15min.py)                                                         | python     | URL+EXCEL | Yes                | Yes         | -                    |
| [thess_env_imet_speed_15min_batch.py](thess_env_imet_speed_15min_batch.py)                                             | python     | URL+EXCEL | Yes                | -           | -                    |

## Python Crawlers

General instructions for python crawlers. Further instructions can be found under each data crawler folder

### Getting started with python

#### Prerequisites

You need to install python3, pip (python package manager) and a virtualenv (a tool to create virtual environments for python)

- For linux
  ```
  sudo apt-get install python3
  sudo apt-get install python3-pip
  sudo pip3 install virtualenv
  ```
- For windows
  - download the executable from [Python.org](https://www.python.org/downloads/) and run it
  - latest versions of python include pip; follow the instructions [here](https://packaging.python.org/tutorials/installing-packages/#id13) to check if it is installed and how to proceed if not
  - install virtualenv with pip
    ```
    pip install virtualenv
    ```

#### Installation

You need to create a virtual environment, activate it and install the corresponding requirements

- For linux
  - Create and activate the virtual environment _myenv_
    ```
    virtualenv -p python3 myenv
    source myenv/bin/activate
    ```
    After you activate the environment, your command line will reflect the change
  - Install requirements
    ```
    (myenv) $ pip3 install -r requirements/requirements.txt
    ```
    Corresponding requirements.txt can be found under corresponding requirements folder.
- For windows
  - Create and activate the virtual environment _myenv_
    ```
    cd my-project
    virtualenv --python python3 myenv
    .\myenv\Scripts\activate
    ```
    After you activate the environment, your command prompt will be modified to reflect the change
  - Install requirements (corresponding requirements.txt can be found under requirements folder)
    ```
    (myenv) C:\Path\To\my-project> pip3 install -r requirements/requirements.txt
    ```

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

## Java Crawlers

More information under the correponding folder

- [IMEC Data Crawler](ANT_ENV_IMEC/)

## Javascript Crawlers

General instructions for installing nodejs and running javascript crawlers and producers/consumers

### Getting started with nodejs

#### Prerequisites

You need to install nodejs and npm for running crawlers.

- For linux

```

sudo apt-get install nodejs

sudo apt-get install nodejs-legacy

sudo apt-get install npm

```

- For windows and MAC

       download the executable from [https://nodejs.org/en/](https://nodejs.org/en/) and run it

  This will install nodejs and npm in your system.

  After successfully install nodejs and npm in your system:
  `cd /project_name && npm install`
  to install all the necessary libraries.

### Running as stand alone

#### Run the script

All the javascript crawlers run the same way

```

node name_of_the_script.js

```

### Consumers / Producers

#### Environment Variables

The following environment variables are required:

- KAFKA_HOST
- ELASTICSEARCH_HOST

If these aren't set, you can create an `.env` file in the root of the project and place them inside there.

#### Create Topics

Before any messages can be sent to a topic, it has to be created first.

1. Edit file `lib/Kafka/KafkaTopics.js` and specify the topics that you want to create. Set "replicationFactor" equal to the number of available brokers. Depending on the amount of data the consumers will process, set the "partitions" for the topic. The data will be split across all partitions and then you can assign a consumer to each partition to process them.

2. Run command `node create_all_topics.js`

#### Start Consumer(s)

You can start a consumer by issuing command `node anta_soc_visitors_monthly_draxis_consumer.js`. You can start as many as you want, each consumer will be responsible for processing the items in a specific partition of the topic.

#### Invoke Producer

Run the producer to send data to the kafka topic by issuing command `node anta_soc_visitors_monthly_draxis_producer.js`
