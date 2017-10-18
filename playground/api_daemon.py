"""
Hosts a websocket server and miantains a API websocket connection
Interact with the server to get latest data from the API
Author: Theunkn0wn1
"""

import asyncio
import json
import logging
import pickle  # for sending / receiving cmd data
import threading

import websocket as ws_client  # for interacting with the API
import websockets as ws_server  # for hosting the WS server

import playground.shared_resources as shared_utils


class Config:
    api_url = "wss://dev.api.fuelrats.com/?bearer={token}/"
    # api_url = "wss://api.fuelrats.com/?bearer={token}/"
    token_file = "token.txt"


async def launcher(**kwargs):
    """
    Launches an async task with provided arguments without blocking
    :param kwargs: 'task' task to run, 'args' args to pass to async task
    :return:
    """
    my_task = asyncio.ensure_future(kwargs['task'](kwargs['args']))  # define a task, so it can be called
    # a task is different from a coroutine within asyncio... not exactly sure how
    asyncio.wait([my_task])  # awaiting here is blocking, so just call it


class Parser:
    @staticmethod
    def _parse_updates(data):
        pass

    @staticmethod
    def _parse_created(data):
        try:
            api_id = data['data']['id']  # API ID
            client = data['data']['attributes']['data']['IRCNick']  # as their IRC nickname can differ from their name
            system = data['data']['attributes']['system']  # fetch the system
            cr = data['data']['attributes']['codeRed']  # code red status
            platform = data['data']['attributes']['platform']  # platform
            index = data['data']['attributes']['data']['boardIndex']  # where they are on the board
            lang = data['data']['attributes']['data']['langID']  # and their language
            return shared_utils.Case(client=client, index=index, cr=cr, platform=platform, system=system,
                                     language=lang, api_id=api_id)
        except IndexError   :
            print("[CRITICAL]: Case creation failed, invalid data")
            return None  # default state, if parsing fails for some reason

    @staticmethod
    def parse(raw_json):
        try:
            data = json.loads(raw_json)
            if data['meta']['event'] == "rescueCreated":
                return Parser._parse_created(data=data)
            elif data['meta']['event'] == "rescueUpdated":
                return Parser._parse_updates(data=data)
        except Exception:
            return None


class API(threading.Thread):
    """
    Manages API connectivity
    """
    def __init__(self, url, api_token=None):
        super().__init__()
        self.url = url
        self.api_token = api_token
        self.socket = None
        self.messages_since_last_call = {}

    def subscribe(self, stream):
        query = {
            'action': ['stream', 'subscribe'],
            'id': stream,
            'data': {},
            'meta': {}
        }
        print(f"subscribing to {json.dumps(query)}")
        self.socket.send(json.dumps(query))

    def unsubscribe(self, stream):
        query = {
            'action': ['stream', 'subscribe'],
            'id': stream,
            'data': {},
            'meta': {}
        }
        print(f"subscribing to {json.dumps(query)}")
        self.socket.send(json.dumps(query))

    def _on_recv(self, socket, message):
        print("got message: data is {}".format(message))
        self.messages_since_last_call = message
        # socket:websocket.WebSocketApp
        # print("potato")
        # socket.close()

    def _on_open(self, socket):
        print("connection to API opened")
        # Api.my_websocket = socket

    def _on_error(self, socket, error):
        print("some error occured!\n{}".format(error))

    def _on_close(self, socket):
        print("####\tsocket closed\t####")

    def run(self):
        print("thread started")
        self.socket = ws_client.WebSocketApp(url=self.url.format(token=self.api_token),
                                             on_close=self._on_close,
                                             on_error=self._on_error,
                                             on_message=self._on_recv)
        self.socket.on_open = self._on_open
        logger.log(msg="Running server...", level=10)
        self.socket.run_forever()
        logger.log(level=0, msg="Exiting thread...")

    def send_message(self, message):
        # self.socket: ws_client.WebSocketApp
        self.socket.send(message)
        # await self.socket.close()

    def get_last_message(self):
        return self.messages_since_last_call

    def close_connection(self):
        print("Closing connection...")
        self.socket.close()


class Server(threading.Thread):
    def __init__(self, port=8765):
        super().__init__()
        print("Server init")
        self.port = port  # port to host websocket server
        self.server = None

    async def on_message(self, websocket, path):
        """
        Handles incoming commands from websocket clients
        :param websocket: client websocket connection to respond over
        :param path: not entirely sure what this is for...
        :return:
        """
        message = await websocket.recv()
        print(f"[INCOMING] --> {message}")
        try:
            data = pickle.loads(message)
        except TypeError:
            if message == "qqq":
                await websocket.send("farewell cruel world!")
                websocket: ws_server.server.WebSocketServerProtocol
                api_instance.close_connection()
                websocket.close()
                asyncio.get_event_loop().stop()
            elif message == "fetch":
                # await websocket.send("Done.")
                api_instance.send_message(
                    '{"action": ["rescues", "read"], "status": {"$not": "closed"}, "data": {}, "meta": {}}')
                await websocket.send("Done.")
                # await websocket.close()
            elif message == "potato":
                await websocket.send("POTATOES!")
            elif message == "latest":
                await websocket.send(api_instance.messages_since_last_call)
            elif message == "deadbeef":
                print("sending done...")
                await websocket.send("Done.")
                # api_instance.send_message(0xDEADBEEF)
                print("subscribing...")
                api_instance.subscribe("0xDEADBEEF")
            else:
                await websocket.send(message)

        else:
            if isinstance(data, shared_utils.Request):
                api_instance.send_message(data.request())
                await websocket.send("DONE.")

    def run(self):
        print("server start")
        loop = asyncio.new_event_loop()
        self.server = ws_server.serve(self.on_message, 'localhost', self.port)
        # asyncio.get_event_loop().run_until_complete(self.server)
        # asyncio.get_event_loop().run_forever()
        loop.run_until_complete(self.server)
        loop.run_forever()
        pass


if __name__ == "__main__":
    logger = logging.getLogger('websockets.server')
    logger.setLevel(logging.ERROR)
    logger.addHandler(logging.StreamHandler)
    print("registering Server instance...")
    my_server = Server(port=8700)
    print("starting server instance...")
    my_server.start()
    print("instance started")
    print("starting API session...")
    api_instance = API(Config.api_url, api_token=input())
    api_instance.start()
    my_server.join()  # prevent server from terminating ungracefully
    # TODO implement graceful shutdown when commanded over ws
    # TODO somehow implement unit tests for this project...
    # TODO replace print() calls with a logger call (makes it thread safe and easier to understand / expand
