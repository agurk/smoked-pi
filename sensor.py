import re
from statistics import mean
from enum import Enum
import calendar
import math
import time

class sensor:

    State = Enum('State', 'online offline error')

    currentState = State.offline

    sampleSize = 3
    samplePosition = 0
    startingTemp = 25
    badReading = '-666'
    disconnected = '-1337'
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

    def Status(self):
        return self.currentState
        
    def UpdateTemp(self):
        newTemp = self.RawTemp()
        if newTemp == self.badReading:
            if self.LastUpdate() > 3:
                self.currentState = self.State.error
        elif newTemp == self.disconnected:
            self.currentState = self.State.offline
        else:
            self.currentState = self.State.online
            self.lastReading = calendar.timegm(time.gmtime())
            oldPosn = self.samplePosition
            self.samplePosition += 1
            self.samplePosition = self.samplePosition % self.sampleSize
            self.deltas[self.samplePosition] = newTemp - self.temps[oldPosn]
            self.temps[self.samplePosition] = newTemp


class thermocouple(sensor):

    badValues = [0]
    disconnectedValue = 2047.812

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
        elif convertedValue == self.disconnectedValue:
            return self.disconnected
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

    def Calibrate(self, temp):
        return

class thermistor(sensor):

    sps = 250  # 250 samples per second
    gain = 4096  # +/- 4.096V

    #calibration data
    cRecipTemp=[0.0] * 3
    cLnRes=[0.0] * 3
    cInputNo=0

    minRes = 0
    maxRes = 500000

    def __init__(self, name, sensorId, adc, a, b, c):
        super().__init__(name)
        self.name = name
        self.sensorId= sensorId
        self.adc = adc
        self.a = a
        self.b = b
        self.c = c

    def RawTemp(self):
        resistance = self.adc.getResistance(self.sensorId)
        if resistance > self.minRes and resistance < self.maxRes:
            ln_r = math.log(resistance)
            temp = self.a + self.b*ln_r + self.c*ln_r**3
            return 1/temp-273.15
        return self.disconnected

    def Calibrate(self, temp: float):
        print ('Calibrating with ' + str(temp))
        if self.cInputNo >= 3:
            self.cInputNo = 0
        self.cRecipTemp[self.cInputNo] = 1 / (temp + 273.15)
        self.cLnRes[self.cInputNo] = math.log(self.adc.getResistance(self.sensorId))
        self.cInputNo += 1
        if self.cInputNo == 3:
            cLnRes = self.cLnRes
            cRecipTemp = self.cRecipTemp
            y_2 =(cRecipTemp[1] - cRecipTemp[0]) / (cLnRes[1] - cLnRes[0])
            y_3 =(cRecipTemp[2] - cRecipTemp[0]) / (cLnRes[2] - cLnRes[0])
            self.c = ((y_3 - y_2) / (cLnRes[2] - cLnRes[1])) * ( 1 / (cLnRes[0] + cLnRes[1] + cLnRes[2]) )
            self.b = y_2 - self.c * (cLnRes[0]**2 + cLnRes[0]*cLnRes[1] + cLnRes[1]**2)
            self.a = cRecipTemp[0] - cLnRes[0] * (self.b + cLnRes[0]**2 * self.c)
            print (self.name + ' - a: ' +str(self.a) + ' b:' + str(self.b) + ' c:' + str(self.c))


