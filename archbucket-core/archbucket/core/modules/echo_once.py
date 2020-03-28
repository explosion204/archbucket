from archbucket.core.bot import Request

def run(request: Request) -> bool:
    '''
    Example function.
    ARGS: request -> Request from core module
    RETURN VALUE: flag whether active session is needed by script to be closed. 
    '''
    if len(request.args) != 0:
        request.response =  ' '.join(request.args)
    else: 
        request.response = 'error'
    return True