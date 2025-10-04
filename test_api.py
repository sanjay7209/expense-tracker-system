import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ------------------------------
# SIGNUP TESTS
# ------------------------------
def test_signup_success():
    response = client.post("/Signup", json={
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
        "password": "SecurePass123",
        "country_id": 1,
        "role_id": 1,
        "is_admin": False
    })
    assert response.status_code == 200


def test_signup_missing_fields():
    response = client.post("/Signup", json={
        "email": "incomplete@example.com",
        "password": "password123"
    })
    assert response.status_code == 422


def test_signup_invalid_email():
    response = client.post("/Signup", json={
        "username": "baduser",
        "first_name": "Bad",
        "last_name": "Email",
        "email": "not-an-email",
        "password": "password123",
        "country_id": 1,
        "is_admin": False
    })
    assert response.status_code == 422


# ------------------------------
# LOGIN TESTS
# ------------------------------
def test_login_success():
    # Ensure user exists
    client.post("/Signup", json={
        "username": "loginuser",
        "first_name": "Login",
        "last_name": "User",
        "email": "login@example.com",
        "password": "SecurePass123",
        "country_id": 1,
        "is_admin": False
    })
    response = client.post("/Login", json={
        "email": "login@example.com",
        "password": "SecurePass123"
    })
    assert response.status_code == 200


def test_login_wrong_password():
    response = client.post("/Login", json={
        "email": "login@example.com",
        "password": "WrongPassword"
    })
    assert response.status_code == 400


def test_login_missing_fields():
    response = client.post("/Login", json={"email": "user@example.com"})
    assert response.status_code == 422


# ------------------------------
# EXPENSES TESTS
# ------------------------------
def test_add_expense_success():
    # Ensure user exists
    client.post("/Signup", json={
        "username": "expenseuser",
        "first_name": "Expense",
        "last_name": "User",
        "email": "expense@example.com",
        "password": "SecurePass123",
        "country_id": 1,
        "is_admin": False
    })
    response = client.post("/add_expenses", json={
        "user_id": 1,
        "category_id": 1,
        "amount": 50.75,
        "payment_method_id": 1,
        "description": "Test expense",
        "date": "2025-01-15T00:00:00"
    })
    assert response.status_code == 200


def test_add_expense_invalid_amount():
    response = client.post("/add_expenses", json={
        "user_id": 1,
        "category_id": 1,
        "amount": "not-a-number",
        "payment_method_id": 1,
        "description": "Invalid expense",
        "date": "2025-01-15T00:00:00"
    })
    assert response.status_code == 422


def test_all_expenses_success():
    response = client.get("/AllExpenses/1/2025-01-01/2025-12-31")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "expenses" in data
    assert "category_spent" in data


def test_all_expenses_invalid_date():
    response = client.get("/AllExpenses/1/invalid-date/2025-12-31")
    assert response.status_code == 422


def test_filter_expenses_success():
    response = client.post("/FilterExpense", json={
        "user_id": 1,
        "from_date": "2025-01-01T00:00:00",
        "to_date": "2025-12-31T23:59:59",
        "category_id": 1
    })
    assert response.status_code == 200


# ------------------------------
# MASTER DATA TESTS
# ------------------------------
def test_get_countries():
    response = client.get("/Countries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_categories():
    response = client.get("/Categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_payment_methods():
    response = client.get("/PaymentMethods")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ------------------------------
# DASHBOARD TESTS
# ------------------------------
def test_dashboard_success():
    # Ensure user exists
    client.post("/Signup", json={
        "username": "dashuser",
        "first_name": "Dash",
        "last_name": "User",
        "email": "dash@example.com",
        "password": "SecurePass123",
        "country_id": 1,
        "is_admin": False
    })
    response = client.get("/DashboardExpense/1")
    assert response.status_code == 200


def test_dashboard_invalid_user():
    response = client.get("/DashboardExpense/9999")
    assert response.status_code == 404
