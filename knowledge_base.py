# ======== CATEGORY DEFINITIONS ========
# High-level goal categories used for user selection
GOAL_CATEGORIES = [
    'basic_protection', 'family_protection', 'medical_coverage',
    'critical_illness', 'cancer_coverage', 'female_protection',
    'mental_care', 'investment', 'charity', 'education', 'funeral_cover'
]

# ======== MAPPINGS ========
# Map raw benefit strings to direct goal categories
BENEFIT_TO_GOALS = {
    'Maturity Benefit': ['basic_protection', 'investment'],
    'Death Benefit': ['basic_protection', 'family_protection'],
    'Total and Permanent Disability (TPD) Benefit': ['basic_protection', 'family_protection'],
    'Accidental Death Benefit (Up to 500%)': ['basic_protection', 'family_protection'],
    'Diagnosis of Cancer': ['cancer_coverage'],
    'Room & Board Benefit: Hospital Daily Room & Board Benefit': ['medical_coverage'],
    'Hospital & Surgical Benefits: Intensive Care Unit/Cardiac Care Unit Benefit, In-Hospital & Related Services Benefit': ['medical_coverage'],
    'Outpatient Treatment Benefits: Pre-Hospitalisation Treatment Benefit, Post-Hospitalisation Treatment Benefit, Day Surgery Benefit': ['medical_coverage'],
    'Emergency Treatment for Accidental Injury Benefit': ['medical_coverage'],
    'Government Hospital Daily Cash Benefit': ['medical_coverage'],
    'Outpatient Cancer Treatment Benefit': ['cancer_coverage'],
    'Outpatient Kidney Dialysis Treatment Benefit': ['medical_coverage'],
    'EduAchieve Bonus': ['education'],
    'Kasih Bonus': ['charity'],
    # Anggun-specific
    'Female Illness Benefit': ['female_protection'],
    'Female Care Benefit': ['female_protection'],
    'Mental Care Benefit': ['mental_care'],
    'Life Stage Benefit': ['basic_protection'],
    # Gadai Janji
    'Compassionate Benefit: RM2,000 upon your death': ['funeral_cover'],
    'RM1,000 upon death of your spouse': ['funeral_cover'],
    'RM500 upon death of your children (maximum 2 children below age 20)': ['funeral_cover'],
    'RM1,000 medical expenses if you suffer Total and Permanent Disability (TPD)': ['medical_coverage'],
    # Aspirasi
    'Annual Cash Payout': ['investment']
}

# Map raw rider strings to indirect goal categories
RIDER_TO_GOALS = {
    'Cancer Protector': ['cancer_coverage', 'critical_illness'],
    'Accidental Protector Plus': ['basic_protection'],
    'Accidental Medical Protector': ['medical_coverage'],
    'Accident Income Protector':  ['basic_protection'],
    'Income Protector': ['basic_protection'],
    'Parent Term': ['family_protection'],
    'Contributor Protect': ['basic_protection'],
    'Contributor Saver': ['investment'],
    'Contributor Parent Protect': ['family_protection'],
    'Contributor Parent Saver': ['investment'],
    'Contributor Spouse Protect': ['family_protection'],
    'Contributor Spouse Saver': ['investment'],
    'Contributor Joint Protect': ['family_protection'],
    'Contributor Joint Saver': ['investment'],
    'Crisis Shield': ['family_protection'],
    'Crisis Protector': ['family_protection'],
    'Crisis TotalCare': ['basic_protection'],
    'Medic TotalCare': ['medical_coverage'],
    'Medik Asas': ['medical_coverage'],
    'Baby TotalCare': ['family_protection'],
    'Vital Care Plus': ['medical_coverage'],
    'Health Protector': ['medical_coverage'],
    'Health360': ['medical_coverage'],
    'Takaful Saver': ['investment'],
    'Takaful Saver Kid': ['education'],
    'Takaful Saver Impian': ['investment'],
    'Ihsan': ['charity'],
    'Mom Care': ['female_protection'],
    'Hajj Protection': ['charity'],
    'Hajj Umrah Protector': ['charity'],  # new rider on WarisanGold
    'Level Term Benefit': ['basic_protection'],  # term rider
    'Accidental Disablement Protector': ['basic_protection']  # renamed from 'Accidental Disablement'
}

# ======== TakafulPlan Class ========
class TakafulPlan:
    def __init__(self, name, coverage_term, contribution_term, entry_age, min_entry_age, max_entry_age, allow_prenatal, allow_newborn, expiry_age,
                 min_monthly_contribution, min_sum_covered, gender, benefits, riders, goal
                 ):
        self.name = name
        self.coverage_term = coverage_term
        self.contribution_term = contribution_term
        self.entry_age = entry_age
        self.min_entry_age = min_entry_age
        self.max_entry_age = max_entry_age
        self.allow_prenatal = allow_prenatal
        self.allow_newborn = allow_newborn
        self.expiry_age = expiry_age
        self.min_monthly_contribution = min_monthly_contribution
        self.min_sum_covered = min_sum_covered
        self.gender = gender
        self.benefits = benefits
        self.riders = riders
        # original broad goals (proposal-level)
        self.proposal_goals = goal
        # compute direct and indirect categories
        self.direct_goals = self._compute_direct_goals()
        self.indirect_goals = self._compute_indirect_goals()

        # --- NEW ATTRIBUTES FOR ELIGIBILITY & FILTERING ---
        # parse minimum contribution value (RM)
        self.min_contribution_value = self._parse_contribution(self.min_monthly_contribution)
        # child-friendly if entry_age mentions days or min age == 0
        self.child_friendly = self.min_entry_age < 19
        # only AnugerahMax has EduAchieve Bonus for schoolgoers (1–18)
        self.education_age_range = (1, 18) if 'EduAchieve Bonus' in self.benefits else None

    def _compute_direct_goals(self):
        dg = set()
        for b in self.benefits:
            dg.update(BENEFIT_TO_GOALS.get(b, []))
        return list(dg)

    def _compute_indirect_goals(self):
        ig = set()
        for r in self.riders:
            ig.update(RIDER_TO_GOALS.get(r, []))
        return list(ig)

    def _parse_contribution(self, text):
        import re
        # finds first decimal or integer in the string
        m = re.search(r'(\d+\.?\d*)', text.replace(',', ''))
        return float(m.group(1)) if m else 0.0

# Plan Frame
anugerah_max = TakafulPlan(
    name="PruBSN AnugerahMax",
    coverage_term="5, 10, 20 years or until age 70, 80, 90 or 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    min_entry_age = 1, # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age = 70,
    allow_prenatal = False,  # True if supports pregnancy-based enrollment
    allow_newborn = False,   # True if supports 14-day-old babies
    expiry_age="100",
    min_monthly_contribution="RM50",
    min_sum_covered="RM10,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "EduAchieve Bonus"
    ],
    riders=[
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medic TotalCare", "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect",
        "Contributor Spouse Saver", "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    goal = ["basic_protection", "family_protection", "investment"]

)

warisan_gold = TakafulPlan(
    name="PruBSNWarisanGold",
    coverage_term="20 years or until age 70, 80, 90 or 100",
    contribution_term="5, 10, 20 years or throughout the coverage term",
    entry_age="14 days -70",
    min_entry_age=0,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=True,  # True if supports 14-day-old babies
    expiry_age="100",
    min_monthly_contribution="RM100 for adult and RM50 for child",
    min_sum_covered="Adult: RM350,000, Child: RM250,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Accidental Death Benefit (Up to 500%)"
    ],
    riders=[
        "Hajj Umrah Protector", "Level Term Benefit", "Accidental Disablement Protector",
        "Crisis Shield", "Crisis Protector", "Takaful Saver", "Takaful Saver Kid", "Ihsan",
        "Contributor Parent Protect", "Contributor Parent Saver", "Contributor Protect",
        "Contributor Saver", "Contributor Spouse Protect", "Contributor Spouse Saver"
    ],
    goal= [
        # original proposal-level:
        "family_protection", "basic_protection",
        # plus indirect via riders:
        "charity", "investment", "education"
    ]
)

cegah_famili_epf = TakafulPlan(
    name="PruBSN Cegah Famili (EPF)",
    coverage_term="Yearly Renewable up to age 75",
    contribution_term="Throughout coverage term",
    entry_age="EPF Member/Spouse: 19 to 65; Children: 14 days to 65",
    min_entry_age=0,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=65,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=True,  # True if supports 14-day-old babies
    expiry_age="75",
    min_monthly_contribution="RM1.36 per covered member",
    min_sum_covered="RM10,000",
    gender="Both",
    benefits=[
        "Death Benefit",
        "Critical Illness Benefit",
    ],
    riders=[],
    goal=["basic_protection", "family_protection", "critical_illness"]
)

lindung_famili_epf = TakafulPlan(
    name="PruBSN Lindung Famili (EPF)",
    coverage_term="Yearly Renewable up to age 75",
    contribution_term="Throughout coverage term",
    entry_age="EPF Member/Spouse: 19 to 65; Children: 14 days to 65",
    min_entry_age=0,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=65,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=True,  # True if supports 14-day-old babies
    expiry_age="75",
    min_monthly_contribution="RM1.15 per covered member",
    min_sum_covered="RM10,000",
    gender="Both",
    benefits=[
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Accidental Death Benefit (Up to 300%)",
    ],
    riders=[],
    goal=["basic_protection", "family_protection"]
)

asas360 = TakafulPlan(
    name="PruBSN Asas360",
    coverage_term="20 years or until age 60, 70, 80, 90 or 100",
    contribution_term="Up to age 100",
    entry_age="Prenatal/Child: 13 gestational weeks of pregnancy to 18 years old; Adult: 19 to 70 years old",
    min_entry_age=-1,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=True,  # True if supports pregnancy-based enrollment
    allow_newborn=True,  # True if supports 14-day-old babies
    expiry_age="100",
    min_monthly_contribution="RM100 for adult and RM50 for child",
    min_sum_covered="RM25,000",
    gender="Both",
    benefits=[
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Kasih Bonus"
    ],
    riders=[
        "Accidental Protector Plus", "Accidental Medical Protector", "Accident Income Protector",
        "Baby TotalCare", "Vital Care Plus", "Crisis Protector", "Crisis Shield", "Crisis TotalCare",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect", "Contributor Parent Saver",
        "Contributor Spouse Protect", "Contributor Spouse Saver", "Contributor Joint Protect",
        "Contributor Joint Saver", "Health Protector", "Health360", "Ihsan", "Takaful Saver", "Takaful Saver Impian"
    ],
    goal = ["basic_protection", "family_protection", "investment"]
)

damaigenz = TakafulPlan(
    name="PruBSN DamaiGenZ",
    coverage_term="5, 10, 20 years or until age 70, 80, 90 or 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    min_entry_age=1,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="100",
    min_monthly_contribution="RM50",
    min_sum_covered="RM10,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Medic TotalCare"
    ],
    riders=[
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect", "Contributor Spouse Saver",
        "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    goal = ["basic_protection", "investment", "critical_illness", "medical_coverage",
        "education", "charity"]
)

damai = TakafulPlan(
    name="PruBSN Damai",
    coverage_term="5, 10, 20 years or until age 70, 80, 90 or 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    min_entry_age=1,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="100",
    min_monthly_contribution="RM50",
    min_sum_covered="RM10,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Medic TotalCare",
        "Unlimited Lifetime Limit"
    ],
    riders=[
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect", "Contributor Spouse Saver",
        "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    goal = ["basic_protection", "investment", "critical_illness", "medical_coverage",
        "education", "charity"]
)

anggun = TakafulPlan(
    name="PruBSN Anggun",
    coverage_term="Up to 70 or 80",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
    min_entry_age=19,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=60,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="70 or 80",
    min_monthly_contribution="RM50",
    min_sum_covered="RM25,000",
    gender="Female",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Female Illness Benefit",
        "Female Care Benefit",
        "Mental Care Benefit",
        "Life Stage Benefit"
    ],
    riders=[
        "Mom Care", "Cancer Protector", "Takaful Saver", "Ihsan"
    ],
    goal = ["basic_protection", "critical_illness", "family_protection"]
)

lindungi = TakafulPlan(
    name="PruBSN Lindungi",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
    min_entry_age=19,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=60,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="70",
    min_monthly_contribution="RM4.5",
    min_sum_covered="RM20,000",
    gender="Both",
    benefits=[
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit"
    ],
    riders=[],
    goal = ["basic_protection"]
)

cancer_plan = TakafulPlan(
    name="Cancer Plan",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
    min_entry_age=19,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=60,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="70",
    min_monthly_contribution="RM2.4",
    min_sum_covered="RM20,000",
    gender="Both",
    benefits=[
        "Diagnosis of Cancer"
    ],
    riders=[],
    goal = ["cancer_coverage", "critical_illness"]
)

gadai_janji = TakafulPlan(
    name="PruBSN Gadai Janji",
    coverage_term="5–33 years",
    contribution_term="5, 10, 20 years or throughout the coverage term",
    entry_age="19–70",
    min_entry_age=19,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="Depending on financing tenure and entry age",
    min_monthly_contribution="Single Contribution",
    min_sum_covered="RM5,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Spouse Death Benefit",
        "Children Death Benefit",
        "Total and Permanent Disability (TPD) Benefit"
    ],
    riders=[],
    goal = ["basic_protection", "family_protection", "funeral_cover"]
)

aspirasi = TakafulPlan(
    name="PruBSN Aspirasi",
    coverage_term="15, 20, 25 or 30 years",
    contribution_term="5, 10 or 20 years",
    entry_age="1–70",
    min_entry_age=1,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=70,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="NA",
    min_monthly_contribution="NA",
    min_sum_covered="RM15,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Annual Cash Payout"
    ],
    riders=[
        "Hajj Protection",
        "Contributor Protect",
        "Contributor Saver",
        "Contributor Parent Protect",
        "Contributor Parent Saver",
        "Takaful Saver",
        "Ihsan"
    ],
    goal = ["investment", "basic_protection", "family_protection", "charity"]
)

medic_plan = TakafulPlan(
    name="Medic Plan",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–45",
    min_entry_age=19,  # e.g. 0 = newborn, 0.25 = 3 months, 1 = 1 year
    max_entry_age=45,
    allow_prenatal=False,  # True if supports pregnancy-based enrollment
    allow_newborn=False,  # True if supports 14-day-old babies
    expiry_age="70",
    min_monthly_contribution="RM28.8 per day",
    min_sum_covered="RM100,000",
    gender="Both",
    benefits=[
        "Room & Board Benefit: Hospital Daily Room & Board Benefit",
        "Hospital & Surgical Benefits: Intensive Care Unit/Cardiac Care Unit Benefit, In-Hospital & Related Services Benefit",
        "Outpatient Treatment Benefits: Pre-Hospitalisation Treatment Benefit, Post-Hospitalisation Treatment Benefit, Day Surgery Benefit",
        "Emergency Treatment for Accidental Injury Benefit",
        "Government Hospital Daily Cash Benefit",
        "Outpatient Cancer Treatment Benefit",
        "Outpatient Kidney Dialysis Treatment Benefit"
    ],
    riders=[],
    goal = ["medical_coverage", "cancer_coverage"]
)

from collections import OrderedDict
plans = OrderedDict([
    ("PruBSN AnugerahMax", anugerah_max),
    ("PruBSN WarisanGold", warisan_gold),
    ("PruBSN Cegah Famili (EPF)", cegah_famili_epf),
    ("PruBSN Lindung Famili (EPF)", lindung_famili_epf),
    ("PruBSN Asas360", asas360),
    ("PruBSN DamaiGenZ", damaigenz),
    ("PruBSN Damai", damai),
    ("PruBSN Anggun", anggun),
    ("PruBSN Lindungi", lindungi),
    ("Cancer Plan", cancer_plan),
    ("PruBSN Gadai Janji", gadai_janji),
    ("PruBSN Aspirasi", aspirasi),
    ("Medic Plan", medic_plan)
])
