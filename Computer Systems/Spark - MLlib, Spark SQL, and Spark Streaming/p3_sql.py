from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import *
from pyspark.sql import types

import sys


sc = SparkContext("local[2]", appName="Part4")
sqlContext = SQLContext(sc)
lines = sc.textFile(sys.argv[1])
lines = lines.map(lambda x: str(x.encode('utf-8')))
lines = lines.map(lambda x: x.split(' ', 1))

fields = [types.StructField("topic", types.StringType(), True), types.StructField("title", types.StringType(), True)]
schema = types.StructType(fields)
schemaTopics = sqlContext.createDataFrame(lines, schema)
schemaTopics.registerTempTable("clusters")



def part4(input_topic):
    input_topic = input_topic.collect()
    if len(input_topic) > 0:
        input_topic = input_topic[0]
        query = "SELECT title FROM clusters WHERE topic = '" + input_topic + "'"
        results = sqlContext.sql(query)
        titles = results.map(lambda p: p.title)
        for title in titles.collect():
            print title


ssc = StreamingContext(sc, 3)
input_topic = ssc.socketTextStream("localhost", int(sys.argv[2]))
input_topic.foreachRDD(part4)
ssc.start()
ssc.awaitTermination()




    