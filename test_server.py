from server import check_input, create_new, check_exist, download_all
import pytest
import requests
import pandas as pd


def test_exist():
    file_info = {'Encoded .BIN file': 'ASDFWEAGJ',
                 'Pin': 1112,
                 'Year': 2018,
                 'Date': "10-23-2017",
                 'Time': "11:02:53"
                 }
    create_new(file_info)
    assert check_exist(file_info) is True
    input2 = {'Encoded .BIN file': 'ASDFWEAGJ',
              'Pin': 1112,
              'Year': 2018,
              'Date': "10-23-2017",
              'Time': "11:02:55"
              }
    assert check_exist(input2) is False
    input3 = {'Encoded .BIN file': 'ASDFWEAGJ',
              'Pin': 1112,
              'Year': 2018,
              'Date': "10-22-2017",
              'Time': "11:02:53"
              }
    assert check_exist(input3) is False
    input4 = {'Encoded .BIN file': 'ASDFWEAGJ',
              'Pin': 1122,
              'Year': 2018,
              'Date': "10-23-2017",
              'Time': "11:02:53"
              }
    assert check_exist(input4) is False

# def test_dataframe():
#     path = ["rep_data"]
#     [success, bin_files] = find_folders(path)
#     pins = get_pins(bin_files)
#     [times, dates, seasons] = get_creation_date(bin_files)
#     [boolean, binary] = open_bin_files(bin_files)
#     [total, sort_date, sort_pin] = sort(pins, dates, times, seasons, binary)
#     for row in total.itertuples():
#         print(row)
#         print(getattr(row,"Time"))
#         print('next')


def test_input():
    input1 = {'Encoded .BIN file': "AGSDFWJOGS",
              'Pin': 1112,
              'Year': 2018,
              'Date': "10-23-2017",
              'Time': "11:02:53"
              }
    assert check_input(input1) is True
    input2 = {'Encoded .BIN file': "AGSDFWJOGS",
              'Pin': '11A2',
              'Year': 2018,
              'Date': "10-23-2017",
              'Time': "11:02:53"
              }
    assert check_input(input2) is False
    input3 = {'Encoded .BIN file': "AGSDFWJOGS",
              'Pin': 1112,
              'Year': 2018,
              'Date': "1a-23-2017",
              'Time': "11:02:53"
              }
    assert check_input(input3) is False
    input4 = {'Encoded .BIN file': "AGSDFWJOGS",
              'Pin': 1112,
              'Year': 2018,
              'Date': "10-23-2017",
              'Time': "11:a2:53"
              }
    assert check_input(input4) is False
    input5 = {'Encoded .BIN file': "AGSDFWJOGS",
              'Pin': 1112,
              'Year': '20A8',
              'Date': "10-23-2017",
              'Time': "11:02:53"
              }
    assert check_input(input5) is False


# def test_all():
#     filename = [7, 7, 7, 5, 5, 5]
#     date = ["10-2-2016", "10-2-2016", "10-2-2016", "10-2-2016",
#  "10-2-2016", "10-2-2016"]
#     time = ["10:10:29", "10:10:32", "10:10:40", "10:10:50",
#  "10:10:55", "10:10:59"]
#     season = [2016, 2016, 2016, 2016, 2016, 2016]
#     spy = ["ASDFAEGIAEG", "ASDFOAEWG", "ADSGA", "WEGIEHG",
#  "ASGIAB", "AEGIABN"]
#     input1 = pd.DataFrame({
#         "Pin": filename,
#         "Date": date,
#         "Time": time,
#         "Year": season,
#         "Encoded .BIN file": spy
#         })
#     print(download_all(input1))
#     #  assert download_all(input1) == msg


if __name__ == "__main__":
    # file_info = {'Encoded .BIN file': 'ASDFWEAGJ',
    #              'Pin': 1122,
    #              'Year': 2018,
    #              'Date': "10-23-2017",
    #              'Time': "11:02:53"
    #              }
    # r = requests.post("http://127.0.0.1:5000/api/download", json=file_info)
    # test_all()
    test_exist()
    test_input()
