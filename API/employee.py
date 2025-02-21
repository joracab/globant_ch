from flask import Flask, request, jsonify
from datetime import datetime
import pymysql

# db config
db_config = {
    "host": "your_host",
    "user": "your_user",
    "password": "your_password",
    "database": "your_database",
    "cursorclass": pymysql.cursors.DictCursor
}

# Init Flask
app = Flask(__name__)

# get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get employee by ID
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
            employee = cursor.fetchone()
            if not employee:
                return jsonify({"error": "Employee not found"}), 404
            return jsonify(employee)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert employee
@app.route("/employees", methods=["POST"])
def create_employee():
    try:
        data = request.json
        date_value = datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
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
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    try:
        data = request.json
        date_value = datetime.strptime(data['datetime'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            sql = """
                UPDATE employees SET name=%s, datetime=%s, department_id=%s, job_id=%s WHERE id=%s
            """
            cursor.execute(sql, (data['name'], date_value, data['department_id'], data['job_id'], id))
            connection.commit()
        return jsonify({"message": "Update employee"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete employee @app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "Employee deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
