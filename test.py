import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------- Signup Tests ----------
def test_signup_success():
    response = client.post("/Signup", json={
        "email": "newuser@example.com",
        "password": "SecurePass123",
        "country_id": 1
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_signup_missing_fields():
    response = client.post("/Signup", json={
        "email": "user@example.com"
    })
    assert response.status_code == 422

def test_signup_invalid_email():
    response = client.post("/Signup", json={
        "email": "invalidemail",
        "password": "password",
        "country_id": 1
    })
    assert response.status_code == 422


# ---------- Login Tests ----------
def test_login_success():
    response = client.post("/Login", json={
        "email": "newuser@example.com",
        "password": "SecurePass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/Login", json={
        "email": "newuser@example.com",
        "password": "WrongPassword"
    })
    assert response.status_code == 400

def test_login_missing_fields():
    response = client.post("/Login", json={})
    assert response.status_code == 422


# ---------- Expense Tests ----------
def test_add_expense_success():
    response = client.post("/add_expenses", json={
        "user_id": 1,
        "category_id": 1,
        "amount": 50.75,
        "payment_method_id": 1,
        "description": "Test expense"
    })
    assert response.status_code == 200

def test_add_expense_invalid_amount():
    response = client.post("/add_expenses", json={
        "user_id": 1,
        "category_id": 1,
        "amount": -10,
        "payment_method_id": 1
    })
    assert response.status_code == 422


def test_all_expenses_success():
    response = client.get("/AllExpenses/1/2025-01-01/2025-12-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_all_expenses_invalid_date():
    response = client.get("/AllExpenses/1/invalid-date/2025-12-31")
    assert response.status_code == 422


def test_filter_expenses_success():
    response = client.post("/FilterExpense", json={
        "user_id": 1,
        "from_date": "2025-01-01",
        "to_date": "2025-12-31",
        "category_id": 1
    })
    assert response.status_code == 200


# ---------- Reference Data ----------
def test_get_countries():
    response = client.get("/Countries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/ExpenseCategory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_payment_methods():
    response = client.get("/PaymentMethod")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- Dashboard ----------
def test_dashboard_success():
    response = client.get("/DashboardExpense/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_dashboard_invalid_user():
    response = client.get("/DashboardExpense/99999")  # unlikely user
    assert response.status_code in (200, 404)  # depending on your implementation
