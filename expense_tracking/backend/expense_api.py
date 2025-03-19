from fastapi import FastAPI, Query
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class Expense(BaseModel):
    id: int
    expense_date: date
    amount: float
    category: str
    notes: str

class AddExpense(BaseModel):
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

@app.get("/expensefromtodate/", response_model=List[Expense])
def get_expenses_for_date_between(from_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
                                to_date: date = Query(..., description="End date (YYYY-MM-DD)")):
    expense = database_helper.fetch_expenses_for_date_between(from_date, to_date)
    return expense

@app.post("/expense/{expense_date}")
def add_expenses(expense_date: date, expenses: List[AddExpense]):
    for expense in expenses:
        database_helper.insert_expenses(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses added sucessfully"}

@app.post("/expense/delete/")
def delete_expenses(id: List[int] = Query(..., description="list of id")):
    database_helper.delete_expenses_item(id)
    return {"message": "Expenses deleted sucessfully"}