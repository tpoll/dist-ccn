import time
import socket
import ccnlite.ndn2013 as ndn
import ccnlite.util as util
import sys
from locust import Locust, events, task, TaskSet


class NdnUdpClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(2)

    #Ndn content string and (ip, port) 
    def get(self, req, host):
        try:
            start_time = time.time()
            self.socket.sendto(req, host)
            data, addr = self.socket.recvfrom(1000)
        except socket.timeout, e:
            total_time = float((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="udp", name="content", response_time=total_time, exception=e)
        else:
            total_time = float((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="udp", name="content", response_time=total_time, response_length=len(data))


class NdnUdpLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(NdnUdpLocust, self).__init__(*args, **kwargs)
        self.client = NdnUdpClient()


class ApiUser(NdnUdpLocust):
    min_wait = 50
    max_wait = 2000
    print dir(NdnUdpLocust)

    class task_set(TaskSet):
        @task
        def get_content(self):
            req = ndn.mkInterest(['ndn', 'test', 'mycontent1'])
            self.client.get(req, (sys.argv[1].split("=")[1], 9980))