from functools import wraps  # so decorators don't swallow docstrings

import hexchat as hc
from tabulate import tabulate  # for outputting pretty tables

# Globals
__module_name__ = "dispatch"
__module_version__ = "0.0.1"
__module_description__ = "Assist with automating trivial FuelRat dispatch interactions"
database = {}
verbose_logging = True  # if you want to see everything, it can be deafening.
# Debug constants
debug_constant_a = [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":ClientName's", 'case', 'opened', 'with:', '"sol', 'pc"', '(Case', '4,', 'PC)']
debug_constant_B = [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":Potato's", 'case', 'opened', 'with:', '"ki', 'ps"', '(Case', '9,', 'PS4)']
debug_constant_C = ['\x0329RatMama[BOT]', 'Incoming Client: Azrael Wolfmace - System: LP 673-13 - Platform: XB - O2: OK - Language: English (English-US) - IRC Nickname: Azrael_Wolfmace', '&']
rsig_message = [':MechaSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#fuelrats', ':RATSIGNAL', '-', 'CMDR', '\x02dan8630\x02', 'potato', '-', 'System:', '\x02Praea', 'Euq', 'PI-B', 'c11\x02', '(377.53', 'LY', 'from', 'Sol)', '-', 'Platform:', '\x02PC\x02', '-', 'O2:', 'OK', '-', 'Language:', 'English', '(en-US)', '(Case', '#4)']
ps_risg_message = [':MechaSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#fuelrats', ':RATSIGNAL', '-', 'CMDR', '\x02Rawbird\x02', '-', 'System:',
                  '\x02OOCHOST', 'FD-N', 'A75-0\x02', '(not', 'in', 'EDDB)', '-', 'Platform:',
                  '\x02\x0312PS4\x03\x02', '-', 'O2:', 'OK', '-', 'Language:', 'German', '(de-DE)', '(Case', '#2)']

hc.prnt("\0033=============\n\0033custom module dispatch.py loading!\n\0033* Author:theunkn0wn1\n\0034---------")
# Decorators


def eat_all(wrapped_function):
    """:returns hc.EAT_ALL at end of wrapped function"""
    @wraps(wrapped_function)  # prevents decorator from swallowing docstrings
    def wrapper(*args):
        wrapped_function(args[0], args[1], args[2])
        return hc.EAT_ALL
    return wrapper


def required_args(num, is_strict=False):
    def decorator(my_function):
        def fun_wrapper(*func_args):
            log("[DEBUG]", func_args[0])
            log("[DEBUG]", len(func_args[1]))
            if len(func_args[1]) == num+1:
                my_function
            elif len(func_args[1]) >= num+1 and not is_strict:
                my_function(func_args)
            else:
                print("argument mismatch. Got {} expected {}".format(len(func_args[1]), num))
                return -1
        return fun_wrapper
    return decorator


def log(trace, msg, verbose=False):
    global verbose_logging
    if verbose_logging:
        print("[{Stack}:{trace}]\t {message}".format(Stack=__module_name__, message=msg, trace=trace))
    elif verbose:
        print("[{Stack}:{trace}]\t {message}".format(Stack=__module_name__, message=msg, trace=trace))


class Translations:
    """container for translations"""

    class English:
        """Container for English facts"""
        fr = {
            'pre': "Please add the following rats to your friends list: {rats}",
            'fact': "!{platform}fr {client}"
        }
        wr = {
            'pre': "Now, please invite your rats to the wing.",
            'fact': "!{platform}wing {client}"
        }
        wb = {
            'pre': "lastly, please blind us with your beacon!",
            'fact': "!{platform}beacon {client}"
        }
        clear = {
            'pass': "{client} please stick around with your rats for some useful tips!",
            'fail':
                {
                    '+': "{client} Im sorry we could not get you in time. please stick with your rats to learn some"
                                 "useful tips as to avoid happening again",
                    '-': "{client}, Im sorry we could not get you in time, if you could please join us in"
                                 "#debrief our rats can give you some great advise as to avoid this happening again."
                                 "\n you can do so by typing '/join #debrief ' "
                }

        }


class Utilities:
    @staticmethod
    def strip_fancy(word):
        """
        Strips non alphanumeric values from a string
        :param word: word to strip
        :returns ret: sanitized string
        """
        ret = ""
        for char in word:
            if char.isalpha() or char.isnumeric():
                ret += char
        return ret


def on_message_received(*args):
    phrase = args[0]
    channel = phrase[2]
    sender = phrase[0]
    try:
        if sender == ':DrillSqueak[BOT]!sopel@bot.fuelrats.com':
            log("on_message_received", "sender is correct, attempting parse...")
            Tracker.inject([None, None, None], True, phrase)
        else:
            pass
            # log("on_message_received", 'not the expected user')
    except Exception as e:
        log("on_message_received", 'some error occurred! Error is as follows:]\n{}'.format(e))
    return hc.EAT_PLUGIN


class Parser:
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
            # platform = inject_args['system']
            case = -1
            log("step1", 'completed!')
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
                else:
                    # log("failed:", "word not read: {}".format(phrase))
                    pass
                i += 1
            log("parse_inject", "append({},{},{},{},{})".format(case, client, platform, False, 'En-us'))
            temp_dict = {'case': case, 'platform': platform, 'cr': False, 'lang': 'English-us',
                         'client': client, 'system': 'Sol', 'stage': 0}
            return temp_dict

    @staticmethod
    def parse_ratsignal(phrase):
        """parses ratsignal events"""
        i = 0
        client = platform = lang = cr = cid = system = None  # init before use.. prevent potential errors

        for word in phrase:
            cleaned_word = hc.strip(word)
            if cleaned_word == "CMDR":
                z = i + 2
                client = Utilities.strip_fancy(phrase[i + 1])
                while phrase[z] != "-":
                    client += "_"  # as IRC turns spaces into underscores
                    client += Utilities.strip_fancy(phrase[z])
                    z += 1

            elif cleaned_word == 'Platform:':
                platform = Utilities.strip_fancy(phrase[i + 1])

            elif cleaned_word == "Language:":
                lang = Utilities.strip_fancy(phrase[i + 2])  # fetch the lang code

            elif cleaned_word == "O2:":
                cr = phrase[i + 1]

            elif cleaned_word == "(Case":
                cid = phrase[i + 1].strip("#").strip(")")

            elif cleaned_word == "System:":
                z = i + 1
                system = ""
                while phrase[z] != "-":
                    system += " "
                    system += Utilities.strip_fancy(phrase[z])
                    z += 1
            i += 1
        return {'client': client, 'platform': platform, 'cr': cr, "case": cid, "lang": lang,
                        'system': system, 'stage': 0}


class Tracker:
    """Handles case storage and handling"""
    def __init__(self):
        global database
        log("Tracker", "Initializing database...")
        database = {}

    @staticmethod
    @eat_all
    def readout(*args):
        headers = ["#", "Client", "Platform", "cr", "system", "Assigned rats"]
        data = []
        # print("readout\t",database)
        # log("readout", "- Index - | - client- | - platform - |- - - - - System - - - - -| - - - - Rats - - - -")
        for key in database:
            case = database.get(key)
            client = case['client']
            system = case['system']
            platform = case['platform']
            code_red = case['cr']
            rats = case['rats']
            data.append([key, client, platform, code_red, system, rats])
        log("readout",tabulate(data, headers, "grid", missingval="<ERROR>"), True)
        # print("readout", database)

    @staticmethod
    def inject(list_arguments, from_capture=False, capture_data=None):
        """Generates a new case via  !inject and via ratsignal text events"""
        if list_arguments is None or len(list_arguments) < 3:
            return -1  # not enough arguments
        else:
            try:
                prefix = list_arguments[3]
                if prefix.lower() == ":RATSIGNAL".lower():
                    log("inject", "ratsignal is present")
            except Exception as e:
                pass
            # inject_args = {'client': list_arguments[1], 'system': list_arguments[3], 'platform': list_arguments[2]}
            # order: client, platform, system
            # hc.command("say !inject {} {} {}".format(inject_args['client'], inject_args['platform'],
            #                                          inject_args['system']))
            pass

        if from_capture:
            if capture_data is None or capture_data == "":
                log("Tracker", "[FAIL]\t capture_data was None or was blank")
            else:
                log('is_capture_check', 'PASSED')
                try:
                    log("from_capture", "capture_data={}".format(capture_data))
                    if capture_data[3] == ":RATSIGNAL":
                        log("from_capture", "parse_ratsignal returned:")
                        Tracker.append(Parser.parse_ratsignal(capture_data))
                    else:
                        Tracker.append(Parser.parse_inject(capture_data))
                except Exception as e:
                    # log("[FATAL]", "an error occured as follows:\n {error}".format(error=e))
                    raise e
        else:
            log("Tracker", "not capture data")

    @staticmethod
    def append(args):
        """Appends a new entry to the db
        expected: None,id,client,system,platform,cr,language
        """

        log('debug', "args =\t{}".format(args))
        case_id = int(args['case'])  # mecha's case id
        client = args['client']  # clients IRC name
        system = args['system']  # in-game location of client
        platform = args['platform']  # client platform
        is_cr = bool(args['cr'])  # CR status of client
        language = args['lang']  # client language
        stage = args['stage']
        new_entry = {case_id: {'client': client, 'system': system, 'platform': platform,
                          'cr': is_cr, 'language': language, 'stage': stage, 'wing': False,
                               'has_forwarded': False, 'rats': {
                                0: None, 1: None, 2: None
                                }}}
        database.update(new_entry)
        log("append", "new entry created...")
        return 1

    @staticmethod
    def rm(word, word_eol, user_data):
        cid = int(word[1])
        log("rm", "removing case with CID {}...".format(cid))
        try:
            if database.pop(cid, None) is None:
                log("rm", "Failed to remove {cid}, no such case {cid}.".format(cid=cid))
            else:
                log("rm", "successfully removed case {}".format(cid))
        except Exception:
            log("rm", "unable to remove case {}. An unknown error occurred.")


class Commands:
    """contains the Commands invoked via slash hooked during init"""
    def __init__(self):
        translate = Translations()

    @staticmethod
    @eat_all
    def run_tests(word, word_eol, userdata):
        """Runs tests and generates some dummy cases"""
        log("run_tests", "Running Tracker.inject Test 1...")
        Tracker.inject([None], True, None)
        # log("run_tests", "running test 2")
        # print(Tracker.inject([None, 'clientName', 'systemName', 'PC'], True, debug_constant_a))
        log('run_tests', 'running test 3')
        Tracker.inject([None, None, None], True, debug_constant_B)

        log('run_tests', "Running pc rsig...")
        Tracker.inject([None, None, None], True, rsig_message)
        log("run_tests", "done!")

    @staticmethod
    @eat_all
    def oxy_check(a, b, c):
        name = "oxy_check"
        log(name, "checking o2 for client:\t{cmdr}".format(cmdr=a[1]))
        hc.command("say greetings " + a[1] + ",are you on emergency o2?(blue timer top right)")

    @staticmethod
    @eat_all
    def oxy_ack(a, b, c):
        name = "oxyAck"
        log(name, "ackowledging OK o2")
        commander = a[1]
        hc.command("say {}, Understood, please let me know at once if it makes itself known ;)".format(commander))

    @staticmethod
    @eat_all
    def print_test(a, b, c):
        print("a=\t{}".format(a))
        print("b=\t{}".format(b))
        hc.command("msg TNTom[PC] " + a[1])

    @staticmethod
    @eat_all
    def inject_case(x, y, z):
        name = "injectCase"
        log(name, "Injecting case")
        subject = x[1]
        sys = x[2]
        platform = x[3]
        hc.command("say !inject {} {} {}".format(subject, sys, platform))

    @staticmethod
    @eat_all
    def go(x, y, z):
        name = "go"
        case = x[1]
        rat = x[2]
        client = x[3]
        log(name, "Giving {} the go signal for case {}".format(rat, case))
        hc.command("say {} please add the following rat to your friends list".format(client))
        hc.command("say !go {cid} {rat}".format(cid=case, rat=rat))
        # time.sleep()
        hc.command("say !pcfr {}".format(client))

    @staticmethod
    @eat_all
    def clear(a, b, c):
        """ Reminds client to remain with their rats for the DB, then clears the case with Mecha
        expected order of a: id,rat,client
        """
        name = "clear"
        entry = database.get(a[1])
        commander = entry['client']

        case = a[1]
        rat = a[2]
        log(name, "Commander= \"{x}\",Case \"{y}\",rat \"{z}\"".format(x=commander, y=case, z=rat))
        hc.command("say {cmdr} ,please stick with your rat(s) for a moment to learn some useful tips! ;)".format(
            cmdr=commander))
        hc.command("say !clear {case} {rat}".format(case=case, rat=rat).format(case=case, rat=rat))

    @staticmethod
    @eat_all
    def clear_drill(a, b, c):
        name = "clear"
        commander = a[2]
        case = a[1]
        log(name, "Commander= \"{x}\",Case \"{y}\"".format(x=commander, y=case))
        hc.command("say {cmdr} ,please stick with your rat(s) for a moment to learn some useful tips! ;)".format(
            cmdr=commander))
        hc.command("say !clear {case}".format(case=case))

    # ['\x0324Helitony[XB]', 'Comms+ for EldestDrifter']
    # target element is the [1] element, will have to parse the hard way. Need that string first
    @staticmethod
    @eat_all
    def print_hook(x, y, z):
        log("print_hook", hc.strip(x[1]))

    @staticmethod
    @eat_all
    def server_hook(x, y, z):
        log("server_hook", x)

    @staticmethod
    @eat_all
    def generic_msg(x, y, z):
        log("generic_msg", x)

    @staticmethod
    @eat_all
    def stage(x, y, z):
        event_args = [None]*3
        if len(x) < 1:
            log('stage', 'expected format /stage {index} {mode} {param}')
        else:
            mode = x[2]
            cid = int(x[1])
            try:  # if we have extra args
                event_args[0] = x[3]
                event_args[1] = x[4]
                event_args[2] = x[5]
                log("\0034stage\003", "event_args={}".format(event_args))
            except IndexError:  # but less than 3
                try:
                    event_args[0] = x[3]
                    event_args[1] = x[4]
                except IndexError:  # only one extra argument
                    event_args[0] = x[3]
            if StageManager.do_stage(cid, mode, event_args[0], event_args[1], event_args[2]):
                pass
            else:
                log("stage", 'unknown mode {}'.format(mode))
        # log("stage", 'current stage is {stage}'.format())


class StageManager:
    """Tracks client stage and responds accordingly"""
    @staticmethod
    def say(message, colour=None):
        """Output a message into the channel (*this is server-side!*)"""
        if colour is None:
            hc.command("say {msg}".format(msg=message))
        else:
            hc.command("say \003{color} {msg}".format(color=colour, msg=message))

    @staticmethod
    def change_platform(key, platform, case_object):
        """Changes a client's platform
        :param key: database key for client
        :param platform: new platform
        :param case_object: clients case object
        """
        global database
        if platform == 'ps' or platform == 'pc' or platform == 'xb':
            formed_dict = case_object
            formed_dict['platform'] = platform
            database.update({key:formed_dict})
            log('change_platform', "Successfully updated platform for case {}".format(key),True)

    @staticmethod
    def friend_request(case_object):
        """Tells client to add rat(s) to friends list"""
        platform = case_object['platform']
        client = case_object['client']
        if case_object['language'].lower() == 'enus':
            # StageManager.say(Translations.English.fr['pre'].format(rats=case_object['rats']))  # TODO make work
            log("friend_request", "triggered!", True)
            StageManager.go(case_object, None)
            StageManager.say(Translations.English.fr['fact'].format(client=client, platform=platform))
        log("friend_request", "Client {client} is on platform {platform} with lang {lang}"
            .format(client=client, platform=platform, lang=case_object['language']), True)
        # TODO: implement other languages, add option to outsource facts to Mecha

    @staticmethod
    def wing_invite(case_object):
        if case_object['language'] == 'English-us':
            StageManager.say(Translations.English.wr['pre'], '03')
            StageManager.say(Translations.English.wr['fact'].format(client=case_object['client'], platform=
                                                                    case_object['platform']), '03')
            # TODO: implement other languages,
            # TODO: implement Mecha facts

    @staticmethod
    def wing_beacon(case_object):
        if case_object['language'] == 'English-us':
            StageManager.say(Translations.English.wb['pre'], '03')
            StageManager.say(Translations.English.wb['fact'].format(client=case_object['client'], platform=
                                                                    case_object['platform']), '03')
        # TODO implement other languages and implement Mecha interaction

    @staticmethod
    def fail(case_object):
        if case_object['wing']:
            StageManager.say(Translations.English.clear['fail']['+'].format(client=case_object['client']))
        else:
            StageManager.say(Translations.English.clear['fail']['-'].format(client=case_object['client']))

    @staticmethod
    def wing_conf(case_object, key):
        formed_dict = case_object
        formed_dict.update({'wing': True})
        database.update({key: formed_dict})

    @staticmethod
    def check_o2(case_object):
        StageManager.say("Greetings {client}, are you on emergency oxygen? (blue countdown timer top right)?".format(
            client=case_object['client']))

    @staticmethod
    def add_rats(case_object, rats):
        """Adds up to 3 rats to a given case
        :param case_object: case to update
        :param rats: list of rats to add
        """
        # formed_dict = case_object
        try:
            rat_object = case_object.get('rats')
            log("\0034add_rats\003", "rats = {}".format(rats))
            rat_object.update({0: rats[0]})
            rat_object.update({1: rats[1]})
            rat_object.update({2: rats[2]})
            print(rat_object)
            log("add_rats", "rats added", True)
        except Exception as e:
            log('add_rats', "an error occurred!", True)
            print(e)

    @staticmethod
    def go(case_object, event_args):
        if event_args is not None:
            StageManager.add_rats(case_object, event_args)
        rats = case_object.get('rats')
        quantity_none = 0
        for rat in rats:
            if rat is None:
                quantity_none += 1
        if quantity_none == 0:
            StageManager.say("Please add {alpha},{beta},{gamma} to your friends list.".format(alpha=rats[0], beta=rats[1], gamma=rats[2]))
        elif quantity_none == 1:
            StageManager.say(
                "Please add {alpha},{beta} to your friends list.".format(alpha=rats[0], beta=rats[1]))
        elif quantity_none == 2:
            StageManager.say(
                "Please add {alpha} to your friends list.".format(alpha=rats[0]))
            StageManager.say(
                "!{platform}fr".format(platform=case_object['platform'])
            )

    @staticmethod
    @eat_all
    def do_stage(key, mode, alpha=None, beta=None, gamma=None):
        """Advances the case's stage and does the next step
        :param beta: optional extra argument, for supported functions
        :param gamma: optional extra argument, for supported functions
        :param alpha: optional extra argument, for supported functions
        :param key: Database key to use
        :param mode: dictate which method to execute
        :returns boolean success
        """
        global database
        steps = {0: StageManager.check_o2,
                 1: StageManager.friend_request,
                 2: StageManager.wing_invite,
                 3: StageManager.wing_beacon,
                 }
        case_object = database.get(key)
        if mode == 'get' or mode == 'status':
            log('stage; [get]', 'attempting to retrieve case_object with key {} of type {}'.format(key, type(key)))
            if case_object is not False:
                log('stage', 'status of {CID} is:\nStage: {status}'.format(CID=key, status=case_object['stage']), True)
                log('stage', "Platform:{platform}\tRats: {rats}".format(platform=case_object['platform'],
                                                                        rats=case_object['rats']), True)
                return True

            else:
                log('stage', 'case_object not found.',True)
                return False

        elif mode == 'up':
            steps[case_object['stage']](case_object)
            case_object['stage'] += 1
            case_object['has_forwarded'] = True
            log('stage:up', 'stage set to {}'.format(case_object['stage']), True)
            return True

        elif mode == 'back':
            """Steps a case back a step and issues the previous command"""
            if case_object['has_forwarded']:
                case_object['stage'] -= 2
                case_object['has_forwarded'] = False
                # log('Stage:back', "Backing up..", True)
            else:
                case_object['stage'] -= 1
            steps[case_object['stage']](case_object)
            return True

        elif mode == 'repeat':
            """Repeats current stage command"""
            steps[case_object['stage']](case_object)
            return True

        elif mode == "fr":
            """Instructs client to add rats to friends list"""
            steps[0](case_object)
            return True

        elif mode == "wing+":
            StageManager.wing_conf(case_object, key)
            log("do_stage:wing+", 'writing wing status for key {}'.format(key), True)
            return True

        elif mode == 'fail':
            StageManager.fail(case_object)
            return True
        elif mode == 'platform':
            log('do_stage:platform', "writing platform {} for key {}".format(alpha, key))
            StageManager.change_platform(key, alpha, case_object)
            return True
        elif mode == 'add':
            log("do_stage:add", "adding rats {},{},{} to {}".format(alpha, beta, gamma, key))
            StageManager.add_rats(case_object, [alpha, beta, gamma])
            return True


def init():
    cmd = Commands()
    board = Tracker()
    log("Init", "Adding hooks!")
    commands = {
        # 'potato': cmd.temp,
        'test': cmd.run_tests,
        'o2': cmd.oxy_check,
        "test2": cmd.print_test,
        "clear": cmd.clear,
        "o2k": cmd.oxy_ack,
        "go": cmd.go,
        "inject": cmd.inject_case,
        "dClear": cmd.clear_drill,
        "stage": cmd.stage,
        # "new": board.append,  # yeah no, this needs to be put into a wrapper (expects dict, gets string array)
        "del": board.rm,
        'rm': board.rm,
        "readout": board.readout

    }
    try:
        for key in commands:
            log("init", "adding hook for\t{}".format(key))
            hc.hook_command(key, commands[key])
        hc.hook_server("PRIVMSG", on_message_received)

    except Exception as e:
        log("Init", "\0034Failure adding hooks! error reads as follows:", True)
        log("Init", e, True)
    else:
        log("Init", "\0033 Everything is prepared. Ready.", True)


# ['\x0329RatMama[BOT]', 'Incoming Client: Azrael Wolfmace - System: LP 673-13 - Platform: XB - O2: OK - Language: English (English-US) - IRC Nickname: Azrael_Wolfmace', '&']
if __name__ == '__main__':  # this prevents script code from being executed on import. (bad!)
    init()
