from flask import Flask, render_template, request, redirect, url_for, session
from Takaful import signup as takaful_signup, login as takaful_login, get_recommendations
from Takaful import PLAN_SIGNATURES
from knowledge_base import plans, BENEFIT_TO_GOALS, RIDER_TO_GOALS
import os

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
    #recommended = None

    if request.method == 'POST':
        # 1. Gather inputs
        age = int(request.form['age'])
        is_child = age < 19
        income = int(request.form['income'])
        gender = request.form['gender']
        marital_status = request.form['marital_status'].lower()
        has_dependents = request.form['has_dependents'].lower() == 'yes'
        coverage_pref = request.form['coverage_preference']
        selected_goals = request.form.getlist('goals')
        # Only allow the Education goal for children
        if 'education' in selected_goals and not is_child:
            selected_goals.remove('education')

        # 2. Get raw scores ([(plan_name, match_count), ...])
        username = session['username']
        result = get_recommendations(
            username=username,
            age=age,
            income=income,
            gender=gender,
            marital_status=marital_status,
            has_dependents=has_dependents,
            coverage_pref=coverage_pref,
            goals=selected_goals
        )
        scored = result['plans']
        #recommended = result.get('plans', [])
        TOP_N = 2
        recommendations = []
        count = 0

        for plan_name, _ in scored:
            plan = plans[plan_name]
            # 1) skip non‑child plans if child
            if age < 19 and not getattr(plan, "child_friendly", False):
                continue

            # 2) build direct_map
            direct_map = {}
            for benefit in plan.benefits:
                for goal_key in BENEFIT_TO_GOALS.get(benefit, []):
                    if goal_key in selected_goals:
                        if goal_key == 'education':
                            er = plan.education_age_range or (0, 0)
                            if not (er[0] <= age <= er[1]):
                                continue
                        direct_map.setdefault(goal_key, []).append(benefit)

            # 3) build indirect_map
            indirect_map = {}
            for rider in plan.riders:
                for goal_key in RIDER_TO_GOALS.get(rider, []):
                    if goal_key in selected_goals:
                        indirect_map.setdefault(goal_key, []).append(rider)

            # Match preferred coverage
            coverage_match = False
            if coverage_pref:
                # reuse exactly the same logic you used when filtering in get_recommendations()
                yrs = plan.coverage_term_years
                until = plan.coverage_until_ages
                if coverage_pref == 'short':
                    if any(y <= 10 for y in yrs) or any(a < 60 for a in until):
                        coverage_match = True
                elif coverage_pref == 'medium':
                    if any(15 <= y <= 20 for y in yrs) or any(65 <= a <= 75 for a in until):
                        coverage_match = True
                elif coverage_pref == 'long':
                    if any(y >= 25 for y in yrs) or any(a >= 80 for a in until):
                        coverage_match = True

            # did we bump this plan because of family / dependents?
            family_boost = False
            if (marital_status == "married" or has_dependents) and (
                    "family_protection" in set(plan.direct_goals + plan.indirect_goals)
            ):
                family_boost = True

            # 4) append a single dict per plan
            recommendations.append({
                'name': plan_name,
                'direct_map': direct_map,
                'indirect_map': indirect_map,
                'coverage_match': coverage_match,
                'family_boost': family_boost
            })

            count += 1
            if count >= TOP_N:
                break

        return render_template(
            'Recommend_Page.html',
            recommendations=recommendations,
            goals_choices=goals_choices,
            selected_goals=selected_goals,
            plans=plans,
            age=age,
            coverage_pref=coverage_pref,
            marital_status=marital_status,
            has_dependents=has_dependents
        )
    # GET: just show form
    return render_template(
        'package.html',
        goals_choices=goals_choices,
        selected_goals=selected_goals,
        recommendations=None
    )


@app.route('/agent')
def agent():
    return render_template('agent.html')

@app.route("/all-packages")
def all_packages():
    return render_template("all-packages.html", plans=plans)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Support message from {name} ({email}): {message}")  # or save to DB/email etc.
        return render_template('support.html', success=True)
    return render_template('support.html')

@app.route('/details/<plan_name>')
def show_plan_details(plan_name):
    from knowledge_base import plans
    if plan_name not in plans:
        return "Plan not found", 404
    return render_template('package_details.html', plan_name=plan_name, plan=plans[plan_name])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

