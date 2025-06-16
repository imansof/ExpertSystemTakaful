from experta import *
import sqlite3
import re
from knowledge_base import plans as all_plans

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
    for name, plan in all_plans.items():
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
    raw_scores = []
    for plan_name, plan in all_plans.items():
        # count how many of the user’s goals this plan can satisfy
        plan_goals = set(plan.direct_goals + plan.indirect_goals)
        match_count = len(user_goals & plan_goals)
        if match_count:
            raw_scores.append((plan_name, match_count))

    # 4. Filter out plans the user can’t have or afford
    filtered = []
    for plan_name, match_count in raw_scores:
        plan = all_plans[plan_name]

        # age eligibility
        min_age, max_age = plan.age_range
        if not (min_age <= age <= max_age):
            continue

        # affordability (use 5% of income as threshold)
        if plan.min_contribution_value > 0.05 * income:
            continue

        filtered.append((plan_name, match_count))

    # 5. If nothing left, fallback to default
    if not filtered:
        return {'plans': [], 'rejections': {}}

    # 6. Pick only those with the highest match_count
    best_count = max(cnt for _, cnt in filtered)
    best_plans = [(p, c) for (p, c) in filtered if c == best_count]

    # 7. Limit to top‑2
    best_plans = best_plans[:2]

    return {
        'plans': best_plans,
        'rejections': {}
    }
