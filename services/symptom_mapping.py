# symptom_mapping.py
from rapidfuzz import fuzz, process

SYMPTOM_KEYWORDS = {
    # Cardiology
    "chest pain": "Cardiology, SuperSpecialist",
    "heart pain": "Cardiology, SuperSpecialist",
    "palpitations": "Cardiology, SuperSpecialist",
    "irregular heartbeat": "Cardiology, SuperSpecialist",
    "shortness of breath": "Cardiology, SuperSpecialist",
    "high blood pressure": "Cardiology, SuperSpecialist",
    "low blood pressure": "Cardiology, SuperSpecialist",
    "swelling in legs": "Cardiology, SuperSpecialist",

    # Neurology
    "headache": "Neurology, SuperSpecialist",
    "migraine": "Neurology, SuperSpecialist",
    "dizziness": "Neurology, SuperSpecialist",
    "seizures": "Neurology, SuperSpecialist",
    "epilepsy": "Neurology, SuperSpecialist",
    "memory loss": "Neurology, SuperSpecialist",
    "stroke": "Neurology, SuperSpecialist",
    "weakness in limbs": "Neurology, SuperSpecialist",
    "numbness": "Neurology, SuperSpecialist",

    # Pulmonology
    "cough": "Pulmonology, SuperSpecialist",
    "asthma": "Pulmonology, SuperSpecialist",
    "wheezing": "Pulmonology, SuperSpecialist",
    "lung infection": "Pulmonology, SuperSpecialist",
    "tuberculosis": "Pulmonology, SuperSpecialist",
    "breathing difficulty": "Pulmonology, SuperSpecialist",
    "chest congestion": "Pulmonology, SuperSpecialist",

    # Gastroenterology
    "stomach pain": "Gastroenterology, SuperSpecialist",
    "nausea": "Gastroenterology, SuperSpecialist",
    "vomiting": "Gastroenterology, SuperSpecialist",
    "diarrhea": "Gastroenterology, SuperSpecialist",
    "constipation": "Gastroenterology, SuperSpecialist",
    "acid reflux": "Gastroenterology, SuperSpecialist",
    "indigestion": "Gastroenterology, SuperSpecialist",
    "bloody stool": "Gastroenterology, SuperSpecialist",
    "liver pain": "Gastroenterology, SuperSpecialist",

    # Orthopedics
    "joint pain": "Orthopedics, SuperSpecialist",
    "fracture": "Orthopedics, SuperSpecialist",
    "back pain": "Orthopedics, SuperSpecialist",
    "neck pain": "Orthopedics, SuperSpecialist",
    "arthritis": "Orthopedics, SuperSpecialist",
    "swollen joints": "Orthopedics, SuperSpecialist",
    "bone injury": "Orthopedics, SuperSpecialist",

    # ENT
    "ear pain": "ENT, SuperSpecialist",
    "hearing loss": "ENT, SuperSpecialist",
    "ear discharge": "ENT, SuperSpecialist",
    "blocked nose": "ENT, SuperSpecialist",
    "sinus pain": "ENT, SuperSpecialist",
    "sore throat": "ENT, SuperSpecialist",
    "tonsils": "ENT, SuperSpecialist",
    "nose bleeding": "ENT, SuperSpecialist",

    # Dermatology
    "skin rash": "Dermatology, SuperSpecialist",
    "itching": "Dermatology, SuperSpecialist",
    "eczema": "Dermatology, SuperSpecialist",
    "psoriasis": "Dermatology, SuperSpecialist",
    "acne": "Dermatology, SuperSpecialist",
    "skin infection": "Dermatology, SuperSpecialist",
    "hair loss": "Dermatology, SuperSpecialist",
    "dandruff": "Dermatology, SuperSpecialist",
    "nail infection": "Dermatology, SuperSpecialist",

    # Ophthalmology
    "eye pain": "Ophthalmology, SuperSpecialist",
    "blurred vision": "Ophthalmology, SuperSpecialist",
    "red eyes": "Ophthalmology, SuperSpecialist",
    "watery eyes": "Ophthalmology, SuperSpecialist",
    "cataract": "Ophthalmology, SuperSpecialist",
    "glaucoma": "Ophthalmology, SuperSpecialist",
    "double vision": "Ophthalmology, SuperSpecialist",

    # Gynecology
    "menstrual pain": "Gynecology, SuperSpecialist",
    "irregular periods": "Gynecology, SuperSpecialist",
    "pregnancy checkup": "Gynecology, SuperSpecialist",
    "infertility": "Gynecology, SuperSpecialist",
    "vaginal infection": "Gynecology, SuperSpecialist",
    "pelvic pain": "Gynecology, SuperSpecialist",

    # Pediatrics
    "fever in child": "Pediatrics, SuperSpecialist",
    "cough in child": "Pediatrics, SuperSpecialist",
    "diarrhea in child": "Pediatrics, SuperSpecialist",
    "vomiting in child": "Pediatrics, SuperSpecialist",
    "growth delay": "Pediatrics, SuperSpecialist",
    "newborn checkup": "Pediatrics, SuperSpecialist",

    # Psychiatry
    "depression": "Psychiatry, SuperSpecialist",
    "anxiety": "Psychiatry, SuperSpecialist",
    "stress": "Psychiatry, SuperSpecialist",
    "sleep disorder": "Psychiatry, SuperSpecialist",
    "bipolar disorder": "Psychiatry, SuperSpecialist",
    "hallucinations": "Psychiatry, SuperSpecialist",

    # Nephrology
    "kidney pain": "Nephrology, SuperSpecialist",
    "urine infection": "Nephrology, SuperSpecialist",
    "blood in urine": "Nephrology, SuperSpecialist",
    "kidney stones": "Nephrology, SuperSpecialist",
    "frequent urination": "Nephrology, SuperSpecialist",

    # Urology
    "prostate issues": "Urology, SuperSpecialist",
    "urine blockage": "Urology, SuperSpecialist",
    "painful urination": "Urology, SuperSpecialist",
    "urinary retention": "Urology, SuperSpecialist",

    # Endocrinology
    "diabetes": "Endocrinology, SuperSpecialist",
    "thyroid problem": "Endocrinology, SuperSpecialist",
    "weight loss": "Endocrinology, SuperSpecialist",
    "weight gain": "Endocrinology, SuperSpecialist",
    "hormonal imbalance": "Endocrinology, SuperSpecialist",

    # Oncology
    "cancer checkup": "Oncology, SuperSpecialist",
    "tumor": "Oncology, SuperSpecialist",
    "lump in breast": "Oncology, SuperSpecialist",
    "blood cancer": "Oncology, SuperSpecialist",

    # Dentistry
    "tooth pain": "Dentistry, SuperSpecialist",
    "cavity": "Dentistry, SuperSpecialist",
    "gum bleeding": "Dentistry, SuperSpecialist",
    "wisdom tooth": "Dentistry, SuperSpecialist",
    "bad breath": "Dentistry, SuperSpecialist",

    # General
    "fever": "General, SuperSpecialist",
    "weakness": "General, SuperSpecialist",
    "body ache": "General, SuperSpecialist",
    "fatigue": "General, SuperSpecialist",
    "cold": "General, SuperSpecialist",
    "flu": "General, SuperSpecialist",
    "injury": "General, SuperSpecialist",
}

def match_specialty(description: str):
    """
    Map patient description to closest matching specialty.
    Uses fuzzy matching with similarity scores.
    """
    description = description.lower().strip()

    best_match, score, _ = process.extractOne(
        description,
        SYMPTOM_KEYWORDS.keys(),
        scorer=fuzz.token_sort_ratio
    )

    print(f"[DEBUG] Input: '{description}' | Best Match: '{best_match}' | Score: {score}")

    if score >= 40:
        return SYMPTOM_KEYWORDS[best_match]
    else:
        return "General, SuperSpecialist"
