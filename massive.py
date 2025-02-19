import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# DataFrames for employees and jobs
try:
    employees_df = pd.read_csv("employees.csv")
except FileNotFoundError:
    print("Error: 'employees.csv' not found. Creating a new one.")
    employees_df = pd.DataFrame(columns=['id', 'department'])
    employees_df.to_csv("employees.csv", index=False)

try:
    jobs_df = pd.read_csv("jobs.csv")
except FileNotFoundError:
    print("Error: 'jobs.csv' not found. Creating a new one.")
    jobs_df = pd.DataFrame(columns=['id', 'job'])
    jobs_df.to_csv("jobs.csv", index=False)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        try:
            department_filter = request.args.get('department')
            if department_filter:
                filtered_df = employees_df[employees_df['department'] == department_filter]
            else:
                filtered_df = employees_df
            return jsonify(filtered_df.to_dict('records'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'id' not in data or 'department' not in data:
                return jsonify({"error": "Invalid input data. 'id' and 'department' are required."}), 400
            new_employee = pd.DataFrame(data, index=[0])
            global employees_df
            employees_df = pd.concat([employees_df, new_employee], ignore_index=True)
            employees_df.to_csv("employees.csv", index=False)
            return jsonify({"message": "Employee added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/jobs', methods=['POST'])
def jobs():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'id' not in data or 'job' not in data:
                return jsonify({"error": "Invalid input data. 'id' and 'job' are required."}), 400
            new_job = pd.DataFrame(data, index=[0])
            global jobs_df
            jobs_df = pd.concat([jobs_df, new_job], ignore_index=True)
            jobs_df.to_csv("jobs.csv", index=False)
            return jsonify({"message": "Job added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)