import pymysql
import csv
import os
from datetime import datetime
# Database connection parameters 
db_config = {
    "host": "mysql-1ce5eb8-jose-eae6.e.aivencloud.com",
    "port": 20906,
    "user": "avnadmin",
    "password": "AVNS_u4xv4qhGhPxOY13Gm-L",
    "db": "globant_challenge",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


csv_file_path1 = "data/hired_employees.csv" # Example file path
error_file_path1 = "error_records_employees.txt"

csv_file_path2 = "data/jobs.csv" 
error_file_path2 = "error_records_jobs.txt"

csv_file_path3 = "data/departments.csv" 
error_file_path3 = "error_records_deps.txt"

def process_dept(file_path, error_file):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) # Assuming the first row is a header
            for row in csv_reader:
                try:
                  #SQL query 
                    sql = """
                        INSERT INTO departments (id, department) 
                        VALUES (%s, %s)
                    """
                    values = (row['id'], row['department'])
                    cursor.execute(sql, values)
                    connection.commit()
                except Exception as e:
                    with open(error_file, "a") as error_log:
                        error_log.write(f"Error inserting row: {row} - Error: {e}\n")
                    print(f"Error inserting row: {row} - Error: {e}")  
                    connection.rollback() # rollback transaction in case of error

        print(f"CSV file '{file_path}' processed successfully.")

    except Exception as e:
        print(f"Error processing CSV file: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def process_jobs(file_path, error_file):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) # Assuming the first row is a header
            for row in csv_reader:
                try:
                  #sql query#
                    sql = """
                        INSERT INTO jobs (id, job) 
                        VALUES (%s, %s)
                    """
                    values = (row['id'], row['job'])
                    cursor.execute(sql, values)
                    connection.commit()
                except Exception as e:
                    with open(error_file, "a") as error_log:
                        error_log.write(f"Error inserting row: {row} - Error: {e}\n")
                    print(f"Error inserting row: {row} - Error: {e}")  # Optionally print to console
                    connection.rollback() # rollback transaction in case of error

        print(f"CSV file '{file_path}' processed successfully.")

    except Exception as e:
        print(f"Error processing CSV file: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def process_employee(file_path, error_file):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) # Assuming the first row is a header
            for row in csv_reader:
                try:
                    try:
                        date_value = datetime.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                            raise ValueError(f"Formato de fecha incorrecto en fila {row['id']}: {row['datetime']}")
                        
                 
                    sql = """
                        INSERT INTO employees (id,name, datetime, department_id, job_id) 
                        VALUES (%s,%s,%s, %s, %s)
                    """
                    values = (row['id'],row['name'], date_value, row['department_id'], row['job_id'])
                    cursor.execute(sql, values)
                    connection.commit()
                except Exception as e:
                    with open(error_file, "a") as error_log:
                        error_log.write(f"Error inserting row: {row} - Error: {e}\n")
                    print(f"Error inserting row: {row} - Error: {e}")  # Optionally print to console
                    connection.rollback() # rollback transaction in case of error

        print(f"CSV file '{file_path}' processed successfully.")

    except Exception as e:
        print(f"Error processing CSV file: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    if os.path.exists(csv_file_path2):
      process_jobs(csv_file_path2, error_file_path2)
      process_dept(csv_file_path3, error_file_path3)
      process_employee(csv_file_path1, error_file_path1)
      
    else:
      print("The CSV file does not exist.")