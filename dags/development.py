import psycopg2
import csv


def connect_to_db():
    print("Connecting to the database...")

    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            dbname="db",
            user="db_user",
            password="db_password",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def create_table(conn):
    print("Creating table if it does not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE dev.farms (
                    farm_id VARCHAR(10) PRIMARY KEY,
                    crop_type VARCHAR(50),
                    farm_area_acres NUMERIC(10,2),
                    irrigation_type VARCHAR(50),
                    fertilizer_used_tons NUMERIC(10,2),
                    pesticide_used_kg NUMERIC(10,2),
                    yield_tons NUMERIC(10,2),
                    soil_type VARCHAR(50),
                    season VARCHAR(20),
                    water_usage_m3 NUMERIC(15,2)
                );
        """
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {e}")


conn = connect_to_db()
create_table(conn)
