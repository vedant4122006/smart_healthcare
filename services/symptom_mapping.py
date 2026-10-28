import re
from rapidfuzz import fuzz, process

SYMPTOM_KEYWORDS = {
    'stomach': ['Gastroenterology', 'SuperSpecialist'],
    'abdomen': ['Gastroenterology', 'SuperSpecialist'],
    'belly': ['Gastroenterology', 'SuperSpecialist'],
    'heart': ['Cardiology', 'SuperSpecialist'],
    'chest': ['Cardiology', 'SuperSpecialist'],
    'brain': ['Neurology', 'SuperSpecialist'],
    'nerve': ['Neurology', 'SuperSpecialist'],
    'lungs': ['Pulmonology', 'SuperSpecialist'],
    'breathing': ['Pulmonology', 'SuperSpecialist'],
    'bone': ['Orthopedics', 'SuperSpecialist'],
    'knee': ['Orthopedics', 'SuperSpecialist'],
    'shoulder': ['Orthopedics', 'SuperSpecialist'],
    'ear': ['ENT', 'SuperSpecialist'],
    'nose': ['ENT', 'SuperSpecialist'],
    'throat': ['ENT', 'SuperSpecialist'],
    'skin': ['Dermatology', 'SuperSpecialist'],
    'eye': ['Ophthalmology', 'SuperSpecialist'],
    'vision': ['Ophthalmology', 'SuperSpecialist'],
    'pregnancy': ['Gynecology', 'SuperSpecialist'],
    'child': ['Pediatrics', 'SuperSpecialist'],
    'baby': ['Pediatrics', 'SuperSpecialist'],
    'kidney': ['Nephrology', 'SuperSpecialist'],
    'urine': ['Urology', 'SuperSpecialist'],
    'thyroid': ['Endocrinology', 'SuperSpecialist'],
    'cancer': ['Oncology', 'SuperSpecialist'],
    'tooth': ['Dentistry', 'SuperSpecialist'],
    'teeth': ['Dentistry', 'SuperSpecialist'],
    'dental': ['Dentistry', 'SuperSpecialist'],

    # -------------------
    # Cardiology
    # -------------------
    "chest pain": ["Cardiology", "SuperSpecialist"],
    "heart pain": ["Cardiology", "SuperSpecialist"],
    "palpitations": ["Cardiology", "SuperSpecialist"],
    "irregular heartbeat": ["Cardiology", "SuperSpecialist"],
    "shortness of breath": ["Cardiology", "SuperSpecialist"],
    "high blood pressure": ["Cardiology", "SuperSpecialist"],
    "low blood pressure": ["Cardiology", "SuperSpecialist"],
    "swelling in legs": ["Cardiology", "SuperSpecialist"],
    "angina": ["Cardiology", "SuperSpecialist"],
    "chest tightness": ["Cardiology", "SuperSpecialist"],
    "fainting": ["Cardiology", "SuperSpecialist"],
    "blue lips": ["Cardiology", "SuperSpecialist"],
    "poor circulation": ["Cardiology", "SuperSpecialist"],

    # -------------------
    # Neurology
    # -------------------
    "headache": ["Neurology", "SuperSpecialist"],
    "migraine": ["Neurology", "SuperSpecialist"],
    "dizziness": ["Neurology", "SuperSpecialist"],
    "seizures": ["Neurology", "SuperSpecialist"],
    "epilepsy": ["Neurology", "SuperSpecialist"],
    "memory loss": ["Neurology", "SuperSpecialist"],
    "stroke": ["Neurology", "SuperSpecialist"],
    "weakness in limbs": ["Neurology", "SuperSpecialist"],
    "numbness": ["Neurology", "SuperSpecialist"],
    "paralysis": ["Neurology", "SuperSpecialist"],
    "tingling": ["Neurology", "SuperSpecialist"],
    "blurred speech": ["Neurology", "SuperSpecialist"],
    "difficulty walking": ["Neurology", "SuperSpecialist"],
    "shaking hands": ["Neurology", "SuperSpecialist"],
    "loss of balance": ["Neurology", "SuperSpecialist"],
    "memory confusion": ["Neurology", "SuperSpecialist"],

    # -------------------
    # Pulmonology
    # -------------------
    "cough": ["Pulmonology", "SuperSpecialist"],
    "asthma": ["Pulmonology", "SuperSpecialist"],
    "wheezing": ["Pulmonology", "SuperSpecialist"],
    "lung infection": ["Pulmonology", "SuperSpecialist"],
    "tuberculosis": ["Pulmonology", "SuperSpecialist"],
    "breathing difficulty": ["Pulmonology", "SuperSpecialist"],
    "chest congestion": ["Pulmonology", "SuperSpecialist"],
    "pneumonia": ["Pulmonology", "SuperSpecialist"],
    "bronchitis": ["Pulmonology", "SuperSpecialist"],
    "sleep apnea": ["Pulmonology", "SuperSpecialist"],
    "bloody cough": ["Pulmonology", "SuperSpecialist"],

    # -------------------
    # Gastroenterology
    # -------------------
    "stomach pain": ["Gastroenterology", "SuperSpecialist"],
    "nausea": ["Gastroenterology", "SuperSpecialist"],
    "vomiting": ["Gastroenterology", "SuperSpecialist"],
    "diarrhea": ["Gastroenterology", "SuperSpecialist"],
    "constipation": ["Gastroenterology", "SuperSpecialist"],
    "acid reflux": ["Gastroenterology", "SuperSpecialist"],
    "indigestion": ["Gastroenterology", "SuperSpecialist"],
    "bloody stool": ["Gastroenterology", "SuperSpecialist"],
    "liver pain": ["Gastroenterology", "SuperSpecialist"],
    "hepatitis": ["Gastroenterology", "SuperSpecialist"],
    "jaundice": ["Gastroenterology", "SuperSpecialist"],
    "appendicitis": ["Gastroenterology", "SuperSpecialist"],
    "gas": ["Gastroenterology", "SuperSpecialist"],
    "bloating": ["Gastroenterology", "SuperSpecialist"],

    # -------------------
    # Orthopedics
    # -------------------
    "joint pain": ["Orthopedics", "SuperSpecialist"],
    "fracture": ["Orthopedics", "SuperSpecialist"],
    "back pain": ["Orthopedics", "SuperSpecialist"],
    "neck pain": ["Orthopedics", "SuperSpecialist"],
    "arthritis": ["Orthopedics", "SuperSpecialist"],
    "swollen joints": ["Orthopedics", "SuperSpecialist"],
    "bone injury": ["Orthopedics", "SuperSpecialist"],
    "shoulder pain": ["Orthopedics", "SuperSpecialist"],
    "knee pain": ["Orthopedics", "SuperSpecialist"],
    "osteoporosis": ["Orthopedics", "SuperSpecialist"],
    "sprain": ["Orthopedics", "SuperSpecialist"],

    # -------------------
    # ENT
    # -------------------
    "ear pain": ["ENT", "SuperSpecialist"],
    "hearing loss": ["ENT", "SuperSpecialist"],
    "ear discharge": ["ENT", "SuperSpecialist"],
    "blocked nose": ["ENT", "SuperSpecialist"],
    "sinus pain": ["ENT", "SuperSpecialist"],
    "sore throat": ["ENT", "SuperSpecialist"],
    "tonsils": ["ENT", "SuperSpecialist"],
    "nose bleeding": ["ENT", "SuperSpecialist"],
    "vertigo": ["ENT", "SuperSpecialist"],
    "voice change": ["ENT", "SuperSpecialist"],

    # -------------------
    # Dermatology
    # -------------------
    "skin rash": ["Dermatology", "SuperSpecialist"],
    "itching": ["Dermatology", "SuperSpecialist"],
    "eczema": ["Dermatology", "SuperSpecialist"],
    "psoriasis": ["Dermatology", "SuperSpecialist"],
    "acne": ["Dermatology", "SuperSpecialist"],
    "skin infection": ["Dermatology", "SuperSpecialist"],
    "hair loss": ["Dermatology", "SuperSpecialist"],
    "dandruff": ["Dermatology", "SuperSpecialist"],
    "nail infection": ["Dermatology", "SuperSpecialist"],
    "boils": ["Dermatology", "SuperSpecialist"],
    "allergy": ["Dermatology", "SuperSpecialist"],
    "vitiligo": ["Dermatology", "SuperSpecialist"],

    # -------------------
    # Ophthalmology
    # -------------------
    "eye pain": ["Ophthalmology", "SuperSpecialist"],
    "blurred vision": ["Ophthalmology", "SuperSpecialist"],
    "red eyes": ["Ophthalmology", "SuperSpecialist"],
    "watery eyes": ["Ophthalmology", "SuperSpecialist"],
    "cataract": ["Ophthalmology", "SuperSpecialist"],
    "glaucoma": ["Ophthalmology", "SuperSpecialist"],
    "double vision": ["Ophthalmology", "SuperSpecialist"],
    "night blindness": ["Ophthalmology", "SuperSpecialist"],

    # -------------------
    # Gynecology
    # -------------------
    "menstrual pain": ["Gynecology", "SuperSpecialist"],
    "irregular periods": ["Gynecology", "SuperSpecialist"],
    "pregnancy checkup": ["Gynecology", "SuperSpecialist"],
    "infertility": ["Gynecology", "SuperSpecialist"],
    "vaginal infection": ["Gynecology", "SuperSpecialist"],
    "pelvic pain": ["Gynecology", "SuperSpecialist"],
    "menopause": ["Gynecology", "SuperSpecialist"],

    # -------------------
    # Pediatrics
    # -------------------
    "fever in child": ["Pediatrics", "SuperSpecialist"],
    "cough in child": ["Pediatrics", "SuperSpecialist"],
    "diarrhea in child": ["Pediatrics", "SuperSpecialist"],
    "vomiting in child": ["Pediatrics", "SuperSpecialist"],
    "growth delay": ["Pediatrics", "SuperSpecialist"],
    "newborn checkup": ["Pediatrics", "SuperSpecialist"],
    "weak baby": ["Pediatrics", "SuperSpecialist"],

    # -------------------
    # Psychiatry
    # -------------------
    "depression": ["Psychiatry", "SuperSpecialist"],
    "anxiety": ["Psychiatry", "SuperSpecialist"],
    "stress": ["Psychiatry", "SuperSpecialist"],
    "sleep disorder": ["Psychiatry", "SuperSpecialist"],
    "bipolar disorder": ["Psychiatry", "SuperSpecialist"],
    "hallucinations": ["Psychiatry", "SuperSpecialist"],
    "addiction": ["Psychiatry", "SuperSpecialist"],

    # -------------------
    # Nephrology
    # -------------------
    "kidney pain": ["Nephrology", "SuperSpecialist"],
    "urine infection": ["Nephrology", "SuperSpecialist"],
    "blood in urine": ["Nephrology", "SuperSpecialist"],
    "kidney stones": ["Nephrology", "SuperSpecialist"],
    "frequent urination": ["Nephrology", "SuperSpecialist"],
    "swelling in face": ["Nephrology", "SuperSpecialist"],

    # -------------------
    # Urology
    # -------------------
    "prostate issues": ["Urology", "SuperSpecialist"],
    "urine blockage": ["Urology", "SuperSpecialist"],
    "painful urination": ["Urology", "SuperSpecialist"],
    "urinary retention": ["Urology", "SuperSpecialist"],
    "bed wetting": ["Urology", "SuperSpecialist"],

    # -------------------
    # Endocrinology
    # -------------------
    "diabetes": ["Endocrinology", "SuperSpecialist"],
    "thyroid problem": ["Endocrinology", "SuperSpecialist"],
    "weight loss": ["Endocrinology", "SuperSpecialist"],
    "weight gain": ["Endocrinology", "SuperSpecialist"],
    "hormonal imbalance": ["Endocrinology", "SuperSpecialist"],
    "goiter": ["Endocrinology", "SuperSpecialist"],

    # -------------------
    # Oncology
    # -------------------
    "cancer checkup": ["Oncology", "SuperSpecialist"],
    "tumor": ["Oncology", "SuperSpecialist"],
    "lump in breast": ["Oncology", "SuperSpecialist"],
    "blood cancer": ["Oncology", "SuperSpecialist"],
    "leukemia": ["Oncology", "SuperSpecialist"],
    "chemotherapy": ["Oncology", "SuperSpecialist"],

    # -------------------
    # Dentistry
    # -------------------
    "tooth pain": ["Dentistry", "SuperSpecialist"],
    "cavity": ["Dentistry", "SuperSpecialist"],
    "gum bleeding": ["Dentistry", "SuperSpecialist"],
    "wisdom tooth": ["Dentistry", "SuperSpecialist"],
    "bad breath": ["Dentistry", "SuperSpecialist"],
    "tooth sensitivity": ["Dentistry", "SuperSpecialist"],

    # -------------------
    # General / Family Medicine
    # -------------------
    "fever": ["Multispeciality", "SuperSpecialist"],
    "weakness": ["Multispeciality", "SuperSpecialist"],
    "body ache": ["Multispeciality", "SuperSpecialist"],
    "fatigue": ["Multispeciality", "SuperSpecialist"],
    "cold": ["Multispeciality", "SuperSpecialist"],
    "flu": ["Multispeciality", "SuperSpecialist"],
    "injury": ["Multispeciality", "SuperSpecialist"],
    "head cold": ["Multispeciality", "SuperSpecialist"],
    "general checkup": ["Multispeciality", "SuperSpecialist"],
}

def match_specialty(description: str):
    description = description.lower().strip()
    if not description:
        return ["Multispeciality", "SuperSpecialist"]

    # 1. Direct phrase/word check (longest keyword first)
    for keyword in sorted(SYMPTOM_KEYWORDS.keys(), key=len, reverse=True):
        if re.search(r'\b' + re.escape(keyword) + r'\b', description):
            return SYMPTOM_KEYWORDS[keyword]

    # 2. Strip common conversational stopwords before fuzzy matching
    stopwords = {"i", "am", "not", "feeling", "good", "well", "in", "my", "the", "a", "an", "having", "have", "severe", "very", "bad", "some", "of", "from", "since", "feel", "like"}
    tokens = [w for w in re.findall(r"[a-z]+", description) if w not in stopwords]
    cleaned = " ".join(tokens)
    if not cleaned:
        return ["Multispeciality", "SuperSpecialist"]

    best_match, score, _ = process.extractOne(
        cleaned,
        SYMPTOM_KEYWORDS.keys(),
        scorer=fuzz.token_set_ratio
    )
    print(f"[DEBUG] Input: '{description}' | Cleaned: '{cleaned}' | Best Match: '{best_match}' | Score: {score}")
    if score >= 75:
        return SYMPTOM_KEYWORDS[best_match]
    return ["Multispeciality", "SuperSpecialist"]
