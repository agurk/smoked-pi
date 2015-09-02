#!/usr/bin/python3

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature
import json

temp = temperature()

sensors={}
sensors['inlet_temp'] = 'aoeu'
sensors['exhaust_temp'] = 'aoeu'
sensors['chamber_temp_1'] = 'aoeu'
sensors['chamber_temp_2'] = 'aoeu'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp/<sensor>')
def getTemperature(sensor):
    foo={}
    if sensor in sensors.keys():
        foo[sensor]=temp.CurrentTemp(sensors[sensor])
    return str(json.JSONEncoder().encode(foo))

@app.route('/temps/')
def getTemperatures():
    foo={}
    for sensor in sensors:
        foo[sensor]=temp.CurrentTemp(sensors[sensor])
    return str(json.JSONEncoder().encode(foo))

if __name__ == '__main__':
    app.run(debug=True)

