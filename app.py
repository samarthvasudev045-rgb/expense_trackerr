import streamlit as st
from expense import Expense
from utils import add_expense, view_expenses
from analytics import analyze_expenses_df
from ai_insights import generate_insights
from finance_api import get_stock_data
from db import create_table

create_table()

st.set_page_config(page_title="Expense Tracker AI", layout="wide")
st.title("💰 Smart Expense Tracker AI")

menu = st.sidebar.selectbox(
    "Menu", ["Add Expense", "View Expenses", "Analytics", "AI Insights", "Finance"]
)

# ➤ Add Expense
if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Title")
        amount = st.number_input("Amount", min_value=0.0)

    with col2:
        category = st.text_input("Category")
        date = st.date_input("Date")

    if st.button("Add Expense"):
        exp = Expense(title, amount, category, str(date))
        add_expense(exp)
        st.success("Expense added!")

# ➤ View Expenses
elif menu == "View Expenses":
    st.subheader("📋 All Expenses")
    data = view_expenses()
    st.dataframe(data)

# ➤ Analytics
elif menu == "Analytics":
    st.subheader("📊 Analytics")
    df = analyze_expenses_df()

    if not df.empty:
        st.dataframe(df)
        st.bar_chart(df.groupby("category")["amount"].sum())
    else:
        st.warning("No data available")

# ➤ AI Insights
elif menu == "AI Insights":
    st.subheader("🤖 AI Insights")

    df = analyze_expenses_df()

    if not df.empty:
        if st.button("Generate Insights"):
            with st.spinner("Thinking..."):
                insights = generate_insights(df)
                st.write(insights)
    else:
        st.warning("No data available")

# ➤ Finance
elif menu == "Finance":
    st.subheader("📈 Stock Market")

    ticker = st.text_input("Enter stock (e.g., AAPL, TSLA, INFY.NS)")
    if st.button("Fetch Data"):
        df = get_stock_data(ticker)

        if df is not None and not df.empty:
            st.line_chart(df["Close"])
        else:
            st.error("Invalid ticker")
