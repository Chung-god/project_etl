from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from spark_transform import transform_data  # 데이터 변환 함수

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'transform_dag',
    default_args=default_args,
    description='Transform extracted data',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 5),
    catchup=False,
) as dag:

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        # 필요한 경우 op_kwargs로 인자 전달 (예: 이전 단계 결과가 저장된 위치)
    )

    # transform DAG가 완료되면 load DAG를 트리거
    trigger_load = TriggerDagRunOperator(
        task_id='trigger_load_dag',
        trigger_dag_id='load_dag',  # 트리거할 load DAG의 ID
        reset_dag_run=True,
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=['success'],
        failed_states=['failed']
    )

    transform_task >> trigger_load

transform_pipeline = dag
