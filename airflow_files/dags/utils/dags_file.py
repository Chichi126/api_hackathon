from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils.aws import aws_sesion
from utils.main import copy_to_s3, extract_file

boto3session = aws_sesion()


default_args = {
    'owner': 'faker_project',
    'email': ['chinyere.nwigwe126@gmail.com'],
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 15),
    'retries': 5,
    'retry_delay': timedelta(seconds=10),
    'execution_timeout': timedelta(minutes=10)
}


dag = DAG(
    dag_id="api_countries",
    default_args=default_args,
    description='creating an elt pipeline using python code and sql',
    schedule_interval="0 * * * *",
    max_active_runs=1,
    catchup=False
)

extract_task = PythonOperator(
    task_id="to_extract",
    dag=dag,
    python_callable=extract_file,
    op_kwargs={"url": "https://restcountries.com/v3.1/all"}
)
copy_task = PythonOperator(
    task_id='send_to_s3',
    python_callable=copy_to_s3,
    dag=dag,
    op_kwargs={"boto_session": boto3session}
)

extract_task >> copy_task
