# -*- coding: utf-8 -*-
"""Assignment 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fRND_Zag0o7N4lWEwdlfynImOMCuZdYe
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://mirrors.sonic.net/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
!tar xzf spark-3.1.2-bin-hadoop3.2.tgz
!pip install -q findspark


import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.1.2-bin-hadoop3.2"


import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

df = spark.read.options(header=True, InferSchema=True).csv("/content/drive/MyDrive/cruise_ship_info.csv")
df.show()
df.printSchema()

from pyspark.ml.feature import VectorAssembler

df.columns

assembler = VectorAssembler(inputCols=['Tonnage', 'passengers', 'length', 
                                       'cabins','passenger_density'], outputCol='features')
output = assembler.transform(df) 
output.show()

output.select('features').head(1)

final_data=output.select(['features','crew'])

train_data, test_data = final_data.randomSplit([0.7, 0.3])

final_data.describe().show()
train_data.describe().show()
test_data.describe().show()

from pyspark.ml.regression import LinearRegression 
lr = LinearRegression(labelCol='crew')

lr_model = lr.fit(train_data)

test_results = lr_model.evaluate(test_data)

test_results.rootMeanSquaredError

test_results.r2

unlabeled_data = test_data.select('features')

unlabeled_data.show()

predictions_crew = lr_model.transform(unlabeled_data)

predictions_crew.show()