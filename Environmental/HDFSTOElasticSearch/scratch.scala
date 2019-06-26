/** - This scripts reads data stored in HDFS directory and indexes it to Elastic Search
- To run this script Apache Spark and respective Elastic Search jars on the host machine where Apache Spark is , are required
- The indexed data can be then used for visualization"""
- This is at the moment very basic scripts and needs further experimentation
*/
/**
  *
  * @ author= Hassan Mehmood
  * @ email = "hassan.mehmood@oulu.fi
  * @ origin = "UbiComp - University of Oulu
  */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.SparkConf
import org.elasticsearch.spark._
import org.elasticsearch.spark.sql._

/** Create a new spark context or use the existing one
  *
  */
val sc = SparkContext.getOrCreate()
/** Create a new spark session or use the existing one
  *
  */
val sparkSession = SparkSession.builder.config(sc.getConf).getOrCreate()
/** Provide format of file and path to HDFS folder
  *
  */
val df = spark.read.format("csv").option("header","true").option("mo de","DROPMALFORMED").option("inferSchema", "true").load("hdfs://ADDRESSofNameNode:8020/path/to/the/folder/")
df.saveToEs("Index_Name/FileName") //stores to ES
