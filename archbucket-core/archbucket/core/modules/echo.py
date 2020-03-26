from ..request_router import Request

def run(request: Request) -> bool:
    '''
    Example function.
    ARGS: request -> Request from core module
    RETURN VALUE: flag whether active session is needed by script to be closed. 
    '''
    if len(request.args) != 0:
        if request.args[0] == 'stop':
            return True
        request.response =  ' '.join(request.args)
    else: 
        request.response = 'error'
    return False