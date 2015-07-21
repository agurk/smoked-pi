#!/usr/bin/python3

from flask import Flask
from flask import render_template
app = Flask(__name__)

from temperature import temperature

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp/<sensor>')
def getTemperature(sensor):
    temp=temperature()
    return str(temp.CurrentTemp(sensor))

if __name__ == '__main__':
    app.run(debug=True)

