# Daniel Karamitrov
# 10/1/2018

# original template:
#   https://github.com/apache/spark/blob/master/examples/src/main/python/ml/linear_regression_with_elastic_net.py

from pyspark.sql import SparkSession
from pyspark.sql.types import *

sc = SparkSession \
    .builder \
    .appName("example_LinReg") \
    .getOrCreate()

schema = StructType([
    StructField("contactID", StringType(), False),
    StructField("actionID", IntegerType(), False),
    StructField("timestamp", IntegerType(), True),  # technically TimestampType() but we pretend its an int
    StructField("productID", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("moneySpent", IntegerType(), True),
])

csv_df = sc.read.csv('small_dataset_raw.csv', header=True, mode='DROPMALFORMED', schema=schema)
