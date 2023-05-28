from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from git import Repo
import os

with DAG('docker_dag', 
         start_date = datetime(2023, 5, 27), 
         schedule = timedelta(minutes=5)) as dag:

    @task()
    def git_sync():
        repo_dir = "/home/vagrant/projects/rstats-piper"
        git_url = "https://github.com/fjuniorr/rstats-pipeline.git"
        if not os.path.exists(repo_dir):
            Repo.clone_from(git_url, repo_dir)
        else:
            repo = Repo(repo_dir)
            origin = repo.remotes.origin
            origin.pull()

    # Task to build the Docker image
    docker_build = BashOperator(
        task_id='build_docker_image',
        bash_command='sudo docker build -t piper /home/vagrant/projects/rstats-piper',
    )

    # Task to run the Docker container
    docker_run = DockerOperator(
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

    git_sync() >> docker_build >> docker_run  # Define task dependency
