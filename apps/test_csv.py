from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("TestCSV") \
    .getOrCreate()

# Read the CSV file from the correct container path
df = spark.read.option("header", "true").csv("/opt/spark/data/Online Retail.csv")

# Show first 5 rows
df.show(5)

# Stop the Spark session
spark.stop()

