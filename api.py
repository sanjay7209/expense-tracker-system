from typing import List, Optional
from fastapi import status, Depends, APIRouter,HTTPException, status
from matplotlib.dates import relativedelta
from sqlalchemy import  func,and_,or_,any_
from sqlalchemy.exc import IntegrityError  
from fastapi.exceptions import HTTPException
import models, schemas, oauth2
from sqlalchemy.orm import Session 
from database import get_db
import datetime
from datetime import  date, time, timedelta

from sqlalchemy import func, extract
from datetime import date, timedelta


api_router = APIRouter(tags=["API"])



@api_router.post("/Login")
async def login(obj: schemas.UserLogin,
    db:Session = Depends(get_db)
    ):
    user = db.query(models.User).filter(or_(func.lower(models.User.username) == obj.username.lower().strip(), func.lower(models.User.email) == obj.username.lower().strip()) ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.password != obj.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "email": user.email,
        "last_login_at": user.last_login_at,
        "country_id": user.country_id,
        "country": user.country.name,
        "role_id": user.role_id,    
        "is_admin": user.is_admin,
    }

@api_router.post("/ChangePassword")
async def change_password(obj: schemas.PasswordChange,
    db:Session = Depends(get_db)
    ):
    user = db.query(models.User).filter(models.User.id == obj.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.password == obj.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be same as old password")
    
    user.password = obj.new_password
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "Password changed successfully"}


@api_router.get("/ExpenseCategory")
async def get_expense_categories(
    db:Session = Depends(get_db)
    ):
    return db.query(models.ExpenseCategory).order_by(models.ExpenseCategory.name).all()

@api_router.get("/PaymentMethod")
async def get_payment_methods(
    db:Session = Depends(get_db)
    ):
    return db.query(models.PaymentMethod).order_by(models.PaymentMethod.type).all()

@api_router.get("/Countries")
async def get_countries(
    db:Session = Depends(get_db)
    ):
    return db.query(models.Country).order_by(models.Country.name).all()


@api_router.get("/Users")
async def get_users(
    db:Session = Depends(get_db)
    ):
    return db.query(models.User).order_by(models.User.username.asc()).all()


@api_router.post("/Signup")
async def signup(obj: schemas.Signup,
    db:Session = Depends(get_db)
    ):

    user_name_exists = db.query(models.User).filter(func.lower(models.User.username) == obj.username.lower().strip()).first()

    if user_name_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User name already exists")

    user_email_exists = db.query(models.User).filter(func.lower(models.User.email) == obj.email.lower().strip()).first()

    if user_email_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User email already exists")
    
    user = models.User(
        username=obj.username,
        first_name=obj.first_name,
        middle_name=obj.middle_name,
        last_name=obj.last_name,
        email=obj.email,
        password=obj.password,
        country_id=obj.country_id,
        role_id=obj.role_id,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@api_router.get("/UserbyId/{user_id}")
async def get_user_by_id(user_id:int,
    db:Session = Depends(get_db)
    ):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "email": user.email,
        "last_login_at": user.last_login_at,
        "country_id": user.country_id,
        "country": user.country.name,
        "role_id": user.role_id,
        "is_admin": user.is_admin,
        "role": user.role.name if user.role else None
    }



@api_router.post("/updateUser")
async def update_user(obj : schemas.UpdateUser,
    db:Session = Depends(get_db)
    ):
    user = db.query(models.User).filter(models.User.id == obj.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.username = obj.username
    user.first_name = obj.first_name
    user.middle_name = obj.middle_name
    user.last_name = obj.last_name
    user.email = obj.email
    user.country_id = obj.country_id

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "User updated successfully"}

@api_router.post("/add_expenses")
async def add_expenses(obj: schemas.AddExpense,
    db:Session = Depends(get_db)
    ):

    category = db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == obj.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if obj.payment_method:
        payment_method = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == obj.payment_method).first()
        if not payment_method:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
        

    expense = models.Expense(
        user_id=obj.user_id,
        category_id=obj.category_id,
        payment_method=obj.payment_method,
        amount=obj.amount,
        description=obj.description,
        date=obj.date
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    
    return {"message": "Expense added successfully"}


@api_router.put("/update_expense")
async def update_expense(obj : schemas.UpdateExpense,
    db:Session = Depends(get_db)
    ):

    expense = db.query(models.Expense).filter(models.Expense.id == obj.id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    category = db.query(models.ExpenseCategory).filter(models.ExpenseCategory.id == obj.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if obj.payment_method:
        payment_method = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == obj.payment_method).first()
        if not payment_method:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")

    expense.user_id = obj.user_id
    expense.category_id = obj.category_id
    expense.payment_method = obj.payment_method
    expense.amount = obj.amount
    expense.description = obj.description
    expense.date = obj.date

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {"message": "Expense updated successfully"}


@api_router.get("/expense/{id}")
async def get_expense_by_id(id:int,
    db:Session = Depends(get_db)
    ):
    expense = db.query(models.Expense.id,
                       models.Expense.user_id,
                       models.Expense.amount,
                       models.Expense.date,
                       models.Expense.category_id,
                       models.Expense.payment_method,
                       models.Expense.description,
                       models.ExpenseCategory.name.label("category_name"),
                       models.PaymentMethod.type.label("payment_method_name")
                       ).join(
                           models.ExpenseCategory, models.Expense.category_id == models.ExpenseCategory.id
                       ).outerjoin(
                           models.PaymentMethod, models.Expense.payment_method == models.PaymentMethod.id
                       ).filter(models.Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    

    return {
        "id": expense.id,
        "user_id": expense.user_id,
        "amount": expense.amount,
        "date": expense.date,
        "category_id": expense.category_id,
        "category_name": expense.category_name,
        "description": expense.description,
        "payment_method_id": expense.payment_method,
        "payment_method_name": expense.payment_method_name
    }


@api_router.get("/AllExpenses/{user_id}/{start_date}/{end_date}")
async def get_all_expenses(user_id: int, start_date: date, end_date: date, db: Session = Depends(get_db)):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be greater than end date"
        )

   
    expenses = db.query(
        models.Expense.id,
        models.Expense.user_id,
        models.Expense.amount,
        models.Expense.date,
        models.Expense.category_id,
        models.Expense.payment_method,
        models.Expense.description,
        models.ExpenseCategory.name.label("category_name"),
        models.PaymentMethod.type.label("payment_method_name")
    ).join(
        models.ExpenseCategory, models.Expense.category_id == models.ExpenseCategory.id
    ).outerjoin(
     models.PaymentMethod, models.Expense.payment_method == models.PaymentMethod.id   
    ).filter(
        models.Expense.user_id == user_id,
        models.Expense.date.between(start_date, end_date)
    ).order_by(models.Expense.date.desc()).all()

 
    expenses_list = [
        {
            "id": exp.id,
            "user_id": exp.user_id,
            "amount": exp.amount,
            "date": exp.date,
            "description": exp.description,
            "category_id": exp.category_id,
            "category_name": exp.category_name,
            "payment_method_id": exp.payment_method,
            "payment_method_name": exp.payment_method_name
        }
        for exp in expenses
    ]

 
    category_spent = db.query(
        models.Expense.category_id,
        models.ExpenseCategory.name.label("category_name"),
        func.sum(models.Expense.amount).label("total_spent")
    ).join(
        models.ExpenseCategory, models.Expense.category_id == models.ExpenseCategory.id
    ).filter(
        models.Expense.user_id == user_id,
        models.Expense.date.between(start_date, end_date)
    ).group_by(
        models.Expense.category_id, models.ExpenseCategory.name
    ).all()


    total_spent = sum(cat.total_spent for cat in category_spent)


    category_spent_with_percentage = [
        {
            "category_id": cat.category_id,
            "category_name": cat.category_name,
            "total_spent": cat.total_spent,
            "percentage_spent": round((cat.total_spent / total_spent) * 100, 2) if total_spent > 0 else 0
        }
        for cat in category_spent
    ]

    return {
        "expenses": expenses_list,
        "category_spent": category_spent_with_percentage
    }





@api_router.post("/FilterExpense")
async def filter_expense(obj : schemas.FilterExpense, db: Session = Depends(get_db)):
    if obj.start_date and obj.end_date and obj.start_date > obj.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be greater than end date"
        )

   
    query = db.query(
        models.Expense.id,
        models.Expense.user_id,
        models.Expense.amount,
        models.Expense.date,
        models.Expense.category_id,
        models.Expense.payment_method,
        models.Expense.description,
        models.ExpenseCategory.name.label("category_name"),
        models.PaymentMethod.type.label("payment_method_name")
    ).join(
        models.ExpenseCategory, models.Expense.category_id == models.ExpenseCategory.id
    ).outerjoin(
     models.PaymentMethod, models.Expense.payment_method == models.PaymentMethod.id   
    ).filter(
        models.Expense.user_id == obj.user_id,
        models.Expense.category_id == obj.category_id if obj.category_id else True

    ).order_by(models.Expense.date.desc())
    if obj.start_date and obj.end_date:
        query = query.filter(models.Expense.date.between(obj.start_date, obj.end_date))

    results = query.all()
    total_amount_spent = sum(exp.amount for exp in results)
 
    expenses_list = [
        {
            "id": exp.id,
            "user_id": exp.user_id,
            "amount": exp.amount,
            "date": exp.date,
            "description": exp.description,
            "category_id": exp.category_id,
            "category_name": exp.category_name,
            "payment_method_id": exp.payment_method,
            "payment_method_name": exp.payment_method_name
        }
        for exp in results
    ]

 
    return {
        "expenses": expenses_list,
        "total_amount_spent": total_amount_spent if results else 0

    }


def get_past_12_months(first_day_of_current_month):
    past_12_months = []
    for i in range(12):
        month_date = first_day_of_current_month - relativedelta(months=i)
        past_12_months.append((month_date.year, month_date.month))
    past_12_months.reverse()
    return past_12_months

@api_router.get("/DashboardExpense/{user_id}")
async def dashboard_expense(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    today = date.today()
    first_day_of_current_month = datetime.datetime.today()
    print(first_day_of_current_month)

    last_12_months = get_past_12_months(first_day_of_current_month)

    first_day_of_previous_12_months = date(last_12_months[0][0], last_12_months[0][1], 1)

    expenses_by_month_category = (
        db.query(
            extract('year', models.Expense.date).label("year"),
            extract('month', models.Expense.date).label("month"),
            models.Expense.category_id,
            models.ExpenseCategory.name.label("category_name"),
            func.sum(models.Expense.amount).label("total_spent")
        ).join(
            models.ExpenseCategory, models.Expense.category_id == models.ExpenseCategory.id
        )
        .filter(
            models.Expense.user_id == user_id,
            models.Expense.date >= first_day_of_previous_12_months, 
            models.Expense.date < first_day_of_current_month,  
        )
        .group_by("year", "month", "category_id", "category_name")
        .order_by("year", "month")
        .all()
    )

  
    expense_dict = {}
    for year, month, category_id, category_name, total_spent in expenses_by_month_category:
        expense_dict.setdefault((year, month), {})[category_name] = float(total_spent)


    month_wise_expenses = []
    for year, month in last_12_months:
        categories = expense_dict.get((year, month), {})
        month_wise_expenses.append({
            "year": year,
            "month": month,
            "total_spent": sum(categories.values()), 
            "category_wise_spending": [{"category_name": category_name, "total_spent": amount} for category_name, amount in categories.items()]
        })

    category_wise_spending = db.query(
        models.ExpenseCategory.name.label("category_name"),
        func.sum(models.Expense.amount).label("total_spent")
    ).join( 
        models.Expense, models.Expense.category_id == models.ExpenseCategory.id
    )\
    .filter(
        models.Expense.user_id == user_id,
        models.Expense.date >= first_day_of_previous_12_months, 
        models.Expense.date < first_day_of_current_month,
    ).group_by("category_name").order_by("total_spent").all()

    category_spending = [{"category_name": category_name, "total_spent": total_spent} for category_name, total_spent in category_wise_spending ] 
    return {"user_id": user_id, "monthly_expenses": month_wise_expenses, "category_spending": category_spending}
