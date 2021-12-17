from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from datetime import datetime 
import time
from airflow.utils.dates import days_ago
import os
import requests
def start(): 
    os.popen('./spark/bin/spark-submit spark/spark.py')
    pass
	
def process():
    os.popen('nifi/bin/nifi.sh start')
    pass

def finalize():
    os.popen('./spark/bin/spark-submit script/script.py')
    pass


with DAG(
    dag_id="projet_data_pipeline",
    schedule_interval='@hourly',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['projet'],
) as dag:

    start_task = PythonOperator(
	
	
        task_id="start_task",
        python_callable=start,
    )
    process_task = PythonOperator(
        task_id="process_task",
        python_callable=process,
    )

    final_task = PythonOperator(
        task_id="final_task",
        python_callable=finalize,
    )
    start_task >> process_task >> final_task
