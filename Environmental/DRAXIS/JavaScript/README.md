## Javascript Crawlers

General instructions for installing Node.js and running JavaScript crawlers with Kafka's producers/consumers.

Information about the javascript crawlers and the relevant data can be found in deliverable 5.1 here: https://zenodo.org/record/3385992#.XYirLCj7RnI 
and deliverable 5.2 here: https://zenodo.org/record/3386009#.XYirMCj7RnI.   


### Getting started with Node.js

#### Prerequisites

You need to install nodejs and npm for running crawlers.

- Linux
  
  Node.js v10.x:
  
  ```
  # Using Ubuntu
  curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
  sudo apt-get install -y nodejs

  # Using Debian, as root
  curl -sL https://deb.nodesource.com/setup_10.x | bash -
  apt-get install -y nodejs
  Optional: install build tools
  ```
  
  To compile and install native addons from npm you may also need to install build tools:

  ```
  # use `sudo` on Ubuntu or run this as root on debian
  apt-get install -y build-essential
  ```

- Windows and mac

  Download the executable from [https://nodejs.org/en/](https://nodejs.org/en/) and run it

  This will install nodejs and npm in your system.

<br>
After cloning the project 

`cd /path/to/DRAXIS/JavaScript && npm install` to install all the necessary libraries.

### Running Node.JS crawlers in Dell's cloud

To run the crawlers in Dell's cloud [follow the instructions](../Python/README.md#dell-cloud) about signing certificates and
properly configure the environment variables.

### Running Node.JS crawlers as stand alone

Rename `.env.example` file to `.env` at the parent folder (`/path/to/DRAXIS/`) and set the appropriate values.
If you will run Kafka/Elasticsearch locally for testing purposes, you won't probably have set up SSL, so you need to end up with an `.env` as the following:

```
KAFKA_HOST=kafka_host
KAFKA_PORT=kafka_port

ES_HOST=es_host
ES_PORT=es_port

DRAXIS_API_WEATHER_FORECAST_URL=weather_forecast_draxis_api_url
API_KEY=draxis_api_key
``` 

#### Create Topics and Elasticsearch indices

Before any messages can be sent to a topic, it has to be created first.
Also some Elasticsearch indices require special mapping for their fields such as `geo_point`.

To initialize the Kafka topics and the Elasticsearch indices there are scripts per pilot.
E.g for the Cork pilot you run:

`node lib/ElasticSearch/InitCORK.js`

#### Start Consumer(s)

You can start the main consumer by issuing command 

`node lib/Kafka/KafkaMainConsumer.js`

This consumer will listen for all the topics in the Kafka cluster.

#### Invoke Producer
Open another terminal and run the producer to send data to the corresponding Kafka topic by issuing command (for example for the anta_soc_visitors_monthly_draxis ES index).

`node anta_soc_visitors_monthly_draxis.js`
