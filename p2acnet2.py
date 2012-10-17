import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class P2ACNET(object):
    '''
    This class uses the iter_lines() requests method to iterate over each line of the returned content
    instead of loading the whole response into memory and then performing operations on it. Also,
    this version does not convert the datetime elements into matplotlib date types in parse_query. (This
    seemed to be the cause of significant slowdown)
        
    '''

    def __init__(self, channel, start_time, end_time, node = 'fastest'):
        self.channel = channel
        self.start_time = start_time
        self.end_time = end_time
        self.node = node
        geturl = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node='\
                       + self.node + '/start='+ self.start_time + '/end='+ self.end_time + '+' + self.channel
        self.r = requests.get(geturl, prefetch=False)
        print "\tQuery to", self.channel, "successful"
        # print "HTTP get status: ", r.status_code
        # print "HTTP error? ", r.raise_for_status()
        
    def parse_query(self):
        print "\tParsing returned content..."
        data_list = []
        for element in self.r.iter_lines():
            data_split = element.split('   ')
            datetime_el = dt.datetime.strptime(data_split[0], '%d-%b-%Y %H:%M:%S.%f')
            value_el = float(data_split[1].strip())
            data_list.append([datetime_el, value_el])
        self.data_array = np.array(data_list)
        print "\tNumber of returned time-value pairs:", self.data_array.shape[0]
        return self.data_array

def plot_response(data_array):
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(data_array[0], data_array[1])
    fig.autofmt_xdate()
    hfmt = mdates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(hfmt)
    # set the format of dates in the toolbar
    ax.fmt_xdata = mdates.DateFormatter('%y-%m-%dT%H:%M:%S')
    plt.show()
    
if __name__ == '__main__':

    query1 = P2ACNET('E:TCIP', '13-OCT-2012-12:30', '14-OCT-2012-12:35')
    result = query1.parse_query()
    print "data_array[0][0] = ", result[0][0]
    print "data_array[0][1] = ", result[0][1]
    print "data_array shape = ", result.shape
