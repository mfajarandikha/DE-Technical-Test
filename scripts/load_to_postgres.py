import psycopg2
import csv

def connect_to_db():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host="destination_postgres",  
            port="5432",                  
            dbname="destination_db",
            user="destination_user",
            password="secret",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def create_table(conn):
    print("Creating table...")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS dev;
        CREATE TABLE IF NOT EXISTS dev.farms (
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
    """)
    conn.commit()
    cursor.close()

def insert_data(conn):
    print("Inserting data into the table...")
    count = 0
    cursor = conn.cursor()
    try:
        with open("/opt/airflow/data/agriculture_dataset.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cursor.execute("""
                    INSERT INTO dev.farms (
                        farm_id, crop_type, farm_area_acres, irrigation_type,
                        fertilizer_used_tons, pesticide_used_kg, yield_tons,
                        soil_type, season, water_usage_m3
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, row)
                count += 1
        conn.commit()
        print(f"Data inserted successfully. {count} rows inserted.")
        return count
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()

def main():
    conn = None
    try:
        conn = connect_to_db()
        create_table(conn)
        inserted_count = insert_data(conn)
        return inserted_count
    except Exception as e:
        print(f"Load failed: {e}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    rows_inserted = main()
    print(f"{rows_inserted} rows successfully inserted.")
