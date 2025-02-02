from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
from airflow.utils.task_group import TaskGroup

# 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
with DAG(
    'spark_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline using Spark',
    schedule_interval='@daily',  # 매일 실행
    start_date=datetime(2025, 1, 5),
    catchup=False,
) as dag:

    # 경로 및 연결 정보 정의
    s3_input_path = "s3a://commen-myaws-bucket/data/raw/concatenated.csv"
    s3_output_path = "s3a://commen-myaws-bucket/data/processed/processed_data.csv"

    postgres_url = "jdbc:postgresql://postgres:5432/etl_db"
    postgres_user = "etl_user"
    postgres_password = "etl_password"
    postgres_table = "processed_data"

    # Task Group을 활용한 ETL 작업 그룹화
    with TaskGroup(group_id="spark_etl_tasks") as spark_etl_tasks:
        
        # Spark 작업 실행
        run_spark_etl = SparkSubmitOperator(
            task_id='spark_etl_process',
            application='/usr/src/app/spark_etl.py',
            conn_id='spark_default',  # Airflow 연결 ID
            application_args=[
                '--input', s3_input_path,
                '--output', s3_output_path,
                '--postgres_url', postgres_url,
                '--postgres_user', postgres_user,
                '--postgres_password', postgres_password,
                '--postgres_table', postgres_table
            ],
            executor_cores=2,
            executor_memory='2g',
            driver_memory='1g',
            name='spark_etl_task',
            verbose=True,
        )

    # 실행 순서 설정
    spark_etl_tasks
