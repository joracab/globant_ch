from flask import  Blueprint,Flask, request, jsonify
from datetime import datetime
from config import Config
import pymysql

employees_bp=Blueprint("employees",__name__)
# db config
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


# get all employees
@employees_bp.route("/", methods=["GET"])
def get_employees():
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get employee by ID
@employees_bp.route("/<int:id>", methods=["GET"])
def get_employee(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
            employee = cursor.fetchone()
            if not employee:
                return jsonify({"error": "Employee not found"}), 404
            return jsonify(employee)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert employee
@employees_bp.route("/", methods=["POST"])
def create_employee():
    try:
        data = request.json
        date_value = datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
        
        with get_db_connection() as connection, connection.cursor() as cursor:

            sql = """
                INSERT INTO employees (id, name, datetime, department_id, job_id) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (data['id'], data['name'], date_value, data['department_id'], data['job_id']))
            connection.commit()
        return jsonify({"message": "Employee created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update employee
@employees_bp.route("/<int:id>", methods=["PUT"])
def update_employee(id):
    try:
        data = request.json
        date_value = datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
        
        with get_db_connection() as connection, connection.cursor() as cursor:

            sql = """
                UPDATE employees SET name=%s, datetime=%s, department_id=%s, job_id=%s WHERE id=%s
            """
            cursor.execute(sql, (data['name'], date_value, data['department_id'], data['job_id'], id))
            connection.commit()
        return jsonify({"message": "Update employee"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete employee 
@employees_bp.route("/<int:id>", methods=["DELETE"])
def delete_employee(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "Employee deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()



