#!/bin/bash

for ((i=0; i <31; i++));do
        echo "----------------------------Experiment no $i------------------------------------"
	cd ~/das-bigdata-deployment/frameworks/hadoop-3.2.2
	cd etc/hadoop


sed -i 's:</configuration>::g'  mapred-site.xml

echo '<property>
  <name>yarn.app.mapreduce.am.env</name>
  <value>HADOOP_MAPRED_HOME=/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2
</value>
</property>

<property>
  <name>mapreduce.map.env</name>
  <value>HADOOP_MAPRED_HOME=/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2
</value>
</property>

<property>
  <name>mapreduce.reduce.env</name>
  <value>HADOOP_MAPRED_HOME=/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2</value>
</property>

<property> 
    <name>mapreduce.application.classpath</name>
    <value>/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/mapreduce/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/mapreduce/lib/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/common/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/common/lib/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/yarn/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/yarn/lib/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/hdfs/*,/home/ddps2207/das-bigdata-deployment/frameworks/hadoop-3.2.2/share/hadoop/hdfs/lib/*</value>
</property>
</configuration>' >> mapred-site.xml
	cd ../..

	bin/hdfs dfs -rm -r /outputwc
	bin/hdfs dfs -mkdir /inputwc 
	bin/hdfs dfs -put ~/DDPS_A1/WC/yelp_dataset_review /inputwc
	bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.2.jar wordcount /inputwc/yelp_dataset_review /outputwc
	bin/hdfs dfs -rm -r /outputwc
done

