from expense_tracking.backend import database_helper


def test_fetch_all_record():
    expense = database_helper.fetch_all_record()
    assert len(expense) == 56

def test_fetch_expenses_for_date():
    expense = database_helper.fetch_expenses_for_date("2024-08-03")
    assert len(expense) == 5
    assert expense[0]['amount'] == 100
    assert expense[0]['category'] == "Food"
    assert expense[0]['notes'] == "Dinner at a restaurant"

def test_fetch_expenses_for_date_between():
    expense = database_helper.fetch_expenses_for_date_between("2024-08-05", "2024-09-05")
    assert len(expense) == 30
    assert expense[0]['amount'] == 350
    assert expense[0]['category'] == "Rent"
    assert expense[0]['notes'] == "Shared rent payment"


