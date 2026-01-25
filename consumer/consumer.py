import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import polars as pl
from datetime import datetime
import os

RAW_PATH = "/data/raw/retail"
PROCESSED_PATH = "/data/processed/retail"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

# Retry connection to Kafka
max_retries = 10
retry_delay = 5

for attempt in range(max_retries):
    try:
        consumer = KafkaConsumer(
            "retail-transactions",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
        print("✓ Connected to Kafka")
        break
    except NoBrokersAvailable:
        print(f"⏳ Kafka not ready, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})")
        time.sleep(retry_delay)
else:
    raise Exception("Failed to connect to Kafka after maximum retries")

batch = []

for message in consumer:
    batch.append(message.value)

    if len(batch) >= 10:
        df = pl.DataFrame(batch)

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        # RAW
        df.write_parquet(f"{RAW_PATH}/batch_{timestamp}.parquet")

        # PROCESSED
        df.filter(pl.col("Quantity") > 0) \
          .write_parquet(f"{PROCESSED_PATH}/batch_{timestamp}.parquet")

        print(f"✓ Written batch {timestamp}")
        batch = []
        time.sleep(1)
