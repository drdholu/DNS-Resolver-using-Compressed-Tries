# DNS Resolver with Compressed Trie

A small full-stack project that demonstrates how a DNS resolver can be built on top of a compressed trie for fast look-ups while persisting results on disk.  The Flask backend exposes a simple HTTP API, and a React + Vite frontend lets you query domains and visualise the trie in real time.

## Tech Stack

- **Backend:** Python 3.11, Flask, Gunicorn
- **Data structure:** Custom compressed trie (`backend/ct.py`)
- **Storage:** JSON file via `DNSStorage`
- **Frontend:** React 18, Vite, Tailwind CSS
- **Containerisation:** Docker & Docker Compose, Nginx (serves the built frontend)

## API Overview

| Method | Endpoint                | Description                                 |
| ------ | ----------------------- | ------------------------------------------- |
| GET    | `/resolve?domain=`      | Resolve a domain; fetches and stores if new |
| POST   | `/store`                | Store a randomly generated IP for a domain  |
| GET    | `/trie`                 | Return the current trie structure           |

The backend listens on port **5000** inside the container.

## Project Structure

```
backend/          # Flask API, compressed trie, storage layer
frontend/         # React UI that consumes the API and renders the trie
Dockerfile.*      # Image definitions for each service
docker-compose.yml
```

## Getting Started

### Prerequisites

- Docker and Docker Compose 1.29+ installed

> Prefer a manual setup? See “Running locally without Docker” below.

### Quick Start (Docker)

```bash
git clone <repository-url>
cd dnsResolver
# build images and start both services
docker compose up --build
```

Once the containers are ready:

- Frontend: http://localhost:8080  
- Backend API: http://localhost:5000

### Running locally without Docker

Backend (Flask):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py   # runs on http://127.0.0.1:5000
```

Frontend (React/Vite):

```bash
cd frontend
npm install
npm run dev      # by default on http://localhost:5173
```

## Example API Usage

```bash
# Resolve a domain
curl "http://localhost:5000/resolve?domain=google.com"

# Store a random IP for a domain
curl -X POST -H "Content-Type: application/json" \
     -d '{"domain":"example.com"}' \
     http://localhost:5000/store

# Retrieve the current trie
curl http://localhost:5000/trie
```

## Deployment Notes

The provided Dockerfiles are production-ready:

- `Dockerfile.backend` installs only run-time dependencies and serves the app via Gunicorn.
- `Dockerfile.frontend` uses a multi-stage build; Nginx serves the static bundle.

Deploy the stack anywhere Docker is available:

```bash
docker compose up -d --build
```

## License

This project is open-sourced under the MIT license (see `LICENSE` if present).