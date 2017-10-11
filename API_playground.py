import asyncio
import json

import websocket

# import dispatch
from dispatch import Case

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


class Api:
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
        socket: websocket.WebSocket
        socket.send(Request(['rescues', 'read'], {}, {}, status={'$not': 'open'}))
        response = await socket.recv()  # as this may take a while
        return Api.parse_json(response)
        # return response


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
    message = Request(['rescues', 'read'], {}, {}, status={'$not': 'open'})
    # message = Request(['rescues', 'read'], {}, {}, {})
    print(message.request())
    ws.send(message.request())
    result = ws.recv()
    print("Received '%s'" % result)

    print("attempting parse_json")
    parsed_result = json.loads(result)
    print(parsed_result)
    loop = asyncio.get_event_loop().run_until_complete(Api.retrieve_cases())
    print("attempting Case conversion...")
    case_data = parse_json()
    for case in case_data:
        x=case_data.get(case)
        print("{index}: client = {client}\tplatform={platform}\tcr={cr}\tsystem={system}".format(
            index=x.index, client=x.client, platform=x.platform, cr=x.cr, system=x.system))
    ws.close()
