class Encryptor:
    def __init__(self, key):
        # מקבלים את המפתח שיעשה בעצם את ההצפנה
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
    
en = Encryptor(42)
print(en.decrypt(en.encrypt("hello david")))