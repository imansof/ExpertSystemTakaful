from experta import *
import sqlite3

# ======== DATABASE CONNECTION ========
def get_db_connection():
    conn = sqlite3.connect('takaful_users.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

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
    conn.close()

initialize_db()

# ======== LOGIN / SIGNUP ========
def signup(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return "Signup successful!"
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()

def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ======== EXPERTA FACT & ENGINE ========
class UserInput(Fact):
    age = Field(int, mandatory=True)
    income = Field(int, mandatory=True)
    marital_status = Field(str, mandatory=True)
    has_dependents = Field(bool, mandatory=True)
    goal = Field(str, mandatory=True)

class TakafulEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @Rule(UserInput(goal='medical', age=P(lambda x: x <= 40), income=P(lambda x: x >= 3000)))
    def medical_young(self):
        self.recommendations.append("PruBSN AnugerahMax")

    @Rule(UserInput(goal='medical', age=P(lambda x: x > 40), income=P(lambda x: x >= 3000)))
    def medical_older(self):
        self.recommendations.append("PruBSN Medic Plan")

    @Rule(UserInput(goal='critical_illness', income=P(lambda x: x >= 3000)))
    def critical(self):
        self.recommendations.append("PruBSN Cegah Famili")

    @Rule(UserInput(goal='family_protection', marital_status='married', has_dependents=True))
    def married_family(self):
        self.recommendations.append("PruBSN Lindung Famili")

    @Rule(UserInput(goal='family_protection', income=P(lambda x: x >= 4000), has_dependents=True))
    def family_income(self):
        self.recommendations.append("PruBSN Cegah Famili")

    @Rule(UserInput(goal='legacy', age=P(lambda x: x >= 35), income=P(lambda x: x >= 5000)))
    def legacy(self):
        self.recommendations.append("PruBSN WarisanGold")

    @Rule(UserInput(goal='savings', income=P(lambda x: x >= 2500)))
    def savings(self):
        self.recommendations.append("PruBSN Aspirasi")

    @Rule(UserInput(goal='basic_protection', age=P(lambda x: x <= 30), income=P(lambda x: x <= 3000)))
    def basic_young(self):
        self.recommendations.append("PruBSN Aspirasi")

    @Rule(UserInput(goal='basic_protection', age=P(lambda x: x <= 30), income=P(lambda x: x <= 3000), marital_status='single', has_dependents=False))
    def basic_genz(self):
        self.recommendations.append("PruBSN DamaiGenZ")

# ======== MAIN RECOMMENDATION FUNCTION ========
def get_recommendations(username, age, income, marital_status, has_dependents, goal):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Save input
        cursor.execute('''
            INSERT INTO user_input (username, age, income, marital_status, has_dependents, goal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, age, income, marital_status, int(has_dependents), goal))
        conn.commit()

        # Run Experta Engine
        engine = TakafulEngine()
        engine.reset()
        engine.declare(UserInput(
            age=age,
            income=income,
            marital_status=marital_status,
            has_dependents=has_dependents,
            goal=goal
        ))
        engine.run()
        return engine.recommendations

    finally:
        conn.close()
