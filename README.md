Greetings Commander. Dispatch.py is a module that aims to ease the burden on Fuel Rat dispatchers by offering a dispatch board and the means of keeping it up to date.
# Build Status
## Master
[![Build Status](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist.svg?branch=master)](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist)
## Dev
[![Build Status](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist.svg?branch=dev)](https://travis-ci.org/theunkn0wn1/Fuelrats-DispatchAssist)
# Requirements:
* Hexchat - {link} - currently this project only supports Hexchat. 
* Python 3.5.2 - {link}
* Pip3 - part of the standard python3 install, required for installing dependencies
# quick setup guide
1. Install python version 3.5.2 to a location of your choice, i suggest the default
 - You need to check the box that allows Python to install itself to the PATH
2. Install Hexchat to a location of your choice, be sure under _advanced setup_ to check `python interface` version `3.5`
3. open hexchat and verify the python module was loaded correctly. type `/py about`
    - if that returns `py: command not found` something went wrong, and that needs to be fixed before you can continue
4. Get yourself a copy of this repository, i suggest using Git.
    1. From within your preferred CLI browse to the directory you would like to install my script to
    2. type `git clone https://github.com/theunkn0wn1/Fuelrats-DispatchAssist.git` and note down the path to the created folder.
    3. Open hexchat and, in the message box, type `/py load "/path/to/dispatch.py"`, replacing `/path/to` with the full system path to where `dispatch.py` is located
    4. **_(OPTIONAL)_** If you live on the edge you or want access to the latest features you can checkout my dev branch
        - Features on the dev branch are in development and are subject to change/deletion, use it at your own risk
        - Should that little warning not scare you away, go back to your CLI and type `git checkout dev` and reload the script in Hexchat.

5. Should you prefer to update the script manually by downloading files yourself every time, you can just download the ZIP archive instead.
    1. On my Github page click the green `Clone or download`
    2. on the resulting dropdown click 'download ZIP' and save it somewhere
    3. Extract the archive to your desired installation directory and note that directory down.
    4. Open up your terminal and browse to the installation directory for the script
    5. run command 'pip install requirements.txt'
    4. Open up hexchat and, in the messagebox, type '/py load /path/to/dispatch.py', replacing `/path/to` with the full system path to where `dispatch.py` is located

Plans are in place to support other IRC clients that have a python3 interface at later point in time
# Usage:
Once loaded into hexchat, it will automatically detect Ratsignals as they arrive in #Fuelrats
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
you can add as many rats you need to a case, why do you need more than three i have no idea...
Use the command `/assign case_number rat1 rat2... ratn` at minimum you must give one rat.

### 4. Removing rats
Mistakes are made, sometimes you give the wrong rat the go. you can use `/unassign case_number rat1.. ratn` to remove them from tracking
### 5. Changing system
Should the client give you an inaccurate system name you can update it using the command `/sys case_number really_long_syste_name_that_can_contain_spaces`
Anything after the case number will be treated as part of the System.

### 6. Updating platform
Should you need to update the client's platform, you can do so using `/platform platform`. vakid options are pc,xb, or ps; anything else will result in a warning.

### 7. Updating clients IRC name
Clients sometimes make mistakes and enter ' client' into the commander name field on Kiwi, so a means of correcting that is needed.
You can update their IRC name via the command `/client case_number new_irc_name`. It cannot contain spaces.
### 8. Toggling CR status
Some clients turn code-red mid rescue, please follow all standard proceedures first then you can, should this script fail to detect the change, use the command `/cr case_number` to update the board
The same command can be used say, for instance, a client connects CR but then reports OK o2. the command is a toggle.
