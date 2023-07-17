import os
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from etl import extract_data, transform_data,  load_to_redshift


default_args = {
    'start_date': datetime(2023, 7, 2),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'job_board_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

with dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url':"https://jsearch.p.rapidapi.com/search",
            'querystring':{"query": "data engineer in canada, data analyst in canada", "page": "1", "num_pages": "1", "date_posted": "today"},
            'headers':{
                "X-RapidAPI-Key": os.getenv("rapidAPI-key"),
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
        },
    )

   
    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    load_to_redshift_task = PythonOperator(
        task_id='load_to_redshift',
        python_callable=load_to_redshift
    )

    extract_task >> transform_data_task >> load_to_redshift_task