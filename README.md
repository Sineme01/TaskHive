# JobQueue API

A production-grade, FastAPI-based background job processing system with:
- JWT authentication for secure access
- Background task queue using Celery
- PostgreSQL for data persistence
- Redis as a message broker
- Docker for containerized development
- Swagger UI for API exploration
- Built-in rate limiting

## Getting Started

### Prerequisites
Ensure the following are installed on your system:
- Docker & Docker Compose
- Git

## Setup

```bash
git clone https://github.com/Sineme01/TaskHive.git
cd TaskHive
```

### Environment File
Create a `.env` file in the root directory:

## Running with Docker

```bash
docker-compose up --build
```

- API is accessible at: http://localhost:8000
- Swagger UI is available at: http://localhost:8000/docs

## Shutdown

```bash
docker-compose down
```