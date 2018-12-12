from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields, errors
import pymodm
import requests
from datetime import datetime
import os
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
    Flask server function to download individual files with parsed data
    :return:
    """
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
    return


def download_all(files):
    """
    Client Function to iterate thru all parsed and encoded files to download
    :param files:
    :return:
    """
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
                     "Encoded .BIN file": data}
        r = requests.post("http://127.0.0.1/5000/api/download", json=file_info)
    msg = "All files downloaded"
    return msg


def check_input(file_info):
    """
    Check types and values of file input parameters
    :param file_info:
    :return:
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
    Check if the particular file recorded at specific time for pin number already exists in database
    :param file_info:
    :return:
    """
    pin = file_info['Pin']
    date = file_info['Date']
    time_in = file_info['Time']
    try:
        HeadData.objects.raw({"date_measured": date,
                              "time": time_in,
                              "pin_number": str(pin)}).first()
    except pymodm.errors.DoesNotExist:
        return False
    return True


def create_new(file_info):
    """
    Unnecessary function to create a new file in the database.
    functionality exists in Flask Post function "download"
    :param file_info:
    :return:
    """
    pin = file_info['Pin']
    szn = file_info['Year']
    date = file_info['Date']
    data = file_info['Encoded .BIN file']
    t = file_info['Time']
    hd = HeadData(szn, pin, date, data, t)
    hd.save()
    return hd


# def client(file_info):
#     r = requests.post("http://127.0.0.1/5000/api/download", json=file_info)
#     return

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
