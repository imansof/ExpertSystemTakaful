from flask import Flask, render_template, request, redirect, url_for, session
from Takaful import signup as takaful_signup, login as takaful_login, get_recommendations
from Takaful import PLAN_SIGNATURES

app = Flask(__name__)
# Set your SECRET_KEY here:
app.config['SECRET_KEY'] = 'surematchisthebest'

# Utility to build human-readable goal labels
#def build_goal_choices():
#    return { key: key.replace('_', ' ').title() for key in PLAN_SIGNATURES.keys() }

def build_goal_choices():
    """
    Build a dict of all possible goal‑keys → human labels
    derived from every plan’s goals, benefits, and riders.
    """
    choices = {}
    # PLAN_SIGNATURES maps each plan_name to its set of normalized tokens
    for sig_set in PLAN_SIGNATURES.values():
        for key in sig_set:
            # e.g. "cancer_protector" → "Cancer Protector"
            label = key.replace('_', ' ').title()
            choices[key] = label
    # Sort by label so your UI is consistent
    return dict(sorted(choices.items(), key=lambda item: item[1]))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if takaful_login(email, password):
            session['username'] = email
            return redirect(url_for('start'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        result_message = takaful_signup(username, password)
        if "successful" in result_message:
            session['username'] = username
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=result_message)
    return render_template('register.html')

@app.route('/start')
def start():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('start.html')

@app.route('/package', methods=['GET', 'POST'])
def package():
    if 'username' not in session:
        return redirect(url_for('login'))

    goals_choices = build_goal_choices()
    selected_goals = []
    recommended = None

    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        gender = request.form['gender']
        marital_status = request.form['marital_status'].lower()
        has_dependents = request.form['has_dependents'].lower() == 'yes'
        selected_goals = request.form.getlist('goals')

        username = session['username']
        result = get_recommendations(
            username=username,
            age=age,
            income=income,
            gender=gender,
            marital_status=marital_status,
            has_dependents=has_dependents,
            goals=selected_goals
        )
        #recommended = result.get('plans', [])

        # result["plans"] is now a list of tuples
        return render_template(
            'Recommend_Page.html',
            recommendations=result["plans"],
            goals_choices=goals_choices,
            selected_goals=selected_goals
        )

    return render_template(
        'package.html',
        goals_choices=goals_choices,
        selected_goals=selected_goals,
        recommendations=None
    )


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

@app.route('/details/<plan_name>')
def show_plan_details(plan_name):
    from knowledge_base import plans
    if plan_name not in plans:
        return "Plan not found", 404
    return render_template('package_details.html', plan_name=plan_name, plan=plans[plan_name])

if __name__ == '__main__':
    app.run(debug=True)
