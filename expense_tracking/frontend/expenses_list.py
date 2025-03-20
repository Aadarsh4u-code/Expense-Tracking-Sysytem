import streamlit as st
from datetime import datetime, timedelta, date
import requests
import pandas as pd
import os

from dotenv import load_dotenv
# Load Constant variables from .env file
load_dotenv()

API_URL = os.getenv("BASE_URL")

def select_date_range():
    with st.container():
        col1, col2 = st.columns(2)
        today_date = datetime.today().date()
        two_week_back = today_date - timedelta(weeks=2)

        with col1:
            from_date = st.date_input(label="From", value=two_week_back, key="from_date_")
        with col2:
            to_date = st.date_input(label="To", value=today_date, key="to_date_")
    return from_date, to_date


def expenses_list_ui():
    st.header("Expenses List")
    from_date, to_date = select_date_range()
    response = requests.get(f"{API_URL}/expensefromtodate/?from_date={from_date}&to_date={to_date}")
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            data_table(data)
        else: 
            st.error("No data for this date range")
    else:
        st.error("Failed to retrieve expenses.")
        
def data_table(expense_data):

        # Initialize DataFrame in session state if not present
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(expense_data)

    # Display the table with row selection
    event = st.dataframe(
        st.session_state.df,
        hide_index=True,
        key="exp_data",
        on_select="rerun",
        selection_mode="multi-row", # Only allow row selection
        column_order=["expense_date","amount","category","notes"],
    )

    # Retrieve selected rows
    selected_rows = event.selection.get("rows", []) if event.selection else []

    # Show delete button only if rows are selected
    if selected_rows:
        if st.button(f"Delete Selected Rows ({len(selected_rows)})"):
            ids_to_delete = list(st.session_state.df.iloc[selected_rows]['id'])
            params = {"id": ids_to_delete}
            del_response = requests.post(f"{API_URL}/expense/delete/", params=params)
            if del_response.status_code == 200:
                # Get selected row indices
                selected_indices = list(selected_rows)  # Convert to list if needed
                (selected_indices)


                if del_response.status_code == 200:
                    # Drop selected rows from DataFrame
                    st.session_state.df.drop(index=selected_indices, inplace=True)
                    st.session_state.df.reset_index(drop=True, inplace=True)  # Reset index after deletion
                    st.rerun()  # Rerun script to update UI
                else:
                    st.error("Failed to delete rows. Please try again.")