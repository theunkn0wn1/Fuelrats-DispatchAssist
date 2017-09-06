import hexchat as hc

# Globals
__module_name__ = "dispatch"
__module_version__ = "0.0.1"
__module_description__ = "Assist with automating trivial FuelRat dispatch interactions"
database = {}
hc.prnt("=============\ncustom module dispatch.py loaded!\n* Author:theunkn0wn1\n===========")

# Debug constants
x = [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":ClientName's", 'case', 'opened', 'with:', '"sol', 'pc"', '(Case', '3,', 'PC)']

# Decorators
def eat_all(wrapped_function):
    """:returns hc.EAT_ALL at end of wrapped function"""
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


def log(trace, msg):
    print("[{Stack}:{trace}]\t {message}".format(Stack=__module_name__, message=msg, trace=trace))


def on_message_received(*args):
    phrase = args[0]
    channel = phrase[2]
    sender = phrase[0]
    try:
        if channel != '#RatChat' and channel != '#ratchat':
            log('on_message_received', 'sender = {sender}\nData= {data}'.format(sender=sender, data=phrase))
        elif sender == ':DrillSqueak[BOT]!sopel@bot.fuelrats.com':
            log("on_message_received", "sender is correct, attempting parse...")
            Tracker.inject([None, None, None], True, phrase)
        else:
            pass
            # log("on_message_received", 'not the expected user')
    except Exception as e:
        log("on_message_received", 'some error occurred! Error is as follows:]\n{}'.format(e))
    return hc.EAT_PLUGIN


class Tracker:
    """Handles case storage and handling"""
    def __init__(self):
        global database
        log("Tracker", "Initializing database...")
        database = {}

    @staticmethod
    def readout(*args):
        print("readout", database)

    @staticmethod
    def inject(list_arguments, is_capture=False, capture_data=None):
        """Generates a new case via  !inject"""
        if list_arguments is None or len(list_arguments) < 3:
            return -1  # not enough arguments
        elif is_capture:
            pass
        else:
            inject_args = {'client': list_arguments[1], 'system': list_arguments[3], 'platform': list_arguments[2]}
            # order: client, platform, system
            hc.command("say !inject {} {} {}".format(inject_args['client'], inject_args['platform'], inject_args['system']))

        def on_message_captured(capture):
            """Parses target message events"""
            log("on_message_captured", "parsing capture event with data: {}".format(capture))
            # [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":ClientName's", 'case', 'opened',
            #  'with:', '"sol', 'pc"', '(Case', '3,', 'PC)']
            if capture is None:
                log("on_message_captured", "Invalid capture event")
            elif capture[0] != ':DrillSqueak[BOT]!sopel@bot.fuelrats.com':
                log("on_message_captured"," invalid capture event")
            else:
                log("on_message_captured", 'Beginning parse attempt ZZZZzzzZz...')
                i = 0
                # client = inject_args['client']
                # platform = inject_args['system']
                case = -1
                log("step1", 'completed!')
                for phrase in capture:
                    if phrase == 'PC)' or phrase == 'PS4)' or phrase == 'XB)':
                        log('step2', 'searching for platform...')
                        platform = phrase
                        log('step2', 'platform is {}'.format(platform))
                    elif phrase[:5] == 'case':
                        log('step3', 'looking for client name...')
                        parsed_string = capture[i-1]  # phrase before is the client name
                        parsed_string = parsed_string[:len(parsed_string)-2]  # strip the 's from the end
                        parsed_string = parsed_string.strip(':')  # and the : from the start
                        client = parsed_string  # And we have our product!
                        log('step3', 'client is {}'.format(client))
                    elif phrase == "(Case":
                        log('step4', 'searching for CaseID...')
                        case = capture_data[i+1].strip(',')
                        log('step4', 'cid is {CID}'.format(CID = case))
                    else:
                        # log("failed:", "word not read: {}".format(phrase))
                        pass
                    i += 1
                log("on_message_captured", "append({},{},{},{},{})".format(case, client, platform, False, 'En-us'))
                temp_dict = {'case': case, 'platform': platform, 'cr': False, 'lang': 'EN-us',
                             'client': client, 'system': 'Sol'}
                Tracker.append(temp_dict)
            log("miss?","miss?")
        if is_capture:
            if capture_data is None or capture_data == "":
                log("Tracker", "[FAIL]\t capture_data was None or was blank")
            else:
                log('is_capture_check', 'PASSED')
                try:
                    on_message_captured(capture_data)
                except Exception as e:
                    log("[FATAL]", "an error occured as follows:\n {error}".format(e))
        else:
            log("Tracker", "not capture data")

    @staticmethod
    def append(args):
        """Appends a new entry to the db
        expected: None,id,client,system,platform,cr,language
        """

        log('debug', "args =\t{}".format(args))
        case_id = int(args['case'])  # mecha's case id
        client_name = args['client']  # clients IRC name
        system = args['system']  # in-game location of client
        platform = args['platform']  # client platform
        is_cr = bool(args['cr'])  # CR status of client
        language = args['lang']  # client language
        new_entry = {case_id: {'client_name': client_name, 'system': system, 'platform': platform,
                          'cr': is_cr, 'language': language}}
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
        pass

    @staticmethod
    @eat_all
    def run_tests(word, word_eol, userdata):
        log("run_tests", "Running Tracker.inject Test 1...")
        Tracker.inject(None, True, None)
        log("run_tests", "running test 2")
        print(Tracker.inject([None, 'clientName', 'systemName', 'PC'], True, x))
        log("run_tests", "done!")

    @staticmethod
    @eat_all
    def oxy_check( a, b, c):
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
        commander = a[3]

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
        log("stage", "x = {}\ty={}".format(x, y))


def init():
    cmd = Commands()
    board = Tracker()
    log("Init", "Adding hooks!")
    commands = {
        # 'potato': cmd.inject_case,
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
        log("init")
    # hc.hook_print("Channel Message",cmd.print_hook)
    # hc.hook_print("Beep",cmd.print_hook)
    # hc.hook_print("Generic message",cmd.generic_msg)
    # hc.hook_server("PRIVMSG",cmd.server_hook)#x = MyClass() #hooks when the user is mentioned
    except Exception as e:
        log("Init", "Failure adding hooks! error reads as follows:")
        log("Init", e)
    else:
        log("Init", "Done adding hooks!")


# ['\x0329RatMama[BOT]', 'Incoming Client: Azrael Wolfmace - System: LP 673-13 - Platform: XB - O2: OK - Language: English (en-US) - IRC Nickname: Azrael_Wolfmace', '&']
# Now that the methods are defined, lets hook them into the slash-Commands
# note that the slash command needs not be defined in Hexchat for this to work
init()
