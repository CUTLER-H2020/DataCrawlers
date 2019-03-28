# Crawler for maps.me

DUTH's crawler to download data from maps.me

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created: 
```
DATA_ANW_ECO_IMMOSCOOPEBE_CRAWLER
```

- elasticsearch - indexes created:
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
