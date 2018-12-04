from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields, errors
import pymodm
import os
import logging

connect("mongodb://almostdone:2tired@ds145148.mlab.com:45148/bme590final")
app = Flask(__name__)

class Data(MongoModel):
    season = fields.DateTimeField()
    pin_number = fields.ListField(field=fields.IntegerField())
    dates = fields.ListField(field=fields.ListField(field=fields.DateTimeField()))
    bin_files = fields.ListField(field=fields.ListField(field=fields.ListField(field=fields.BinaryField())))

@app.route("/api/download", methods=["POST"])
def download():
    files = request.get_json()
    return


def check_pin_exists(file_info):
    try:
        Data.objects.raw({"pin_number": str(info["Pin"])})
    except pymodm.errors.DoesNotExist:
        return False
    return True

def create_newseason(file_info):


def create_pin_folder(file_info):