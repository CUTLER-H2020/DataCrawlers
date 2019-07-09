# Crawler for immoscoop.be

DUTH's crawler to download data from immoscoop.be
The crawler downloads several information regarding the house prices for the city of Antwerp
The table bellow presents the fields used by the crawler:

| Field on immoscoop.be  | Description |
| ------------- | ------------- |
| Category  | Property category (eg. Apartment, Office, Commercial)  |
| Postal  | Property postal conde  |
| Address  | Property address (if applicable)  |
| Property purpose  | Either Sale or Rent  |
| Price per m²  | Property price per square meter  |
| Construction year  | Property construction year  |
| date  | The date (format: yyyy-mm) the crawler downloaded the data  |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. The crawler downloads the data from immoscoop.be and ingest them in an elasticsearch index. The crawler then pushes a message into a Apache KAFKAF topic. 

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based dist

- Apache KAFKA - needed topics: 
```
DATA_ANW_ECO_IMMOSCOOPEBE_CRAWLER
```

- elasticsearch - needed indexes:
```
antwerp-immoscoop
```

- Install python3 - virtualenv
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
```

- Install tesseract
```
sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
sudo apt install tesseract-ocr
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
