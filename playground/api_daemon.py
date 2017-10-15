"""
Hosts a websocket server and miantains a API websocket connection
Interact with the server to get latest data from the API
Author: Theunkn0wn1
"""

import asyncio
import logging
import threading

import websocket as ws_client  # for interacting with the API
import websockets as ws_server  # for hosting the WS server


class Config:
    api_url = "wss://dev.api.fuelrats.com/?bearer={token}/"
    # api_url = "wss://api.fuelrats.com/?bearer={token}"
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


class API(threading.Thread):
    """
    Manages API connectivity
    """
    def __init__(self, url, api_token=None):
        super().__init__()
        self.url = url
        self.api_token = api_token
        self.socket = None

    def on_recv(self, socket, message):
        print("got message: data is {}".format(message))
        # socket:websocket.WebSocketApp
        print("potato")
        # socket.close()

    def on_open(self, socket):
        print("connection to API opened")
        # Api.my_websocket = socket

    def on_error(self, socket, error):
        print("some error occured!\n{}".format(error))

    def on_close(self, socket):
        print("####\tsocket closed\t####")

    def run(self):
        print("thread started")
        self.socket = ws_client.WebSocketApp(url=self.url.format(token=self.api_token),
                                             on_close=self.on_close,
                                             on_error=self.on_error,
                                             on_message=self.on_recv)
        self.socket.on_open = self.on_open
        logger.log(msg="Running server...", level=10)
        self.socket.run_forever()
        logger.log(level=0, msg="Exiting thread...")

    async def potato(self):
        self.socket: ws_client.WebSocketApp
        await self.socket.send("{}")
        # await self.socket.close()


class Server(threading.Thread):
    def __init__(self, port=8765):
        super().__init__()
        print("Server init")
        self.port = port  # port to host websocket server
        self.server = None

    async def on_message(self, websocket, path):
        message = await websocket.recv()
        print(f"--> {message}")
        if message == "qqq":
            await websocket.send("farewell cruel world!")
            await api_intance.potato()
            websocket: ws_server.server.WebSocketServerProtocol
            websocket.close()
            print(f"{type(websocket)})")
            asyncio.get_event_loop().stop()
        elif message == "test":
            await api_intance.potato()
            await websocket.send("Done.")
            websocket.close()
        else:
            await websocket.send(message)

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
    api_intance = API(Config.api_url, api_token=input())
    api_intance.start()
    my_server.join()
