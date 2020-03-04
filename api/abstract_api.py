from abc import ABC, abstractmethod

import core

class AbstractAPI(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send_response(self, request: core.Request):
        pass