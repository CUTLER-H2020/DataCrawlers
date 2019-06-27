# Crawlers for twitter

This folder contains different crawlers for twitter developed in Cutler

## Structure of the folder

There are two types of files:

* Python based crawler
  * TweetCrawler.py, tweet-json2csv.py, tweet-sentiment.py, tweet-wordcloud.py
* Necessary files to directly injest data into HDFS with Flume
  * CORK-SOC_TWITTER.conf: configuration file
  * flume.twitter-0.0.1-SNAPSHOT.jar: twitter connector for flume
  
## Direct injestion into HDFS

Steps to follow:

1.	Establish vpn connection to cloud infrastructure (credentials can be requested from DELL)
2.	Connect to the cloud infrastructure
3.	Create Twitter API keys by following [this guideline](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)
4.	Clone the jar file flume.twitter-0.0.1-SNAPSHOT.jar to 
```
$FLUME_HOME/lib
```
5.	Clone the configuration file CORK-SOC_TWITTER.conf and place it to 
```
$FLUME_HOME/conf
```
6.	Add *API keys*, *keywords* to follow, *geo location* etc in the config file
7.	Specify *HDFS path* to store data
8.	Run the config file from $FLUME_HOME using following script:
```
bin/flume-ng agent --conf conf --conf-file conf/flume-conf.conf --classpath apache-flume-1.9.0-bin/lib/ --name agent -Dflume.root.logger=INFO,console
```
9.	To have flume agent as Daemon service, add *nohup* before the previous script:
```
nohup bin/flume-ng agent --conf conf --conf-file conf/flume-conf.conf --classpath apache-flume-1.9.0-bin/lib/ --name agent -Dflume.root.logger=INFO,console
```


