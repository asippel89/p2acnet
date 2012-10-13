
import requests
import numpy as np

# filepath = 'test.txt'
# f = open(filepath, 'r')

r = requests.get('http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node=fastest/start=11-OCT-2012-12:30/end=11-OCT-2012-12:35+E:HADC02')
raw = r.content
print len(raw)


data_list = []
for line in raw:
    dataline = line.split('  ')
    data_list.append(dataline)
data = np.array(data_list)

print 'Data = ', data

# Do you see this message?
