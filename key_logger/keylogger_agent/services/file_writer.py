import os 
from interfaces.iwriter import IWriter
from datetime import datetime

class FileWriter(IWriter):
    def __init__(self, file_path:str):
        self.file_path = file_path
        self._ensure_directory_exists(file_path)

    def send_data(self, data:str, machine_name:str):
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"log_{date_str}.txt"
        full_path = os.path.join(self.file_path, machine_name, file_name)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "a", encoding="utf-8") as f:
            f.write(f"{data}\n")

    def _ensure_directory_exists(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path)