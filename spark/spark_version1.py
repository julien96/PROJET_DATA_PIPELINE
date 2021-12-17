from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean


sc=SparkContext("local","projet")
spark=SparkSession(sc)

df=spark.read.option('header','True').option('delimiter',';').option('inferSchema','True').csv('data/data.csv')
df.printSchema()
df=df.na.drop()
df=df.dropDuplicates()
df.show()



df1=df.filter((df.orientation != "")&(df.parti != "")&(df.score != 0.0))
df1.write.csv('nifi/inputfile/')
df1.show()
df1.groupBy('orientation').count().show()


df1.groupBy('parti').mean('score').show()

