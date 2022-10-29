#!/bin/bash
cd ~/das-bigdata-deployment/frameworks/hadoop-3.2.2


bin/hdfs dfs -mkdir /input; bin/hdfs dfs -put ~/DDPS_A1/PageRank/wiki-Vote.txt  /input

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


chmod 777 ~/DDPS_A1/PageRank/mapper.py ~/DDPS_A1/PageRank/reducer.py

cd ../..

hadoop_performance=$(bin/mapred streaming -input /input/wiki-Vote.txt -output /ouputPR -mapper ~/DDPS_A1/PageRank/mapper.py -reducer ~/DDPS_A1/PageRank/reducer.py)

echo $hadoop_performance >> ~/DDPS_A1/PageRank/performance_log.txt
