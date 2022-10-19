import os
from tempfile import TemporaryFile
import tempfile
from turtle import left
from pyspark.sql import SparkSession
from pyspark.ml.functions import vector_to_array
from pyspark.sql.functions import concat_ws,col,split,concat
import pandas as pd
spark = SparkSession.builder.getOrCreate()

train_df = spark.read.format("libsvm")\
        .load(os.getcwd() + '/sample_linear_regression_data.txt')

df1 = train_df.select('label',vector_to_array('features').alias('features'))
df = df1.withColumn('features',concat_ws(', ', col('features')))
df = df.select(split('features',',')).rdd.flatMap(lambda x: x).toDF(schema=["col0","col1","col2","col3","col4","col5","col6","col7","col8","col9"])
# concat(df,train_df)

# convert toe the pandas and conver
df_split = df.toPandas()
df_label = df1.toPandas()
result = pd.concat([df_split,df_label['label']],axis=1)
result.to_csv(r'input.txt',header=None,index=None,sep=',',mode='a')
print(result.head(5))
# df_split.append(df_label['label'],axis=1)
# df.withColumn("LABEL",df1.label).show()
# label = train_df.select('label').show()
# df.join(df1.select('label')).show()
# df1.select('label').join(df,how='left')
# train_df.show()
# ouput as txt
# train_df.write.csv(os.path.join(tempfile.mkdtemp(), 'DFData'))
# train_DF = train_df.toPandas()


spark.stop()