
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class P2ACNETGroup(object):

    def __init__(self, channel_list, start_time, end_time):
        self.channel_list = channel_list
        self.start_time = start_time
        self.end_time = end_time
            
    def run_group(self):
        data_dict = {}
        for channel in self.channel_list:
            new_instance = P2ACNET(channel, self.start_time, self.end_time)
            data_dict[channel] = new_instance.parse_query()
        return data_dict

class P2ACNET(object):
    ''' This class responds to the full http query content and does splitlines() on it,
        then goes through with the parsing.'''
    def __init__(self, channel, start_time, end_time, node = 'fastest'):
        self.channel = channel
        self.start_time = start_time
        self.end_time = end_time
        self.node = node

        r = requests.get('http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node='\
                             + self.node + '/start='+ self.start_time + '/end='+ self.end_time + '+' + self.channel)
        self.raw = r.content.splitlines()
        print "\tQuery to", self.channel, "successful"
        # print "HTTP get status: ", r.status_code
        # print "HTTP error? ", r.raise_for_status()
        
    def parse_query(self):
        print "\tParsing returned content..."
        data_list = []
        for element in self.raw:
            data_split = element.split('   ')
            datetime_el = dt.datetime.strptime(data_split[0], '%d-%b-%Y %H:%M:%S.%f')
            value_el = float(data_split[1].strip())
            data_list.append([datetime_el, value_el])
        self.data_array = np.array(data_list)
        self.delta_t = self.data_array[1][0] - self.data_array[0][0]
        print "\tNumber of returned time-value pairs:", self.data_array.shape[0]
        return self.data_array

def plot_response(data_array):
    delta_t = mdates.relativedelta(data_array[1][0], data_array[0][0])
    # print "Time scale =", dt
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot_date(data_array[0], data_array[1])
    fig.autofmt_xdate()
    hfmt = mdates.AutoDateFormatter()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(hfmt)
    # set the format of dates in the toolbar
    ax.fmt_xdata = mdates.DateFormatter('%y-%m-%dT%H:%M:%S')
    plt.show()
    
if __name__ == '__main__':
    
    channel_list = ['E:TCIP', 'E:TNIP1', 'E:TNIP0']
    query1 = P2ACNETGroup(channel_list, '17-OCT-2012-12:30', '17-OCT-2012-14:30')
    result = query1.run_group()
    # print "data_array[0][0] = ", result[0][0]
    # print "data_array[0][1] = ", result[0][1]
    # print "data_array shape = ", result.shape
    
