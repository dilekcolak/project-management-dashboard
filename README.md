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

- Python 3.12+
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

## 🗄️ Database Design

The application uses a PostgreSQL relational database designed according to Third Normal Form (3NF).

The database consists of four main entities:

- Users
- Projects
- Project Members
- Documents

## 📊 Database Schema

The following Entity Relationship Diagram (ERD) illustrates the PostgreSQL database design and relationships between the tables.

![Database Schema](docs/database-schema.png)

## 📚 Database Normalization

The database schema follows Third Normal Form (3NF).

### First Normal Form (1NF)

- Every table has a primary key.
- Every column contains atomic values.
- No repeating groups or multi-value attributes exist.

### Second Normal Form (2NF)

- Every non-key attribute depends on the entire primary key.
- User, project, membership, and document information are separated into different tables.

### Third Normal Form (3NF)

- Non-key attributes depend only on the primary key.
- Duplicate information is avoided by using foreign keys.
- Project membership is implemented through the `project_members` junction table to resolve the many-to-many relationship between users and projects.

## 🧪 Running Tests

```bash
pytest
```

---

## 📌 Project Status

🚧 This project is currently under development.
