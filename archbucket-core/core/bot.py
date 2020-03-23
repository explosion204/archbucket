from core.request_router import RequestRouter, Request
from core.pipeline import Pipeline
from threading import Thread

class Bot:
    def __init__(self):
        self.pipelines = list()
        self.request_router = RequestRouter()

    def push_request(self, request):
        free_pipelines = [item for item in self.pipelines]
        min_pipeline = min(free_pipelines, key=lambda item: item.count)
        min_pipeline.push_request(request)

    def create_pipeline(self):
        new_pipeline = Pipeline(self)
        self.pipelines.append(new_pipeline)
        pipeline_thread = Thread(target=new_pipeline.start)
        pipeline_thread.start()

    def start_bot(self, bot_api):
        self.bot_api = bot_api
        self.bot_api.start(self)

    def stop_bot(self):
        self.bot_api.stop()

    def send_response(self, request: Request):
        self.bot_api.send_response(request)