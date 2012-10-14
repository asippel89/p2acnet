
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# filepath = 'test.txt'
# f = open(filepath, 'r')

r = requests.get('http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node=fastest/start=11-OCT-2012-12:30/end=11-OCT-2012-12:35+E:HADC02')
raw = r.content.splitlines()
# print raw
print len(raw)
print type(raw)

data_list = []
for element in raw:
    data_split = element.split('   ')
    datetime_el = dt.datetime.strptime(data_split[0], '%d-%b-%Y %H:%M:%S.%f')
    value_el = float(data_split[1].strip())
    data_list.append([datetime_el, value_el])

data_array = np.array(data_list)

print "Data array shape = ", data_array.shape
print "Data array type = ", data_array.dtype
print data_array

x = range(100)
y = np.sin(x)
plt.plot(x, y)
