#!/opt/python3.4/bin/python3.4

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature
import json
import os

temp = 0

@app.route('/')
def index():
    return render_template('overview.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/logging')
def logging():
    data=temp.Logs()
    return render_template('logging.html', data=data)

def getDetails(sensor):
    foo={}
    if sensor in temp.sensors.keys():
        foo['temperature'] = temp.CurrentTemp(sensor)
        foo['change'] = temp.Change(sensor)
        foo['last_update'] = temp.LastUpdate(sensor)
        foo['max_temp'] = temp.Max(sensor) 
        foo['min_temp'] = temp.Min(sensor) 
        foo['status'] = temp.Status(sensor) 
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

@app.route('/calibrate/<temperature>')
def calibrate(temperature):
    temperature = float(temperature)
    for sensor in temp.sensors.keys():
        temp.sensors[sensor].Calibrate(temperature)
    return getTemperatures()

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        temp = temperature()
        temp.Start()
    app.run(host='0.0.0.0', debug=True, threaded=False)

