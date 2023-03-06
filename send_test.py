import requests

def sendToServer():
    url = "http://20.81.124.56/endpointDestination"
    data ={'message':'wtflolol'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Message sent successfully >>> ' + str(data))
        print('Message server reply >>> ' + response.text)
    else:
        print('Error sending message: {}'.format(response.text))
    
    return

sendToServer()
