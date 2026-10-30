# Smart Healthcare — Emergency Triage & Hospital Recommendation System

A full-stack healthcare triage web application designed to help patients identify relevant medical specializations and find nearby hospitals based on their reported symptoms and location. The platform also provides role-based dashboards and an SOS workflow for notifying available ambulance drivers.

**Live Demo:** [https://smart-healthcare-is62.onrender.com](https://smart-healthcare-is62.onrender.com)  
**GitHub Repository:** [vedant4122006/smart_healthcare](https://github.com/vedant4122006/smart_healthcare)  
**Docker Hub:** [pbrsearch/smart-healthcare](https://hub.docker.com/r/pbrsearch/smart-healthcare)

---

## Features

### Symptom-to-Specialty Triage

- Accepts symptom descriptions written in natural language, including common spelling mistakes and conversational phrasing.
- Normalizes symptom text and uses **RapidFuzz** fuzzy string matching to identify relevant medical specializations.
- Supports 16+ specializations, including Cardiology, Neurology, Pulmonology, Gastroenterology, Orthopedics, and Multispeciality.

### Location-Based Hospital Recommendations

- Retrieves the patient's coordinates through the browser Geolocation API, with a manual coordinate fallback.
- Uses **GeoPy** geodesic calculations to estimate the distance between the patient and registered hospitals.
- Ranks matching hospitals by distance so patients can identify nearby options.

### Interactive Maps

- Uses **Leaflet.js** and **OpenStreetMap** to display patient and hospital locations.
- Includes Street and Satellite map layers.
- Displays map markers, connecting polylines, and distance information for hospital recommendations.

### Emergency SOS Workflow

- Allows a patient to send an SOS alert from the application.
- Shares the patient's coordinates and a map link with the Ambulance Driver Dashboard.
- Supports optional email notifications through Gmail SMTP.

### Role-Based Portals

The application provides separate interfaces and workflows for:

- **Patients:** Search symptoms, review recommended hospitals, view map information, and trigger SOS alerts.
- **Ambulance Drivers:** Toggle availability and view incoming SOS alerts with patient map links.
- **Doctors:** View doctor profile information and specialization details.
- **Administrators:** Manage hospital records, equipment tags, and hospital map locations through an interactive map picker.

### Multilingual Interface

The interface includes support for:

- English
- Hindi
- Marathi

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python 3.10, Flask, Flask-SQLAlchemy |
| WSGI Server | Gunicorn |
| Database | SQLite |
| Symptom Matching | RapidFuzz, text normalization |
| Geospatial Calculations | GeoPy (geodesic distance) |
| Maps | Leaflet.js, OpenStreetMap |
| Frontend | HTML, CSS, JavaScript, Jinja2 templates |
| Containerization | Docker, Docker Compose |
| Image Registry | Docker Hub |

---

## Run with Docker

The published Docker image includes an SQLite database that is automatically seeded with 10 sample hospitals and demo accounts when the application starts.

```bash
docker pull pbrsearch/smart-healthcare:latest

docker run -d \
  --name smart_healthcare \
  -p 5000:5000 \
  pbrsearch/smart-healthcare:latest
```

Open the application in your browser:

```text
http://localhost:5000
```

To view the container logs:

```bash
docker logs -f smart_healthcare
```

To stop the container:

```bash
docker stop smart_healthcare
```

To remove the stopped container:

```bash
docker rm smart_healthcare
```

---

## Demo Accounts

The database seeder creates the following accounts for testing:

| Portal | Email | Password |
|---|---|---|
| Admin | `admin@smarthealthcare.com` | `admin123` |
| Ambulance Driver | `driver@smarthealthcare.com` | `driver123` |
| Doctor | `doctor@smarthealthcare.com` | `doctor123` |
| Patient | Register through `/register/patient` | Set during registration |

**Demo account capabilities:**

- **Admin:** Add, edit, and delete hospitals; manage equipment tags; place hospital pins using the map picker.
- **Ambulance Driver:** Change availability status and view incoming patient SOS alerts.
- **Doctor:** View the doctor profile and specialization dashboard.
- **Patient:** Search symptoms, view nearby hospital recommendations, inspect map information, and trigger an SOS alert.

> **Security note:** These are demo credentials intended for local testing. Change or disable default accounts and credentials before deploying the application for any non-demo use.

---

## Run Locally

### Option 1: Docker Compose

Clone the repository and start the development environment:

```bash
git clone https://github.com/vedant4122006/smart_healthcare.git
cd smart_healthcare
docker compose up -d --build
```

### Option 2: Python Virtual Environment

**1. Clone the repository**

```bash
git clone https://github.com/vedant4122006/smart_healthcare.git
cd smart_healthcare
```

**2. Create and activate a virtual environment**

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create the environment file**

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux / macOS:

```bash
cp .env.example .env
```

Add the required configuration values to `.env`. Gmail SMTP settings are needed only when using the optional email alert functionality. Refer to `.env.example` for the available variables.

**5. Seed the database**

```bash
python seed_admin.py
```

**6. Start the Flask application**

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Project Structure

```text
smart_healthcare/
|
|-- app.py                       # Main Flask application, routes, and coordinate parser
|-- seed_admin.py                # Seeds demo accounts and 10 sample hospitals
|-- requirements.txt             # Python dependencies
|-- Dockerfile                   # Production Gunicorn container definition
|-- docker-compose.yml            # Local development container configuration
|-- .env.example                  # Environment variable template
|
|-- models/                       # SQLAlchemy models
|   |-- User
|   |-- Doctor
|   |-- Driver
|   |-- Hospital
|   `-- Admin
|
|-- services/
|   |-- symptom_mapping.py       # Symptom-to-specialization matching engine
|   `-- notifications.py         # Optional Gmail SMTP notification service
|
|-- static/
|   `-- css/
|       `-- style.css            # Global stylesheet
|
`-- templates/                    # Jinja2 pages and Leaflet map integrations
```

---

## How the Application Works

1. A patient enters a description of their symptoms.
2. The triage service normalizes the text and uses fuzzy matching to identify relevant medical specializations.
3. The application obtains the patient's coordinates through browser geolocation or manual input.
4. Hospitals matching the identified specialization are ranked using geodesic distance.
5. The patient can inspect hospital locations and distance information on the interactive map.
6. When the patient triggers SOS, the application sends the patient's coordinates and map link to the Ambulance Driver Dashboard. Optional email notification can also be enabled.

---

## Important Notes

- Geodesic distance is a straight-line geographic distance. It is not the same as driving distance or estimated road travel time.
- Map markers and polylines are provided for location visualization; they should not be treated as verified turn-by-turn navigation.
- Browser-based location detection requires the user to grant location permission. Manual coordinate entry is available as a fallback.
- Email alerts are optional and require valid SMTP configuration.
- The live deployment may have different availability or configuration from a locally running instance.

## Disclaimer

Smart Healthcare is an educational and demonstration project. Its symptom matching, hospital recommendations, and SOS workflow are not a clinically validated medical triage or emergency dispatch service. Do not use the application as a substitute for professional medical advice or official emergency services. Do not enter real patient records or sensitive personal health information into the public demo.

---

## License

No license information has been specified for this repository. Unless a license is added, the source code should not be assumed to be available for unrestricted reuse or redistribution.
