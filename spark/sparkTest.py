from pyspark.sql import Row
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame([Row(a=1, b=2.0, c="sdf")])
print(df.show())
