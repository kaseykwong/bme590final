from import_data import find_folders, get_creation_date


def test_find_folders():
    path = ['rep_data']
    filenames = find_folders(path)
    assert filenames == ['rep_data/L11.BIN', 'rep_data/L12.BIN',
                         'rep_data/L0.BIN', 'rep_data/L1.BIN', 'rep_data/L2.BIN']


def test_get_creation_date():
    file_path1 = ['rep_data/L0.BIN']
    [date1, days1, year1] = get_creation_date(file_path1)
    assert [date1, days1, year1] == [['12-06-2018'], [17871.836215277777], [2018]]

    file_path2 = ['rep_data/L1.BIN']
    [date2, days2, year2] = get_creation_date(file_path2)
    assert [date2, days2, year2] == [['12-06-2018'], [17871.836215277777], [2018]]

    file_path3 = ['rep_data/L0.BIN', 'rep_data/L1.BIN']
    [date3, days3, year3] = get_creation_date(file_path3)
    assert [date3, days3, year3] == [['12-06-2018', '12-06-2018'],
                                     [17871.836215277777, 17871.836215277777],
                                     [2018, 2018]]
