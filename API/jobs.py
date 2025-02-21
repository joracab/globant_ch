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
@app.route("/jobs, methods=["GET"])
def get_jobs():
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs")
            jobs = cursor.fetchall()
            return jsonify(jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get job by ID
@app.route("/jobs/<int:id>", methods=["GET"])
def get_job(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM job WHERE id = %s", (id,))
            job = cursor.fetchone()
            if not job:
                return jsonify({"error": "job not found"}), 404
            return jsonify(job)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert new job
@app.route("/jobs", methods=["POST"])
def create_job():
    try:
        data = request.json
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            sql = "INSERT INTO jobs (id, department) VALUES (%s, %s)"
            cursor.execute(sql, (data['id'], data['job']))
            connection.commit()
        return jsonify({"message": "job created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update job
@app.route("/jobs/<int:id>", methods=["PUT"])
def update_job(id):
    try:
        data = request.json
        
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            sql = "UPDATE jobs SET job=%s WHERE id=%s"
            cursor.execute(sql, (data['job'], id))
            connection.commit()
        return jsonify({"message": "job updated!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete job
@app.route("/job/<int:id>", methods=["DELETE"])
def delete_job(id):
    try:
        with pymysql.connect(**db_config) as connection, connection.cursor() as cursor:
            cursor.execute("DELETE FROM jobs WHERE id = %s", (id,))
            connection.commit()
        return jsonify({"message": "job deleted!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)