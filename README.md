# bme590final
Head Impact Exposure (HIE) Sensor Multi-Unit Downloading, Logging and Storage Management Tool

##GENERAL INFO:
This code is able to automatically download binary files from selected USB drives. 
* This code is able to run on a Mac OS High Sierra (Version 10.13.6). Windows functionality has not yet been achieved.
    * To get it working on Windows, the subprocess portion of the code (in the get_usb function of import_data.py) must be altered.
* This code also depends on the USB devices following a naming scheme in order to obtain the PIN numbers of the devices.
    * Devices must be named MV1-####. This ensures the code will pull and sort the data by the correct PIN number.
* This code puts the data into a database and does not put it into separate folders.
    
##TO RUN:
