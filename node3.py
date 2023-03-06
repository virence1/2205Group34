from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/endpoint3",methods=['POST'])
def receive_message():
	data = request.get_json()
	return'Node3 received message >>> ' + str(data)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
