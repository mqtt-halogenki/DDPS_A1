#!/bin/bash
for ((i=0; i <10; i++));do
echo "Experiment no $i"

~/das-bigdata-deployment/frameworks/spark-3.1.1/bin/spark-submit \
--packages co.datamechanics:delight_2.12:latest-SNAPSHOT \
--repositories https://oss.sonatype.org/content/repositories/snapshots \
--conf spark.delight.accessToken.secret=21d2463bbc831c664e20afff2c4b3919772165337b3200b7de87488bed075b52 \
--conf spark.extraListeners=co.datamechanics.delight.DelightListener \
~/DDPS_A1/WC/spark.py /home/ddps2207/DDPS_A1/WC/yelp_dataset_review.txt
done
