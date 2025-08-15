from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_load_script():
    script_path = "/opt/airflow/scripts/load_to_postgres.py"
    print(f"Running load script...")
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Load script failed")

default_args = {
    "owner": "fajar",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="eratani_pipeline",
    default_args=default_args,
    schedule="0 6 * * *", 
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    run_script = PythonOperator(
        task_id="run_load_script",
        python_callable=run_load_script
    )

    run_script