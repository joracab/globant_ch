from flask import  Blueprint,Flask, request, jsonify
import pymysql
from config import Config

departaments_bp=Blueprint("departments",__name__)
# database config
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
# get all departments
@departaments_bp.route("/", methods=["GET"])
def get_departments():
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments")
            departments = cursor.fetchall()
            return jsonify(departments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get dept by ID
@departaments_bp.route("/<int:id>", methods=["GET"])
def get_department(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments WHERE id = %s", (id,))
            department = cursor.fetchone()
            if not department:
                return jsonify({"error": "Department not found"}), 404
            return jsonify(department)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add new dept
@departaments_bp.route("/", methods=["POST"])
def create_department():
    try:
        data = request.json
        
        with get_db_connection() as connection, connection.cursor() as cursor:
            sql = "INSERT INTO departments (id, department) VALUES (%s, %s)"
            cursor.execute(sql, (data['id'], data['department']))
            connection.commit()
        return jsonify({"message": "Department created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#update dept
@departaments_bp.route("/<int:id>", methods=["PUT"])
def update_department(id):
    try:
        data = request.json
        
        with get_db_connection() as connection, connection.cursor() as cursor:
            sql = "UPDATE departments SET department=%s WHERE id=%s"
            cursor.execute(sql, (data['department'], id))
            connection.commit()
        return jsonify({"message": "Department updated!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Delete dept
@departaments_bp.route("/<int:id>", methods=["DELETE"])
def delete_department(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM departments WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "Department deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
