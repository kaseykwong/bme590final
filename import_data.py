import os
import base64
import datetime
import pandas as pd
import subprocess
import re


def find_usb():
    process = subprocess.Popen(['df -h | awk \'{print $(NF-1),$NF}\''], stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.splitlines()[1:]
    results = {}
    for i in out:
        tmp = i.split()
        results[tmp[1]] = tmp[0]
    dev = []
    for key, value in results.items():
        dev.append(key.decode('ASCII'))
    luck_usb = [s for s in dev if "MV" in s]
    return luck_usb


def find_folders(paths):
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
        print("No files found")
    print('Files:', count)
    return file_names


def get_pins(file_names):
    pin = []
    pin_keep = []
    for item in file_names:
        pin.append(re.sub(r'.*MV1-', '', item))
    for items in pin:
        pin_keep.append(items.split('/', 1)[0])
    return pin_keep


def get_creation_date(files):
    time = []
    year = []
    for dir_path in files:
        t = datetime.datetime.fromtimestamp(os.stat(dir_path).st_ctime)
        time.append(t.strftime('%m-%d-%Y'))
        year.append(t.year)
    return time, year


def open_bin_files(paths):
    i = 0
    spy = []
    for name in paths:
        with open(name, mode="rb") as file:
            file_content = file.read()
            i = i + 1
            spy.append(base64.b64encode(file_content))
    if i == 0:
        print("Files were not properly encoded.")
    print('Encoded:', i)
    return spy


def sort(filename, date, season, spy):
    overall = pd.DataFrame({
        "Pin": filename,
        "Date": date,
        "Year": season,
        "Encoded .BIN file": spy
        })
    interval_date = list(overall.groupby('Date'))
    interval_pin = list(overall.groupby('Pin'))
    return interval_date, interval_pin


if __name__ == "__main__":
    # path = ["/Users/liameirose/Desktop/Textbooks"]
    # path = ["rep_data"]
    path = find_usb()
    bin_files = find_folders(path)
    pins = get_pins(bin_files)
    [dates, seasons] = get_creation_date(bin_files)
    result = open_bin_files(bin_files)
    [sort_date, sort_pin] = sort(pins, dates, seasons, result)






