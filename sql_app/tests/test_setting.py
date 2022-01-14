
from fastapi.testclient import TestClient

from sql_app.config import Settings
from sql_app.main import app, get_settings

client = TestClient(app)


def get_settings_override():
    return Settings()


app.dependency_overrides[get_settings] = get_settings_override


def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "ChimichangApp",
        "admin_email": "deadpool@gmail.com",
        "items_per_user": 50,
    }
