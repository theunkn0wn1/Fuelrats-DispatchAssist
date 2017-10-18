import json
import threading
import websocket
from time import sleep
import json
import threading
from time import sleep

import websocket

# import dispatch
# from dispatch import Case
__module_name__ = "api_playground"
__module_version__ = "0.0.2"
__module_description__ = "what could possibly go wrong?"
bearer_token = ""  # TODO: NO NOT COMMIT!
is_shutdown = False  # set this to true for child threads to quit
try:
    import hexchat as hc
except ImportError:
    hc = None


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


class Api:
    my_websocket = None
    @staticmethod
    def on_recv(socket, message):
        print("got message: data is {}".format(message))
        # socket:websocket.WebSocketApp
        sleep(2)
        print("potato")
        socket.close()
    @staticmethod
    def on_open(socket):
        print("connection to API opened")
        Api.my_websocket = socket

    @staticmethod
    def on_error(socket, error):
        print("some error occured!\n{}".format(error))

    @staticmethod
    def on_close(socket):
        print("####\tsocket closed\t####")

    @staticmethod
    async def parse_json(data: dict):
        """
        parse_json incoming client data from API
        :param data: dict, raw JSON dict to parse_json
        :return output_data: array of Case instances
        """
        output_data = {}  # since we are going to be parsing multiple cases at once
        for entry in data['data']:
            await output_data.update({entry['attributes']['data']['boardIndex']: Case(
                client=entry['attributes']['data']['IRCNick'],
                language=entry["attributes"]['data']['langID'],
                cr=entry['attributes']['codeRed'],
                system=entry['attributes']['system'],
                index=entry['attributes']['data']['boardIndex'],
                platform=entry['attributes']['platform'],
                raw=entry

            )})
        return output_data

    @staticmethod
    async def retrieve_cases(socket):
        """

        :param socket: open websocket to tx/rx over
        :return:
        """
        # socket: websocket.WebSocket
        await socket.send(Request(['rescues', 'read'], {}, {}, status={'$not': 'open'}))
        response = await socket.recv()  # as this may take a while
        return Api.parse_json(response)
        # return response

    @staticmethod
    def worker():
        """
        Fetch and maintain a websocket connection to the API
        :return:
        """

        if is_shutdown:  # if this thread was somehow spawned during shutdown
            return None
        else:  # let the games begin
            # Do init
            # ws = websocket.create_connection(Config.api_url.format(token=bearer_token), )
            # spawn a websocket client instance
            url =Config.api_url.format(token=bearer_token)
            # print("url = {}".format(url))
            ws_client = websocket.WebSocketApp(url=url,
                                               on_close=Api.on_close,
                                               on_error=Api.on_error,
                                               on_message=Api.on_recv)
            ws_client.on_open = Api.on_open
            # loop = asyncio.get_event_loop()
            ws_client.run_forever()


def start_api_connection():
    print("====================")
    print("actually starting the worker now...")
    t = threading.Thread(target=Api.worker)
    t.start()
    return t


def init():
    """Sets things up"""
    global bearer_token
    with open(Config.token_file, 'r') as file_object:
        file_object.readline()
        bearer_token = file_object.readline()


if __name__ == "__main__":
    api_instance = start_api_connection()
