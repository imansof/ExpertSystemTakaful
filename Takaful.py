from experta import *
import sqlite3
from knowledge_base import plans

# ======== DATABASE CONNECTION ========
def get_db_connection():
    conn = sqlite3.connect('takaful_users.db')
    conn.row_factory = sqlite3.Row
    return conn

# ======== SIGNUP / LOGIN ========
def signup(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return "Signup successful!"
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()

def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ======== USER INPUT FACT ========
class UserInput(Fact):
    age             = Field(int, mandatory=True)
    income          = Field(int, mandatory=True)
    gender          = Field(str, mandatory=True)
    marital_status  = Field(str, mandatory=True)
    has_dependents  = Field(bool, mandatory=True)
    goals           = Field(list, mandatory=True)  # multiple selection

# ======== NORMALIZATION HELPERS ========
def normalize(text: str) -> str:
    import re
    s = text.lower()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    return s.strip('_')

def build_plan_signatures():
    """
        Build a dict mapping each plan name to the set of goal-category tokens
        it can satisfy (directly via benefits, indirectly via riders).
        """
    sigs = {}
    for name, plan in plans.items():
        # plan.direct_goals and plan.indirect_goals are lists of keys like 'cancer_coverage'
        sigs[name] = set(plan.direct_goals + plan.indirect_goals)
    return sigs

PLAN_SIGNATURES = build_plan_signatures()

# ======== EXPERTA ENGINE WITH DYNAMIC RULES ========
class TakafulEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []
        self.rejection_reasons = {}

    def log_rejection(self, plan, reason):
        self.rejection_reasons.setdefault(plan, []).append(reason)

    # Default fallback if nothing matches
    @Rule(AS.ui << UserInput())
    def fallback(self, ui):
        if not self.recommendations:
            self.recommendations.append("PruBSN Lindung Famili (EPF)")
            self.log_rejection("None matched", "Default fallback applied")

# Dynamically add one @Rule per plan (optional simpler version: any match)
for plan_name, signature in PLAN_SIGNATURES.items():
    def make_rule(pname, psig):
        goals_sig = psig  # ✅ Define it here so it's in scope

        def _test(goals):
            # Match if at least one user goal is in the plan’s signature
            return any(normalize(g) in goals_sig for g in goals)

        @Rule(
            UserInput(goals=MATCH.goals),
            TEST(_test)
        )
        def plan_rule(self, goals):
            self.recommendations.append(pname)

        plan_rule.__name__ = f"rule_{pname.replace(' ', '_')}"
        return plan_rule

    setattr(
        TakafulEngine,
        f"rule_{plan_name.replace(' ', '_')}",
        make_rule(plan_name, signature)
    )

# ======== MAIN RECOMMENDATION FUNCTION ========
def get_recommendations(username, age, income, gender,
                        marital_status, has_dependents, goals):
    """
    Save user input and recommend plans based on goal-category matching.
    Returns a dict with:
      - plans: list of (plan_name, match_count) tuples, sorted by match_count desc
      - rejections: any logged rejections (empty here)
    """
    # 1. Log the input into the database
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO user_input
                           (username, age, income, gender, marital_status, has_dependents, goals)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (
                           username,
                           age,
                           income,
                           gender,
                           marital_status,
                           int(has_dependents),
                           ",".join(goals)
                       ))
        conn.commit()
    finally:
        conn.close()

    # 2. Build a set of the user’s selected goal keys
    user_goals = set(goals)

    # 3. Score each plan by how many selected goals it satisfies
    scored = []
    from knowledge_base import plans as all_plans
    for plan_name, plan in all_plans.items():
        # Combine direct_goals + indirect_goals
        plan_goals = set(plan.direct_goals + plan.indirect_goals)
        match_count = len(user_goals & plan_goals)
        if match_count > 0:
            scored.append((plan_name, match_count))

    # 4. Sort descending by number of matches
    scored.sort(key=lambda x: x[1], reverse=True)

    # 5. Return the scored list
    return {
        'plans': scored,
        'rejections': {}  # you can fill this if you implement rejection logging
    }
