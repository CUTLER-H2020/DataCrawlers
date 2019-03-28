# Crawler for maps.me

DUTH's crawler to download data from maps.me

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes. See deployment for notes on how to deploy the project on a live system.

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
