import sqlite3

# ======== SETUP DATABASE STRUCTURE ========
conn = sqlite3.connect('takaful_users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create user input table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_input (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        age INTEGER,
        income INTEGER,
        marital_status TEXT,
        has_dependents BOOLEAN,
        goal TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    )
''')
conn.commit()

# ======== LOGIN / SIGNUP FUNCTIONS ========
def signup(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return "Signup successful!"
    except sqlite3.IntegrityError:
        return "Username already exists."

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    return result is not None

# ======== PLAN LOGIC ========
class TakafulPlan:
    def __init__(self, name, goal, min_age=None, max_age=None,
                 min_income=None, max_income=None,
                 marital_required="any", dependents_required="any"):
        self.name = name
        self.goal = goal
        self.min_age = min_age
        self.max_age = max_age
        self.min_income = min_income
        self.max_income = max_income
        self.marital_required = marital_required
        self.dependents_required = dependents_required

    def is_match(self, user):
        if self.goal != user["goal"]:
            return False
        if self.min_age is not None and user["age"] < self.min_age:
            return False
        if self.max_age is not None and user["age"] > self.max_age:
            return False
        if self.min_income is not None and user["income"] < self.min_income:
            return False
        if self.max_income is not None and user["income"] > self.max_income:
            return False
        if self.marital_required != "any" and self.marital_required != user["marital_status"]:
            return False
        if self.dependents_required != "any" and self.dependents_required != user["has_dependents"]:
            return False
        return True

# List of available Takaful plans
plans = [
    TakafulPlan("PruBSN AnugerahMax", "medical", max_age=40, min_income=3000),
    TakafulPlan("PruBSN Medic Plan", "medical", min_age=41, min_income=3000),
    TakafulPlan("PruBSN Cegah Famili", "critical_illness", min_income=3000),
    TakafulPlan("PruBSN Lindung Famili", "family_protection", marital_required="married", dependents_required=True),
    TakafulPlan("PruBSN Cegah Famili", "family_protection", min_income=4000, dependents_required=True),
    TakafulPlan("PruBSN WarisanGold", "legacy", min_age=35, min_income=5000),
    TakafulPlan("PruBSN Aspirasi", "savings", min_income=2500),
    TakafulPlan("PruBSN Aspirasi", "basic_protection", max_age=30, max_income=3000),
    TakafulPlan("PruBSN DamaiGenZ", "basic_protection", max_age=30, max_income=3000, marital_required="single", dependents_required=False)
]

def get_recommendations(username, age, income, marital_status, has_dependents, goal):
    # Save user input to DB
    cursor.execute('''
        INSERT INTO user_input (username, age, income, marital_status, has_dependents, goal)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, age, income, marital_status, int(has_dependents), goal))
    conn.commit()

    # Fetch latest input for this user
    cursor.execute('''
        SELECT age, income, marital_status, has_dependents, goal
        FROM user_input WHERE username=? ORDER BY id DESC LIMIT 1
    ''', (username,))
    row = cursor.fetchone()

    if row:
        latest_user = {
            "age": row[0],
            "income": row[1],
            "marital_status": row[2],
            "has_dependents": bool(row[3]),
            "goal": row[4]
        }

        # Match plans
        matched = [plan.name for plan in plans if plan.is_match(latest_user)]
        return matched
    return [] # Return empty list if no user data found (shouldn't happen if just saved)

# ======== MAIN FLOW SIMULATION ========
def simulate_flow():
    # Signup or login
    username = input("Enter username: ")
    password = input("Enter password: ")

    action = input("Type 'signup' or 'login': ").lower()
    if action == "signup":
        print(signup(username, password))
    if not login(username, password):
        print("Login failed. Exiting.")
        return
    print("Login successful!\n")

    # Collect user input
    age = int(input("Enter your age: "))
    income = int(input("Enter your monthly income: "))
    marital_status = input("Enter marital status (single/married): ").lower()
    has_dependents = input("Do you have dependents? (yes/no): ").lower() == "yes"
    goal = input("Enter your goal (basic_protection/medical/family_protection/legacy/savings/critical_illness): ")

    # Save user input to DB
    cursor.execute('''
        INSERT INTO user_input (username, age, income, marital_status, has_dependents, goal)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, age, income, marital_status, int(has_dependents), goal))
    conn.commit()

    # Fetch latest input for this user
    cursor.execute('''
        SELECT age, income, marital_status, has_dependents, goal
        FROM user_input WHERE username=? ORDER BY id DESC LIMIT 1
    ''', (username,))
    row = cursor.fetchone()

    if row:
        latest_user = {
            "age": row[0],
            "income": row[1],
            "marital_status": row[2],
            "has_dependents": bool(row[3]),
            "goal": row[4]
        }

        # Match plans
        matched = [plan.name for plan in plans if plan.is_match(latest_user)]
        if matched:
            print("\nRecommended Plan(s):")
            for plan in matched:
                print("-", plan)
        else:
            print("\nNo exact match. Recommend: PruBSN Asas360 + suitable rider.")

#simulate_flow()
#conn.close()
