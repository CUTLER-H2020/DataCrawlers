# Crawler for maps.me

DUTH's crawler to download data from maps.me
The crawler downloads several information regarding some points of interest for the 4 pilot-cities (Antalya, Antwerp, Cork, Thessaloniki)
The table bellow presents the fields used by the crawler:

| Field on maps.me  | Description |
| ------------- | ------------- |
| Category  | Property category (eg. Entertainment, Shops, Lodging)  |
| Subcategory  | Property sub-category (eg. Cafe, Water Park, Bakery, Clothes shop, Church, Viewpoint)  |
| GPS coordination  | The given GPS coordination (latitude and longitude) for each point of interest  |
| Date  | The date (format: yyyy-mm) the crawler downloaded the data  |


## Getting Started

These instructions will get you a copy of the project up and running on your local machine. The crawler downloads the data from maps.me and ingest them in an elasticsearch index. The crawler then pushes a message into a Apache KAFKAF topic. 

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created: 
```
DATA_ANT_ECO_MAPSME_CRAWLER 
DATA_CRK_ECO_MAPSME_CRAWLER
DATA_ANW_ECO_MAPSME_CRAWLERDATA_THE_ECO_MAPSME_CRAWLER
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
