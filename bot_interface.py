import core
import pipeline
import threading
from api.abstract_api import AbstractAPI

class BotInterface:
    def __init__(self):
        self.pipelines = list()

    def push_request(self, request):
        free_pipelines = [item for item in self.pipelines]
        min_pipeline = min(free_pipelines, key=lambda item: item.count)
        min_pipeline.push_request(request)

    def create_pipeline(self):
        new_pipeline = pipeline.Pipeline(self.bot_api)
        self.pipelines.append(new_pipeline)
        pipeline_thread = threading.Thread(target=new_pipeline.start)
        pipeline_thread.start()

    def set_api(self, bot_api: AbstractAPI):
        self.bot_api = bot_api

    def start_bot(self):
        self.bot_api.start()