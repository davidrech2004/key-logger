from interfaces.iwriter import IWriter
import requests
from encryption.encryptor import Encryptor

class NetworkWriter(IWriter):
    def __init__(self, key: int, server_url: str):
        self.key = key
        self.server_url = server_url.rstrip("/")  
        self.encryptor = Encryptor(key)

    def send_data(self, data: str, machine_name: str) -> None:
        encrypted_data = self.encryptor.encrypt(data)
        payload = {"machine": machine_name, "data": encrypted_data}
        url = f"{self.server_url}/api/upload"

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            print(f"✅ Data sent successfully to {url}")
        except requests.RequestException as e:
            print(f"❌ Failed to send data: {e}")
            # שמירה מקומית לגיבוי
            fallback_file = f"failed_{machine_name}.txt"
            with open(fallback_file, "a", encoding="utf-8") as f:
                f.write(data + "\n")