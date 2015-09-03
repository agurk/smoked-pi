#!/opt/python3.4/bin/python3.4

import re

class temperature:

    sensors={}

    def __init__(self):
        self.sensors['inlet_temp'] = sensor('inlet_temp', '3b-00000018784c')
        self.sensors['exhaust_temp'] = sensor('exhaust_temp', '3b-0000001916d9')
        self.sensors['chamber_temp_1'] = sensor('chamber_temp_1', '3b-000000191fc3')
        self.sensors['chamber_temp_2'] = sensor('chamber_temp_2', 'aoeu')
        self.sensors['food_temp_1'] = sensor('food_temp_1', 'aoeu')
        self.sensors['food_temp_2'] = sensor('food_temp_2', 'aoeu')

    def CurrentTemp(self, sensorName):
        sensor = self.sensors[sensorName]
        rawC = sensor.Temperature()
        rawF = (rawC * 9) / 5 + 32
        prettyC = str("{0:.2f}".format(rawC)) + ' C'
        prettyF = str("{0:.1f}".format(rawF)) + ' F'
        return prettyC + '  |  ' + prettyF


class sensor:

    name=''
    w1id=''
    sumOffset=0
    productOffset=1

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        self.name = name
        self.w1id = w1id
        self.sumOffset = sumOffset
        self.productOffset = productOffset

    def Temperature(self):
        raw = self.RawTemp()
        if raw == '':
            raw = '0'
        return (int(raw) / 1000) * self.productOffset + self.sumOffset

    def RawTemp(self):
        try:
            file = open('/sys/bus/w1/devices/'+self.w1id+'/w1_slave', 'r')
            p = re.compile('t=([0-9]*)')
            m = p.search(file.read())
            if m:
                return m.groups(1)[0]
        except FileNotFoundError:
            return '-373260'
        return '-373260'

