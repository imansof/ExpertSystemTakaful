from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Here you can add real authentication logic

        return redirect(url_for('package'))  # ✅ Redirect after login
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/package')
def package():
    return render_template('package.html')

@app.route('/agent')
def agent():
    return render_template('agent.html')

@app.route('/all-packages')
def all_packages():
    return render_template('all-packages.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/support')
def support():
    return render_template('support.html')


if __name__ == '__main__':
    app.run(debug=True)
