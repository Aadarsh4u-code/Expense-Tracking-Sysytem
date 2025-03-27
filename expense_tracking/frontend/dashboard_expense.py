import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
import uuid

from expense_tracking.frontend.chart_components import budget_tracking_and_cumulative_spending, expense_category, expense_distribution_and_outlier, expense_trend
from expense_tracking.utils import get_expense_btn_daterange, get_filter_year_month_df

# Load Constant variables from .env file
load_dotenv()
API_URL = os.getenv("BASE_URL")

def expense_dashboard_ui():

    # Get Expense data from database based on selected date range
    expense_data = get_expense_btn_daterange(API_URL)

    if expense_data is not None:
        # Convert data in Pandas Dataframe
        df = pd.DataFrame(expense_data)
        df.sort_values(by="expense_date", ascending=False, inplace=True)
        # Extract Year/Month
        df["date"] = pd.to_datetime(df["expense_date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month_name()


        # Define the correct month order (Jan–Dec)
        month_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

        # Sidebar Filters
        st.sidebar.header("Filters")

        # Sidebar Filter for Year and Month
        with st.sidebar:
            col1, col2 = st.columns(2)
            with col1:
                selected_year = st.selectbox(label="Select Year", options=sorted(df['year'].unique(), reverse=True), index=None, key=f"year_")
            with col2:
                selected_month = st.selectbox(label="Select Month", options=month_order, index=None, key=f"month_")

        # Apply filters year and month based on selected values
        df_filtered_year_month = get_filter_year_month_df(df, selected_year, selected_month)

        # Apply filter for category
        category_filter = st.sidebar.multiselect("Select Category:", options=df_filtered_year_month["category"].unique(), default=df_filtered_year_month["category"].unique())
        df_filtered_category = df_filtered_year_month[df_filtered_year_month["category"].isin(category_filter)]
        
        df_filtered = df_filtered_category.copy()

        # Categorical Analysis
        expense_category(df_filtered)

        # Time Series Analysis
        expense_trend(df_filtered)

        # Expense distribution and Outlier
        expense_distribution_and_outlier(df_filtered)

        # Budget tracking and cumulative spending over time
        budget_tracking_and_cumulative_spending(df_filtered)

       



def get_kpi(df):
    # Extract Year/Month
    df["date"] = pd.to_datetime(df["expense_date"])
    df["year"] = df["date"].dt.year
    # df["month"] = df["date"].dt.strftime("%b")
    df["month"] = df["date"].dt.month_name()

    # KPI Calculations
    total_expense = df["amount"].sum()
    highest_category = df.groupby("category")["amount"].sum().idxmax()
    highest_month = df.groupby("month")["amount"].sum().idxmax()
    average_monthly_expense = df.groupby("month")["amount"].sum().mean()

    a, b = st.columns(2)
    c, d = st.columns(2)

    a.metric("💰 Total Expense", f"${total_expense:,.2f}", border=True,)
    b.metric("📌 Top Category", highest_category, border=True)
    c.metric("📆 Highest Spending Month", highest_month, border=True)
    d.metric("📊 Avg Monthly Expense", f"${average_monthly_expense:,.2f}", border=True)
   
# st.write("🚀 **Interactive Expense Dashboard with Streamlit!**")
