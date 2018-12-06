import os
import usb.core
import base64
import datetime
import usb


# def get_usb():
#     for dev in usb.core.find(find_all=1):
#         print
#         "Device:", dev.filename
#         print
#         "  idVendor: %d (%s)" % (dev.idVendor, hex(dev.idVendor))
#         print
#         "  idProduct: %d (%s)" % (dev.idProduct, hex(dev.idProduct))
#     return usb


def make_folder(destination, name):
    new_path = destination + '/' + name
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def find_folders(path):
    filepaths = []
    dirs = os.listdir(path)
    for folder in dirs:
        filepaths.append(path + "/" + str(folder))
    return filepaths


def get_data(filepaths):
    files = []
    for dir in filepaths:
        new_dir = os.listdir(str(dir))
        for file in new_dir:
            if file.endswith(".BIN"):
                if file.startswith("L"):
                    files.append(filepaths[0] + '/' + str(file))
        print(files)
        return files


def get_creation_date(files):
    days = []
    for dir_path in files:
        t = datetime.datetime.fromtimestamp(os.stat(dir_path).st_ctime)
        seconds = t.strftime("%s")
        year = t.year
        print(year)
        days.append(int(seconds)/86400)
    return t, days, year


def sort_creation(creation):
    delta = [creation[i] - creation[i + 1] for i in range(len(creation) - 1)]
    for diff in delta:
        if diff <= -1:
            print('New Day')
    return delta


def open_bin_files(paths):
    #i = 0
    for name in paths:
        with open(name, mode="rb") as file:
            file_content = file.read()
            i = i + 1
            spy = base64.b64encode(file_content)
            #print(result)
            #print(i)
    return spy


def combo(t, spy, season):
    combo = {
        #"Pin": ,
        "Year": season,
        "Date": t,
        "Encoded .BIN file": spy
    }
    return combo


if __name__ == "__main__":
    path = "/Volumes/MV1-1765"
    new_path = "/Users/liameirose/Desktop"
    folder_name = "Practice"
    # make_folder(new_path, folder_name)
    # get_usb()
    file_paths = find_folders(path)
    files = get_data(file_paths)
    [dates, creation_date, year] = get_creation_date(files)
    sort_creation(creation_date)
    result = open_bin_files(files)
    combo(dates, result, year)




