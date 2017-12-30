import json
from abc import ABC, abstractmethod
from functools import wraps

# Globals  # im pretty sure im going to need these since im importing into hex...
__module_name__ = "Dispatch-resources"
__module_version__ = "0.0.2"
__module_description__ = "Shared resources for Dispatch and its children"
verbose_logging = False  # if you want to see everything, it can be deafening.
"""Shared data structures for communicating with the daemon"""
try:
    import hexchat as hc
except ImportError as ex:
    hc = None

def eat_all(wrapped_function):
    """:returns hc.EAT_ALL at end of wrapped function"""


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

class Utilities:
    @staticmethod
    def play_beep():
        """PLay a sound"""
        pass

    @staticmethod
    def strip_fancy(word, allowed_fancy=None):
        """
        Strips non alphanumeric values from a string
        :param word: word to strip
        :param allowed_fancy: non-alpha numeric characters to preserve
        :returns ret: sanitized string
        """
        ret = ""
        for char in word:
            if char.isalpha() or char.isnumeric():
                ret += char
            elif allowed_fancy is not None and char in allowed_fancy:
                ret += char
        return ret


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

        def __init__(self, severity, message: str):
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

class Parser:
    """
    Contains methods to parse incoming data. use .parse()
    """
    @staticmethod
    def parse_inject(capture):
        """Parses inject message events"""
        log("parse_inject", "parsing capture event with data: {}".format(capture))
        # [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":ClientName's", 'case', 'opened',
        #  'with:', '"sol', 'pc"', '(Case', '3,', 'PC)']
        if capture is None:
            log("parse_inject", "Invalid capture event")
        elif capture[0] != ':DrillSqueak[BOT]!sopel@bot.fuelrats.com' and capture[0] != ':MechaSqueak[BOT]!sopel@bot.fuelrats.com':
            log("parse_inject", " invalid capture event")
        else:
            log("parse_inject", 'Beginning parse attempt')
            i = 0
            # client = inject_args['client']
            # platform = inject_args['set_system']
            case = -1
            log("step1", 'completed!')
            client = platform =system = None  # init before use
            for phrase in capture:
                if phrase == 'PC)' or phrase == 'PS4)' or phrase == 'XB)':
                    log('step2', 'searching for platform...')
                    platform = phrase.strip(')')
                    log('step2', 'platform is {}'.format(platform))
                elif phrase[:5] == 'case':
                    log('step3', 'looking for client name...')
                    parsed_string = capture[i - 1]  # phrase before is the client name
                    parsed_string = parsed_string[:len(parsed_string) - 2]  # strip the 's from the end
                    parsed_string = parsed_string.strip(':')  # and the : from the start
                    client = parsed_string  # And we have our product!
                    log('step3', 'client is {}'.format(client))
                elif phrase == "(Case":
                    log('step4', 'searching for CaseID...')
                    case = capture[i + 1].strip(',')
                    log('step4', 'cid is {CID}'.format(CID=case))
                elif phrase.lower() == "with:":
                    system = capture[i + 1].strip('"')
                else:
                    # log("failed:", "word not read: {}".format(phrase))
                    pass
                i += 1
            # log("parse_inject", "append({},{},{},{},{})".format(case, client, platform, False, 'En-us'))
            return Case(client, case, platform=platform, system=system)

    @staticmethod
    def parse_ratsignal(phrase):
        """
        parses ratsignal events
        """
        i = 0
        client = platform = lang = cr = cid = system = None  # init before use.. prevent potential errors
        for word in phrase:
            cleaned_word = word
            if cleaned_word == "CMDR":
                z = i + 2
                client = Utilities.strip_fancy(phrase[i + 1])
                while phrase[z] != "-":
                    client += "_"  # as IRC turns spaces into underscores
                    client += Utilities.strip_fancy(phrase[z])
                    z += 1

            elif cleaned_word == 'Platform:':
                platform = Utilities.strip_fancy(phrase[i + 1])
                if platform == "12PS4" or platform == "03XB":
                    platform = platform[2:]  # strip the colour code

            elif cleaned_word == "Language:":
                lang = Utilities.strip_fancy(phrase[i + 2])  # fetch the lang code

            elif cleaned_word == "O2:":
                log("parser:parse_ratsignal", "o2 is {}".format(phrase[i+1]))
                cr = phrase[i + 1]
                if cr == 'OK':
                    cr = False
                else:
                    cr = True
            elif cleaned_word == "(Case":
                cid = phrase[i + 1].strip("#").strip(")")

            elif cleaned_word == "System:":
                z = i + 1
                system = ""
                while phrase[z] != "-":
                    if "(" in phrase[z] or "not" in phrase[z]:  # checks if we have reached the distance from part of the system
                        break  # and discard, since it is not part of the actual system name
                    else:
                        system += " "
                        system += Utilities.strip_fancy(phrase[z], allowed_fancy="-")
                        z += 1
                # set_system.find()
            i += 1
        if cid is None:
            cid = -1  # error handling, so the case can still be deleted
        # return Case(client, cid, cr, platform, stage=0)
        return Case(client=client, index=cid, cr=cr, platform=platform, system=system, language=lang, raw=phrase)
        # return {'client': client, 'platform': platform, 'cr': cr, "case": cid, "lang": lang,
        #                 'set_system': set_system, 'stage': 0}

    @staticmethod
    def parse_clear(**kwargs):
        # [':MechaSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#fuelrats', ':Case', 'Slate_gorgon', 'got', 'cleared!']
        data = kwargs['data']
        is_valid = False
        client = None
        if data is not None or "":
            i = 0
            for word in data:
                if word == ":Case":
                    log("parse_clear", "found client name")
                    client = data[i+1]
                    log("parse_clear", "client is {}".format(client))
                elif word == "got" and data[i+1] == "cleared!":
                    is_valid = True
                i += 1
            return client if is_valid else None

    @staticmethod
    def parse_cr(**kwargs):
        i = 0
        client = None
        #  [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ':CODE', 'RED!', 'rowdy0452', 'is', 'on', 'emergency', 'oxygen.']
        data = kwargs['data']
        for word in data:
            if Utilities.strip_fancy(word).lower() == 'code' and Utilities.strip_fancy(data[i+1]).lower() == "red":
                client = data[i+2]
            i += 1
        case = Tracker.get_case(value=client)
        # case: Case
        case.toggle_cr()
        return case

    @staticmethod
    def parse(**kwargs):
        """Attempts to parse incoming data,
        :returns bool or Case object
        """
        # [':MechaSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#fuelrats', ':tonyg940:', 'To', 'add', 'th
        data = kwargs['data']
        event_type = data[3]  # What kind of input
        if event_type == ":RATSIGNAL":
            return Parser.parse_ratsignal(data)
        elif Utilities.strip_fancy(event_type).lower() == "case":
            return Parser.parse_clear(data=data)
        elif event_type[-2:] == "'s":  # injected cases open with "{client}'s"
            log("Parse.part", "event type = {}".format(event_type))
            return Parser.parse_inject(data)
        elif Utilities.strip_fancy(event_type).lower() == "code":
            return Parser.parse_cr(data=data)
        else:
            log("Parser.parse", "Unknown phrase.")
            return None
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

class CommandBase(ABC):
    """
    Abstract for defining stage commands
    """
    registered_commands = {}  # registry
    name = ""  # command name
    alias = []  # command alias
    # commands = {}
    @classmethod
    def _registerCommand(cls, func_instance, hook=True) -> None:
        """

        :param func_instance:
        :return:
        """
        new_entry = {func_instance.name:func_instance}
        if hc is not None:
            if hook:
                hc.hook_command(func_instance.name, func_instance.func)
        if func_instance.alias:  # type coercion, as long as its not empty nor None this is true
            for val in func_instance.alias:
                log("CommandBase._registerCommand", "registering hook for {}".format(val))
                new_entry.update({val:func_instance})
                if hc is not None and hook:
                    hc.hook_command(val, func_instance.func)

        cls.registered_commands.update(new_entry)

    @classmethod
    def getCommand(cls, name):
        """
        Fetches command by name or alias
        :param name: name/alias to lookup
        :return: CommandBase Instance
        """
        if isinstance(name, str):
            if name in cls.registered_commands:
                return cls.registered_commands[name]
            else:
                return None
        else:
            raise TypeError("name was of type {} with data {}".format(type(name), name))

    @abstractmethod
    def func(self, word, word_eol, userdata=None):
        """Command action"""
        raise NotImplementedError("func method not defined, please do tell the developer they missed a spot.")

    def __init__(self):
        self._registerCommand(self)

