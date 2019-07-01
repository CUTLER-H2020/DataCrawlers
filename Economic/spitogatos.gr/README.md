# Crawler for spitogatos.gr

DUTH's crawler to download data from spitogatos.gr
The crawler downloads several information regarding the house prices for the city of Thessaloniki
The table bellow presents the fields used by the crawler:

| Field on spitogatos.gr  | Description |
| ------------- | ------------- |
| category  | Property category (eg. Commercial, Land)  |
| type  | Property sub-category (eg. Apartment, Studio, Office, Hotel)  |
| Περιοχή (Location)  | Property location (based on Thessaloniki's municipalities)  |
| purpose  | Either Sale or Rent  |
| Τιμή ανά τ.μ. (Price per m²)  | Property price per square meter  |
| Construction year  | Property construction year  |
| date  | The date (format: yyyy-mm) the crawler downloaded the data  |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. The crawler downloads the data from maps.me and ingest them in an elasticsearch index. The crawler then pushes a message into a Apache KAFKAF topic.

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created: 
```
DATA_THE_ECO_SPITOGATOSGR_CRAWLER
```

- elasticsearch - indexes created:
```
thessaloniki-spitogatos
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
