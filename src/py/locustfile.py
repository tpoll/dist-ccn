import time
import socket
import ccnlite.ndn2013 as ndn
import ccnlite.util as util
import sys
from itertools import cycle
from locust import Locust, events, task, TaskSet


class NdnUdpClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(2.5)

    #Ndn content string and (ip, port) 
    def get(self, req, host):
        try:
            start_time = time.time()
            self.socket.sendto(req, host)
            data, addr = self.socket.recvfrom(1000)
        except Exception, e:
            total_time = float((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="udp", name="content", response_time=total_time, exception=e)
        else:
            total_time = float((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="udp", name="content", response_time=total_time, response_length=len(data))


class NdnUdpLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(Locust, self).__init__(*args, **kwargs)
        self.client = NdnUdpClient()

content_names = cycle([['ndn', 'test', "mycontent" + str(x)] for x in xrange(1,51)])

class ApiUser(NdnUdpLocust):
    min_wait = 50
    max_wait = 2000


    class task_set(TaskSet):
        @task
        def get_content(self):
            req = ndn.mkInterest(content_names.next())
            self.client.get(req, (sys.argv[1].split("=")[1], 9980))


