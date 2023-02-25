import requests
import random

def connect():
    return

def generate():
    return


def store():
    return

def generatePath():
    nodes=[1,2,3]
    pathToDest = random.sample(nodes,len(nodes))
    sendData(tuple(pathToDest))
    for n in pathToDest:
        print(n)
    
def sendData(order):
    mapping = {
        (1,2,3) : sendToNode1,
        (1,3,2) : sendToNode1,
        (2,1,3) : sendToNode2,
        (2,3,1) : sendToNode2,
        (3,1,2) : sendToNode3,
        (3,2,1) : sendToNode3
    }
    function = mapping.get(order)
    if function is not None:
        function()
    else:
        print(f"Invalid order: {order}")
    

def sendToNode2():
    print("Node 2 Function invoked.")
    pass

def sendToNode3():
    print("Node 3 Function invoked.")
    pass

def sendToNode1():
    print("Node 1 Function invoked.")
    url = "http://20.81.121.55/endpoint"
    data ={'vote':'Person A', 'nextNode' : 'xxx', 'remainingPath' : 'xxxx'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.text)
        print('Message sent successfully')
    else:
        print('Error sending message: {}'.format(response.text))
    
    return


generatePath()
