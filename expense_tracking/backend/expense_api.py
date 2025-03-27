from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from expense_tracking.backend import database_helper
from expense_tracking.logger import logging

logger = logging.getLogger('expense_api')
class GetExpense(BaseModel):
    id: int
    expense_date: date
    amount: float
    category: str
    notes: str

class AddExpense(BaseModel):
    amount: float
    category: str
    notes: str
class UpdateExpense(BaseModel):
    expense_id: Optional[int]
    expense_date: date
    amount: float
    category: str
    notes: Optional[str] = None


# Creating an instance of FastAPI
app = FastAPI()

# Get all expenses.
@app.get("/expensesall", response_model=List[GetExpense])
def get_all_expenses_summary():
    expense = database_helper.fetch_all_record()
    if expense is None:
        raise HTTPException(status_code=500, detail="Failed to retrive expense data from the database.")
    return expense

# Get expenses for given date.
@app.get("/expense/{expense_date}", response_model=List[GetExpense])
def get_expenses_for_date(expense_date: date, ):
    expense = database_helper.fetch_expenses_for_date(expense_date)
    return expense

# Get expenses for given Id.
@app.get("/expense/{id}", response_model=GetExpense)
def get_expense_by_id(id: int):
    expense = database_helper.fetch_expenses_for_id(id)
    return expense

# Get expenses for given date range.
@app.get("/expensefromtodate/", response_model=List[GetExpense])
def get_expenses_for_date_between(from_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
                                to_date: date = Query(..., description="End date (YYYY-MM-DD)")):
    expense = database_helper.fetch_expenses_for_date_between(from_date, to_date)
    if expense is None:
        raise HTTPException(status_code=500, detail="Failed to retrive expense data from the database.")
    return expense

# Add expenses for given date.
@app.post("/expense/{expense_date}")
def add_expenses(expense_date: date, expenses: List[AddExpense]):
    for expense in expenses:
        database_helper.insert_expenses(expense_date, expense.amount, expense.category, expense.notes)
    return JSONResponse(status_code=201, content={"message": "Expense added successfully!"})

# Delete expenses for given date.
@app.post("/expense/delete/")
def delete_expenses(id: List[int] = Query(..., description="list of id")):
    database_helper.delete_expenses_item(id)
    return {"message": "Expenses deleted sucessfully"}

@app.put("/expense/{expense_id}")
def update_expense(expense_id: int, expenses: UpdateExpense):
    logging.info(f"Updating expense with ID {expense_id}")
    database_helper.update_expenses_for_id(expense_id, expenses.expense_date, expenses.amount, expenses.category, expenses.notes)
    return JSONResponse(status_code=202, content={"message": "Expense updated successfully!"})


