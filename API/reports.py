from flask import Blueprint, jsonify, request
import pymysql
from config import Config

reports_bp = Blueprint("reports", __name__)

# db connection
def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT,
        charset=Config.DB_CHARSET,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@reports_bp.route("/hiring-report", methods=["GET"])
def get_hiring_report():
    
    try:
        connection = get_db_connection()  
        cursor = connection.cursor()

        year = request.args.get("year", default=2021, type=int)

        sql = """
            SELECT 
                d.id,
                d.department, 
                j.job, 
                SUM(CASE WHEN QUARTER(e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN QUARTER(e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN QUARTER(e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN QUARTER(e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            JOIN jobs j ON e.job_id = j.id
            WHERE YEAR(e.datetime) = %s
            GROUP BY d.id, d.department, j.job
            ORDER BY d.department ASC, j.job ASC
        """

        cursor.execute(sql, (year,))
        results = cursor.fetchall()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})
    
    finally:
        cursor.close()
        connection.close()

@reports_bp.route("/top-hiring-departments", methods=["GET"])
def get_top_hiring_departments():
  
    try:
        connection = get_db_connection()  # Usamos la conexión desde config.py
        cursor = connection.cursor()

        year = request.args.get("year", default=2021, type=int)

        sql_mean = """
            SELECT AVG(hired_count) as mean_hired
            FROM (
                SELECT d.id, COUNT(*) as hired_count
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE YEAR(e.datetime) = %s
                GROUP BY d.id
            ) AS department_hires
        """

        cursor.execute(sql_mean, (year,))
        mean_hired = cursor.fetchone()["mean_hired"] or 0

        sql_departments = """
            SELECT 
                d.id,
                d.department AS name,
                COUNT(*) AS employees_hired
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            WHERE YEAR(e.datetime) = %s
            GROUP BY d.id, d.department
            HAVING employees_hired > %s
            ORDER BY employees_hired DESC
        """

        cursor.execute(sql_departments, (year, mean_hired))
        results = cursor.fetchall()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})
    
    finally:
        cursor.close()
        connection.close()
