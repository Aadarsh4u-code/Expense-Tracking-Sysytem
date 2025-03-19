import streamlit as st

from expense_tracking.frontend.expenses_list import expenses_list_ui
from expense_tracking.frontend.add_expense import add_expense

st.title("Expense Tracking System")

tab1, tab2, tab3, tab4 = st.tabs(["Expenses / Delete", "Add", "Update", "Analytics"])

with tab1:
    expenses_list_ui()
    
with tab2:
    add_expense()
    pass
with tab3:
    # update_expense()
    pass
with tab4:
    # analytics_expense()
    pass