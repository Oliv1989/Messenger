"""Constants"""

#Default port for web processing
DEFAULT_PORT = 7777
#IP default address for client connection
DEFAULT_IP_ADDRESS = '127.0.0.1'
#Max connection queue
MAX_CONNECTIONS = 5
#Max message length in bytes
MAX_PACKAGE_LENGTH = 1024
#Project encoding
ENCODING = 'utf-8'

#Protocol JIM main keys:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

#Additional keys
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'

#Logging keys
LOGGING_LEVEL = 10 #0-NOTSET, 10-DEBUG, 20-INFO, 30-WARNING, 40-ERROR, 50-CRITICAL
