/** - This scripts reads data stored in HDFS directory and indexes it to Elastic Search
- To run this script Apache Spark and respective Elastic Search jars on the host machine where Apache Spark is , are required
- The indexed data can be then used for visualization"""
- This is a generic scripts which can be adapted for different data sources
  */

  /**
  *
  * @ author= Hassan Mehmood
  * @ email = "hassan.mehmood@oulu.fi
  * @ origin = "UbiComp - University of Oulu
  */
 /** Import necessary classes
  *
  */ 
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.SparkConf
import org.elasticsearch.spark._
import org.elasticsearch.spark.sql._
import org.apache.spark.sql.types._
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
val df = spark.read.format("csv").option("header","true").option("mode","DROPMALFORMED").option("inferSchema", "true").load("/zone/aawa/sections_geometry/*.csv")
/** Change the datatypes to match the mapping format of Elastic Search
  *
  */
val df_c = df.selectExpr("cast(section_id as int) section_id", "cast(section_trace as double) section_trace", "cast(section_elevation as double) section_elevation","cast(candlestick_type as int) candlestick_type","cast(river_id as int) river_id"
,"cast(river as string) river","cast(description as string) description" )
/** Verify the Schema
  *
  */
df_c.printSchema

/** Cast the datetime to ISO8601 format
  *
  */
val df_f = df_c.withColumn("created", date_format(col("created").cast(TimestampType), "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))
/** Index to ES
  *
  */
df_f.write.format("org.elasticsearch.spark.sql").save("stations_geometry/amico")
