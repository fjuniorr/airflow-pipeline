from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

with DAG('docker_dag', 
         start_date = datetime(2023, 5, 27), 
         schedule = timedelta(minutes=5)) as dag:

    # Task to build the Docker image
    t1 = BashOperator(
        task_id='build_docker_image',
        bash_command='docker build -t piper /home/vagrant/projects/rstats-piper',
    )

    # Task to run the Docker container
    t2 = DockerOperator(
        task_id='run_docker_container',
        image='piper',
        api_version='auto',
        auto_remove='success',
        command="make all",  # Command to run inside the container
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[
            Mount(source="/home/vagrant/projects/rstats-piper", target="/project", type="bind"),
        ]
    )

    t1 >> t2  # Define task dependency
