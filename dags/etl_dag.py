from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'spark_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline using Spark',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # SparkSubmitOperator를 사용하여 Spark 작업 실행
    run_spark_etl = SparkSubmitOperator(
        task_id='run_spark_etl',
        application='/usr/src/app/spark_etl.py',  # Spark 애플리케이션 경로
        conn_id='spark_default',  # Airflow에서 Spark 연결 ID
        application_args=['--input', 's3a://your-bucket/input', '--output', 's3a://your-bucket/output'],  # 스크립트 매개변수
        executor_cores=2,
        executor_memory='2g',
        driver_memory='1g',
        name='spark_etl_task',
        verbose=True,
    )

    # DAG 실행 순서 설정
    run_spark_etl
