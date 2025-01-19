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
    schedule_interval=timedelta(days=1),  # 매일 실행
    start_date=datetime(2025, 1, 5),
    catchup=False,
) as dag:

    # S3 입력 및 출력 경로
    s3_input_path = "s3a://commen-myaws-bucket/data/raw/concatenated.csv"
    s3_output_path = "s3a://commen-myaws-bucket/data/processed/processed_data.csv"

    # PostgreSQL 연결 정보 (환경 변수 기반)
    postgres_url = "jdbc:postgresql://postgres:5432/etl_db"
    postgres_user = "etl_user"
    postgres_password = "etl_password"
    postgres_table = "processed_data"

    # SparkSubmitOperator를 사용하여 Spark 작업 실행
    run_spark_etl = SparkSubmitOperator(
        task_id='run_spark_etl',
        application='/usr/src/app/spark_etl.py',  # Spark 애플리케이션 경로
        conn_id='spark_default',  # Airflow에서 Spark 연결 ID
        application_args=[
            '--input', s3_input_path,
            '--output', s3_output_path,
            '--postgres_url', postgres_url,
            '--postgres_user', postgres_user,
            '--postgres_password', postgres_password,
            '--postgres_table', postgres_table
        ],  # 스크립트 매개변수 전달
        executor_cores=2,
        executor_memory='2g',
        driver_memory='1g',
        name='spark_etl_task',
        verbose=True,
    )

    # DAG 실행 순서 설정
    run_spark_etl
