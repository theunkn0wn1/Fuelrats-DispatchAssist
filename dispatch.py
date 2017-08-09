__module_name__ = "dispatch"
__module_version__ = "0.0.1"
__module_description__ = "Assist with automating trivial FuelRat dispatch interactions"
import hexchat as hc
import time
hc.prnt("=============\ncustom module hc.py loaded!\n* Author:theunkn0wn1\n===========")
#hc.command("say test")
def log(trace,msg):
	print("[{Stack}:{trace}]\t {message}".format(Stack = __module_name__,message = msg,trace=trace))


class commands(object):
	"""contains the commands invoked via slash hooked during init"""
	def commandCallBack(self,word,word_eol,userdata):
		name = "commandCallBack"
		hc.prnt("Called back!")
		print(word) #list of words, including the invoked command
		print(word_eol) #array of size 1, the whole command invoked
		print(userdata) #not sure what this does yet :/
		return(hc.EAT_ALL) # allow hc to process the command as normal

	def oxyCheck(self,a,b,c):
		name = "oxyCheck"
		log(name,"checking o2 for client:\t{cmdr}".format(cmdr=a[1]))
		hc.command("say greetings "+a[1]+",are you on emergency o2?(blue timer top right)")
		return(hc.EAT_ALL)
	
	def oxyAck(self,a,b,c):
		name = "oxyAck"
		log(name,"ackowledging OK o2")
		commander = a[1]
		hc.command("say {}, Understood, please let me know at once if it makes itself known ;)".format(commander))
		return(hc.EAT_ALL)
	
	def printTest(self,a,b,c):
		name = "printTest"
		print("a=\t{}".format(a))
		print("b=\t{}".format(b))
		hc.command("msg TNTom[PC] " +a[1])
		return(hc.EAT_ALL)
	def injectCase(self,x,y,z):
		name = "injectCase"
		log(name,"Injecting case")
		subject = x[1]
		sys = x[2]
		platform = x[3]
		hc.command("say !inject {} {} {}".format(subject,sys,platform))
		return(hc.EAT_ALL)
	def go(self,x,y,z):
		name = "go"
		case = x[1]
		rat = x[2]
		client = x[3]
		log(name,"Giving {} the go signal for case {}".format(rat,case))
		hc.command("say {} please add the following rat to your friends list".format(client))
		hc.command("say !go {cid} {rat}".format(cid=case,rat=rat))
		#time.sleep()
		hc.command("say !pcfr {}".format(client))		
		return(hc.EAT_ALL)
	#expected order of a: id,rat,client
	def clear(self,a,b,c):
		name = "clear"
		commander = a[3]
		case = a[1]
		rat = a[2]
		log(name,"Commander= \"{x}\",Case \"{y}\",rat \"{z}\"".format(x=commander,y=case,z=rat))
		hc.command("say {cmdr} ,please stick with your rat(s) for a moment to learn some useful tips! ;)".format(cmdr=commander))
		hc.command("say !clear {case} {rat}".format(case=case,rat=rat).format(case=case,rat=rat))
		return(hc.EAT_ALL)
	def drillClear(self,a,b,c):
		name = "clear"
		commander = a[2]
		case = a[1]
		log(name,"Commander= \"{x}\",Case \"{y}\"".format(x=commander,y=case))
		hc.command("say {cmdr} ,please stick with your rat(s) for a moment to learn some useful tips! ;)".format(cmdr=commander))
		hc.command("say !clear {case}".format(case=case,))
		return(hc.EAT_ALL)
	def prepCR(self,a,b,c):
		log("prepCR",a)
		client = a[1]
#['\x0324Helitony[XB]', 'Comms+ for EldestDrifter']
#target element is the [1] element, will have to parse the hard way. Need that string first
	def printHook(self,x,y,z):
		log("printHook",hc.strip(x[1]))
		return(hc.EAT_NONE)
	def serverHook(self,x,y,z):
		log("serverHook",x)
		return(hc.EAT_NONE)
	def genericMSg(self,x,y,z):
		log("genericMSg",x)
def init():
	cmd = commands()
	log("Init","Adding hooks!")
	try:
		hc.hook_command("test",cmd.commandCallBack)
		hc.hook_command("o2",cmd.oxyCheck)
		hc.hook_command("test2",cmd.printTest)
		hc.hook_command("clear",cmd.clear)
		hc.hook_command("o2k",cmd.oxyAck)
		hc.hook_command("go",cmd.go)
		hc.hook_command("inject",cmd.injectCase)
		hc.hook_command("dClear",cmd.drillClear)
		#hc.hook_print("Channel Message",cmd.printHook)
		#hc.hook_print("Beep",cmd.printHook)
		#hc.hook_print("Generic message",cmd.genericMSg)
		#hc.hook_server("PRIVMSG",cmd.serverHook) #hooks when the user is mentioned
	except Exception as e:
		log("Init","Failure adding hooks! error reads as follows:")
		log("Init",e)
	else:
		log("Init","Done adding hooks!")
#['\x0329RatMama[BOT]', 'Incoming Client: Azrael Wolfmace - System: LP 673-13 - Platform: XB - O2: OK - Language: English (en-US) - IRC Nickname: Azrael_Wolfmace', '&']
#Now that the methods are defined, lets hook them into the slash-commands
#note that the slash command needs not be defined in Hexchat for this to work
init()