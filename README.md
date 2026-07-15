# Project Management Dashboard

A RESTful backend service for managing projects, documents, and user access permissions.

This project is developed using **FastAPI** and follows a layered architecture. It provides authentication, project management, document storage, and project sharing functionality.

---

## 🚀 Features

- User registration and authentication (JWT)
- Create, update, and delete projects
- Upload, download, and delete project documents
- Share projects with other users
- AWS S3 integration for file storage
- AWS Lambda for project size calculation
- PostgreSQL database
- Docker support
- CI/CD with GitHub Actions

---

## 🛠️ Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker & Docker Compose
- AWS S3
- AWS Lambda
- Pytest
- GitHub Actions

---

## 📁 Project Structure

```text
project-management-dashboard/
│
├── app/
├── alembic/
├── tests/
├── lambda_functions/
├── .github/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/dilekcolak/project-management-dashboard.git
```

Go to the project directory:

```bash
cd project-management-dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the application

```bash
uvicorn app.main:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📌 Project Status

🚧 This project is currently under development.
