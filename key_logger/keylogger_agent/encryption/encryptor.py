import hashlib

class Encryptor:
    def __init__(self, key):
        if isinstance(key, str):
            # מפתח דטרמיניסטי מבוסס SHA256
            self.key = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 65536
        else:
            self.key = int(key) % 65536
            

    def transform(self, text:str) -> str:
        # בשביל לעשות את ההמרה מה שעושים זה בעצם הופכים כל אות מהמילה שמקבלים לקוד יוניקוד ועושים הצפנת יוניקוד ומוסיפים את זה למערך אחרי שעושים המרה הפוכה
        result = []
        for char in text:
            code = ord(char)
            encrypted = code ^ self.key
            # בודק שזה נמצא בתחום שצריך בקוד יוניקוד ולא יחזיר שגיאה
            result.append(chr(encrypted % 0x110000))
        return ''.join(result)
    
    def encrypt(self, text:str) -> str:
        return self.transform(text)
    
    def decrypt(self, text) -> str:
        # ההמרה ההפוכה היא בדיוק אותו הדבר
        return self.transform(text)