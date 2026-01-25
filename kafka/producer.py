import json
import time
from kafka import KafkaProducer
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("=" * 70)
print("Loading Online Retail dataset from /data/source/online_retail.xlsx")
print("=" * 70)

# Read the Excel file from mounted volume
df = pd.read_excel("/data/source/online_retail.xlsx")

print(f"\n✓ Loaded {len(df):,} records")

# Clean the data
print("\nCleaning data...")
original_count = len(df)
df = df.dropna(subset=['CustomerID'])  # Remove rows without customer ID
df = df[df['Quantity'] > 0]  # Keep only positive quantities
print(f"  - Removed {original_count - len(df):,} invalid records")
print(f"  - Remaining: {len(df):,} valid transactions")

# Convert date to string for JSON serialization
df['InvoiceDate'] = df['InvoiceDate'].astype(str)

print(f"\n{'=' * 70}")
print(f"Starting to send {len(df):,} transactions to Kafka topic 'retail-transactions'")
print(f"{'=' * 70}\n")

# Send each transaction
for idx, row in df.iterrows():
    transaction = {
        "InvoiceNo": str(row['InvoiceNo']),
        "StockCode": str(row['StockCode']),
        "Description": str(row['Description']) if pd.notna(row['Description']) else "",
        "Quantity": int(row['Quantity']),
        "InvoiceDate": row['InvoiceDate'],
        "UnitPrice": float(row['UnitPrice']),
        "CustomerID": str(int(row['CustomerID'])),
        "Country": str(row['Country'])
    }
    
    producer.send("retail-transactions", value=transaction)
    
    # Progress updates every 1000 records
    if (idx + 1) % 1000 == 0:
        print(f"✓ Sent {idx+1:,} / {len(df):,} transactions ({((idx+1)/len(df)*100):.1f}%)")
    
    # Small delay every 100 records to avoid overwhelming Kafka
    if idx % 100 == 0:
        time.sleep(0.05)

producer.flush()
print(f"\n{'=' * 70}")
print(f"✓ SUCCESS! All {len(df):,} transactions sent to Kafka!")
print(f"{'=' * 70}")
