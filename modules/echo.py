from core import Request

def run(request: Request) -> str:
    if len(request.args) != 0:
        request.response =  ' '.join(request.args)
    else: 
        request.response = 'error'