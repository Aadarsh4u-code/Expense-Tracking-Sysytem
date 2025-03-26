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

from expense_tracking.utils import select_date_range, get_filter_year_month_df

# Load Constant variables from .env file
load_dotenv()
API_URL = os.getenv("BASE_URL")

def expense_dashboard_ui():
    st.header("Expenses Tracker Dashboard")
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
            selected_year = st.selectbox(label="Select Year", options=sorted(df['year'].unique(), reverse=True), index=None)
        with col2:
            selected_month = st.selectbox(label="Select Month", options=month_order, index=None)

    # Apply filters year and month based on selected values
    df_filtered = get_filter_year_month_df(df, selected_year, selected_month)

    # Apply filter for category
    category_filter = st.sidebar.multiselect("Select Category:", options=df_filtered["category"].unique(), default=df_filtered["category"].unique())
    df_filtered = df_filtered[df_filtered["category"].isin(category_filter)]

    # Section 1: Categorical Analysis
    st.write(df_filtered)

    # Section : Time Series Analysis
    st.subheader("📊 Expense Trend Over Time")
    fig = px.line(df_filtered, x="expense_date", y="amount", title="Daily Expense Trend", markers=True)
    st.plotly_chart(fig)

    # st.write(df_filtered)
    """
    

    # Section 2: Category-Wise Spending
    st.subheader("📌 Category-Wise Expense Distribution")
    category_expense = df_filtered.groupby("Category")["Amount"].sum().reset_index()
    fig = px.pie(category_expense, names="Category", values="Amount", title="Spending by Category")
    st.plotly_chart(fig)

    # Section 3: Expense Distribution & Variability
    st.subheader("📉 Expense Distribution & Outliers")
    fig, ax = plt.subplots()
    sns.boxplot(x=df_filtered["Amount"], ax=ax)
    st.pyplot(fig)

    # Section 4: Expense Comparison & Outlier Detection
    st.subheader("🚀 Expense Comparison & Outlier Detection")
    fig = px.scatter(df_filtered, x="Date", y="Amount", color="Category", title="Outlier Detection in Expenses")
    st.plotly_chart(fig)

    # Section 5: Budget Tracking
    st.subheader("📈 Budget Utilization")
    # budget = st.sidebar.number_input("Set Monthly Budget ($)", min_value=100, max_value=10000, value=2000)
    # total_spent = df_filtered["Amount"].sum()
    # progress = total_spent / budget * 100
    # st.progress(progress / 100)
    # st.write(f"Total Spent: **${total_spent:.2f}** | Budget: **${budget:.2f}** | Utilization: **{progress:.2f}%**")

    # Section 6: Cumulative Spending Over Time
    st.subheader("⏳ Cumulative Spending Trend")
    df_filtered["Cumulative"] = df_filtered["Amount"].cumsum()
    fig = px.line(df_filtered, x="Date", y="Cumulative", title="Cumulative Expenses Over Time")
    st.plotly_chart(fig)

    # Section 7: Notes Word Cloud
    st.subheader("📝 Expense Notes Word Cloud")
    text = " ".join(df_filtered["Notes"])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    """
    # End of Streamlit App
    st.write("🚀 **Interactive Expense Dashboard with Streamlit!**")
