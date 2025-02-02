from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from spark_extract import extract_data  # 데이터 추출 함수

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'extract_dag',
    default_args=default_args,
    description='Extract data from S3',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 5),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        op_kwargs={
            'input_path': 's3a://commen-myaws-bucket/data/raw/concatenated.csv'
        }
    )

    # extract DAG가 완료되면 transform DAG를 트리거
    trigger_transform = TriggerDagRunOperator(
        task_id='trigger_transform_dag',
        trigger_dag_id='transform_dag',  # 트리거할 transform DAG의 ID
        reset_dag_run=True,
        wait_for_completion=False,  # 다음 DAG 실행 완료를 기다리지 않음
        poke_interval=60,
        allowed_states=['success'],
        failed_states=['failed']
    )

    extract_task >> trigger_transform

# 전역 변수에 할당해서 DAG가 등록되도록 함
extract_pipeline = dag
