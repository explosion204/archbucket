from abc import ABCMeta

class AbstractAPI(metaclass=ABCMeta):
    class Meta:
        name = None
        
    def __init__(self, request_queue):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def send_response(self, request):
        pass

class AbstractScript(metaclass=ABCMeta):
    class Meta:
        name = None
        
    def run(self, request):
        pass
