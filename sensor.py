#!/opt/python3.4/bin/python3.4

import re
from statistics import mean
import threading
import calendar
import time
from Adafruit_ADS1x15 import ADS1x15
import math

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

    badValues = [2048, 0]

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

    a=0.00240299448648968000
    b=0.00000418117517891415
    c=0.00000071582625490280

    sps = 250  # 250 samples per second
    gain = 4096  # +/- 4.096V

    def __init__(self, name, w1id, sumOffset=0, productOffset=1):
        super().__init__(name)
        self.name = name
        self.w1id = w1id
        self.sumOffset = sumOffset
        self.adc = ADS1x15(ic=0x01)

    def RawTemp(self):
        resistance = self.adc.readADCSingleEnded(0, self.gain, self.sps)
        print (resistance)
        if resistance > 0:
            ln_r = math.log(resistance)
            temp = self.a + self.b*ln_r + self.c*ln_r*ln_r*ln_r
            return 1/temp-273.15
        return self.badReading
