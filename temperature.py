import re

from sensor import thermocouple
from sensor import thermistor
from Adafruit_ADS1x15 import ADS1x15

class temperature:

    def __init__(self):
        self.adc = ADS1x15(ic=0x01)
        self.adc.Start()
        self.sensors={}
        self.sensors['gauge_1'] = thermistor('food_temp_1', 0, self.adc)
        self.sensors['gauge_2'] = thermistor('food_temp_2', 1, self.adc)
        self.sensors['gauge_3'] = thermocouple('inlet_temp', '3b-000000191eb6')
        self.sensors['gauge_4'] = thermocouple('exhaust_temp', '3b-000000191db5')
        self.sensors['gauge_5'] = thermocouple('chamber_temp_1', '3b-000000191713')
        self.sensors['gauge_6'] = thermocouple('chamber_temp_2', '3b-000000191fc3')
        for key, sensor in self.sensors.items():
            sensor.Start()

    def CurrentTemp(self, sensorName):
        sensor = self.sensors[sensorName]
        rawC = sensor.Temperature()
        rawF = (rawC * 9) / 5 + 32
        temp={}
        temp['c'] = str("{0:.1f}".format(round(rawC, 1)))# + ' C'
        temp['f'] = str("{0:.0f}".format(round(rawF, 0)))# + ' F'
        return temp

    def Change(self, sensorName):
        sensor = self.sensors[sensorName]
        return sensor.TempChange()

    def LastUpdate(self, sensorName):
        sensor = self.sensors[sensorName]
        return sensor.LastUpdate()

    def __del__(self):
        print ("Exiting")

