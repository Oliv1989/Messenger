"""Utils"""

import json
from decos import log
from common.variables import MAX_PACKAGE_LENGTH, ENCODING

@log
def rcv_msg(client):
    '''
    Util is getting and decoding messages (in-bytes; out-dict; else-ValueError)
    '''
    encoded_resp = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_resp, bytes):
        json_resp = encoded_resp.decode(ENCODING)
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            return resp
        raise ValueError
    raise ValueError

@log
def set_off_msg(sock, msg):
    '''
    Util is coding and setting off messages (in-dict; out-dict)
    '''
    js_msg = json.dumps(msg)
    encoded_msg = js_msg.encode(ENCODING)
    sock.send(encoded_msg)
