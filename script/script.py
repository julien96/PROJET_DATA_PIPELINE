import sys
from operator import add

from pyspark.sql import SparkSession


if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("CsvTransformation")\
        .getOrCreate()

    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "ElectionCsvs") \
        .option("startingOffsets", "earliest") \
        .option("includeHeaders", "true") \
        .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    df.printSchema()
    df.show(10)

    