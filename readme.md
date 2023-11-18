# Log Ingestion and Monitoring

## Specifications

This project demonstrates a log ingestion and searching service. 

Backend: Python FastAPI
<br>
Frontend: React, Typescript
<br>
Database: Postgres

Celery is used for asynchronous log ingestion.

## Docker

Docker needs to be installed. Run this command to get started:
```commandline
docker-compose up --build
```

## How to use

Go to http://localhost:3000/docs to view the backend APIs
![img.png](backend.png)
Go to http://localhost:8000 to view the frontend searching service
![img_1.png](ui.png)