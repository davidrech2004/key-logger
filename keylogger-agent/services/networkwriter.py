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
        print(f"Sending to URL: {url}")  
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print(f"✅ Data sent successfully to {url}")
        except requests.RequestException as e:
            print(f"❌ Failed to send data: {e}")