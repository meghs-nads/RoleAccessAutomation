from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- function to get db_name from meta table ---
def get_target_db_name(app_name):
    app_name = app_name.lower()  # normalize input

    # connect to meta database
    meta_conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("META_DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    meta_cur = meta_conn.cursor()

    meta_cur.execute("SELECT db_name FROM app_db_map WHERE app_alias = %s", (app_name,))
    row = meta_cur.fetchone()

    meta_cur.close()
    meta_conn.close()

    if not row:
        raise ValueError(f"Unknown app name: {app_name}")

    return row[0]

# --- main connection function ---
def get_db_connection(app_name):
    db_name = get_target_db_name(app_name)

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=db_name,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# --- API endpoint ---
@app.route('/assign_role', methods=['POST'])
def assign_role():
    data = request.json
    app_name = data.get('AppName')
    employee_id = data.get('EmployeeId')
    role_name = data.get('RoleName')

    if not app_name or not employee_id or not role_name:
        return jsonify({'error': 'AppName, EmployeeId, and RoleName are required'}), 400

    try:
        conn = get_db_connection(app_name)
        cur = conn.cursor()
        cur.execute('SELECT assign_role_to_employee(%s, %s);', (employee_id, role_name))
        result = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
