from flask import Flask
from API.employees import employees_bp
from API.departments import departaments_bp
from API.jobs import jobs_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Registrar los Blueprints
app.register_blueprint(employees_bp, url_prefix="/employees")
app.register_blueprint(departaments_bp, url_prefix="/departments")
app.register_blueprint(jobs_bp, url_prefix="/jobs")


if __name__ == "__main__":
    app.run(debug=True)
