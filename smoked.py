#!/usr/bin/python3

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp/<sensor>')
def getTemperature(sensor):
    temp=temperature()
    foo={}
    foo['inlet_temp']=temp.CurrentTemp(sensor)
    foo['exhaust_temp']=temp.CurrentTemp(sensor)
    foo['chamber_temp_1']=temp.CurrentTemp(sensor)
    foo['chamber_temp_2']=temp.CurrentTemp(sensor)
    return str(json.JSONEncoder().encode(foo))

if __name__ == '__main__':
    app.run(debug=True)

