Greetings Commander. Dispatch.py is a module that aims to ease the burden on Fuel Rat dispatchers by offering a dispatch board and the means of keeping it up to date.

# Requirements:
    Hexchat - currently this project only supports Hexchat. Plans are in place to support other IRC clients that have a python3 interface at later point in time
    Python 3.5.2
    Tabulate - This is for graphical representation of the collected data
    
# Usage:
       Once loaded into hexchat, it will automaticially detect Ratsignals as they arrive in #Fuelrats
       You can view the collected data with the command `/board`
   ## Case management:
    If a entry was created with an incorrect index, you can move it via `/mv` followed by the current index and the new index as follows:
    `/mv -1 2` this will move the case at index -1 to case #2. 
        **BEWARE: this will overwrite the destination case!**
    If a case should have beem cleared but was not, you can delete the case using the 'rm' command or its alias '/del'
    Usage: `del 2` . this will delete case #2 from the board and stop tracking it.
    
