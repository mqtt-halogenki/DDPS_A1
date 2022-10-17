from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession
import os
spark = SparkSession\
    .builder\
    .appName("KMeansExample")\
    .getOrCreate()

# $example on$
# Loads data.
#dataset = spark.read.format("libsvm").load(os.getcwd()+'/sample_kmeans_data.txt')
dataset = spark.read.format("csv").load(os.getcwd()+'/f_1901_1978.csv')

# Trains a k-means model.
kmeans = KMeans().setK(2).setSeed(1)
model = kmeans.fit(dataset)

# Make predictions
predictions = model.transform(dataset)

# Evaluate clustering by computing Silhouette score
evaluator = ClusteringEvaluator()

silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

# Shows the result.
centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)
# $example off$

spark.stop()