# DE-Technical-Test Setup Instructions

1. **Create `.env` file with correct Airflow UID**
   Open a terminal in the project directory (`DE-Technical-Test`) and run:

   ```bash
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

2. **Update environment variables**
   In the `eratani_pipeline.py` file, set the following variables according to your local paths:

   * `DBT_PROJECT` → Path to your dbt project directory
   * `DBT_HOME` → Path to your dbt home directory
   * `DATA_DIR` → Path to your data directory

3. **Start the Airflow environment**
   Run the following command in the project root:

   ```bash
   docker compose up
   ```

## Notes

* Ensure Docker is running and has sufficient resources (≥ 4GB RAM, ≥ 2 CPUs).
* The Airflow webserver will be accessible at: [http://localhost:8080](http://localhost:8080)
* dbt commands (seed, run) are executed via Airflow DAGs using the DockerOperator