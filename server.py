from flask import Flask, request
from pymodm import connect
from pymodm import MongoModel, fields, errors
import pymodm
import requests
from datetime import datetime
import logging


connect("mongodb://almostdone:2tired@ds145148.mlab.com:45148/bme590final")
app = Flask(__name__)


class HeadData(MongoModel):
    season = fields.IntegerField()
    pin_number = fields.CharField()
    date_measured = fields.CharField()
    encoded_binary = fields.CharField()
    time = fields.CharField()


@app.route("/api/download", methods=["POST"])
def download():
    """
    Function downloads individual BIN files to server

    Returns:
        msg: status message of file download
    """
    set_logging()
    files = request.get_json()
    if check_input(files) is True:
        if check_exist(files) is False:
            pin = files['Pin']
            szn = files['Year']
            date = files['Date']
            data = files['Encoded .BIN file']
            t = files['Time']
            hd = HeadData(szn, pin, date, data, t)
            hd.save()
            file_info = {'pin_number': pin,
                         'Year': szn,
                         'Date': date,
                         'Time': t
                         }
            logging.info(file_info)
            msg = "Data saved"
            print(msg)
            return msg
        else:
            msg = "Data file already exists"
            print(msg)
            return "Data already exists"
    else:
        msg = "Data input not correct"
        print(msg)
        return "Data input not correct"


def download_all(files):
    """
    Client Function downloads all .BIN folders in given
    Pandas dataframe

    Args:
        files: datafram of all files
    Returns:
        result: boolean to determine if all files completed
    """
    # count = 0
    for row in files.itertuples():
        pin = getattr(row, "Pin")
        date = getattr(row, "Date")
        time = getattr(row, "Time")
        year = getattr(row, "Year")
        data = getattr(row, "_5")
        file_info = {"Pin": pin,
                     "Date": date,
                     "Time": time,
                     "Year": year,
                     "Encoded .BIN file": data
                     }
        # file_check = {'Pin': pin,
        #               'Date': date,
        #               'Time': time
        #               }
        # if check_input(file_info) is True:
        #     if check_exist(file_check) is False:
        #         count = count + 1
        #     else:
        #         count = count
        r = requests.post("http://127.0.0.1:5000/api/download", json=file_info)
        # print(count)
    # set_logging()
    # logging.info(str(count)+" new files.")
    return True


def check_input(file_info):
    """
    Function finds all .BIN folders in given path

    Args:
        file_info: dictionary with individual file information
        Pin, Date, Time, Year, Encoded .BIN file
    Returns:
        result: boolean to determine if file inputs were appropriate type
    """
    pin = file_info['Pin']
    date = file_info['Date']
    time = file_info['Time']
    year = file_info['Year']
    msg = "Data is ok"
    try:
        int(pin)
    except KeyError:
        msg = "No pin number attached."
        print(msg)
        return False
    except ValueError:
        msg = "Pin number is not a number"
        print(msg)
        return False
    try:
        datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        msg = "Date entry is not Month-Day-Year"
        print(msg)
        return False
    try:
        datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        msg = "Time entry is not Hour:Minute:Second"
        print(msg)
        return False
    try:
        datetime.strptime(str(year), "%Y")
    except ValueError:
        msg = "Season entry is not Year"
        print(msg)
        return False
    print(msg)
    return True


def check_exist(file_info):
    """
    Function checks if file already exists in database

    Args:
        file_info: file info dictionary
        Pin, Date, Time, Year, Encoded .BIN file
    Returns:
        result: boolean to determine if file was found.
                True is file was found. False if not.
    """
    pin = file_info['Pin']
    date = file_info['Date']
    time_in = file_info['Time']
    try:
        # HeadData.objects.raw({"date_measured": date,
        #                       "time": time_in,
        #                       "pin_number": str(pin)}).first()
        HeadData.objects.raw({"pin_number": str(pin),
                              "date_measured": date,
                              "time": time_in}).first()
    except pymodm.errors.DoesNotExist:
        return False
    return True


def create_new(file_info):
    """
    Non flask function to create new database file
    not necessary for server to run

    Args:
        file_info: file info dictionary
        Pin, Date, Time, Year, Encoded .BIN file
    Returns:
        result: hd, HeadData object created
    """
    set_logging()
    pin = file_info['Pin']
    szn = file_info['Year']
    date = file_info['Date']
    data = file_info['Encoded .BIN file']
    t = file_info['Time']
    hd = HeadData(szn, pin, date, data, t)
    hd.save()
    logging.info(file_info)
    return hd


def set_logging():
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True
    logging.basicConfig(filename='data_server.txt',
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)
    return


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
