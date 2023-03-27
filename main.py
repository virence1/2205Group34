from flask import *
import pymysql
import secrets
from vault import *
import subprocess as sp
from flask import session
app = Flask(__name__ ,)

# Connect to the MariaDB database
# conn = pymysql.connect(host="localhost", user="root", password="", database="user_accounts")

# Set a secret key for the Flask session
app.secret_key = "helloworld"

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
  conn_new = pymysql.connect(host="localhost", user="dddadmin", password="Securepassword123", database="user_accounts")
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
    with open("sessionUser.json", "w") as user_file:
      json.dump(session, user_file)
    return redirect(url_for("home"))   
  else:
    return "Error: Invalid username or password", 400

@app.route("/home", methods=['get'])
def home():
    if "username" not in session:
      return redirect(url_for("index"))
    username=session.get('username')
    # Otherwise, return a greeting
    #return render_template('home.html', username=session["username"])
    out = sp.run(["/usr/bin/php", "templates/home.php", username], stdout=sp.PIPE)
    return out.stdout  

@app.route("/alreadyVoted")
def alreadyVoted():
  if "username" not in session:
    return redirect(url_for("index"))
  
  out = sp.run(["/usr/bin/php", "templates/alreadyVoted.php"], stdout=sp.PIPE)
  return out.stdout


@app.route('/vote', methods=['post', 'get'])
def vote():
  if "username" not in session:
    return redirect(url_for("index"))
  
  # Check if user has already voted
  vote_value = request.form["vote_value"]
  account_username = request.form["account_username"]

  db = pymysql.connect(host="localhost", user="dddadmin", password="Securepassword123", database="user_accounts")
  cursor = db.cursor()
  cursor.execute("SELECT voteStatus FROM account WHERE username = %s", (account_username,))
  result = cursor.fetchone()
  
  if result and result[0] == 1:
    return redirect(url_for("alreadyVoted"))
  else:
    out = sp.run(["/usr/bin/php", "templates/vote.php", vote_value, account_username], stdout=sp.PIPE)
    return out.stdout 


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
