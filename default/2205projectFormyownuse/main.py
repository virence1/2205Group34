from flask import Flask, render_template, request

app = Flask(__name__)

vote_count = {'a': 0, 'b': 0, 'c': 0}

@app.route('/')
def index():
    return render_template('index.html', vote_count=vote_count)

@app.route('/vote', methods=['POST'])
def vote():
    vote = request.form['vote']
    vote_count[vote] += 1
    return render_template('index.html', vote_count=vote_count)

if __name__ == '__main__':
    app.run(debug=True)