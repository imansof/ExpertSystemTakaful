from flask import Flask, render_template, request, redirect, url_for, session
from Takaful import signup as takaful_signup, login as takaful_login, get_recommendations

app = Flask(__name__)
# Set your SECRET_KEY here:
app.config['SECRET_KEY'] = 'surematchisthebest'
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if takaful_login(email, password): # Use the login function from Takaful.py
            session['username'] = email # Store username in session
            return redirect(url_for('start')) # Redirect to start after login
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password'] # Added for frontend validation

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        result_message = takaful_signup(username, password) # Use the signup function from Takaful.py

        if "successful" in result_message:
            session['username'] = username # Store username in session upon successful signup
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=result_message)
    return render_template('register.html')

@app.route('/start')
def start():
    if 'username' not in session:
        return redirect(url_for('login')) # Redirect to login if not authenticated
    return render_template('start.html')

@app.route('/package', methods=['GET', 'POST']) # Allow POST for questionnaire submission
def package():
    if 'username' not in session:
        return redirect(url_for('login')) # Redirect if not logged in

    if request.method == 'POST':
        # Get data from form (from package.html)
        age = int(request.form['age'])
        income = int(request.form['income'])
        marital_status = request.form['marital_status'].lower()
        has_dependents = request.form['has_dependents'].lower() == 'yes'
        goal = request.form['goal'].lower()

        username = session['username'] # Get username from session

        recommended_plans = get_recommendations(username, age, income, marital_status, has_dependents, goal)
        # Pass recommendations to the template
        return render_template('package.html', recommendations=recommended_plans)

    # For GET requests (initial load of the page or after login)
    return render_template('package.html', recommendations=None) # Pass None initially


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
