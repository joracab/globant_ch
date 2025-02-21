from flask import  Blueprint,Flask, request, jsonify
import pymysql
from config import Config

jobs_bp=Blueprint("jobs",__name__)
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


# get all jobs
@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs")
            jobs = cursor.fetchall()
            return jsonify(jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get job by ID
@jobs_bp.route("/jobs/<int:id>", methods=["GET"])
def get_job(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs WHERE id = %s", (id,))
            job = cursor.fetchone()
            if not job:
                return jsonify({"error": "job not found"}), 404
            return jsonify(job)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert new job
@jobs_bp.route("/jobs", methods=["POST"])
def create_job():
    try:
        data = request.json
        
        with get_db_connection() as connection, connection.cursor() as cursor:
            sql = "INSERT INTO jobs (id, job) VALUES (%s, %s)"
            cursor.execute(sql, (data['id'], data['job']))
            connection.commit()
        return jsonify({"message": "job created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update job
@jobs_bp.route("/<int:id>", methods=["PUT"])
def update_job(id):
    try:
        data = request.json
        
        with get_db_connection() as connection, connection.cursor() as cursor:
            sql = "UPDATE jobs SET job=%s WHERE id=%s"
            cursor.execute(sql, (data['job'], id))
            connection.commit()
        return jsonify({"message": "job updated!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete job
@jobs_bp.route("/<int:id>", methods=["DELETE"])
def delete_job(id):
    try:
        with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM jobs WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "job deleted!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500