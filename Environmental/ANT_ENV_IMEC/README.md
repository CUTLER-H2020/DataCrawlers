## Decription

### Folder structure
* [imeccrawler](imeccrawler/): sources of the crawler
* [dist](dist/): All the needed libraries

### Crawler description
Crawler to get data from several sensors in Antwerp from IMEC API:
* from four rain gauges located at the city of Antwerp
* from six οpen water level sensors located at the city of Antwerp
* from three pressure sensors located at the city of Antwerp

|Language|Origin|Credentials needed| Schedulling|Notes|
| ------------- | ------------- | ------------- | ------------- |------------- |
|Java|API|Yes|-| |

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
Compile and run (use rpt.properties file).
```
java -jar ImecCrawler.jar -Dapp.properties="/path/to/properties/rpt.properties"
```

### Integrating with Hadoop

