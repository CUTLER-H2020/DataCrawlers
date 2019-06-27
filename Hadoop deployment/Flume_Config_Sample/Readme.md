# Flume Agent Configuration

Sample configuration file needed to use Apache Flume to pass the data from local folder to HDFS of Hadoop cluster. 

Steps:
1.	Clone the sample flume configuration file to $FLUME_HOME/conf
2.	Edit the file to add 
  ```
  /path/to/spooldir
  ```
3.	Add HDFS directory 
  ```
  hdfs://ADDRESS:8020/path/to/hdfs/folder
  ```
4.	Add 
  ```
  /path/to/checkpointdir/and/datadir
  ```
5.	Add additional details commented in the sample config
6.	Save the file and run it using bewlo mentioned shell script
7.	To flume agent as Daemon service add nohup before the following shell scripts (nohup shell_script)
  ```
  bin/flume-ng agent --conf conf --conf-file conf/flume-conf.conf --classpath apache-flume-1.9.0-bin/lib/ --name agent -Dflume.root.logger=INFO,console
  ```
