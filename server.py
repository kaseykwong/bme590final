from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields, errors
import pymodm
import requests
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
    files = request.get_json()
    if check_exist(files) is False:
        pin = files['Pin']
        szn = files['Year']
        date = files['Date']
        data = files['Encoded .BIN file']
        t = files['Time']
        hd = HeadData(szn, pin, date, data, t)
        hd.save()
        return hd
    return


def download_all(files):
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
    pin = file_info['Pin']
    msg = "Data is ok"
    try:
        int(pin)
    except KeyError:
        msg = "No pin number attached."
        return False, msg
    except ValueError:
        msg = "Pin number is not a number"
        return False, msg
    return True, msg


def check_exist(file_info):
    pin = file_info['Pin']
    date = file_info['Date']
    time_in = file_info['Time']
    year = file_info['Year']
    try:
        HeadData.objects.raw({"date_measured": date,
                              "pin_number": pin,
                              "time": time_in}).first()
    except pymodm.errors.DoesNotExist:
        return False
    return True


def create_new(file_info):
    pin = file_info['Pin']
    szn = file_info['Year']
    date = file_info['Date']
    data = file_info['Encoded .BIN file']
    t = file_info['Time']
    hd = HeadData(szn, pin, date, data, t)
    hd.save()
    return hd


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)