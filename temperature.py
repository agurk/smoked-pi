#!/opt/python3.4/bin/python3.4

import re

class temperature:

    def CurrentTemp(self, sensor):
        rawC = int(self.GetRawTemp(sensor))
        rawF = (rawC * 9) / 5 + 32
        prettyC = str("{0:.2f}".format(rawC/1000)) + ' C'
        prettyF = str("{0:.1f}".format(rawF/1000)) + ' F'
        return prettyC + '  |  ' + prettyF

    def GetRawTemp(self, sensor):
        try:
            file = open('/sys/bus/w1/devices/'+sensor+'/w1_slave', 'r')
            p = re.compile('t=([0-9]*)')
            m = p.search(file.read())
            if m:
                return m.groups(1)[0]
        except FileNotFoundError:
            return '-373260'
        return '-373260'

