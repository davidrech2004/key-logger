from abc import ABC, abstractmethod

# פונקציה אבסטרקטית לשליחת המידע לשרת
class IWriter(ABC):
    @abstractmethod
    def send_data(self, data: str, machine_name: str) -> None:
        pass

