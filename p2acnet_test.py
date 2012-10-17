
from datetime import datetime

class P2ACNETTester(object):
    
    def __init__(self, p2acnet_version_list, query_list):
        for element in p2acnet_version_list:
            self.test(element, query_list)

    def test(self, p2acnet_version, query_list):
        print "Begin test with", p2acnet_version, "class..."
        tstart = datetime.now()
        query = p2acnet_version.P2ACNET(query_list[0], query_list[1], query_list[2])  # Could use a list comprehension here?
        result = query.parse_query()
        tend = datetime.now()
        dt = tend - tstart
        print "Time Spent:", dt
        return

if __name__ == '__main__':
    import p2acnet, p2acnet2
    p2acnet_version_list = [p2acnet, p2acnet2]
    query_list = ['E:HTC06', '10-JUN-2012-12:30', '14-OCT-2012-12:30']
    result = P2ACNETTester(p2acnet_version_list, query_list)
