from flask import Flask, request, jsonify
import pymysql

# ConfigDB
db_config = {
    "host": "your_host",
    "user": "your_user",
    "password": "your_password",
    "database": "your_database",
    "cursorclass": pymysql.cursors.DictCursor
}

# Init Flask
app = Flask(__name__)

# get all depts
@app.route("/departments", methods=["GET"])
def get_departments():
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments")
            departments = cursor.fetchall()
            return jsonify(departments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get dept by ID
@app.route("/departments/<int:id>", methods=["GET"])
def get_department(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments WHERE id = %s", (id,))
            department = cursor.fetchone()
            if not department:
                return jsonify({"error": "Department not found"}), 404
            return jsonify(department)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert new dept
@app.route("/departments", methods=["POST"])
def create_department():
    try:
        data = request.json
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            sql = "INSERT INTO departments (id, department) VALUES (%s, %s)"
            cursor.execute(sql, (data['id'], data['department']))
            connection.commit()
        return jsonify({"message": "Departamento created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update department
@app.route("/departments/<int:id>", methods=["PUT"])
def update_department(id):
    try:
        data = request.json
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            sql = "UPDATE departments SET department=%s WHERE id=%s"
            cursor.execute(sql, (data['department'], id))
            connection.commit()
        return jsonify({"message": "Department updated!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete department
@app.route("/departments/<int:id>", methods=["DELETE"])
def delete_department(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM departments WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "Department deleted!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)