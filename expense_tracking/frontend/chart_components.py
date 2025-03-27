import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def expense_category(df_filtered):
    # Group data by category and calculate totals
    category_totals = df_filtered.groupby("category")["amount"].sum().reset_index()
    category_totals = category_totals.sort_values(by="amount", ascending=False)  # Sort descending

    # Compute percentage
    total_amount = category_totals["amount"].sum()
    category_totals["percentage"] = (category_totals["amount"] / total_amount) * 100

    a, b = st.columns(2)
    with a:
        # Bar Chart
        st.subheader("1. Total Expenses by Category")
        fig = px.bar(
            category_totals, 
            x="category", 
            y="amount", 
            color="category",
            labels={"amount": "Total Amount", "category": "Expense Category"},
            title="",
        )

        # Display Outputs in Streamlit
        st.plotly_chart(fig)  # Show bar chart
    
    with b:
        st.subheader("2. Expense Summary")
        # Show table with formatted values
        st.dataframe(category_totals.style.format({"amount": "{:,.2f}", "percentage": "{:.2f}%"}), hide_index=True, use_container_width=True)  

def expense_trend(df_filtered):
    a, b = st.columns(2)
    with a:
        st.subheader("3. Cumulative Expenses Over Time")
        df_filtered["Cumulative"] = df_filtered["amount"].cumsum()
        fig = px.line(df_filtered, x="date", y="Cumulative", title="Cumulative Expenses Over Time")
        st.plotly_chart(fig)
    with b:
        st.subheader("4. Expense Proportion")
        # Section 2: Category-Wise Spending
        category_expense = df_filtered.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(category_expense, names="category", values="amount", title="")
        st.plotly_chart(fig)

def expense_distribution_and_outlier(df_filtered):
     
    a, b = st.columns(2)
    with a:
        # Section 3: Expense Distribution & Variability
        st.subheader("5. Expense Distribution & Outliers")
        fig, ax = plt.subplots()
        sns.boxplot(x=df_filtered["amount"], ax=ax)
        st.pyplot(fig)

    with b:
        # Section 4: Expense Comparison & Outlier Detection
        st.subheader("6. Outlier Detection in Expenses")
        fig = px.scatter(df_filtered, x="date", y="amount", color="category", title="")
        st.plotly_chart(fig)

def budget_tracking_and_cumulative_spending(df_filtered):

    a, b = st.columns(2)
    with a:
        # Section 5: Budget Tracking
        st.subheader("7. Budget Utilization")
        budget = st.sidebar.number_input("Set Monthly Budget ($)", min_value=100, max_value=10000, value=2000)
        total_spent = df_filtered["amount"].sum()
        progress = min(total_spent / budget, 1.0)
        st.progress(progress)
        st.write(f"Total Spent: **${total_spent:.2f}** | Budget: **${budget:.2f}** | Utilization: **{progress:.2f}%**")
    
    with b:
        # Section 6: Notes Word Cloud
        st.subheader("📝 Expense Notes Word Cloud")
        text = " ".join(df_filtered["notes"])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)