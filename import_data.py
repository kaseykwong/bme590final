import os
import base64
import datetime
import pandas as pd
import subprocess


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
    usb = [s for s in dev if "MV" in s]
    print(usb)
    return usb


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
    # path = ["rep_data"]
    path = find_usb()
    files = find_folders(path)
    [dates, year] = get_creation_date(files)
    result = open_bin_files(files)
    sorted = sort(files, dates, year, result)




