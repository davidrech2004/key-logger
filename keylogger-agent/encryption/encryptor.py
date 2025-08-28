# פונקציה שמצפינה ומתרגמת כל תוכן על ידי נתינת מפתח
class Encryptor:
    def __init__(self, key):
        # מקבלים את המפתח שיעשה בעצם את ההצפנה
        if isinstance(key, str):
            # המר את המחרוזת למספר באמצעות hash או קח רק את המספרים
            try:
                self.key = int(key) if key.isdigit() else hash(key) % 65536
            except:
                self.key = hash(key) % 65536
        else:
            self.key = key

    def encrypt(self, text:str) -> str:
        # בשביל לעשות את ההמרה מה שעושים זה בעצם הופכים כל אות מהמילה שמקבלים לקוד יוניקוד ועושים הצפנת יוניקוד ומוסיפים את זה למערך אחרי שעושים המרה הפוכה
        result = []
        for char in text:
            code = ord(char)
            encrypted = code ^ self.key
            # בודק שזה נמצא בתחום שצריך בקוד יוניקוד ולא יחזיר שגיאה
            result.append(chr(encrypted % 0x110000))
        return ''.join(result)
    
    def decrypt(self, text) -> str:
        # ההמרה ההפוכה היא בדיוק אותו הדבר
        return self.encrypt(text)