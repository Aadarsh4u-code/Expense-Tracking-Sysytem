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

# Date range for sidebar - Dashboard UI
def select_date_range(range=26):
        with st.sidebar:
            st.markdown("### Select Date Range")  # Optional title in the sidebar
            col1, col2 = st.columns(2)
            today_date = datetime.today().date()
            week_back = today_date - timedelta(weeks=range)
            
            with col1:
                from_date = st.date_input(label="From", value=week_back, key="from_date_")
            with col2:
                to_date = st.date_input(label="To", value=today_date, key="to_date_")

        return from_date, to_date

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