import requests
import time
import random

DOWN_INTERVAL = 10
ITERATIONS = 10
REDIS_IP = "blah"
TARGET_PORT = 9980


def main():
    nodes = ["127.0.0.1"] # Ip addresses of target node group as strings
    set_size = len(nodes)

    startAllNodes(nodes)

    killNodesOrdered(nodes, set_size)


    stopAllNodes(nodes)

def killRandomNode(nodes, set_size):
    '''Given a list[string]: nodes, int: set_size kills, a random node
    and then starts for the global number of iterations and down time.'''
    for x in xrange(0,ITERATIONS):
        ip = random.randint(0, set_size -1)
        sendRequest(nodes[ip], 'stop')        
        time.sleep(DOWN_INTERVAL)
        sendRequest(nodes[ip], 'start')

def killNodesOrdered(nodes, set_size):
    '''Given a list[string]: nodes, int: set_size, kills and the restarts to nodes in order
    for the global number of iterations and down time.'''
    for x in xrange(0,ITERATIONS):
        ip = x % set_size
        sendRequest(nodes[ip], 'stop')        
        time.sleep(DOWN_INTERVAL)
        sendRequest(nodes[ip], 'start')



def startAllNodes(nodes):
    '''Given a list[string]: nodes, starts all the target ip addresses'''
    print timePrint("Starting all nodes")
    for node in nodes:
        sendRequest(node, 'start')
    time.sleep(3)


def stopAllNodes(nodes):
    '''Given a list[string]: nodes, stops all the target ip addresses'''
    time.sleep(3)
    print timePrint("Stopping all nodes")
    for node in nodes:
        sendRequest(node, 'stop')


def sendRequest(ip_addr, action):
    ''' Takes string: ip_addr, string: action, sends request to the given IP
    to do the given action. action can be 'start' or 'stop' '''
    args = {
            "id" : "1",
            "dist" : True,
            "debug" : False,
            "local_cache": False,
            "redis_ip": REDIS_IP
        }
    try:
        r = requests.post("http://" + ip_addr + ":8000/" + action, data = args)
        if r.status_code == requests.codes.ok:
            timePrint(" %s request to node %s with arguments %s" % (action, ip_addr, args))
        else:
            timePrint("FAILED: request to node %s with arguments %s, CODE: %s" % (action, ip_addr, args, r.status_code))
    except Exception, e:
        timePrint("Raised %s" % (e))






def timePrint(message):
    '''Takes a string: message, prepends a timestamp to the message and then prints '''
    print "[%s]-- %s" % (time.asctime(), message)



if __name__ == '__main__':
    main()