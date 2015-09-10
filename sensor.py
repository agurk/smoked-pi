#!/opt/python3.4/bin/python3.4

import re
from statistics import mean
import threading
import time

class sensor:

    sampleSize = 3
    samplePosition = 0
    startingTemp = 25
    sleepTime = 1.1

    def __init__(self, name):
        self.name=name
        self.temps = [self.startingTemp] * self.sampleSize
        self.deltas = [0] * self.sampleSize

    def Temperature(self):
        return mean(self.temps)

    def TempChange(self):
        return mean(self.deltas)
        
    def UpdateTemp(self):
        newTemp = self.RawTemp()
        oldPosn = self.samplePosition
        self.samplePosition += 1
        self.samplePosition = self.samplePosition % self.sampleSize
        self.deltas[self.samplePosition] = newTemp - self.temps[oldPosn]
        self.temps[self.samplePosition] = newTemp

    def Run(self):
        while 1:
            self.UpdateTemp()
            time.sleep(self.sleepTime)

    def Start(self):
        t = threading.Thread(target=self.Run)
        t.daemon = True
        t.start()

class thermocouple(sensor):

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        super().__init__(name)
        self.w1id = w1id
        self.sumOffset = sumOffset
        self.productOffset = productOffset

    def RawTemp(self):
        raw = self.RawTempString()
        if raw == '':
            raw = '0'
        return (int(raw) / 1000) * self.productOffset + self.sumOffset

    def RawTempString(self):
        try:
            file = open('/sys/bus/w1/devices/'+self.w1id+'/w1_slave', 'r')
            p = re.compile('t=([0-9]*)')
            m = p.search(file.read())
            if m:
                return m.groups(1)[0]
        except FileNotFoundError:
            return '-373260'
        return '-373260'

class thermistor(sensor):

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        self.name = name
        self.w1id = w1id
        self.sumOffset = sumOffset
