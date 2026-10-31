# test_app.py
from app import app
from services.symptom_mapping import match_specialty

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_home_page_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_symptom_matching_logic():
    assert "Cardiology" in match_specialty("severe chest pain")
    assert "Gastroenterology" in match_specialty("not feeling good in stomach")
