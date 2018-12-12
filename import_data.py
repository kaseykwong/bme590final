import os
import base64
import datetime
import pandas as pd
import subprocess
import re


def find_usb():
    """
    Function looks for paths of devices with the MV1 tag

    Returns:
        luck_usb: list of device file paths with the MV1 tag
    """
    process = subprocess.Popen(['df -h | awk \'{print $(NF-1),$NF}\''],
                               stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.splitlines()[1:]
    results = []
    for i in out:
        tmp = i.split()
        results[tmp[1]] = tmp[0]
    dev = []
    for key, value in results.items():
        dev.append(key.decode('ASCII'))
    luck_usb = [s for s in dev if "MV" in s]
    return luck_usb


def find_folders(paths):
    """
    Function finds all .BIN folders in given path

    Args:
        paths: list of file paths
    Returns:
        result: boolean to determine if files were found.
                True is files were found. False if not.
        file_names: list of full binary file paths.
    """
    count = 0
    file_names = []
    for usb in paths:
        for (dir_name, dirs, files) in os.walk(usb):
            for filename in files:
                if filename.endswith('.BIN'):
                    if filename.startswith("L"):
                        count = count + 1
                        file_names.append(os.path.join(dir_name, filename))

    if count == 0:
        result = False
        print("No files found")
    if count > 0:
        print('Files:', count)
        result = True
    return result, file_names


def get_pins(file_names):
    """
    Get pins from USB device name (must be format MV1-****)

    Args:
        file_names: list of binary file paths
    Returns:
        pin_keep: list of pin numbers or devices
    """
    pin = []
    pin_keep = []
    for item in file_names:
        pin.append(re.sub(r'.*-', '', item))
    for items in pin:
        pin_keep.append(items.split('/', 1)[0])
    return pin_keep


def get_creation_date(files):
    """
    Determines file creation parameters for each file.

    Args:
        files: list of binary file paths
    Returns:
        time: time file was created
        date: date file was created
        year: year file was created
    """
    time = []
    date = []
    year = []
    for dir_path in files:
        t = datetime.datetime.fromtimestamp(os.stat(dir_path).st_ctime)
        time.append(t.strftime('%H:%M:%S'))
        date.append(t.strftime('%m-%d-%Y'))
        year.append(t.year)
    return time, date, year


def open_bin_files(paths):
    """
    Opens and encodes binary files

    Args:
        paths: list of binary file paths
    Returns:
        boolean: boolean to determine if files were found.
                True is files were encoded. False if not.
        spy: list of encoded binary files
    """
    i = 0
    spy = []
    for name in paths:
        with open(name, mode="rb") as file:
            file_content = file.read()
            i = i + 1
            spy.append(base64.b64encode(file_content))
    if i == 0:
        boolean = False
        print("Files were not properly encoded.")
    if i > 0:
        boolean = True
        print('Encoded:', i)
    return boolean, spy


def sort(pin_name, date, time, season, spy):
    """
    Creates data frame of results. Sorts by date and pin.

    Args:
        pin_name: list of USB pins
        time: list  of times files were created
        date: list of dates that files were created
        season: list of years that files were created
        spy: list of encoded binary files

    Returns:
        overall: date frame containing necessary file info
        interval_date: data sorted by file creation date
        interval_pin: data sorted by USB pin
    """
    overall = pd.DataFrame({
        "Pin": pin_name,
        "Date": date,
        "Time": time,
        "Year": season,
        "Encoded .BIN file": spy
        })
    interval_date = list(overall.groupby('Date'))
    interval_pin = list(overall.groupby('Pin'))
    return overall, interval_date, interval_pin


if __name__ == "__main__":
    path = ["rep_data"]
    # path = find_usb()
    [success, bin_files] = find_folders(path)
    pins = get_pins(bin_files)
    [times, dates, seasons] = get_creation_date(bin_files)
    [fail, binary] = open_bin_files(bin_files)
    [total, sort_date, sort_pin] = sort(pins, dates, times, seasons, binary)
