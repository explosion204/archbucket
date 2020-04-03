import ast
import re
import os
import json
import importlib
import inspect

from .pipeline import Pipeline
from .request_router import RequestRouter, Request
from threading import Thread

class Bot:
    def __init__(self, pipelines_count, api_dict):
        self.pipelines = list()

        for _ in range(pipelines_count):
            # setting pipelines
            new_pipeline = Pipeline(self)
            self.pipelines.append(new_pipeline)
            pipeline_thread = Thread(target=new_pipeline.start)
            pipeline_thread.start()

        # setting up request router
        self.request_router = RequestRouter()
        
        # loading api classes
        self.api_dict = api_dict
        self.busy = False

    def push_request(self, request):
        while True:
            if not self.busy:
                self._find_pipeline(request)
                break

    def _find_pipeline(self, request):
        self.busy = True
        free_pipelines = [item for item in self.pipelines]
        min_pipeline = min(free_pipelines, key=lambda item: item.count)
        min_pipeline.push_request(request)
        self.busy = False

    def start_bot(self):
        for api_instance in self.api_dict.values():
            try:
                api_thread = Thread(target=api_instance.start, args=(self, ))
                api_thread.start()
            except Exception:
                pass

    def stop_bot(self):
        for api_instance in self.api_dict.values():
            try:
                api_instance.stop()
            except Exception:
                pass

    def send_response(self, request: Request):
        self.api_dict[request.api_name].send_response(request)
