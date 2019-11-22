# Crawler for maps.me

The crawler collects data from maps.me app (https://maps.me/). It includes information about several point of interest categories (Shops, Food, Attractions, Entertainment etc.) for Thessaloniki, Antalya, Antwerp and Cork. The data is analysed in WP4 to provide insights about the socioeconomic activities in CUTLER pilot cities. 
The table bellow presents the fields used by the crawler:

| Field on maps.me  | Description |
| ------------- | ------------- |
| Category  | Property category (eg. Entertainment, Shops, Lodging)  |
| Subcategory  | Property sub-category (eg. Cafe, Water Park, Bakery, Clothes shop, Church, Viewpoint)  |
| GPS coordination  | The given GPS coordination (latitude and longitude) for each point of interest  |
| Date  | The date (format: yyyy-mm) the crawler downloaded the data  |


## Getting Started

These instructions will get you a copy of the project up and running on your local machine. The crawler downloads the data from maps.me and ingest them in an elasticsearch index. The crawler pushes two messages into a Apache KAFKAF topic, the first for crawling procedure and the second for the ingestion stage. 

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created: 
```
DATA_DOWNLOAD_ANT_ECO_MAPSME_CRAWLER 
DATA_DOWNLOAD_CRK_ECO_MAPSME_CRAWLER
DATA_DOWNLOAD_ANW_ECO_MAPSME_CRAWLER
DATA_DOWNLOAD_THE_ECO_MAPSME_CRAWLER

DATA_INGESTION_ANT_ECO_MAPSME_CRAWLER 
DATA_INGESTION_CRK_ECO_MAPSME_CRAWLER
DATA_INGESTION_ANW_ECO_MAPSME_CRAWLER
DATA_INGESTION_THE_ECO_MAPSME_CRAWLER

ECO_MAPSMECRAWLER_DATAINGESTION_ERROR - to report any software failure
```

- elasticsearch - indexes created:
```
antalya-mapsme-dashboard
antwerp-mapsme-dashboard
cork-mapsme-dashboard
thessaloniki-mapsme-dashboard
```

- Install python3 - virtualenv
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
```

### Installing

1. Create a new virtual enviroment
```
$ virtualenv -p python3 myenv
$ source myenv/bin/activate
```

2. Install requirements

```
(myenv) $ pip3 install -r requirements/requirements.txt
```

3. Run the crawler
```
(myenv) $ python3 main.py
```
