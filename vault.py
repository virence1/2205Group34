import requests

def connect():
    return

def generate():
    return


def store():
    return


def sendToServer():
    url = "http://20.81.121.55/endpoint"
    data ={'message':'Hello, world!'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.text)
        print('Message sent successfully')
    else:
        print('Error sending message: {}'.format(response.text))
    
    return

sendToServer()