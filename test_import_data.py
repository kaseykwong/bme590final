from import_data import find_folders, get_pins
from import_data import get_creation_date, sort
from import_data import open_bin_files
import base64


def test_find_folders():
    path = ['rep_data']
    [boolean, file_names] = find_folders(path)
    assert [boolean, file_names] == [True, ['rep_data/L11.BIN',
                                            'rep_data/L12.BIN',
                                            'rep_data/L0.BIN',
                                            'rep_data/L1.BIN',
                                            'rep_data/L2.BIN']]
    path2 = []
    [boolean2, file_names2] = find_folders(path2)
    assert [boolean2, file_names2] == [False, []]


def test_get_pins():
    files = ['rep_data/L11.BIN', 'Volumes/MV1-1756',
             'Volumes/MV1-1756/fake.txt',
             'Volumes/TX1-5786/fake.txt',
             'Volumes/MV1/fake.txt']
    pins = get_pins(files)
    assert pins == ['rep_data', '1756', '1756', '5786', 'Volumes']


def test_get_creation_date():
    file_path1 = ['rep_data/L0.BIN']
    [time1, date1, year1] = get_creation_date(file_path1)
    assert [time1, date1, year1] == [['20:35:38'], ['12-06-2018'], [2018]]

    file_path2 = ['rep_data/L1.BIN']
    [time2, date2, year2] = get_creation_date(file_path2)
    assert [time2, date2, year2] == [['20:35:38'], ['12-06-2018'], [2018]]

    file_path3 = ['rep_data/L0.BIN', 'rep_data/L1.BIN']
    [time3, date3, year3] = get_creation_date(file_path3)
    assert [time3, date3, year3] == [['20:35:38', '20:35:38'],
                                     ['12-06-2018', '12-06-2018'],
                                     [2018, 2018]]


def test_open_bin_files():
    paths1 = ['rep_data/L0.BIN', 'rep_data/L11.BIN', 'rep_data/L12.BIN']
    [boolean1, encode1] = open_bin_files(paths1)
    assert base64.b64encode(base64.b64decode(encode1[0])) == encode1[0]
    assert base64.b64encode(base64.b64decode(encode1[1])) == encode1[1]
    assert base64.b64encode(base64.b64decode(encode1[2])) == encode1[2]
    assert boolean1 is True

    paths2 = []
    [boolean2, encode2] = open_bin_files(paths2)
    print(encode2)
    assert encode2 == []
    assert boolean2 is False


def test_sort():
    pin1 = ['123', '124', '123']
    date1 = ['10-05-1994', '10-05-1994', '10-07-1994']
    time1 = ['00:00:00', '00:00:01', '00:00:02']
    season1 = ['1994', '1994', '1994']
    bin1 = ['abc', 'def', 'ghi']
    [overall1, sort_date1, sort_pin1] = sort(pin1, date1, time1, season1, bin1)
    assert [overall1.loc[0, "Pin"], sort_date1[0][0], sort_pin1[0][0]] == \
           ['123', '10-05-1994', '123']
    assert [overall1.loc[1, "Pin"], sort_date1[1][0], sort_pin1[1][0]] == \
           ['124', '10-07-1994', '124']
