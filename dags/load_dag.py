from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from spark_load import load_data_to_s3, load_data_to_postgresql  # 데이터 적재 함수들

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'load_dag',
    default_args=default_args,
    description='Load transformed data to S3 and PostgreSQL',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 5),
    catchup=False,
) as dag:

    load_s3_task = PythonOperator(
        task_id='load_s3_task',
        python_callable=load_data_to_s3,
        op_kwargs={
            'output_path': 's3a://commen-myaws-bucket/data/processed/processed_data.csv'
        }
    )

    load_postgresql_task = PythonOperator(
        task_id='load_postgresql_task',
        python_callable=load_data_to_postgresql,
        op_kwargs={
            'postgres_url': 'jdbc:postgresql://postgres:5432/etl_db',
            'postgres_user': 'etl_user',
            'postgres_password': 'etl_password',
            'postgres_table': 'processed_data'
        }
    )

    # 예시로 두 태스크를 순차 실행
    load_s3_task >> load_postgresql_task

load_pipeline = dag
