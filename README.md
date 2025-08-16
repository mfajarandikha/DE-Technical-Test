# DE-Technical-Test Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>
cd DE-Technical-Test
```

## 2. Create `.env` file with correct Airflow UID (using Git Bash)

Run this command in the project root to set your local Airflow UID:

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## 3. Update environment variables for dbt

In the `eratani_pipeline.py` file, set the following variables according to your local paths:

* `DBT_PROJECT` → Path to your dbt project directory
* `DBT_HOME` → Path to your dbt home directory
* `DATA_DIR` → Path to your data directory

## 4. Start the Airflow environment

Run the following command in the project root:

```bash
docker compose up
```

## 5. Access destination Postgres

To inspect the database where metrics are stored:

### Open a shell in the container:

```bash
docker exec -it destination_postgres psql -U destination_user -d destination_db
```

### Open list tables and views:

```sql
\dt    -- lists tables
\dv    -- lists views
```

This allows you to verify that your metrics tables and views have been created correctly by dbt and Airflow.

## Notes

* Ensure Docker is running and has sufficient resources (≥ 4GB RAM, ≥ 2 CPUs).
* The Airflow webserver will be accessible at: [http://localhost:8080](http://localhost:8080)
* dbt commands (`seed`, `run`) are executed via Airflow DAGs using the DockerOperator.
* You can use the `\dt` and `\dv` commands in `psql` to quickly explore metrics tables and views in `destination_postgres`.
