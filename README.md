# Retail Analytics Data Pipeline

![CI Pipeline](https://github.com/mahashreevasudevan/retail-analytics-pipeline/workflows/Retail%20Analytics%20Pipeline%20CI/badge.svg)

A production-grade data engineering pipeline that processes over 400,000 retail transactions using real-time streaming, automated orchestration, and quality validation. Built to demonstrate end-to-end data engineering capabilities from ingestion through analytics-ready output.

## Key Objectives

This project tackles the challenge of transforming raw e-commerce transaction data into analysis-ready datasets at scale. The pipeline handles data versioning across multiple processing layers, implements automated quality gates, and provides decision intelligence capabilities through structured data outputs.

The system processes the Online Retail dataset containing 541,909 transactions across multiple countries and product categories. After data filtering and quality validation, it maintains 406,829 clean records optimized for descriptive analytics and trend analysis.

## Methodology

The pipeline follows a medallion architecture pattern with three distinct layers. Raw data lands first without transformation, preserving complete data lineage and enabling data versioning. The processed layer applies business logic and quality filters, creating analytics-ready datasets. This separation supports both exploratory analysis on raw data and production reporting on validated data.

Data flows through Apache Kafka for real-time streaming, enabling data parallelism and fault-tolerant processing. The consumer processes messages in configurable batches, writing to columnar Parquet format for inference optimization and efficient query performance.

Apache Airflow orchestrates the entire pipeline, providing scheduling, monitoring, and automated retries. Each pipeline run includes three validation checkpoints that verify data quality before downstream consumption.

## Model Pipeline
```
Online Retail Dataset (Excel)
         |
    Kafka Producer
    - Reads 406K transactions
    - Streams to retail-transactions topic
    - Handles data serialization
         |
    Apache Kafka Broker
    - Message queuing
    - Fault tolerance
    - Data parallelism
         |
    Kafka Consumer (Polars)
    - Batch processing (10 records/batch)
    - Dual-layer writes
         |
    +-----------------+------------------+
    |                                    |
RAW Layer                        PROCESSED Layer
- All transactions               - Quality filtered
- Complete history              - Quantity > 0 only
- 14,263 parquet files          - Analytics-ready
- Data versioning               - 14,263 parquet files
    |                                    |
    +----------------+-------------------+
                     |
            Airflow Orchestration
            - Data quality validation
            - File count monitoring
            - Automated scheduling
                     |
            Analytics-Ready Output
            - Descriptive analytics
            - Trend analysis
            - Decision intelligence
```

## Technology and Tools

**Streaming and Processing**
- Apache Kafka 7.5.0 for real-time data ingestion
- Zookeeper for distributed coordination
- Python 3.10 with Polars for high-performance data processing
- Pandas for Excel file parsing and initial data handling

**Orchestration and Workflow**
- Apache Airflow 2.7.3 with LocalExecutor
- PostgreSQL 13 for metadata storage
- DAG-based workflow management with automated retries

**Data Storage and Format**
- Parquet columnar format for inference optimization
- Dual-layer storage architecture for data versioning
- 50MB compressed storage across 28,000 files

**Infrastructure**
- Docker and Docker Compose for containerization
- Azure Virtual Machine deployment
- GitHub Actions for continuous integration

**Development**
- Git for version control
- Flake8 for code quality validation
- Automated testing in CI pipeline

## Challenges Addressed

**Data Quality and Validation**

The raw dataset contained invalid records including null customer IDs and negative quantities. Implemented multi-stage validation that removes 135,080 invalid records while preserving data lineage in the raw layer. Quality checks verify positive quantities, non-null values, and revenue sanity before data enters the processed layer.

**Real-Time Processing at Scale**

Processing 400,000 records requires handling variable data velocity and preventing memory overflow. The consumer implements configurable batch processing that balances throughput with resource constraints. Polars provides 10x faster processing compared to Pandas through optimized memory management and parallel execution.

**Pipeline Reliability**

Built fault tolerance through multiple mechanisms. Kafka provides message persistence and replay capabilities. Airflow implements automatic retries with exponential backoff. The dual-layer architecture ensures raw data preservation even if processed layer writes fail.

**Orchestration Complexity**

Coordinating Docker containers across different services required careful dependency management. Implemented health checks for PostgreSQL, startup ordering for Airflow components, and proper volume mounting for data persistence. The scheduler runs separately from the webserver to prevent resource contention.

**Data Parallelism**

The Kafka architecture enables horizontal scaling. Multiple consumers can process different partitions simultaneously, supporting future scaling requirements. The Parquet format enables parallel reads for downstream analytics tools.

## Results

The pipeline successfully processes the complete Online Retail dataset with the following outcomes:

**Data Processing Metrics**
- 406,829 valid transactions processed and stored
- 14,263 batch files in raw layer
- 14,263 filtered files in processed layer
- 50MB total storage in compressed Parquet format
- Zero data quality failures in processed layer

**Pipeline Performance**
- 100% data quality check pass rate
- Automated validation on every pipeline run
- Complete data versioning with raw layer preservation
- Sub-second query performance on Parquet files

**System Reliability**
- Containerized architecture supporting easy deployment
- Automated retry logic preventing data loss
- Comprehensive logging across all pipeline stages
- Health monitoring through Airflow UI

**Data Quality Validation**
- All processed records have positive quantities
- Zero null values in critical fields
- Revenue calculations validated against sanity thresholds
- Duplicate detection and handling

## Impact

This pipeline demonstrates production-ready data engineering practices applicable to real-world e-commerce analytics. The architecture supports several business use cases:

**Descriptive Analytics**

The processed layer enables immediate analysis of sales trends, product performance, and customer behavior. Analysts can query 14,263 time-partitioned files to understand historical patterns without touching raw data.

**Decision Intelligence**

Clean, validated data feeds into business intelligence tools for inventory optimization, demand forecasting, and customer segmentation. The quality gates ensure decisions are based on accurate information.

**Data Versioning and Lineage**

The dual-layer approach maintains complete data history. The raw layer preserves original records for audit and reprocessing. The processed layer provides point-in-time snapshots supporting temporal analysis and data versioning requirements.

**Operational Efficiency**

Automation eliminates manual data processing steps. Airflow scheduling enables daily pipeline runs without human intervention. Quality validation prevents bad data from reaching analytics consumers.

**Scalability Foundation**

The Kafka-based architecture supports scaling from thousands to millions of transactions. Adding more consumer instances enables data parallelism. The Parquet format optimizes for both storage costs and query performance.

## Project Structure
```
retail-analytics/
├── kafka/
│   ├── producer.py              # Streams transactions to Kafka
│   ├── Dockerfile
│   └── requirements.txt
├── consumer/
│   ├── consumer.py              # Batch processing to Parquet
│   ├── Dockerfile
│   └── requirements.txt
├── airflow/
│   ├── dags/
│   │   └── retail_pipeline_dag.py   # Orchestration workflow
│   ├── docker-compose.yml
│   ├── logs/
│   └── plugins/
├── data/
│   ├── source/                  # Input datasets
│   ├── raw/                     # Complete transaction history
│   └── processed/               # Quality-filtered analytics layer
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml      # Automated testing
├── docker-compose.yml           # Main infrastructure
└── README.md
```

## Getting Started

**Prerequisites**
- Docker and Docker Compose installed
- 4GB RAM minimum
- Git for version control

**Quick Start**

Clone the repository and start the infrastructure:
```bash
git clone https://github.com/mahashreevasudevan/retail-analytics-pipeline.git
cd retail-analytics-pipeline

# Start Kafka and consumer
docker-compose up -d

# Start Airflow
cd airflow
docker-compose up -d
```

Access Airflow UI at `http://localhost:8081` with credentials `admin/admin`.

**Running the Pipeline**

In Airflow UI, enable the `retail_data_pipeline` DAG and trigger it manually. The pipeline executes three validation tasks and completes in under one minute.

## Future Enhancements

**Advanced Analytics**
- Implement predictive analytics for demand forecasting
- Add customer lifetime value calculations
- Build product recommendation engine

**Performance Optimization**
- Migrate to Apache Spark for distributed processing
- Implement data partitioning strategies
- Add caching layers for frequently accessed data

**Data Quality**
- Integrate Great Expectations for schema validation
- Add statistical profiling and anomaly detection
- Implement data drift monitoring

**Infrastructure**
- Deploy to Azure Data Lake Storage
- Add real-time monitoring with Grafana
- Implement cost optimization strategies
- Set up alerting for pipeline failures

**Analytics Layer**
- Connect Power BI with DAX measures for business metrics
- Build REST API for programmatic data access
- Create data catalog for discovery

## Author

Mahashree Vasudevan

GitHub: github.com/mahashreevasudevan

## License

MIT License
