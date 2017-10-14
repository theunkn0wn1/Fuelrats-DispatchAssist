"""
Hosts a websocket server and miantains a API websocket connection
Interact with the server to get latest data from the API
Author: Theunkn0wn1
"""

import asyncio
import threading

import websockets as ws_server


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


class Server(threading.Thread):
    def __init__(self, port=8765):
        super().__init__()
        print("Server init")
        self.port = port  # port to host websocket server
        self.server = None

    async def on_message(self, websocket, path):
        message = await websocket.recv()
        print(f"--> {message}")
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
    print("registering Server instance...")
    my_server = Server(port=8700)
    print("starting server instance...")
    my_server.start()
    my_server.join()
