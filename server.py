from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields, errors
import pymodm
import os
import logging

connect("mongodb://almostdone:2tired@ds145148.mlab.com:45148/bme590final")
app = Flask(__name__)

class HeadData(MongoModel):
    season = fields.DateTimeField()
    pin_number = fields.IntegerField(primary_key=True)
    date_measured = fields.DateTimeField()
    encoded_binary = fields.BinaryField()


@app.route("/api/download", methods=["POST"])
def download():
    files = request.get_json()
    if check_pin_date(files) is False:
        create_new(files)
    else:
        print('Data exists')
    return


# def check_pin_exists(file_info):
#     try:
#         HeadData.objects.raw({"_id": file_info["Pin"]}).first()
#     except pymodm.errors.DoesNotExist:
#         return False
#     return True


def check_pin_date(file_info):
    pin = file_info['Pin']
    date = file_info['Date']

    for hd in HeadData.objects.raw({"date_measured": date}):
        if hd.pin_number == pin:
            return True
    return False


def create_new(file_info):
    pin = file_info['Pin']
    szn = file_info['Year']
    date = file_info['Date']
    data = file_info['Encoded .BIN file']
    hd = HeadData(szn,pin,date,data)
    hd.save()