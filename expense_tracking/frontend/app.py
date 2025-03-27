import streamlit as st
import os
import pandas as pd

from expense_tracking.frontend.dashboard_expense import  expense_dashboard_ui, get_kpi
from expense_tracking.frontend.update_expense import update_expense_ui
from expense_tracking.frontend.expenses_list import expenses_list_ui
from expense_tracking.frontend.add_expense import add_expens_ui

from dotenv import load_dotenv

from expense_tracking.utils import get_all_expense

st.set_page_config(layout="wide")

load_dotenv()
API_URL = os.getenv("BASE_URL")

st.title("💰 Expense Tracking Dashboard")
st.caption("By default the summary of all data are displayed in KPI")


expense_data = get_all_expense(API_URL)
df = pd.DataFrame(expense_data)
get_kpi(df)

tab1, tab2, tab3, tab4 = st.tabs(["Analytics","Expenses / Delete", "Add", "Update"])

with tab1:
    expense_dashboard_ui()
with tab2:
    expenses_list_ui()
with tab3:
    add_expens_ui()
with tab4:
    update_expense_ui()

