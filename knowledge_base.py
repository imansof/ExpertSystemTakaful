class TakafulPlan:
    def __init__(self, name, coverage_term, contribution_term, entry_age, expiry_age,
                 min_monthly_contribution, min_sum_covered, gender, benefits, riders, goal,
                 target_group=None):
        self.name = name
        self.coverage_term = coverage_term
        self.contribution_term = contribution_term
        self.entry_age = entry_age
        self.expiry_age = expiry_age
        self.min_monthly_contribution = min_monthly_contribution
        self.min_sum_covered = min_sum_covered
        self.gender = gender
        self.benefits = benefits
        self.riders = riders
        self.target_group = target_group or {}
        self.goal = goal

# Plan Frame
anugerah_max = TakafulPlan(
    name="PruBSN AnugerahMax",
    coverage_term="5, 10, 20 years or until age 70, 80, 90 or 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    expiry_age="Up to 100",
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
    target_group={},
    goal = ["basic_protection", "family_protection", "savings", "legacy"]

)

warisan_gold = TakafulPlan(
    name="PruBSNWarisanGold",
    coverage_term="20 years or until age 70, 80, 90 or 100",
    contribution_term="5, 10, 20 years or throughout the coverage term",
    entry_age="14 days -70",
    expiry_age="Up to 100",
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
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medic TotalCare", "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect",
        "Contributor Spouse Saver", "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    target_group={},
    goal= ["legacy", "family_protection", "basic_protection"]

)

cegah_famili_epf = TakafulPlan(
    name="PruBSN Cegah Famili (EPF)",
    coverage_term="NA",
    contribution_term="NA",
    entry_age="EPF Member/Spouse: 19 to 65 (age next birthday); Children: 14 days to 65 (age next birthday)",
    expiry_age="NA",
    min_monthly_contribution="RM100 for adult and RM50 for child",
    min_sum_covered="RM10,000",
    gender="NA",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Accidental Death Benefit (Up to 500%)",
        "Khairat Benefit of RM3,000",
        "Badal Hajj Benefit of RM3,001"
    ],
    riders=[],
    target_group={},
    goal=["family_protection", "basic_protection"]
)


lindung_famili_epf = TakafulPlan(
    name="PruBSN Lindung Famili (EPF)",
    coverage_term="NA",
    contribution_term="NA",
    entry_age="NA",
    expiry_age="NA",
    min_monthly_contribution="RM100 for adult and RM50 for child",
    min_sum_covered="NA",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit",
        "Accidental Death Benefit (Up to 500%)",
        "Khairat Benefit of RM3,000 and Badal Hajj Benefit of RM3,002"
    ],
    riders=[],
    target_group={},
    goal=["basic_protection", "family_protection"]
)


asas360 = TakafulPlan(
    name="PruBSN Asas360",
    coverage_term="20 years or until age 60, 70, 80, 90 or 100",
    contribution_term="Up to age 100",
    entry_age="Prenatal/Child: 13 gestational weeks of pregnancy to 18 years old; Adult: 19 to 70 years old",
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
        "Contributor Joint Saver", "Health Protector", "Ihsan", "Takaful Saver", "Takaful Saver Impian"
    ],
    target_group={},
    goal = ["basic_protection", "family_protection", "savings"]

)

damaigenz = TakafulPlan(
    name="PruBSN DamaiGenZ",
    coverage_term="Up to 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    expiry_age="100",
    min_monthly_contribution="RM50",
    min_sum_covered="RM25,001",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit"
    ],
    riders=[
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medic TotalCare", "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect", "Contributor Spouse Saver",
        "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    target_group={},
    goal = ["basic_protection", "savings", "critical_illness"]

)

damai = TakafulPlan(
    name="PruBSN Damai",
    coverage_term="Up to 100",
    contribution_term="Throughout the coverage term",
    entry_age="1–70",
    expiry_age="100",
    min_monthly_contribution="RM50",
    min_sum_covered="RM25,002",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit"
    ],
    riders=[
        "Crisis Shield", "Crisis Protector", "Crisis TotalCare", "Cancer Protector",
        "Medic TotalCare", "Medik Asas", "Accidental Protector Plus",
        "Accidental Medical Protector", "Income Protector", "Parent Term",
        "Contributor Protect", "Contributor Saver", "Contributor Parent Protect",
        "Contributor Parent Saver", "Contributor Spouse Protect", "Contributor Spouse Saver",
        "Takaful Saver", "Takaful Saver Kid", "Ihsan"
    ],
    target_group={},
    goal = ["basic_protection", "savings", "critical_illness"]

)

anggun = TakafulPlan(
    name="PruBSN Anggun",
    coverage_term="Up to 70 or 80",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
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
    target_group={},
    goal = ["basic_protection", "critical_illness", "family_protection"]

)

lindungi = TakafulPlan(
    name="PruBSN Lindungi",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
    expiry_age="70",
    min_monthly_contribution="RM0.15 a day",
    min_sum_covered="RM20,000",
    gender="Both",
    benefits=[
        "Death Benefit",
        "Total and Permanent Disability (TPD) Benefit"
    ],
    riders=[],
    target_group={},
    goal = ["basic_protection"]
)

cancer_plan = TakafulPlan(
    name="Cancer Plan",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–60",
    expiry_age="70",
    min_monthly_contribution="RM0.08 a day",
    min_sum_covered="RM20,000",
    gender="Both",
    benefits=[
        "Diagnosis of Cancer"
    ],
    riders=[],
    target_group={},
    goal = ["critical_illness"]
)


gadai_janji = TakafulPlan(
    name="PruBSN Gadai Janji",
    coverage_term="5–33 years",
    contribution_term="5, 10, 20 years or throughout the coverage term",
    entry_age="19–70",
    expiry_age="Depending on financing tenure and entry age",
    min_monthly_contribution="Single Contribution",
    min_sum_covered="RM5,000",
    gender="Both",
    benefits=[
        "Maturity Benefit",
        "Compassionate Benefit: RM2,000 upon your death",
        "RM1,000 upon death of your spouse",
        "RM500 upon death of your children (maximum 2 children below age 20)",
        "RM1,000 medical expenses if you suffer Total and Permanent Disability (TPD)"
    ],
    riders=[],
    target_group={},
    goal = ["basic_protection", "family_protection"]
)

aspirasi = TakafulPlan(
    name="PruBSN Aspirasi",
    coverage_term="15, 20, 25 or 30 years",
    contribution_term="5, 10 or 20 years",
    entry_age="1–70",
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
    target_group={},
    goal = ["savings", "basic_protection", "family_protection"]
)

medic_plan = TakafulPlan(
    name="Medic Plan",
    coverage_term="Yearly renewable until maximum expiry age of 70",
    contribution_term="Throughout the coverage term",
    entry_age="19–45",
    expiry_age="70",
    min_monthly_contribution="RM0.96 per day",
    min_sum_covered="NA",
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
    target_group={},
    goal = ["medical"]
)

plans = {
    "PruBSN AnugerahMax": anugerah_max,
    "PruBSN WarisanGold": warisan_gold,
    "PruBSN Cegah Famili (EPF)": cegah_famili_epf,
    "PruBSN Lindung Famili (EPF)": lindung_famili_epf,
    "PruBSN Asas360": asas360,
    "PruBSN DamaiGenZ": damaigenz,
    "PruBSN Damai": damai,
    "PruBSN Anggun": anggun,
    "PruBSN Lindungi": lindungi,
    "Cancer Plan": cancer_plan,
    "PruBSN Gadai Janji": gadai_janji,
    "PruBSN Aspirasi": aspirasi,
    "Medic Plan": medic_plan
}
