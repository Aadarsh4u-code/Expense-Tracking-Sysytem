import streamlit as st
from datetime import datetime, timedelta
import requests


# Date range for sidebar - Dashboard UI
def select_date_range(deafult_range=26):
        with st.sidebar:
            st.markdown("### Select Date Range")  # Optional title in the sidebar
            col1, col2 = st.columns(2)
            today_date = datetime.today().date()
            week_back = today_date - timedelta(weeks=deafult_range)
            
            with col1:
                from_date = st.date_input(label="From", value=week_back, key=f"from_date_side")
            with col2:
                to_date = st.date_input(label="To", value=today_date, key=f"to_date_side")

        return from_date, to_date

# Extract Year, Month from expense date 
def get_filter_year_month_df(df, selected_year, selected_month):
    if selected_year and selected_month:  # Both selected
        df_filtered = df[(df["year"] == selected_year) & (df["month"] == selected_month)]
    elif selected_year:  # Only Year selected
        df_filtered = df[df["year"] == selected_year]
    elif selected_month:  # Only Month selected
        df_filtered = df[df["month"] == selected_month]
    else:  # Neither selected, show all data
        df_filtered = df
    
    return df_filtered

# Get expense data from database for selected date range
def get_expense_btn_daterange(API_URL):
    expense_data = None
    # Sidebar date range
    from_date, to_date = select_date_range()

    # Url to get data between selected date range
    response = requests.get(f"{API_URL}/expensefromtodate/?from_date={from_date}&to_date={to_date}")
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            expense_data = data

        else: 
            st.error("No data for this date range")
    else:
        st.error("Failed to retrieve expenses.")
    
    return expense_data

# Get all expense summary
def get_all_expense(API_URL):
    expense_data = None
    
    # Url to get data between selected date range
    response = requests.get(f"{API_URL}/expensesall")
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            expense_data = data
        else: 
            st.error("No data for this date range")
    else:
        st.error("Failed to retrieve expenses.")
    
    return expense_data



