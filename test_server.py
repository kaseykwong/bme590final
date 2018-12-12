from server import check_input, create_new
import pytest
from datetime import datetime
from import_data import open_bin_files, find_folders, get_creation_date, get_pins, sort
import pandas as pd

def test_check():
    path = ["rep_data/L0.BIN", "rep_data/L1.BIN"]
    [time, days, years] = get_creation_date(path)
    spy = open_bin_files(path)
    file = spy[1]
    file_info = {'Encoded .BIN file': file,
                 'Pin': 1112,
                 'Year': 2018,
                 'Date': "10-23-2017",
                 'Time': "11:02:53"
                 }
    print(type(file))
    test1 = create_new(file_info)

def test_dataframe():
    path = ["rep_data"]
    bin_files = find_folders(path)
    pins = get_pins(bin_files)
    [times, dates, seasons] = get_creation_date(bin_files)
    result = open_bin_files(bin_files)
    overall = sort(pins, dates, times, seasons, result)
    for row in overall.itertuples():
        print(row)
        print(getattr(row,"_5"))
        print('next')


if __name__ == "__main__":
    #test_check()
    test_dataframe()