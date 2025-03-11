from fastapi import FastAPI
from datetime import date
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount: float
    category: str
    notes: str



from expense_tracking.backend import database_helper

# Creating an instance of FastAPI
app = FastAPI()

@app.get("/expense/{expense_date}", response_model=List[Expense])
def get_expenses_for_date(expense_date: date, ):
    expense = database_helper.fetch_expenses_for_date(expense_date)
    return expense

@app.post("/expense/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    for expense in expenses:
        database_helper.insert_expenses(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated sucessfully"}

