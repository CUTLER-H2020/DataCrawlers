## Description of the crawlers:

Most of the names of the crawlers are descriptive. They contain the name of the city and some reference to the data set they are crawling.

| Crawler | Description                                                                                                               | Language   | Origin    | Credentials needed | Schedulling | Notes                |
| -------------------------------------------------------------------------------------------------|--------------------- | ---------- | --------- | ------------------ | ----------- | -------------------- |
| [CORK_ENV_OPW_WL_15min.js](CORK_ENV_OPW_WL_15min.js)| Collects historic water levels data provided by the OPW for station 19069 Ringaskiddy NMCI. Related to file: CORK_ENV_OPW_WL_15min.xlsx | javascript | EXCEL | -                  | -           | Contains Irish Public Sector Information licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) licence (source http://waterlevel.ie - provided by the Office of Public Works.) Originally available at: http://waterlevel.ie/0000019069/0001/summary/ |
| [ant_env_cityofant_gwl_(draxis).js](<ant_env_cityofant_gwl_(draxis).js>)| Collects historical dataset of groundwater levels on 460 different sites in Antwerp. Related to file: Export_CUTLER_v40.xlsx | javascript | EXCEL | -                  | -           |Data that belong to the City of Antwerp and that are exploited for internal use. They have been provided to CUTLER for research purposes only.|
| [anta_env_airquality_envmin_hourly_(DRAXIS).js](<anta_env_airquality_envmin_hourly_(DRAXIS).js>)| Collects historic data obtained from the Air Quality Measurement Station of the Ministry of Environment from 2018 to 2019. Related to file: anta_air_quality_2018-2019.xlsx| javascript | EXCEL | -                  | -           | Originally available at: http://www.havaizleme.gov.tr/Default.ltr.aspx |
| [anta_env_waterqualityflow_cityofantalya_monthly_draxis.js](anta_env_waterqualityflow_cityofantalya_monthly_draxis.js)|Collects historical monthly data of water quality, flow and velocity from six sampling points of the Duden Brook of Antalya. Related to file: anta_water_quality_flow_2018_2019.xlsx| javascript | EXCEL | -                  | -           |Data that belongs to the Municipality of Antalya and has been provided to CUTLER for research purposes only.|
| [anta_soc_visitors_monthly_draxis.js](anta_soc_visitors_monthly_draxis.js)| Collects data on the number of visitors in Duden Brook of Antalya. Related to file: visitor_numbers.xlsx| javascript | EXCEL| -                  | -           | Needs raw data in file |
| [cork_env_met_w_daily_draxis.js](cork_env_met_w_daily_draxis.js)| Collects historical weather data of Ireland, specifically data from  Station ROCHES POINT. Related to file: CORK_ENV_MET_W_DAILY.xlsx| javascript | EXCEL | -                  | -           |Originally available by Met Éireann at: https://www.met.ie/climate/available-data/historical-data|
| [cork_soc_visitors_daily_draxis.js](cork_soc_visitors_daily_draxis.js)|Collects data on the number of visitors in Camden Fort Meagher of Cork. Related to file: visitor_numbers_cork.xlsx| javascript | EXCEL | -                  | -           |Needs raw data in file |
| [cutler_thess_speedmeasurements_draxis.js](cutler_thess_speedmeasurements_draxis.js)|Collects historic data of vehicles’ speed for four (4) roads of Thessaloniki. Related to folder file: thess_speedmeasurements_files| javascript | EXCEL | -                  | -           |Originally available at: https://www.trafficthessreports.imet.gr/user_signup.aspx|
| [cork_integr_parking.js](cork_integr_parking.js)|Collects data about the possible locations for the construction of parking facilities in Cork. Related to file: cork dash parking data.xlsx | EXCEL | -                | -         | - | Needs raw data in file |
| [cork_integr_visitors.js](cork_integr_visitors.js)|Collects data about the visitors in a Fort nearby Camden Fort Meagher in Cork. Related to file: cork_max_visitors_revenues_yearly.js| EXCEL | -                | -         | -         |Needs raw data in file |
| [rain_1.js](rain_1.js)|Collects measurements from twelve rain gauges located at the city of Antwerp. Related to files: alladata_v20_deel1.xlsx and alladata_v20_deel2.xlsx| EXCEL | - | -         | -         |Data that belong to the City of Antwerp and that are exploited for internal use. They have been provided to CUTLER for research purposes only.|
| [cutler_thess_envparameters.js](cutler_thess_envparameters.js)| Collects historical data on measurement of air pollution from six air quality monitoring stations located at the city of Thessaloniki (Thessaloniki Open Data Portal). Related to file: metriseis.xlsx| EXCEL | -                | -         | -         |Originally available at: https://opendata.thessaloniki.gr/en/dataset/%CE%BC%CE%B5%CF%84%CF%81%CE%AE%CF%83%CE%B5%CE%B9%CF%82-%CE%B4%CE%B7%CE%BC%CE%BF%CF%84%CE%B9%CE%BA%CE%BF%CF%8D-%CE%B4%CE%B9%CE%BA%CF%84%CF%8D%CE%BF%CF%85-%CF%83%CF%84%CE%B1%CE%B8%CE%BC%CF%8E%CE%BD-%CE%B5%CE%BB%CE%AD%CE%B3%CF%87%CE%BF%CF%85-%CE%B1%CF%84%CE%BC%CE%BF%CF%83%CF%86%CE%B1%CE%B9%CF%81%CE%B9%CE%BA%CE%AE%CF%82-%CF%81%CF%8D%CF%80%CE%B1%CE%BD%CF%83%CE%B7%CF%82-%CF%84%CE%BF%CF%85-%CE%B4%CE%AE%CE%BC%CE%BF%CF%85-%CE%B8%CE%B5%CF%83%CF%83%CE%B1%CE%BB%CE%BF%CE%BD%CE%AF%CE%BA%CE%B7%CF%82|

## Javascript Crawlers

```
NOTE:

The below instructions may be inconsistent with the
repository's state.

It will be updated in the near future!
```

General instructions for installing nodejs and running javascript crawlers and producers/consumers

Information about the javascript crawlers and the relevant data can be found in deliverable 5.1 here: https://zenodo.org/record/3385992#.XYirLCj7RnI 
and deliverable 5.2 here: https://zenodo.org/record/3386009#.XYirMCj7RnI.   


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
