## Python Crawlers

### Getting started with Python.

#### Prerequisites

You need to install python3, pip (python package manager) and a virtualenv (a tool to create virtual environments for python)

For linux

  - `sudo apt-get install python3`
  - `sudo apt-get install python3-pip`
  - `python3 -m pip install --user virtualenv`
  

For windows
  - Download the executable from [Python.org](https://www.python.org/downloads/) and run it
  - Latest versions of python include pip; follow the [instructions](https://packaging.python.org/tutorials/installing-packages/#id13) to check if it is installed and how to proceed if not
  - Install virtualenv with pip
    
    `
    pip install virtualenv
    `

#### Installation

You need to create a virtual environment, activate it and install the corresponding requirements

- Create and activate the virtual environment _env_
    - `python3 -m virtualenv env`
    - `source env/bin/activate`

- Install requirements
    - `(env) $ pip3 install -r requirements.txt`


### Getting started with running Kafka Consumers, Producers.

The whole idea is that each Kafka Topic or Elasticsearch index you want to populate, you **change directory to it** and 
run it's **consumers** and **producers**.

The structure of our crawlers is organized per Kafka topic / Elasticsearch index.

_Example_

First export in the `PYTHONPATH` the required directory where our elastic.py module is, since it's been used by all of our consumers.

- `export PYTHONPATH=$PYTHONPATH:/path/to/DRAXIS/Python/`

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

---
<a id=local-kafka></a>
If you want to populate the Kafka topic "CORK_ENV_WEATHERFORECAST_DAILY" and it's corresponding elasticsearch 
index "cork_env_waterquality_daily", all you have to do is:

   - `cd /path/to/DRAXIS/Python/cork_env_weatherforecast_daily`
   
   - `python3 consumer.py`
   
   - (Optional): 
   
        If you desire concurrent processing and load balancing in the Kafka cluster
        you can run 2 more consumers (we support up to 3) in seperate terminals 
        
   - In another terminal 
   
        `python3 producer.py`
   
   - Done!

### Running crawlers in Dell's cloud.

In addition to the above procedure, in order the crawlers to work in the cloud infrastructure, there are 
some extra steps **before**.

#### 1. Generation of certificates for Kafka 

We will walkthrough an example for your better understanding.

Generate the required certifications since the Kafka cluster is configured with SSL. 
In order to do this you need the following shell script.

Below is the **example** for **Pilot 3** Kafka

- First create an empty folder in your local machine

    `mkdir kafka-certs-p3`

- Then place the required files `ca-cert`,  `ca-key` which are specific for Pilot 3, in the directory 
we just created `kafka-certs-p3`. These are [files per pilot!](https://jira.draxis.gr/browse/CUTL-104)

- Create also a shell script in this directory, named "`kafka-certs.sh`" and place the following code inside
    
    ```
    #!/bin/bash
    
    IP="172.16.33.30" # IP of node on which you are running Kafka with SSL
    Hostname="cutler-p3-c4-00" # Hostname of node on which you are running Kafka client
    
    # Relative path of the previous two file in accordance with the script
    CA="ca-cert"  # Path to the corresponding ca-cert for Pilot 3 (each pilot has a different CA)
    CAkey="ca-key" # Path to the corresponding ca-cert for Pilot 3 (each pilot has a different CA)
    
    capass="cutlerkafka" # Password of CA. Leave it as is.
    
    
    echo Step 1: Generate a key
    openssl genrsa -out $Hostname.key 2048
    
    echo Step 2: Generate a Certificate Signing Request
    openssl req -new -sha256 -key $Hostname.key -config <( printf "[req]\ndefault_bits = 2048\nprompt = no\ndefault_md = \
    sha256\nreq_extensions = req_ext\ndistinguished_name = dn\n[dn]\nC = IR\nL = Cork\nO = CUTLER\nOU = CUTLER\nCN = \
    $Hostname\n[req_ext]\nsubjectAltName = @alt_names\n[alt_names]\nIP.1 = $IP") -out $Hostname.csr
    
    echo Step 3: Create certificate and key signed by the CA
    openssl x509 -req -in $Hostname.csr -CA $CA -CAkey $CAkey -CAcreateserial -out $Hostname.crt -days 3650 -extfile \
    <(printf "subjectAltName=IP:$IP") -passin pass:$capass
    ```
  
- Run the shell script
    - ```cd kafka-certs-p3```
    - ```./kafka-certs.sh```

- The script generates some files. You should look for `ca-cert`, `cutler-p3-c4-00.crt`, `cutler-p3-c4-00.key`

- Next you should copy these files in a directory inside the server (here we're using the IP of the ES node)
where the crawlers will run,
 in a directory let's say `/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/`.
    
    - First create the directory in the server
        
        `ssh cutleruser@172.16.33.40 "mkdir -p /home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/"`
    
    - Enter password in the prompt
    
    - Copy the files to server
        
        `scp ca-cert cutler-p3-c4-00.crt cutler-p3-c4-00.key cutleruser@172.16.33.40:/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/`
        
#### 2. Setup environment variables to point to the generated certificates

Edit `.env` file accordingly to point the path of the certificates

_Example_ in the `.env` file

```
...
KAFKA_SECURITY_PROTOCOL=SSL
KAFKA_CA_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/ca-cert
KAFKA_CERT_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/cutler-p3-c4-00.crt
KAFKA_KEY_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/cutler-p3-c4-00.key
...
```

Also edit the .env file to point to the Elasticsearch certificate. These certificates are in the Elasticsearch nodes, in a directory
`/etc/elasticsearch/certs/ca.crt`. 

Edit the corresponding variable accordingly and don't forget to include the username and password of Elasticsearch.

```
...
ES_CA_CERTS=/etc/elasticsearch/certs/ca.crt
ES_USER=es_user
ES_PASSWORD=es_password
ES_USE_SSL=True
ES_VERIFY_CERTS=True
... 
```

So you end up with `.env` like the following (just fill in the credentials for `ES_USER`, `ES_PASSWORD` and `API_KEY`):

```
KAFKA_HOST=172.16.33.30
KAFKA_PORT=9093
KAFKA_SECURITY_PROTOCOL=SSL
KAFKA_CA_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/ca-cert
KAFKA_CERT_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/cutler-p3-c4-00.crt
KAFKA_KEY_FILE=/home/cutleruser/kafka-certificates/YOUR_COMPANY_NAME/cutler-p3-c4-00.key

ES_HOST=172.16.33.40
ES_PORT=9200
ES_USE_SSL=True
ES_VERIFY_CERTS=True
ES_USER=es_user
ES_PASSWORD=es_password
ES_CA_CERTS=/etc/elasticsearch/certs/ca.crt

DRAXIS_API_WEATHER_FORECAST_URL=https://api.draxis.gr/weather/meteo/hourly
API_KEY=draxis_api_key
```

Then you can follow the same [steps described](#local-kafka) at section `Getting started with running Kafka Consumers, Producers.`