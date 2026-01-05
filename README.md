# Xovate Data Validation Engine

A professional, full-stack data validation platform built with FastAPI, Pandas, and React. This project demonstrates a production-grade monorepo architecture with containerized services.

## Architecture & Design Decisions

### 1. Robust Validation Engine (Backend)
- **Pandas/Regex Hybrid**: Instead of simple loops, the engine uses Pandas for high-performance ingestion and Regex for strict data integrity checks (e.g., distinguishing between "30" and "30yrs").
- **Stateless Validation**: The `/validate` endpoint is purely functional, ensuring scalability and ease of testing.
- **Structured Error Schema**: Uses Pydantic to enforce a consistent JSON structure, allowing the frontend to render precise row-level feedback.

### 2. Premium UX (Frontend)
- **Glassmorphism**: A modern UI style using backdrop-filters and gradients to create a premium feel.
- **Responsive Architecture**: Built with Vite and TypeScript for sub-second hot-reloading and type safety.
- **User-Centric Feedback**: Separate handling for global errors (e.g., volume checks) and row-level errors (e.g., invalid age format), providing clear actionable insights.

### 3. Containerization Strategy
- **Multi-stage Builds**: Both frontend and backend Dockerfiles use multi-stage builds to keep production images lean by excluding build dependencies.
- **Orchestration**: `docker-compose` handles service discovery and networking.

## Quick Start

### Prerequisites
- Docker & Docker Compose

### Run the application
```bash
docker-compose up --build
```
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Sample Data
Provided in the `data/` directory:
- `test_data_clean.csv`: 15 valid rows (should pass).
- `test_data_dirty.csv`: Multiple data quality issues (should fail with details).
- `test_data_sample.csv`: < 10 rows (should fail volume check).

## Assumptions
- The first row is always the header.
- `row_index` 1 refers to the first data row (Excel style).
- Valid age is strictly an integer between 18 and 100. Strings like "30yrs" are treated as invalid formats rather than being coerced, to maintain data integrity.
