#!/opt/python3.4/bin/python3.4

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature
import json

temp = temperature()

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
    for sensor in temp.sensors.keys():
        foo[sensor]=temp.CurrentTemp(sensor)
    return str(json.JSONEncoder().encode(foo))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

