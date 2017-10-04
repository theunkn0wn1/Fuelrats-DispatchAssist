Greetings Commander. Dispatch.py is a module that aims to ease the burden on Fuel Rat dispatchers by offering a dispatch board and the means of keeping it up to date.
# Build Status
## Master
[![Build Status](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist.svg?branch=master)](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist)
## Dev
[![Build Status](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist.svg?branch=dev)](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist)
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
### 3. Adding rats
you can add a up to 5 rats to a case, why do you need that many?
Use the command `/assign case_number rat1 rat2... rat5` at minimum you must give one rat, at maximum 5.

### 4. Changing system
Should the client give you an inaccurate system name you can update it using the command `/sys case_number really_long_syste_name_that_can_contain_spaces`
Anything after the case number will be treated as part of the System.

### 5. Updating platform
Should you need to update the client's platform, you can do so using `/platform platform`. vakid options are pc,xb, or ps; anything else will result in a warning.

### 6. Updating clients IRC name
Clients sometimes make mistakes and enter ' client' into the commander name field on Kiwi, so a means of correcting that is needed.
You can update their IRC name via the command `/client case_number new_irc_name`. It cannot contain spaces.
