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


def required_args(num,is_strict = False):
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


class Tracker:
    """Handles case storage and handling"""
    def __init__(self):
        global database
        log("Tracker", "Initializing database...")
        database = {}

    @staticmethod
    @required_args(0)
    def readout(*args):
        print("readout", database)

    @staticmethod
    def inject(list_arguments, is_capture=False, capture_data=None):
        """Generates a new case via  !inject"""

        def on_message_captured(capture):
            """Parses target message events"""
            log("on_message_captured", "parsing capture event with data: {}".format(capture))
            # [':DrillSqueak[BOT]!sopel@bot.fuelrats.com', 'PRIVMSG', '#DrillRats3', ":ClientName's", 'case', 'opened',
            #  'with:', '"sol', 'pc"', '(Case', '3,', 'PC)']
            if capture[0] != ':DrillSqueak[BOT]!sopel@bot.fuelrats.com':
                log("on_message_captured"," invalid capture event")
            else:
                i = 0
                for phrase in capture:
                    if phrase == 'PC' or phrase == 'PS4' or phrase == 'XB':
                        system = phrase
                    elif phrase[:5] == 'case':
                        capStr = capture[i-1]  # phrase before is the client name
                        capStr = capStr[:len(capStr)-2]  # strip the 's from the end
                        capStr = capStr.strip(':')  # and the : from the start
                        client = capStr  # And we have our product!
                    i+=1

            Tracker.append([0,'name',system])
            # todo: Parse the capture data and add to db
        words = ['client', 'system', 'platform']
        if is_capture:  # if this is called from the msg handler
            log("inject:capture", "spawning internal case with capture_data = {}".format(capture_data))
            on_message_captured(capture_data)
        elif len(list_arguments) > len(words):
            log("inject", "Argument count exceeded limit({}). please try again with less arguments.".format(len(words)))
        else:
            for word in words:
                pass  # TODO build a case via arguments

    @staticmethod
    @required_args(6)
    def append(args):
        args = args[0]
        log('debug',"args =\t{}".format(args))
        case_id = int(args[1])  # mecha's case id
        client_name = args[2]  # clients IRC name
        system = args[3]  # in-game location of client
        platform = args[4]  # client platform
        is_cr = bool(args[5])  # CR status of client
        language = args[6]  # client language
        new_entry = {case_id: {'client_name': client_name, 'system': system, 'platform': platform,
                          'cr': is_cr, 'language': language}}
        database.update(new_entry)
        log("append", "new entry created...")
        return 1

    @staticmethod
    @required_args(1)
    def rm(args):
        cid = int(args[0][1])
        log("rm", "removing case with CID {}...".format(cid))
        try:
            if database.pop(cid, None) is None:
                log("rm", "Failed to remove {}, no such case {}.".format(cid))
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
        Tracker.inject(None, True, None)  # todo replace final none with debug string
)

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
    try:
        hc.hook_command("potato", cmd.inject_case)
        hc.hook_command("test", cmd.run_tests)
        hc.hook_command("o2", cmd.oxy_check)
        hc.hook_command("test2", cmd.print_test)
        hc.hook_command("clear", cmd.clear)
        hc.hook_command("o2k", cmd.oxy_ack)
        hc.hook_command("go", cmd.go)
        hc.hook_command("inject", cmd.inject_case)
        hc.hook_command("dClear", cmd.clear_drill)
        hc.hook_command("stage", cmd.stage)
        hc.hook_command("new", board.append)
        hc.hook_command("rm", board.rm)
        hc.hook_command("readout", board.readout)
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
