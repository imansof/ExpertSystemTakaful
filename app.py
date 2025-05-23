from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    # this will connect to your expert system logic later
    return "This is where your questionnaire will begin!"

if __name__ == '__main__':
    app.run(debug=True)
