from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import JSON
import requests
import logging
from typing import Optional

# Configuration
API_KEY = "9e26b6849844370389437ea21e9b334c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/weather_db"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class WeatherData(BaseModel):
    temperature: float
    description: str
    icon: str

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    coordinates = Column(JSON, nullable=False)
    temperature = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/weather", response_model=WeatherData)
async def get_weather(coordinates: Coordinates, db: Session = Depends(get_db)):
    """
    Fetches weather data for given coordinates using OpenWeatherMap API and stores it in the database.
    """
    url = f"{BASE_URL}?lat={coordinates.latitude}&lon={coordinates.longitude}&appid={API_KEY}&units=metric"  # Convert temperature to Celsius
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        weather = Weather(
            coordinates={"longitude": coordinates.longitude, "latitude": coordinates.latitude},
            temperature=data['main'].get('temp', None),
            description=data['weather'][0].get('description', 'No description available'),
            icon=data['weather'][0].get('icon', 'No icon available')
        )
        db.add(weather)
        db.commit()
        db.refresh(weather)

        logger.info(f"Weather data stored successfully: {weather}")

        return WeatherData(
            temperature=weather.temperature,
            description=weather.description,
            icon=weather.icon
        )

    except requests.HTTPError as e:
        logger.error(f"API request failed: {e}")
        raise HTTPException(status_code=response.status_code, detail="Weather API request failed.")
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        raise HTTPException(status_code=503, detail="Weather API request failed due to network error.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

