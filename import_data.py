import os
import usb.core
import base64


# def get_usb():
#     dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

def make_folder(destination, name):
    new_path = destination + '/' + name
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def find_folders(path):
    filepaths = []
    dirs = os.listdir(path)
    for folder in dirs:
        filepaths.append(path + "/" + str(folder))
        print(filepaths)
    return filepaths


def get_data(filepaths):
    files = []
    new_dir = os.listdir(str(filepaths[0]))
    for file in new_dir:
        if file.endswith(".BIN"):
            files.append(filepaths[0] + '/' + str(file))
    print(files)
    return files


def open_files(files):
    name = files[0]
    with open(name, mode='rb') as file:  # b is important -> binary
        file_content = file.read()
        print(file_content)
    return file_content


def read_file_as_b64(file_path):
    with open(file_path, "rb") as binary_file:
        return base64.b64encode(binary_file.read())


if __name__ == "__main__":
    path = "/Volumes/MV1-1765"
    new_path = "/Users/liameirose/Desktop"
    folder_name = "Practice"
    make_folder(new_path, folder_name)
    # get_usb()
    # file_paths = find_folders(path)
    # files = get_data(file_paths)
    # open_files(files)


