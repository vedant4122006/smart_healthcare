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

    # 1. See
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@smarthealthcare.com')
    admin_pass = os.getenv('ADMIN_PASS', 'admin123')
    if admin_email and admin_pass:
        admin = Admin.query.filter_by(email=admin_email).first()
        if not admin:
            admin = Admin(email=admin_email)
            admin.set_password(admin_pass)
            db.session.add(admin)
            print(f'[OK] Admin ready: {admin_email}')

    driver_email = os.getenv('DRIVER_EMAIL', 'driver@smarthealthcare.com')
    driver_pass = os.getenv('DRIVER_PASS', 'driver123')
    if driver_email and driver_pass:
        # Remove old misconfigured driver email if present
        Driver.query.filter(Driver.email != driver_email).delete()
        driver = Driver.query.filter_by(email=driver_email).first()
        if not driver:
            driver = Driver(
                name='Rajesh Sharma (Unit 1)',
                email=driver_email,
                phone='+91-9876543210',
                password=generate_password_hash(driver_pass),
                is_available=True
            )
            db.session.add(driver)
        else:
            driver.password = generate_password_hash(driver_pass)
            driver.is_available = True
        print(f'[OK] Driver ready: {driver_email}')

    doctor_email = os.getenv('DOCTOR_EMAIL', 'doctor@smarthealthcare.com')
    doctor_pass = os.getenv('DOCTOR_PASS', 'doctor123')
    if doctor_email and doctor_pass:
        doc = Doctor.query.filter_by(email=doctor_email).first()
        if not doc:
            doc = Doctor(
                name='Dr. Ananya Deshmukh',
                email=doctor_email,
                password=generate_password_hash(doctor_pass),
                specialization='Cardiology'
            )
            db.session.add(doc)
            print(f'[OK] Doctor ready: {doctor_email}')

    if Hospital.query.count() < 2:
        sample_hospitals = [
            Hospital(name='Apex Heart & Vascular Institute', specialization='Cardiology, SuperSpecialist', machines='ECG, Defibrillator, Cath Lab, Echo, Ventilator', latitude=20.9320, longitude=77.7523),
            Hospital(name='City Multispeciality & Trauma Care', specialization='Multispeciality, SuperSpecialist', machines='X-Ray, Ultrasound, Blood Analyzer, Ventilator, ICU', latitude=20.9374, longitude=77.7796),
            Hospital(name='Brain & Spine Neuro Centre', specialization='Neurology, SuperSpecialist', machines='MRI, CT Scan, EEG, Ventilator', latitude=20.9258, longitude=77.7640),
            Hospital(name='Sancheti Ortho & Joint Hospital', specialization='Orthopedics, SuperSpecialist', machines='Digital X-Ray, MRI, CT Scan, Arthroscopy', latitude=20.9412, longitude=77.7589),
            Hospital(name='Prana Chest & Lungs Hospital', specialization='Pulmonology, SuperSpecialist', machines='Ventilator, Bronchoscopy, Spirometry, X-Ray', latitude=20.9195, longitude=77.7480),
            Hospital(name='Digestive Health & Gastro Clinic', specialization='Gastroenterology, SuperSpecialist', machines='Endoscopy Unit, Ultrasound, CT Scan, Blood Analyzer', latitude=20.9345, longitude=77.7712),
            Hospital(name='Lotus Women & Child Hospital', specialization='Gynecology, Pediatrics, SuperSpecialist', machines='Ultrasound, Neonatal ICU, Incubator, Blood Analyzer', latitude=20.9288, longitude=77.7555),
            Hospital(name='ClearSight Eye & ENT Hospital', specialization='Ophthalmology, ENT, SuperSpecialist', machines='Laser Suite, Audiometry, Endoscopy Unit', latitude=20.9390, longitude=77.7632),
            Hospital(name='RenalCare Kidney & Urology Centre', specialization='Nephrology, Urology, SuperSpecialist', machines='Dialysis Machine, Ultrasound, CT Scan, Lithotripsy', latitude=20.9210, longitude=77.7690),
            Hospital(name='Hope Cancer & Oncology Institute', specialization='Oncology, SuperSpecialist', machines='PET Scan, Radiotherapy Machine, MRI, Biopsy Suite', latitude=20.9450, longitude=77.7810),
        ]
        db.session.add_all(sample_hospitals)
        print('[OK] 10 sample hospitals seeded.')

    db.session.commit()
