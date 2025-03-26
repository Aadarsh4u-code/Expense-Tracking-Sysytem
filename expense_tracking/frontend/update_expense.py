import streamlit as st
from datetime import datetime, timedelta, date
import requests
import pandas as pd
import os

from dotenv import load_dotenv

# Load Constant variables from .env file
load_dotenv()

API_URL = os.getenv("BASE_URL")
today_date = datetime.today().date()

def update_expense_ui():
    st.header("Update Your Expenses")
    selected_date = st.date_input(label="Select date", value=today_date, key="expense_date")
    
    # Fetch expenses from API
    response = requests.get(f"{API_URL}/expense/{str(selected_date)}")
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            selected_rows = data_table(data)
            st.session_state["selected_rows"] = selected_rows  # Store selection
        else: 
            st.error("No expense for this date")
            st.session_state["selected_rows"] = []
    else:
        st.error("Failed to retrieve expenses.")
        st.session_state["selected_rows"] = []

    # Show update form only if a row is selected
    if "selected_rows" in st.session_state and (len(st.session_state["selected_rows"]) > 0):
        show_update_form()

def data_table(expense_data):

    # Initialize DataFrame in session state if not present
    if "to_update_df" not in st.session_state:
        st.session_state.to_update_df = pd.DataFrame(expense_data)

    # Display the table with row selection
    event = st.dataframe(
        st.session_state.to_update_df,
        hide_index=True,
        key="to_update_df_data",
        on_select="rerun",
        selection_mode="single-row", # Only allow row selection
        column_order=["expense_date","amount","category","notes"],
    )

    # Retrieve selected rows
    selected_rows = event.selection.get("rows", []) if event.selection else []
    return selected_rows
    

    # Function to show the update form
def show_update_form():
    st.subheader("Edit Selected Expense")

    # Get selected row data
    selected_row_index = st.session_state["selected_rows"][0]  # Get first selected row
    data_to_update = st.session_state.to_update_df.iloc[selected_row_index].to_dict()

    categories = ["Rent", "Food", "Shopping", "Grocery", "Transportation", "Entertainment", "Other"]

    with st.form(key="update_form", clear_on_submit=True, border=True):
        date_input = st.date_input("Expense Date", value=data_to_update['expense_date'], key="update_expense_date")
        amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=data_to_update['amount'], key="amount")
        category_input = st.selectbox("Category", options=categories, index=categories.index(data_to_update['category']), key="category")
        notes_input = st.text_input("Notes", value=data_to_update['notes'], key="notes")

        submit_button = st.form_submit_button("Update")

        if submit_button:
            updated_data = {
                "expense_id": data_to_update['id'],
                "expense_date": str(date_input),
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            }

            # Send updated data to API
            response = requests.put(f"{API_URL}/expense/{updated_data['expense_id']}", json=updated_data)

            if response.status_code == 202:
                st.success("Expense updated successfully!")

                # Clear selection and close form
                st.session_state["selected_rows"] = []
                st.session_state.to_update_df.iloc[selected_row_index] = updated_data  # Update local DF
                st.rerun()  # Refresh the UI
            else:
                st.error("Failed to update expense.")

        
