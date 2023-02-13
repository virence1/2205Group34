from flask import *
import pymysql

app = Flask(__name__,)

# Connect to the MariaDB database
conn = pymysql.connect(host="localhost", user="root", password="", database="user_accounts")

# Set a secret key for the Flask session
app.secret_key = "secret_key"

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

@app.route("/authenticate", methods=['POST'])
def authenticate():
  username = request.form["username"]
  password = request.form["password"]
  
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM account WHERE username=%s AND password=%s", (username, password))
  result = cursor.fetchone()
  cursor.close()
  conn.close()

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

@app.route("/confirmation")
def confirmation():
  if "username" not in session:
    return redirect(url_for("index"))
  
  return(render_template('confirmation.html'))

#@app.route('/config')
#def config():
#  referer = request.headers.get('Referer')
#  if referer == "http://127.0.0.1:8080/authenticate":
#    result=subprocess.run(["php", "config.php"], capture_output=True, text=True).stdout
#    return result
 # else:
 #   return "Access Denied"


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=False)
