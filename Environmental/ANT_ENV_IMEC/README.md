## Decription
Crawler to get data from several sensors in Antwerp from IMEC API.
* [imeccrawler](imeccrawler/): sources of the crawler
* [dist](dist/): crawler as an executable jar with all the needed libraries

### Getting started
#### Prerequisites
You need to have Java installed. JavaSE Development Kit for different OS can be downloaded from [here](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
#### Installation
Needed libraries can be found at [dist>lib](dist/lib/)
### Running as stand alone
#### Prerequisites
You need to modify the  following parameters in [rpt.properties](rpt.properties) file:
* output_format = JSON or CSV 
* data_folders_path = path to the folders to which the data will be stored 
* kafka_use = true or false, whether data should be sent to kafka (experimental and requires further development)

#### Run the jar
Compile and run (use rpt.properties file). Alternatively, you can use the already compiled jar file at [dist](dist/) folder
```
java -jar ImecCrawler.jar -Dapp.properties="/path/to/properties/rpt.properties"
```

### Integrating with Hadoop

