from flask import *
import pymysql
import secrets

app = Flask(__name__,)

# Connect to the MariaDB database
conn = pymysql.connect(host="localhost", user="root", password="", database="user_accounts")

# Set a secret key for the Flask session
app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
  # If the user is already logged in, redirect to the home page
  if "username" in session:
    return redirect(url_for("home"))
  return render_template('index.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
  if "username" in session:
    return redirect(url_for("home"))
  return render_template('login.php')

@app.route('/logout')
def logout():
  if "username" in session:
    session.clear()
    return redirect(url_for('index'))
  return redirect(url_for('index'))

@app.route("/authenticate", methods=['POST'])
def authenticate():
  conn_new = pymysql.connect(host="localhost", user="root", password="", database="user_accounts")
  username = request.form["username"]
  password = request.form["password"]
  cursor = conn_new.cursor()
  cursor.execute("SELECT * FROM account WHERE username=%s AND password=%s", (username, password))
  result = cursor.fetchone()
  cursor.close()
  conn_new.close()

  if result:
    # If the credentials exist, store the user's information in the session and return "success"
    session["username"] = username
    return redirect(url_for("home"))   
  else:
    return "Error: Invalid username or password", 400

@app.route("/home")
def home():
    # If the user is not logged in, redirect to the login page
    if "username" not in session:
      return redirect(url_for("index"))

    # Otherwise, return a greeting
    #return "Hello, {}! You are logged in, to go back to the original homepage design just delete the cookie! This home page will have voting buttons upon login".format(session["username"])
    return render_template('home.html')

@app.route('/vote',methods=['POST'])
def vote():
  data=request.get_json()
  print(data)
  return 'OK'


@app.route("/confirmation")
def confirmation():
  if "username" not in session:
    return redirect(url_for("index"))
  
  return(render_template('confirmation.html'))



if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
