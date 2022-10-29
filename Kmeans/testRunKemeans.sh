#!/bin/bash

cd ~/das-bigdata-deployment/frameworks/hadoop-3.2.2

bin/hdfs dfs -mkdir /input
bin/hdfs dfs -put ~/DDPS_A1/Kmeans/dataset.txt /input 

echo "start config mapreduce"
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


chmod 777 ~/DDPS_A1/Kmeans/mapper.py ~/DDPS_A1/Kmeans/reducer.py

cd ../..


####################################
i = 1
echo "start iteration$i"

while :
do
    bin/mapred streaming -input /input/sample_kmeans_data.txt -output /test_KMoutput$i -mapper ~/DDPS_A1/Kmeans/mapper.py -reducer ~/DDPS_A1/Kmeans/reducer.py -file ~/DDPS_A1/Kmeans/centroids.txt
    #####
    rm  -f centroids.txt
    bin/hdfs dfs -copyToLocal /test_KMoutput$i/part-00000 ~/DDPS_A1/Kmeans/centroids.txt

    if [i ]
    