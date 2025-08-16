from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount

DBT_PROJECT = "/workspaces/DE-Technical-Test/dbt/my_project_test"  # Update Path ke DBT project directory
DBT_HOME = "/workspaces/DE-Technical-Test/dbt"  # Update Path ke DBT home directory
DATA_DIR = "/workspaces/DE-Technical-Test/data"  # Update Path ke data directory

with DAG(
    "dbt_seed_dag",
    schedule="0 6 * * *",
    start_date=datetime(2025, 8, 15),
    catchup=False,
) as dag:
    run_dbt_seed = DockerOperator(
        task_id="run_dbt_seed",
        image="ghcr.io/dbt-labs/dbt-postgres:1.8.1",
        api_version="auto",
        auto_remove="success",
        command="seed",
        docker_url="unix://var/run/docker.sock",
        network_mode="de-technical-test_airflow_network",
        working_dir="/usr/app",
        mounts=[
            Mount(
                source=DBT_PROJECT,
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source=DBT_HOME,
                target="/root/.dbt",
                type="bind",
            ),
            Mount(
                source=DATA_DIR,
                target="/usr/app/seeds",
                type="bind",
            ),
        ],
        environment={"DBT_PROFILE_DIR": "/root/.dbt"},
    )

    run_dbt_transform = DockerOperator(
        task_id="run_dbt_transform",
        image="ghcr.io/dbt-labs/dbt-postgres:1.8.1",
        api_version="auto",
        auto_remove="success",
        command="run",
        docker_url="unix://var/run/docker.sock",
        network_mode="de-technical-test_airflow_network",
        working_dir="/usr/app",
        mounts=[
            Mount(
                source=DBT_PROJECT,
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source=DBT_HOME,
                target="/root/.dbt",
                type="bind",
            ),
        ],
        environment={"DBT_PROFILE_DIR": "/root/.dbt"},
    )
    run_dbt_seed >> run_dbt_transform
