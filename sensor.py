#!/opt/python3.4/bin/python3.4

import re
from statistics import mean
import threading
import calendar
import time

class sensor:

    sampleSize = 3
    samplePosition = 0
    startingTemp = 25
    sleepTime = 1.1
    badReading = '-666'
    lastReading = calendar.timegm(time.gmtime())

    def __init__(self, name):
        self.name=name
        self.temps = [self.startingTemp] * self.sampleSize
        self.deltas = [0] * self.sampleSize

    def LastUpdate(self):
        return calendar.timegm(time.gmtime()) - self.lastReading

    def Temperature(self):
        return mean(self.temps)

    def TempChange(self):
        return mean(self.deltas)
        
    def UpdateTemp(self):
        newTemp = self.RawTemp()
        if newTemp != self.badReading:
            self.lastReading = calendar.timegm(time.gmtime())
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

    badValues = [2048]

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        super().__init__(name)
        self.w1id = w1id
        self.sumOffset = sumOffset
        self.productOffset = productOffset

    def RawTemp(self):
        raw = self.RawTempString()
        if raw == '':
            return self.badReading
        convertedValue = int(raw) / 1000
        if convertedValue in self.badValues:
            return self.badReading
        return convertedValue * self.productOffset + self.sumOffset

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

    from Adafruit_ADS1x15 import ADS1x15

    sps = 250  # 250 samples per second
    gain = 4096  # +/- 4.096V

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        self.name = name
        self.w1id = w1id
        self.sumOffset = sumOffset
        self.adc = ADS1x15(ic=ADS1115)

    def RawTemp(self):
        resistance = self.adc.readADCSingleEnded(0, gain, sps)
        t0 = 297.15
        b = 3950
        r0 = 5800
        t_recip=1/t0 + 1/b * ln (resistance / r0)
        return 1/t_recip - 273.15
