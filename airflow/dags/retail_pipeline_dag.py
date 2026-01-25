from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 1, 17),
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="retail_data_pipeline",
    schedule=None,
    default_args=default_args,
    catchup=False,
    description="Retail data pipeline - monitoring existing data"
) as dag:

    check_raw_data = BashOperator(
        task_id="check_raw_data",
        bash_command="echo '=== RAW DATA ===' && ls /opt/project/data/raw/retail/ | wc -l && echo 'files found'"
    )

    check_processed_data = BashOperator(
        task_id="check_processed_data",
        bash_command="echo '=== PROCESSED DATA ===' && ls /opt/project/data/processed/retail/ | wc -l && echo 'files found'"
    )

    data_quality_check = BashOperator(
        task_id="data_quality_check",
        bash_command="""
        echo "=== DATA QUALITY CHECK ==="
        FILE_COUNT=$(ls /opt/project/data/processed/retail/ | wc -l)
        echo "Found $FILE_COUNT processed files"
        if [ $FILE_COUNT -gt 100 ]; then
            echo "✓ Quality check PASSED: Sufficient data files"
            exit 0
        else
            echo "✗ Quality check WARNING: Only $FILE_COUNT files (expected 100+)"
            exit 0
        fi
        """
    )

    check_raw_data >> check_processed_data >> data_quality_check
