import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db, Weather
from sqlalchemy.exc import IntegrityError
import requests

# Setup the database for testing
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/weather_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Setup code before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown code after each test
    Base.metadata.drop_all(bind=engine)

def test_weather_success():
    # Mock successful API response
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.json_data = {
                    "main": {"temp": 25.5},
                    "weather": [{"description": "clear sky", "icon": "01d"}]
                }
            def json(self):
                return self.json_data
        return MockResponse()
    
    requests.get = mock_get  # Override requests.get with the mock

    response = client.post("/weather", json={"latitude": 32.9256, "longitude": 72.4701})
    assert response.status_code == 200
    assert response.json() == {
        "temperature": 25.5,
        "description": "clear sky",
        "icon": "01d"
    }

def test_weather_failure():
    # Mock failed API response
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 404
                self.json_data = {"message": "city not found"}
            def json(self):
                return self.json_data
        return MockResponse()
    
    requests.get = mock_get  # Override requests.get with the mock

    response = client.post("/weather", json={"latitude": 32.9256, "longitude": 72.4701})
    assert response.status_code == 404
    assert response.json() == {"detail": "Weather API request failed."}

def test_database_insertion():
    # Test if data is inserted into the database
    response = client.post("/weather", json={"latitude": 32.9256, "longitude": 72.4701})
    assert response.status_code == 200

    # Check if the data is correctly inserted
    db = TestingSessionLocal()
    weather_entry = db.query(Weather).first()
    assert weather_entry is not None
    assert weather_entry.coordinates == {"longitude": 72.4701, "latitude": 32.9256}
    assert weather_entry.temperature == 25.5
    assert weather_entry.description == "clear sky"
    assert weather_entry.icon == "01d"
    db.close()

