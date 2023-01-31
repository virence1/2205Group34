from flask import *
app = Flask(__name__,)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/about")
def about():
  return render_template('about.html')

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=80, debug=False)
