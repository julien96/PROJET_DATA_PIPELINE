import sys
from operator import add

from pyspark.sql import SparkSession


if __name__ == "__main__":
    CommunesCsvPath = "data/Communes.csv"
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
    
    colsToDel= ["Code du département","Libellé du département","Libellé de la section électorale","Abstentions","% Abs/Ins","% Vot/Ins","Blancs","% Blancs/Ins","% Blancs/Vot","Nuls","% Nuls/Ins","% Nuls/Vot","Exprimés","% Exp/Ins","% Exp/Vot","Libellé Abrégé Liste","% Voix/Exp","Code Officiel EPCI","Nom Officiel EPCI","Localisation"]

    df2 = df.select ([col for col in df.columns if column not in colsToDel])
    df2 = df2.withColumnRenamed('Libellé de la commune','label_com')\
            .withColumnRenamed('Code du b.vote','code_burV')\
            .withColumnRenamed('Libellé Etendu Liste','label_liste')\
            .withColumnRenamed('Nom Tête de Liste','nom_tete_liste')\
            .withColumnRenamed('Nom Officiel Région','nomReg')\
            .withColumnRenamed('Code Officiel Région','codeReg')\
            .withColumnRenamed('"% Voix/Ins"','pourc_voix')
    dfComn = spark.read.format('csv').options(header=True,inferSchema=True).load(CommunesCsvPath)
    dfComn = dfComn.na.drop()
    dfComn = dfComn.dropDuplicates()
    ComnColToDel = ["CODEREG","REG","CODDEP","CODARR","CODCAN","CODCOM","PCAP","PTOT"]
    dfComn2 = dfComn.select ([col for col in dfComn.columns if column not in ComnColToDel])
    dfComn2 = dfComn2.na.drop()
    dfComn2 = dfComn2.dropDuplicates()

    resDf= df2.join(dfComn2, df2.label_com == dfComn2.COM,"left")\
            .groupBy("label_com","label_liste","nom_tete_liste")\
            .agg(sum("Inscrits"),\
                sum("Voix"),\
                avg("pourc_voix"))
    
    resDf.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "ElectionCsvRec") \
        .save()

    

