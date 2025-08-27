import os 
from datetime import datetime
from interfaces.iwriter import IWriter

class FileWriter(IWriter):
    def __init__(self, file_path:str):
        self.file_path = file_path
        self._ensure_directory_exists(file_path)

    def send_data(self, data:str, machine_name:str):
        file_name = self._generate_filename()
        full_path = os.path.join(self.file_path, file_name)
        with open(full_path, "a", encoding="urf-8") as f:
            f.write(f"[{machine_name}] {data}\n")

    def _ensure_directory_exists(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path)
        
    def _generate_filename(self):
        return f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
