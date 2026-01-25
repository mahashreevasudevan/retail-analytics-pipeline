from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestCSV").getOrCreate()

# Read CSV
df = spark.read.option("header", "true").csv("/opt/spark-work-dir/data/Online Retail.csv")

# Show first 5 rows
df.show(5)

# Write to a temporary output file
df.limit(5).write.mode("overwrite").csv("/opt/spark-work-dir/output_test_csv")

spark.stop()
