import re

from sensor import thermocouple
from sensor import thermistor
from Adafruit_ADS1x15 import ADS1x15

class temperature:

    sensorData={}

    def __init__(self):
        a=0.00240299448648968000
        b=0.00000418117517891415
        c=0.00000071582625490280

        self.adc = ADS1x15(ic=0x01)
        self.adc.Start()
        self.sensors={}
        self.sensors['gauge_1'] = thermistor('food_temp_1', 0, self.adc, a, b, c)
        self.sensors['gauge_2'] = thermistor('food_temp_2', 1, self.adc, a, b, c)
        self.sensors['gauge_3'] = thermocouple('inlet_temp', '3b-000000191eb6')
        self.sensors['gauge_4'] = thermocouple('exhaust_temp', '3b-000000191db5')
        self.sensors['gauge_5'] = thermocouple('chamber_temp_1', '3b-000000191713')
        self.sensors['gauge_6'] = thermocouple('chamber_temp_2', '3b-000000191fc3')
        for key, sensor in self.sensors.items():
            sensor.Start()
            self.sensorData[key] = SensorData()

    def CurrentTemp(self, sensorName):
        sensor = self.sensors[sensorName]
        rawC = sensor.Temperature()
        rawF = (rawC * 9) / 5 + 32
        self.sensorData[sensorName].addTemp(rawC)
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

    def Max(self, sensorName):
        return self.sensorData[sensorName].maxTemp

    def Min(self, sensorName):
        return self.sensorData[sensorName].minTemp

    def Status(self, sensorName):
        sensor = self.sensors[sensorName]
        if sensor.Status() == sensor.State.offline:
            return 'offline'
        if sensor.Status() == sensor.State.online:
            return 'online'
        return 'error'

    def __del__(self):
        print ("Exiting")

class SensorData:
    maxTemp=30
    minTemp=20

    def addTemp(self, value):
        if value > self.maxTemp:
            self.maxTemp = value
        elif value < self.minTemp:
            self.minTemp = value

