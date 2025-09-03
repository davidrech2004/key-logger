from abc import ABC, abstractmethod
from typing import List

# פונקציה אבסטרקטית להתחלת הפעולה סיום הפעולה וקבלת המידע
class Ikeylogger(ABC):
    @abstractmethod
    def start_logging(self) -> None:
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        pass

    @abstractmethod
    def get_logged_keys(self) -> List[str]:
        pass