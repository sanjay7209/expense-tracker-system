## Expense Management API

This project is a FastAPI -based backend for an expense management system. It provides user authentication, signup/login, and endpoints for managing and filtering expenses. The application is designed with modular architecture using Pydantic, SQLAlchemy, and OAuth2 for secure user sessions.

---

##  Features

- User signup and login with token-based authentication
- Secure password hashing and JWT tokens
- CRUD operations for expenses
- Dashboard endpoints for categorized expense summaries
- Filtering by date, category, and payment method
- Fully async FastAPI implementation
- Integrated email support (via `fastapi-mail`)
- Ready for deployment with Uvicorn

---

##  Project Structure

├── api.py # FastAPI router definitions
├── main.py # App startup and FastAPI instance
├── models.py # SQLAlchemy models
├── schemas.py # Pydantic schemas
├── database.py # Database connection and session
├── oauth2.py # JWT auth and token validation
├── master_data.py # Country, payment method, category APIs
├── requirements.txt # Dependencies
├── custom-output.log # Sample logs of API usage


---

##  How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt

2. Run the application: 
uvicorn main:app --reload

3. Access the API docs:
Visit http://localhost:8000/docs to explore available endpoints

Sample API Endpoints:

POST /Signup — Register a new user
POST /Login — Authenticate and receive JWT token
GET /DashboardExpense/{user_id} — Summary of expenses
GET /AllExpenses/{user_id}/{start_date}/{end_date} — Full expense list
POST /add_expenses — Add a new expense
POST /FilterExpense — Filter by date, category, or payment method
GET /Countries, /ExpenseCategory, /PaymentMethod — Master data endpoints

Tech Stack:

Backend: FastAPI, SQLAlchemy
Auth: OAuth2, JWT, passlib
Data Handling: Pydantic, Pandas
Server: Uvicorn
Database: PostgreSQL (or SQLite, configurable)
