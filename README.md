Greetings Commander. Dispatch.py is a module that aims to ease the burden on Fuel Rat dispatchers by offering a dispatch board and the means of keeping it up to date.

# Requirements:
* Hexchat - {link} - currently this project only supports Hexchat. 
* Python 3.5.2 - {link}
* Tabulate - {link} This is for graphical representation of the collected data

Plans are in place to support other IRC clients that have a python3 interface at later point in time
# Usage:
Once loaded into hexchat, it will automaticially detect Ratsignals as they arrive in #Fuelrats
You can view the collected data with the command `/board`
## Case management:
### 1. Move case ID
If a entry was created with an incorrect index, you can move it via `/mv` followed by the current index and the new index as follows:
`/mv {current_index} {new_index}`

Example:
`/mv -1 2`  

This will move the case at index -1 to case #2. 
**BEWARE: this will overwrite the destination case!**

### 2. Delete case
If a case should have beem cleared but was not, you can delete the case using the `/rm {case_ID}` command or its alias `/del {case_ID}`

Example:
`/del 2` 

This will delete case #2 from the board and stop tracking it.

# Todo
1. Add links in Requirements section
2. Organize Usage section
2a. Add some more cases
3. Add "First time launch" section
4. Desribe source of data. Are you pluged in some API? MechaSqueak?
