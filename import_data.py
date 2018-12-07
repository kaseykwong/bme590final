import os
#import usb.core
import base64
import datetime
#import usb
import pandas as pd


# def get_usb():
#     for dev in usb.core.find(find_all=1):
#         print
#         "Device:", dev.filename
#         print
#         "  idVendor: %d (%s)" % (dev.idVendor, hex(dev.idVendor))
#         print
#         "  idProduct: %d (%s)" % (dev.idProduct, hex(dev.idProduct))
#     return usb


def find_folders(path):
    count = 0
    file_names = []
    for usb in path:
        for (dir_name, dirs, files) in os.walk(usb):
            for filename in files:
                if filename.endswith('.BIN'):
                    if filename.startswith("L"):
                        count = count + 1
                        file_names.append(os.path.join(dir_name, filename))
    print('Files:', count)
    if count == 0:
        print("No files found")
    return file_names


def get_creation_date(files):
    days = []
    time = []
    year = []
    for dir_path in files:
        t = datetime.datetime.fromtimestamp(os.stat(dir_path).st_ctime)
        time.append(t.strftime('%m-%d-%Y'))
        seconds = t.strftime("%s")
        year.append(t.year)
        days.append(int(seconds)/86400)
    return time, days, year


def sort_creation(creation):
    new_day = [0]
    i = 0
    delta = [creation[i] - creation[i + 1] for i in range(len(creation) - 1)]
    for diff in delta:
        if diff <= -1:
            i = i + 1
            new_day.append(i)
        else:
            new_day.append(i)
    return new_day


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
            "Filename": filename,
            "Date": date,
            "Year": season,
            "Encoded .BIN file": spy
        })
    interval = list(overall.groupby('Date'))
    print(interval)
    return interval

if __name__ == "__main__":
    # path = ["/Users/liameirose/Desktop/Textbooks"]
    # path = ["/Volumes/MV1-1765"]
    path = ["rep_data"]
    # get_usb()
    files = find_folders(path)
    [dates, creation_date, year] = get_creation_date(files)
    new_day = sort_creation(creation_date)
    result = open_bin_files(files)
    sorted = sort(files, dates, year, result)




