from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount

default_args = {
    "owner": "fajar",
    "depends_on_past": False,
}

with DAG(
    "dbt_seed_dag",
    default_args=default_args,
    schedule=None,
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
                source="/workspaces/DE-Technical-Test/dbt/my_project_test",
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source="/workspaces/DE-Technical-Test/dbt",
                target="/root/.dbt",
                type="bind",
            ),
            Mount(
                source="/workspaces/DE-Technical-Test/data",
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
                source="/workspaces/DE-Technical-Test/dbt/my_project_test",
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source="/workspaces/DE-Technical-Test/dbt",
                target="/root/.dbt",
                type="bind",
            ),
        ],
        environment={"DBT_PROFILE_DIR": "/root/.dbt"},
    )
    run_dbt_seed >> run_dbt_transform
