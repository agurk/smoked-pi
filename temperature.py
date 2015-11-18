#!/opt/python3.4/bin/python3.4

import re

from sensor import thermocouple
from sensor import thermistor

class temperature:

    def __init__(self):
        self.sensors={}
#        self.sensors['inlet_temp'] = thermocouple('inlet_temp', '3b-000000191eb6')
#        self.sensors['inlet_temp'].Start()
#        self.sensors['exhaust_temp'] = thermocouple('exhaust_temp', '3b-000000191db5')
#        self.sensors['exhaust_temp'].Start()
#        self.sensors['chamber_temp_1'] = thermocouple('chamber_temp_1', '3b-000000191713')
#        self.sensors['chamber_temp_1'].Start()
#        self.sensors['chamber_temp_2'] = thermocouple('chamber_temp_2', '3b-0000001916d9')
#        self.sensors['chamber_temp_2'].Start()
        self.sensors['food_temp_1'] = thermistor('food_temp_1', 'aoeu')
        self.sensors['food_temp_1'].Start()
#        self.sensors['food_temp_2'] = thermocouple('food_temp_2', 'aoeu')

    def CurrentTemp(self, sensorName):
        sensor = self.sensors[sensorName]
        rawC = sensor.Temperature()
        rawF = (rawC * 9) / 5 + 32
        prettyC = str("{0:.1f}".format(round(rawC, 1))) + ' C'
        prettyF = str("{0:.1f}".format(round(rawF, 1))) + ' F'
        return prettyC + '  |  ' + prettyF

    def Change(self, sensorName):
        sensor = self.sensors[sensorName]
        return sensor.TempChange()

    def LastUpdate(self, sensorName):
        sensor = self.sensors[sensorName]
        return sensor.LastUpdate()

