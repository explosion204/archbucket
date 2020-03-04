from abc import ABC, abstractmethod
from core import Request

class AbstractAPI(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send_response(self, request: Request):
        pass