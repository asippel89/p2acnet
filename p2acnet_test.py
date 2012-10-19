
import numpy as np
from datetime import datetime

class _P2ACNETTest(object):

    def __init__(self, p2acnet_version_list, channel_list, start_time, end_time):
        self.channel_list = channel_list
        self.start_time = start_time
        self.end_time = end_time
        for p2acnet_version in p2acnet_version_list:
            self.test(p2acnet_version)
        
    def test(self, p2acnet_version):
        print "Begin test with", p2acnet_version, "class..."
        tstart = datetime.now()
        query = p2acnet_version.P2ACNETGroup(self.channel_list, self.start_time, self.end_time)
        result = query.run_group()
        tend = datetime.now()
        dt = tend - tstart
        print "Time Spent:", dt
        return

if __name__ == '__main__':
    import p2acnet, p2acnet2
    p2acnet_version_list = [p2acnet, p2acnet2]
    channel_list = ['E:TCIP', 'E:TNIP1', 'E:HADC02']
    start_time = '14-OCT-2012-12:30'
    end_time = '17-OCT-2012-14:30'
    result = _P2ACNETTest(p2acnet_version_list, channel_list, start_time, end_time)

