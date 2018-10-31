# coding:utf-8
import base64
import binascii
import rsa
import sqlite3
import datetime
import logging


def writevisit(command):
    maneger = [r"何云俊"]
    for i in maneger:
        if i in command:
            return
    conn = sqlite3.connect("tools/visit.db")
    cursor = conn.cursor()
    cursor.execute(command)
    # data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    # return data


def toRsa(message):
    # pubkey = "008ec56d6281753fc8d2d1e6ce0f93c38036e1db7b53d1d3ce9a65f2bfc3b385640c61154c7935c4eeea900e982092fe4ae8d41451a56a18707ec195d5c5deb5bdef1b891f5f358c65c6e6f27971be03fff66e0314fda64302e7cf530b35a8e13fdf0b186d593e21f9000da84c84058b9924287d3eab698ec281d9c98646cbea05"
    pubkey = "a9662d4f816fb3161556fe7104accaa87fbd199226f79001b0bea20434eb0b11da0f4b51854ccfc22748820ac399842810ddbb3d86ca91b85650df384ce823f146efd0454f33dba5c25eda6730fda0f33033a9e4d9ca14cb55ca67cdfefad4a3258834e1dfccb978880111c8e28a44a14a22246d33d86ba394665a44915a39f1"
    rsaPublickey = int(pubkey, 16)
    message = str(message)
    key = rsa.PublicKey(rsaPublickey, 65537)
    rsapassword = rsa.encrypt(message, key)
    rsapassword = binascii.b2a_hex(rsapassword)
    basepassword = base64.b64encode(rsapassword)
    a = "!ENCRYPT-CMSS!"
    password = a + basepassword
    return password


def readvisit(command):
    conn = sqlite3.connect("tools/visit.db")
    cursor = conn.cursor()
    cursor.execute(command)
    data = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    conn.close()
    return data, fields


def dateRange(start, end=None, day=7, step=1, format="%Y-%m-%d"):
    logging.debug(start, end)
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    if end == None:
        days = day
    else:
        days = (strptime(start, format) - strptime(end, format)).days + 1
    return [strftime(strptime(start, format) - datetime.timedelta(i), format)
            for i in xrange(0, days, step)]

