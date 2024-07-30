# Weather Microservice

This project implements a weather microservice using FastAPI, SQLAlchemy, and the OpenWeatherMap API. The service fetches weather data for given coordinates, stores it in a PostgreSQL database, and provides the data to clients.

## Features

- **API Endpoint:** `/weather` for fetching weather data.
- **Database Integration:** Utilizes SQLAlchemy to interact with a PostgreSQL database.
- **OpenWeatherMap API Integration:** Retrieves weather data based on coordinates.
- **Error Handling:** Gracefully handles API and network errors.
- **Logging:** Logs API requests, database interactions, and errors.
- **Testing:** Includes unit tests using `pytest` for API endpoints and database interactions.

## Getting Started

### Prerequisites

- Docker
- Docker Compose (bundled with Docker Desktop)


### Create and Activate Python Virtual Environment:
python3 -m venv env
source env/bin/activate

### Install Dependencies:

pip install -r requirements.txt

### Get API Key from OpenWeatherMap:

Create an account at OpenWeatherMap.
Navigate to the API keys section and generate a new API key.
Add your API key to the configuration in main.py.

### Creating main.py

### Testing the Endpoint with Uvicorn:

uvicorn main:app --reload

### Docker Configuration:

Create Dockerfile
Create docker-compose.yml

### Build and Start the Project:

docker-compose build
docker-compose up -d

### Test the Endpoint:

Use Postman or curl to send a POST request to http://localhost:8000/weather with JSON body:
{
  "latitude": 35.6895,
  "longitude": 139.6917
}
or 
Run Tests with Pytest:
pytest

 **Clone the Repository:**
   ```bash
   git clone https://github.com/fatimaryam/weather-microservice.git
