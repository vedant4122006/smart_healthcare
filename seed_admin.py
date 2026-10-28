import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import app, db
from models.admin_model import Admin
from models.hospital_model import Hospital
from models.driver_model import Driver
from models.doctor_model import Doctor

load_dotenv()

with app.app_context():
    db.create_all()

    # 1. Seed Admin
    admin_email = os.getenv("ADMIN_EMAIL", "admin@smarthealthcare.com")
    admin_pass = os.getenv("ADMIN_PASS", "admin123")
    if not Admin.query.filter_by(email=admin_email).first():
        admin = Admin(email=admin_email)
        admin.set_password(admin_pass)
        db.session.add(admin)
        print(f"✅ Admin created: {admin_email}")

    # 2. Seed Default Available Ambulance Driver (so SOS works out-of-the-box)
    if not Driver.query.first():
        driver = Driver(
            name="Rajesh Sharma (Emergency Unit 1)",
            email=os.getenv("EMAIL_USER", "driver@smarthealthcare.com"),
            phone="+91-9876543210",
            password=generate_password_hash("driver123"),
            is_available=True
        )
        db.session.add(driver)
        print("✅ Default available ambulance driver seeded.")

    # 3. Seed Sample Doctor
    if not Doctor.query.first():
        doc = Doctor(
            name="Dr. Ananya Deshmukh",
            email="doctor@smarthealthcare.com",
            password=generate_password_hash("doctor123"),
            specialization="Cardiology"
        )
        db.session.add(doc)

    # 4. Seed 10 Hospitals across key specializations (Amravati/Nagpur region coordinates)
    if Hospital.query.count() < 2:
        sample_hospitals = [
            Hospital(name="Apex Heart & Vascular Institute", specialization="Cardiology, SuperSpecialist", machines="ECG, Defibrillator, Cath Lab, Echo, Ventilator", latitude=20.9320, longitude=77.7523),
            Hospital(name="City Multispeciality & Trauma Care", specialization="Multispeciality, SuperSpecialist", machines="X-Ray, Ultrasound, Blood Analyzer, Ventilator, ICU", latitude=20.9374, longitude=77.7796),
            Hospital(name="Brain & Spine Neuro Centre", specialization="Neurology, SuperSpecialist", machines="MRI, CT Scan, EEG, Ventilator", latitude=20.9258, longitude=77.7640),
            Hospital(name="Sancheti Ortho & Joint Hospital", specialization="Orthopedics, SuperSpecialist", machines="Digital X-Ray, MRI, CT Scan, Arthroscopy", latitude=20.9412, longitude=77.7589),
            Hospital(name="Prana Chest & Lungs Hospital", specialization="Pulmonology, SuperSpecialist", machines="Ventilator, Bronchoscopy, Spirometry, X-Ray", latitude=20.9195, longitude=77.7480),
            Hospital(name="Digestive Health & Gastro Clinic", specialization="Gastroenterology, SuperSpecialist", machines="Endoscopy Unit, Ultrasound, CT Scan, Blood Analyzer", latitude=20.9345, longitude=77.7712),
            Hospital(name="Lotus Women & Child Hospital", specialization="Gynecology, Pediatrics, SuperSpecialist", machines="Ultrasound, Neonatal ICU, Incubator, Blood Analyzer", latitude=20.9288, longitude=77.7555),
            Hospital(name="ClearSight Eye & ENT Hospital", specialization="Ophthalmology, ENT, SuperSpecialist", machines="Laser Suite, Audiometry, Endoscopy Unit", latitude=20.9390, longitude=77.7632),
            Hospital(name="RenalCare Kidney & Urology Centre", specialization="Nephrology, Urology, SuperSpecialist", machines="Dialysis Machine, Ultrasound, CT Scan, Lithotripsy", latitude=20.9210, longitude=77.7690),
            Hospital(name="Hope Cancer & Oncology Institute", specialization="Oncology, SuperSpecialist", machines="PET Scan, Radiotherapy Machine, MRI, Biopsy Suite", latitude=20.9450, longitude=77.7810),
        ]
        db.session.add_all(sample_hospitals)
        print("✅ 10 sample hospitals seeded across specializations.")

    db.session.commit()
    print("🎉 Database seeding complete!")