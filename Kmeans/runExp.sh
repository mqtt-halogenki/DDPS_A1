#!/bin/bash



for ((i=0; i <31; i++));do
echo "Experiment no $i"

./runKmeans.sh $i

done


