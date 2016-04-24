import requests
import time
import random
import json

DOWN_INTERVAL = 45
ITERATIONS = 8
REDIS_IP = "104.41.158.210"
DATA_NODE_IP = "13.92.195.16"
TARGET_PORT = 9980




def main():

    args = {
    "id" : "1",
    "dist" : True,
    "debug" : True,
    "local_cache": False,
    "redis_ip": REDIS_IP
    }
    nodes = ["40.114.2.34", "40.76.29.216", "40.76.58.113"] # Ip addresses of target node group as strings
    set_size = len(nodes)

    print "Testing %d nodes with %d iterations down each for %d" % (set_size, ITERATIONS, DOWN_INTERVAL)


    startAllNodes(nodes, args)

    killNodesOrdered(nodes, set_size, args)


    stopAllNodes(nodes, args)

def killRandomNode(nodes, set_size, args):
    '''Given a list[string]: nodes, int: set_size kills, a random node
    and then starts for the global number of iterations and down time.'''
    for x in xrange(0,ITERATIONS):
        ip = random.randint(0, set_size -1)
        sendRequest(nodes[ip], 'stop', args)        
        time.sleep(DOWN_INTERVAL)
        sendRequest(nodes[ip], 'start', args)

def killNodesOrdered(nodes, set_size, args):
    '''Given a list[string]: nodes, int: set_size, kills and the restarts to nodes in order
    for the global number of iterations and down time.'''
    for x in xrange(0,ITERATIONS):
        ip = x % set_size
        sendRequest(nodes[ip], 'stop', args)        
        time.sleep(DOWN_INTERVAL)
        sendRequest(nodes[ip], 'start', args)



def startAllNodes(nodes, args):
    '''Given a list[string]: nodes, starts all the target ip addresses'''
    print timePrint("Starting all nodes")
    for node in nodes:
        sendRequest(node, 'start', args)
        registerDataNode(node)

    time.sleep(20)


def stopAllNodes(nodes, args):
    '''Given a list[string]: nodes, stops all the target ip addresses'''
    time.sleep(3)
    print timePrint("Stopping all nodes")
    for node in nodes:
        sendRequest(node, 'stop', args)


def sendRequest(ip_addr, action, args):
    headers = {'content-type': 'application/json'}
    ''' Takes string: ip_addr, string: action, sends request to the given IP
    to do the given action. action can be 'start' or 'stop' '''

    try:
        r = requests.post("http://" + ip_addr + ":8000/" + action, data=json.dumps(args), headers=headers)
        if r.status_code == requests.codes.ok:
            timePrint(" %s request to node %s with arguments %s" % (action, ip_addr, args))
        else:
            timePrint("FAILED: request to node %s with arguments %s, CODE: %s" % (action, ip_addr, args, r.status_code))
    except Exception, e:
        timePrint("Raised %s" % (e))


def registerDataNode(ip_addr):
    headers = {'content-type': 'application/json'}
    args = {
        "target_ip": DATA_NODE_IP,
        "prefix": "/ndn"
    }

    try:
        r = requests.post("http://" + ip_addr + ":8000/" + "face", data=json.dumps(args), headers=headers)
        if r.status_code == requests.codes.ok:
            timePrint(" %s request to node %s with arguments %s" % ("face", ip_addr, args))
        else:
            timePrint("FAILED: request to node %s with arguments %s, CODE: %s" % ("face", ip_addr, args, r.status_code))
    except Exception, e:
        timePrint("Raised %s" % (e))






def timePrint(message):
    '''Takes a string: message, prepends a timestamp to the message and then prints '''
    print "[%s]-- %s" % (time.asctime(), message)



if __name__ == '__main__':
    main()