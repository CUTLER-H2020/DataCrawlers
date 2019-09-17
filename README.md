# CUTLER Data Crawlers
This is the official repository of data crawlers and parsers developed for [CUTLER project](https://www.cutler-h2020.eu/).
In this repo you will find the crawlers and their technical documentation. Please, refer also to the [User Manual for Data Crawling Software](https://www.cutler-h2020.eu/download/664). A fairly detailed description of data sources and crawlers is available in deliverables [D3.2](https://www.cutler-h2020.eu/download/520) and [D3.3](https://www.cutler-h2020.eu/download/523) accessible via the [Deliverabels](https://www.cutler-h2020.eu/deliverables/) page of the project website. 


## Project Structure
The crawlers are grouped according to the type of data crawled: 

* [Economic](Economic/) contains crawlers and other software related to economic data as well as instructions to run those
* [Environmental](Environmental/) contains crawlers and other software related to environmental data  as well as instructions to run those
* [Social](Social/) contains crawlers and other software related to social data  as well as instructions to run those

Crawlers have been implemented using different programming languages (R, python, javascript, java). Crawlers are used to inject data either to a Hadoop Distributed File System ([HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html)) or [ElasticSearch](https://www.elastic.co/).  However, most of the crawlers can also be used as stand-alone. You can find more specific documentation under the different folders. 

General information on the deployment in Hadoop:

* [HadoopDeployment](HadoopDeployment/): scripts, configuration files and instructions related to data injestion into/from Hadoop HDFS


