from server import check_pin_date, create_new
import pytest
from datetime import datetime
from import_data import open_bin_files, find_folders, get_creation_date


def test_check():
    path = ["rep_data/L0.BIN", "rep_data/L1.BIN"]
    [time, days, years] = get_creation_date(path)
    spy = open_bin_files(path)
    file = spy[1]
    file_info = {'Encoded .BIN file': file,
                 'Pin': 1112,
                 'Year': 2018,
                 'Date': datetime.strptime(time[1],"%m-%d-%Y")
                 }
    print(type(file))
    test1 = create_new(file_info)


if __name__ == "__main__":
    test_check()