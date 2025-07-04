from typing import Optional,List,Union
from enum import IntEnum
from pydantic import BaseModel, PositiveFloat
from datetime import datetime, date, time


class Baseentity(BaseModel):
    created_by : Optional[int] 
    created_at : Optional[datetime]
    modified_by : Optional[int]
    modified_at : Optional[datetime]
    comments : Optional[str]= None
    status : Optional[int] = None


class TokenData(BaseModel):
    user_id: Optional[str]= None
    role_id: Optional[str]=  None
    access_token : Optional[str]= None


class UserLogin(BaseModel):
    username :str
    password :str


class PasswordChange(BaseModel):
    user_id : int	
    new_password :str


class Signup(BaseModel):
    username :str
    first_name :str
    middle_name :Optional[str]= None
    last_name :str
    email :str
    password :str
    role_id :Optional[int]= None
    country_id :Optional[int]= None


class UpdateUser(BaseModel):
    id :int
    username :str
    first_name :str
    middle_name :Optional[str]= None
    last_name :str
    email :str
    country_id :Optional[int]= None


class Category(BaseModel):
    id :int
    name :str
    

class AddExpense(BaseModel):
    user_id :int	
    category_id :int	
    payment_method : Optional[int]= None	
    amount :PositiveFloat	
    description : Optional[str]= None	
    date :date

class UpdateExpense(BaseModel):
    id :int
    user_id :int	
    category_id :int	
    payment_method : Optional[int]= None	
    amount :PositiveFloat	
    description : Optional[str]= None	
    date :date

class Expense(BaseModel):
    id :int
    user_id :int	
    category_id :int	
    payment_method : Optional[int]= None	
    amount :float	
    description : Optional[str]= None	
    date :date

    category :  Optional[Category]



class FilterExpense(BaseModel):
    user_id :int
    start_date :date
    end_date :date
    category_id :Optional[int]= None