from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

# -------------------------------
# Create Spark session
# -------------------------------
spark = SparkSession.builder \
    .appName("KafkaToADLS") \
    .getOrCreate()

# -------------------------------
# Define the schema for incoming Kafka data
# -------------------------------
schema = StructType([
    StructField("InvoiceNo", StringType()),
    StructField("StockCode", StringType()),
    StructField("Description", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("InvoiceDate", StringType()),
    StructField("UnitPrice", DoubleType()),
    StructField("CustomerID", StringType()),
    StructField("Country", StringType())
])

# -------------------------------
# Read streaming data from Kafka
# -------------------------------
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "retail-transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka value from bytes to string and parse JSON
parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# -------------------------------
# Write to RAW zone in ADLS
# -------------------------------
parsed_df.writeStream \
    .format("parquet") \
    .option("path", "abfss://raw@retailprodatalake.dfs.core.windows.net/retail") \
    .option("checkpointLocation", "/tmp/raw-checkpoint") \
    .outputMode("append") \
    .start()

# -------------------------------
# Write to PROCESSED zone in ADLS (filter Quantity > 0)
# -------------------------------
parsed_df.filter(col("Quantity") > 0) \
    .writeStream \
    .format("parquet") \
    .option("path", "abfss://processed@retailprodatalake.dfs.core.windows.net/retail") \
    .option("checkpointLocation", "/tmp/processed-checkpoint") \
    .outputMode("append") \
    .start()

# Keep streaming job alive
spark.streams.awaitAnyTermination()



