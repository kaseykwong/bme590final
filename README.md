# bme590final
Head Impact Exposure (HIE) Sensor Multi-Unit Downloading, Logging and Storage Management Tool

## GENERAL INFO:
This code is able to automatically download binary files from selected USB drives. 
* This code is able to run on a Mac OS High Sierra (Version 10.13.6). Windows functionality has not yet been achieved.
    * To get it working on Windows, the subprocess portion of the code (in the get_usb function of import_data.py) must be altered.
* This code also depends on the USB devices following a naming scheme in order to obtain the PIN numbers of the devices.
    * Devices must be named MV1-####. This ensures the code will pull and sort the data by the correct PIN number.
* This code puts the data into a database and does not put it into separate folders.
* Currently this runs on a contributor's database, it is recommended to created your own mLAB
database and put the address in the connect function at the top of server.py.
    
## TO RUN:
1. Create virtual environment.
2. `pip install -r requirements.txt`
2. In your python environment, run server.py.
3. Once the server is running on your local, run interface.py.
4. Select desired USB drives and press download. The downloaded data will be in your mLAB database.

Side-note: The server creates a data_server.txt file which will log the data downloaded for the user's reference. 

[![Build Status](https://travis-ci.com/kaseykwong/bme590final.svg?branch=master)](https://travis-ci.com/kaseykwong/bme590final)
