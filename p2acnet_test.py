
import numpy as np
from datetime import datetime

class P2ACNETTester(object):
    
    def __init__(self, p2acnet_version_list, query_array):
        self.p2acnet_version_list = p2acnet_version_list
        if len(query_array.shape) < 2:
            self.query_array = np.array([query_array])
        else:
            self.query_array = query_array

    def runtests(self):
        for element in self.p2acnet_version_list:
            for x in self.query_array:
                test_instance = _P2ACNETTest(element, x)
                test_instance.test()
        return

class _P2ACNETTest(object):

    def __init__(self, p2acnet_version, query):
        self.p2acnet_version = p2acnet_version
        self.query = query
        
    def test(self):
        print "Begin test with", self.p2acnet_version, "class..."
        tstart = datetime.now()
        query = self.p2acnet_version.P2ACNET(query_array[0], query_array[1], query_array[2])  # Could use a list comprehension here?
        result = query.parse_query()
        tend = datetime.now()
        dt = tend - tstart
        print "Time Spent:", dt
        return

    def __str__(self):
        '''Return a more readable representation'''
        return "%a Test" % (self.p2acnet_version)

if __name__ == '__main__':
    import p2acnet, p2acnet2
    p2acnet_version_list = [p2acnet, p2acnet2]
    query_array = np.array(['E:HTC06', '10-SEP-2012-12:30', '14-OCT-2012-12:30'])
    result = P2ACNETTester(p2acnet_version_list, query_array)
    result.runtests()
