#!/opt/python3.4/bin/python3.4

import re

class temperature:

    def CurrentTemp(self, sensor):
        file = open('/sys/bus/w1/devices/3b-00000018784c/w1_slave')
        #foo = file.read()
        #print(foo)
        p = re.compile('t=[0-9]*')
        m = p.search(file.read())
        if m:
            return m.group()
        else:
            return 'null'
        #return re.match('t', foo)
        #return 32
