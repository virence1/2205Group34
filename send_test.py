import requests

def sendToServer():
	url = "http://20.185.31.43/endpoint3"
	data = {'vote': 'Asmarina Luwam', 'user': 'X2398754Y', 'combo': 'ZBPGW', 'nextNode': 'W', 'remainingPath': 'GW', 'prevNode': 'P'}
	response = requests.post(url, json=data)

	if response.status_code == 200:
		print(response.text)
		print('Message sent successfully >>> '+ str(data))
		print('Message server reply >>> ' + response.text)
	else:
		print('Error sending message: {}'.format(response.text))
	return

sendToServer()
