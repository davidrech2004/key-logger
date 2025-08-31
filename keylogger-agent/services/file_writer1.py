from iwriter1 import IWriter

class FileWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def send_data(self, data: str, machine_name: str) -> None:
        try:
            with open(self.file_path, 'a') as file:
                file.write(f"{machine_name}: {data}\n")
        except Exception as e:
            open(f"Error: {e}")
# ## exmple:
# writer = FileWriter("C:\\Program Files\\WindowsPowerShell\\log.txt")