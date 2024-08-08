from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from api_project.my_venv.airflow.dags.utils import copy_to_s3, extract_file

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
    dag_id="faker",
    default_args=default_args,
    description='creating an elt pipeline using python code and sql',
    schedule_interval="0 * * * *",
    max_active_runs=1,
    catchup=False
)

extract_task = PythonOperator(
    task_id="employees_dataset",
    dag=dag,
    python_callable=extract_file,
)

copy_task = PythonOperator(
    task_id='customer_dataset',
    python_callable=copy_to_s3,
    dag=dag,
)

extract_task >> copy_task