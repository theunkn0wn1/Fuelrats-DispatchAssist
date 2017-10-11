import websocket
import json
import dispatch
bearer_token = ""  # TODO: NO NOT COMMIT!


class Config:
    # api_url = "wss://dev.api.fuelrats.com/"
    api_url = "wss://dev.api.fuelrats.com/?bearer={token}"
    token_file = "token.txt"
#
#
# get_board = {
#     'action': ['cases', 'read'],
#     'status': {'$not': 'closed'},
#     'data': {},
#     'meta': {}
# }


class Request:
    """
    Creates a request JSON object
    """
    def __init__(self, action, data, meta, status):
        self.action = action
        self.data = data
        self.meta = meta
        self.status = status

    def request(self):
        obj = {
            'action': self.action,
            'status': self.status,
            'data': self.data,
            'meta': self.meta
        }
        return json.dumps(obj)


def init():
    """Sets things up"""
    global bearer_token
    with open(Config.token_file, 'r') as file_object:
        file_object.readline()
        bearer_token = file_object.readline()[2:]


if __name__ == "__main__":
    # websocket.enableTrace(True)
    print("running init...")
    # init()
    print("init complete...")

    print("opening websocket...")
    print(Config.api_url.format(token=bearer_token))
    ws = websocket.create_connection(Config.api_url.format(token=bearer_token))
    print("connecting to {}".format(Config.api_url[:26]))
    ws.connect(url=Config.api_url[:26])

    print(ws.recv())
    message = Request(['rescues', 'read'], {}, {}, status={'$not': 'closed'})
    print(message.request())

    ws.send(message.request())
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
