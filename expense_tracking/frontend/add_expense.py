import streamlit as st
from datetime import datetime
import requests
import os

from dotenv import load_dotenv
# Load Constant variables from .env file
load_dotenv()
API_URL = os.getenv("BASE_URL")

def add_expense():
    st.header("Add Expenses")
    with st.form(key = "add_form", clear_on_submit=True, border=True):
        selected_date = st.date_input(label="Select Date", value=datetime.today().date())
        categories = ["Rent", "Food", "Shopping", "Grocery", "Transportation", "Entertainment", "Other"]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        form_data = []
        for i in range(3):
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=0.0, key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, key=f"category_{i}", index=0, label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value="", key=f"notes_{i}", label_visibility="collapsed")
        
            form_data.append({
                        "amount":amount_input,
                        "category": category_input,
                        "notes": notes_input
                    })
       
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            expense_data = [data for data in form_data if data['amount'] > 0.0]
            response = requests.post(f"{API_URL}/expense/{selected_date}", json=expense_data)
            if response.status_code == 201:
                st.success(response.json()['message']) 
            else:
                st.error(response.json()['message'])
            


