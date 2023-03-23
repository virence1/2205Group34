from flask import Flask , request
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

# Functions

def sendToNode1(message)

def sendToNode3(message)

def sendToDestination(message)


@app.route("/endpoint2",methods=['POST'])
def receive_message():
        message=request.get_json()
        return "<h1>Hello world</h1>"

def aes_encrypt(payload)
# Throw in your vault code here

if __name__ == "__main__":
    app.run(host='0.0.0.0')
