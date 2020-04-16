import os

# path to modules and api files
API_PATH = os.path.join(os.path.dirname(__file__), 'api')
MODULES_PATH = os.path.join(os.path.dirname(__file__), 'modules')

# module or api state
DISABLED = 'disabled'
ENABLED = 'enabled'

# path to log files
LOGFILES_PATH = os.path.dirname(__file__) + '/logs'

# port value constraints
MIN_PORT_VALUE = 0
MAX_PORT_VALUE = 65535