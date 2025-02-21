from flask import Blueprint, jsonify
import subprocess
import datetime
from config import Config
backup_bp = Blueprint("backup", __name__)

@backup_bp.route("/", methods=["GET"])
def backup_database():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.sql"
        
        db_host = Config.DB_HOST
        db_user = Config.DB_USER
        db_password = Config.DB_PASSWORD
        db_name = Config.DB_NAME

       
        command = f"mysqldump -h {db_host} -u {db_user} -p{db_password} {db_name} > {backup_file}"
        
        
        subprocess.run(command, shell=True, check=True)

        return jsonify({"message": "Backup created", "backup_file": backup_file})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error creating bakckup:", "details": str(e)})
