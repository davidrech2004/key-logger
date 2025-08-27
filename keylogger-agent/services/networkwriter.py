from interfaces.iwriter import IWriter
import requests
from encryption import Encryptor  

# פונקצייה שמקבלת מידע ומצפינה אותו ומכניסה למילון את המידע ואת המיקום שצריך לשלוח את המידע ומוציאה הודעה אם הצליחה
class NetworkWriter(IWriter):
    def __init__(self, key:int, server_url:str):
        self.key = key
        self.server_url = server_url
        self.encryptor = Encryptor(key)

    def send_data(self, data:str, machine_name:str) -> None:
        # ההצפנה של המידע שמקבלים
        encrypted_data = self.encryptor.encrypt(data)
        payload = {"machin_name" : machine_name,
                   "data" : encrypted_data}
        
        try:
            # מבקש מהשרת להעלות את המידע
            response = requests.post(self.server_url, json=payload)
            # בודק אם השרת העלה ואם יש שגיאה (כל דבר שנקבל שהוא לא 200)
            response.raise_for_status()
            print(f"Data sent successfully to {self.server_url}")
        except requests.RequestException as e:
            # ההודעה במקרה של שגיאה
            print(f"Failed to send data: {e}")