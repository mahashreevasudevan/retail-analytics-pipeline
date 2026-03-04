# Retail Analytics Data Pipeline

A data engineering pipeline processing 400,000+ retail transactions using Apache Kafka, Airflow, and automated quality validation.

## Key Objectives

Transform raw e-commerce transaction data into analytics-ready datasets at scale. The pipeline handles data versioning, implements automated quality gates, and provides decision intelligence through structured outputs. Processes 541,909 transactions, maintaining 406,829 clean records optimized for analytics.

## Methodology

Follows medallion architecture with RAW and PROCESSED layers. Data streams through Apache Kafka for real-time processing, with consumers writing to columnar Parquet format. Apache Airflow orchestrates the pipeline with automated scheduling, monitoring, and quality validation checkpoints.

## Model Pipeline
```
Excel Dataset (541K transactions)
         ↓
    Kafka Producer
         ↓
    Apache Kafka + Zookeeper
         ↓
    Consumer (Polars)
         ↓
    ┌─────────────┬──────────────┐
    │  RAW Layer  │ PROCESSED    │
    │  14,263     │ 14,263       │
    │  files      │ files        │
    └──────┬──────┴──────┬───────┘
           │             │
           └──────┬──────┘
                  ↓
          Airflow Orchestration
          (Quality Validation)
                  ↓
          Analytics Output
          (406K+ records)
```

## Technology and Tools

**Processing:** Apache Kafka 7.5.0, Python 3.10, Polars, Pandas  
**Orchestration:** Apache Airflow 2.7.3, PostgreSQL 13  
**Storage:** Parquet format, dual-layer architecture  
**Infrastructure:** Docker, Azure VM, GitHub Actions  
**Development:** Git, Flake8, automated CI/CD

## Challenges Addressed

-- Removed 135,080 invalid records through multi-stage validation while preserving data lineage. Validates positive quantities, non-null values, and revenue sanity.

-- Handles 400,000 records with configurable batch processing. Polars provides 10x faster processing than Pandas through optimized memory management.

-- Built fault tolerance through Kafka message persistence, Airflow automatic retries, and dual-layer architecture ensuring raw data preservation.

-- Coordinated Docker containers with health checks, startup ordering, and proper volume mounting. Scheduler runs separately from webserver preventing resource contention.

-- Kafka architecture enables horizontal scaling with multiple consumers processing different partitions simultaneously. Parquet format supports parallel reads.

## Results

**Data Metrics:**
- 406,829 valid transactions processed
- 14,263 files in each layer (RAW + PROCESSED)
- 50MB compressed storage
- 100% quality check pass rate
- Zero null values in processed data

**Performance:**
- Sub-second query performance on Parquet files
- Complete data versioning with raw layer preservation
- Automated validation on every pipeline run

## Impact

**Analytics:** Enables immediate analysis of sales trends, product performance, and customer behavior through 14,263 time-partitioned files.

**Decision Intelligence:** Clean data feeds BI tools for inventory optimization, demand forecasting, and customer segmentation.

**Data Versioning:** RAW layer preserves original records for audit and reprocessing. PROCESSED layer provides point-in-time snapshots.

**Automation:** Eliminates manual processing. Airflow scheduling enables daily runs without intervention.

**Scalability:** Kafka architecture supports scaling from thousands to millions of transactions. Parquet format optimizes storage and query performance.

## Project Structure
```
retail-analytics/
├── kafka/
│   ├── producer.py              # Kafka producer
│   ├── Dockerfile
│   └── requirements.txt
├── consumer/
│   ├── consumer.py              # Batch processor
│   ├── Dockerfile
│   └── requirements.txt
├── airflow/
│   ├── dags/
│   │   └── retail_pipeline_dag.py
│   └── docker-compose.yml
├── data/
│   ├── source/                  # Input datasets
│   ├── raw/                     # Complete history
│   └── processed/               # Analytics layer
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml
└── docker-compose.yml
```
## Power BI Dashboard

Interactive analytics dashboard with DAX measures tracking revenue trends, product performance, and customer metrics.

**Key Metrics:** Total Revenue, Transaction Count, Unique Customers, Average Transaction Value  
**Visuals:** KPI cards, revenue trends, top products, geographic distribution  
**DAX Measures:** SUM aggregations, DISTINCTCOUNT, DIVIDE, time-based filtering

<img width="1685" height="867" alt="Screenshot (500)" src="https://github.com/user-attachments/assets/29821993-a195-4276-a7e7-78a1a122e55b" />


## Technology and Tools

- **Languages**: Python 3.10, SQL
- **Streaming**: Apache Kafka 7.5.0, Zookeeper
- **Processing**: Polars, Pandas
- **Orchestration**: Apache Airflow 2.7.3
- **Storage**: Parquet (columnar format), dual-layer medallion architecture
- **Database**: PostgreSQL 13
- **Infrastructure**: Docker, Azure VM
- **CI/CD**: GitHub Actions, Flake8
- **Visualisation**: Power BI, DAX
