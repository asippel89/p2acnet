
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict

class P2ACNET(object):
    '''
    This class acts like a factory, creating instances of the P2ACNETSingle class for each channel in channel_list. It creates
    a dictionary of channel:instance pairs, which are used by plot_group and get_group_data.
    '''

    def __init__(self, channel_list, start_time, end_time):
        if type(channel_list) == str:
            self.channel_list = [channel_list]
        else:
            self.channel_list = channel_list
        self.start_time = start_time
        self.end_time = end_time
        
    def run_group(self):
        '''
        This method creates instances of the P2ACNETSingle class for each channel in the list and places them in a dictionary.
        One can access the P2ACNETSingle class methods for each channel by looping over the dictionary.
        '''
        instance_dict = {}
        for channel in self.channel_list:
            new_instance = P2ACNETSingle(channel, self.start_time, self.end_time)
            instance_dict[channel] = new_instance
        return instance_dict

    def plot_group(self, title=""):
        '''
        This method iterates over the instance_dict, calling the plot_single method of the P2ACNETSingle class for each instance
        of that class in the dictionary (basically each channel). The resulting plot has automatically scaled dates as well
        as a legend which shows the channels. This method has logic to make new subplots based on the units of each channel 
        that have been queried. This is done by creating a dictionary of Units:Channel_list pairs and looping over the
        distinct units. A title string can be supplied.
        '''
        instance_dict = self.run_group()
        #-------------Decide How Many Subplots Based on Units--------------------#
        units_dict = defaultdict(list)
        for (channel, instance) in instance_dict.items():
            units_dict[instance.get_info()[1]].append(channel)
        num_units = len(units_dict)
        #---------------------Make subplot for each unit-------------------------#        
        fig = plt.figure()
        for index, key in enumerate(units_dict):
            ax = fig.add_subplot(num_units, 1, index + 1)
            for channel in units_dict[key]:
                instance_dict[channel].plot_single(ax = ax)
                plt.ylabel(key)
            if index == 0:
                plt.title(title)
            plt.legend(loc='lower left').get_frame().set_alpha(.5)
        #-------------------------X Axis Label and Format------------------------#
        ax.autoscale_view()
        fig.autofmt_xdate()        
        xlabel = str("T1 ="+ self.start_time+ "      T2 ="+ self.end_time)
        plt.xlabel(xlabel)
        plt.show()
        return fig

    def get_group_data(self):
        '''
        This method returns a dictionary whose keys are channel names and values are data arrays of time/value
        pairs.
        '''
        instance_dict = self.run_group()
        data_dict = {}
        for channel in instance_dict:
            data_dict[channel] = instance_dict[channel].get_data()
        return data_dict
            
class P2ACNETSingle(object):
    '''
    This class describes the content of a single channel query to Fermilab's ACNET. It accesses a time series
    from one of ACNET's data loggers by making an HTTP get request. The contents of the HTTP request is a short
    script written in Fermi's ACL scripting language (more information can be found here:
    http://www-ad.fnal.gov/help/ul_clib/intro_acl.html)
    Using this class, one can retrieve and perform operations on this channel data from within python, without
    having to copy/paste or directly interact with ACNET's strange interface.
    '''

    def __init__(self, channel, start_time, end_time, node = 'fastest'):
        '''
        This method initializes important instance variables and sends the HTTP request to ACNET. Future versions
        will include more advanced error handling.
        '''
        self.channel = channel
        self.start_time = start_time
        self.end_time = end_time
        self.node = node
        self._send_query()

    def _send_query(self):
        #------------First send info request--------------------------#
        print "\t" + self.channel
        print "\t" + "=" * 50
        info_url = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=show+' + self.channel + '/text/units/FTD'
        info_query = requests.get(info_url)
        info_content = info_query.content.splitlines()
        self.channel_desc = info_content[0][21:].strip()
        self.units = info_content[1][21:].strip()
        self.freq = info_content[2][25:32].strip()
        print "\t\t" + "Description: " + self.channel_desc
        print "\t\t" + "Unit: " + self.units
        print "\t\t" + "Frequency: " + self.freq
        #------------Then send data request---------------------------#
        get_url = 'http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node=' \
            + self.node + '/start=' + self.start_time + '/end='+ self.end_time + '+' + self.channel
        self.r = requests.get(get_url)
        # print "\t\tHTTP get status: ", self.r.status_code
        # Uncomment to test HTTP error handling
        # if int(self.r.status_code) != 200:
        #     print "ERROR: There was a problem with accessing ACNET via HTTP"
        #     print "See response error message:", self.r.raise_for_status() # Not sure if this is correct
        #     raise SOME_ERROR # Need to figure out how to define this error, what to do afterwards
        print "\t\tHTTP data response content length:", len(self.r.content)
        # print "HTTP error? ", r.raise_for_status()
        self._parse_query()
        
    def _parse_query(self):
        '''
        This method uses the iter_lines() requests method to iterate over each line of the returned content
        (instead of loading the whole response into memory and then performing operations on it). It returns
        an array of the time-value pairs for the requested channel, where the times are date-time objects.
        '''
        data_list = []
        for element in self.r.iter_lines():
            single_datetime = element[:24]
            single_value = element[25:]
            datetime_el = mdates.date2num(dt.datetime.strptime(single_datetime, '%d-%b-%Y %H:%M:%S.%f'))
            value_el = float(single_value.strip())
            data_list.append([datetime_el, value_el])
        self.data_array = np.array(data_list)
        print "\t\tNumber of returned time-value pairs:", self.data_array.shape[0]
        print ""
        return self.data_array

    def get_data(self):
        '''
        Simply returns the data. Mainly used by get_group_data in the P2ACNETGroup class.
        '''
        return self.data_array

    def get_info(self):
        info_array = np.array([self.channel_desc, self.units, self.freq])
        return info_array

    def plot_single(self, ax=None):
        '''
        This method plots the data for a data_array with automatic matplotlib formatting for the dates
        on the x-axis. The ax option is used in the P2ACNETGroup class to combine the plots for several
        channels.
        '''
        if ax is None:            
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.autoscale_view()
            fig.autofmt_xdate()
        times = self.data_array[:,0]
        values = self.data_array[:,1]
        ax.plot_date(times, values, '-', label=self.channel)
        return
    
if __name__ == '__main__':
    #-------------Test multiple channels using P2ACNETGroup-----------#
    TIFO_list = ['E:TCIP', 'E:TNIP0', 'E:TNIP1', 'E:TNESIP', 'E:TEIP0', 'E:TEIP1', 'E:TEESIP']
    LIFO_list = ['E:LCIP', 'E:LNIP0', 'E:LNIP1', 'E:LNESIP', 'E:LEIP0', 'E:LEIP1', 'E:LEESIP']
    Temp_env = ['G:OUTTMP', 'G:WCHILL', 'G:HEATIX', 'G:DEWPNT']
    units_test_list = ['E:TCIP', 'E:TNIP0', 'E:TNIP1', 'E:TNESIP', 'E:TEIP0', 'E:TEIP1', 'E:TEESIP', 'G:OUTTMP', 'G:WCHILL']
    other_channel_test = ['E:HADC02', 'E:HADC03', 'E:HADC01']
    single_channel = 'E:TCIP'
    start_time = '24-OCT-2012-17:30'
    end_time = '28-OCT-2012-22:00'
    query = P2ACNET(single_channel, start_time, end_time)
    plot = query.plot_group('T IFO Since Being Connected to ACNET')
    # data = query.get_group_data()
    
    #------Test single plot-----------#
    # channel = 'E:HTC05'
    # start_time = '10-OCT-2012-12:30'
    # end_time = '17-OCT-2012-14:30'
    # instance = P2ACNETSingle(channel, start_time, end_time)
    # plot = instance.plot_single()
    # plt.show()
