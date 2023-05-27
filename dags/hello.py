from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

import logging

logger = logging.getLogger(__name__)

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", 
         start_date=datetime(2023, 5, 27), 
         schedule=timedelta(minutes=5)) as dag:

    # Tasks are represented as operators
    logger.warning('This is a big bad warning')
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        logger.info('This is better')
        logger.error('This is a error')

    # Set dependencies between tasks
    hello >> airflow()
