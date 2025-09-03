from encryption.encryptor import Encryptor

# פונקציה שמפעילה את המצפין על הפייל ומתרגם אותו
def decrypt_file(file_path: str, key:str) -> str:
    # בעצם פותח את הקובץ עם encoding שתומך ברוב השפות ואז מחזירים את זה ללא הצפנה על ידי המחלקה encryptor
    with open(file_path, "r", encoding="utf-8") as f:
        encrypted_text = f.read()

    enc = Encryptor(key)
    return enc.decrypt(encrypted_text)