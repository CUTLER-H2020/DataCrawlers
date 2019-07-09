# HDFS to ElasticSearch data pipe

**EXPERIMENTAL!!!**

We are testing the usage of Apache Spark for porting data from HDFS to ElasticSearch. Necessary steps:
1.	Establish vpn connection to cloud infrastructure (credentials can be requested from DELL)
2.	Connect to the cloud infrastructure
3.	Clone scratch.scala
4.	Make sure to have all necessary jar files required to connect Apache spark and Elastic search, refer to [ES guide](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html#spark-installation)
5.	Specify the necessary directory paths commented in the scripts
6.	Run spark-shell
7.	Run 
   ```
   :load PATH_TO_FILE.scala
   ```
8.	Verify the indexed data ES data nodes
