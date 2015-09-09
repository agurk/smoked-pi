#!/opt/python3.4/bin/python3.4
#!/usr/bin/python3

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature
import json

temp = temperature()

@app.route('/')
def index():
    return render_template('index.html')

def getDetails(sensor):
    foo={}
    if sensor in temp.sensors.keys():
        foo['temperature'] = temp.CurrentTemp(sensor)
        foo['change'] = temp.Change(sensor)
    return foo

@app.route('/temp/<sensor>')
def getTemperature(sensor):
    return str(json.JSONEncoder().encode(getDetails(sensor)))

@app.route('/temps/')
def getTemperatures():
    foo={}
    for sensor in temp.sensors.keys():
        foo[sensor]=getDetails(sensor)
    return str(json.JSONEncoder().encode(foo))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

