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

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/fatimaryam/weather-microservice.git
