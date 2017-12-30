import json
from functools import wraps
# Globals  # im pretty sure im going to need these since im importing into hex...
__module_name__ = "Dispatch-resources"
__module_version__ = "0.0.2"
__module_description__ = "Shared resources for Dispatch and its children"
verbose_logging = False  # if you want to see everything, it can be deafening.
"""Shared data structures for communicating with the daemon"""

def eat_all(wrapped_function):
    """:returns hc.EAT_ALL at end of wrapped function"""
    try:
        import hexchat as hc
    except ImportError as ex:
        hc = None

    @wraps(wrapped_function)  # prevents decorator from swallowing docstrings
    def wrapper(arg,*args, **kwargs):
        wrapped_function(arg, *args, **kwargs)
        if hc is not None:
            # print("returning {}".format(hc.EAT_ALL))
            return hc.EAT_ALL
        else:
            return 3  # so i can test commands without hexchat being loaded,3 is the enum value
    return wrapper


def log(trace, msg, verbose=False):
    global verbose_logging
    if verbose_logging:
        print("[{Stack}:{trace}]\t{message}".format(Stack=__module_name__, message=msg, trace=trace))
    elif verbose:
        print("[{Stack}:{trace}]\t{message}".format(Stack=__module_name__, message=msg, trace=trace))


class Case:
    """
    Stores a case
    """
    def __init__(self, client=None, index=None, cr=False, platform=None, rats=None, system=None, stage=0, language=None,
                 raw=None, api_id=None):
        self.client = client
        self.index = index
        self.platform = platform
        self.cr = cr
        self.rats = rats if rats is not None else []
        self.stage = stage
        self.language = language
        self.wing = False
        self.has_forwarded = False
        self.system = system
        self.api_id = api_id
        self.raw = raw  # debug symbol

    def Stage(self, status):
        """
        Updates client stage
        :param status: status to set
        :return:
        """
        if isinstance(status, int):
            self.stage = status
        elif isinstance(status, str):
            pass

    def Client(self, client):
        """
        Updates client name
        :param client: new name
        """
        if isinstance(client, str):
            self.client = client
        else:
            raise TypeError("client must be of type str")

    def System(self, system):
        """
        Changes the Case's current set_system
        :param system:str new set_system
        """
        if type(system) is str:
            self.system = system
        else:
            raise TypeError("set_system must be of type str")

    def Rats(self, rats, mode='add'):
        if isinstance(rats, str):
            if mode is "add":
                self.rats.append(rats)

            elif mode is "remove":
                try:
                    return self.rats.pop(self.rats.index(rats))
                except ValueError:
                    log("Case:Rats", "{value} is not a assigned rat!")
        elif isinstance(rats, list) and mode == "add":
            for rat in rats:
                    self.rats.append(rat)
            # self.add_rats = add_rats
        elif isinstance(rats, list) and mode is "remove":
            for rat in rats:
                i = 0
                for value in self.rats:
                    if value == rat:
                        self.rats.pop(i)
                    i += 1
        else:
            raise TypeError("add_rats must be type str or list. got {} with mode char {}".format(
                type(rats), mode))

    def Cr(self):
        self.cr = not self.cr

    def Platform(self, data):
        if isinstance(data, str):
            self.platform = data.upper()
        else:
            raise TypeError("data expected to be type str")

    def __contains__(self, item):
        if item is None or not isinstance(item, str):
            if isinstance(item,int):
                if item == self.index:
                    return True
            else:
                raise TypeError("got {} expected str".format(type(item)))
        elif item == self.client:
            return True

        elif item.lower() == self.platform.lower():
            return True
        elif self.rats is not None and item in self.rats:
            return True
        else:
            log("case.__contains__", "value is {} of type {}".format(item, type(item)))
            return False


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


class Stage():
    """
    Contains a missions Stage data
    """

    def __init__(self):
        self.last_run_command = ""

    def get_next_command(self):
        pass

from enum import Enum
events = []
class Logger:
    pass

    @classmethod
    class LogSeverity(Enum):
        """
        Enum defining severity by name
        """
        info = 0
        low = 1
        warning = 2
        error = 3
        fatal = 4
    class Event():
        """
        Event object, expects severity and a message
        """

        def __init__(self, severity: Logger.LogSeverity, message: str):
            self.severity = severity
            self.message = message
    @classmethod
    def print_event(cls,event: Event) -> None:
        """
        prints a given Event to the stdout
        :param event: Event object to print
        :return:None
        """
        if event.severity is cls.LogSeverity.info:
            print("[   info]: {}".format(event.message))
        elif event.severity is cls.LogSeverity.low:
            print("[    low]: {}".format(event.message))
        elif event.severity is cls.LogSeverity.warning:
            print("[warning]: {}".format(event.message))
        elif event.severity is cls.LogSeverity.error:
            print("[   error: {}".format(event.message))
        elif event.severity is cls.LogSeverity.fatal:
            print("[  fatal]: {}".format(event.message))

