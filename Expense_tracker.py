import streamlit as st
import pandas as pd
from streamlit import file_uploader

def initialise():
    if "expense_full" not in st.session_state:
        st.session_state.expense_full = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    if "expense_latest" not in st.session_state:
        st.session_state.expense_latest = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    if "filtered_expense" not in st.session_state:
        st.session_state.filtered_expense = pd.DataFrame()
    if "income" not in st.session_state:
        st.session_state.income = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    if "income_latest" not in st.session_state:
        st.session_state.income_latest = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    if "filtered_income" not in st.session_state:
        st.session_state.filtered_income = pd.DataFrame()

def Add_expense(d,a,c,de):
    new_exp= pd.DataFrame({
        "Date": [d],
        "Amount": [a],
        "Category": [c],
        "Description": [de]
    })
    st.session_state.expense_full = pd.concat([st.session_state.expense_full, new_exp], ignore_index=True)
    st.session_state.expense_latest = pd.concat([st.session_state.expense_latest, new_exp], ignore_index=True)

def load_expense():
    initialise()
    f = file_uploader("Upload Expense File", type=["csv", "xlsx" , "xlsm"])
    if f is not None:
        if f.name.endswith('.csv'):
            if st.session_state.expense_full.empty:
                st.session_state.expense_full = pd.read_csv(f)
            else:
                new_data = pd.read_csv(f)
                st.session_state.expense_full = pd.concat([st.session_state.expense_full, new_data], ignore_index=True)
        elif f.name.endswith('.xlsx'):
            if st.session_state.expense_full.empty:
                st.session_state.expense_full = pd.read_csv(f)
            else:
                new_data = pd.read_excel(f)
                st.session_state.expense_full = pd.concat([st.session_state.expense_full, new_data], ignore_index=True)
        elif f.name.endswith('.xlsm'):
            if st.session_state.expense_full.empty:
                st.session_state.expense_full = pd.read_csv(f)
            else:
                new_data = pd.read_excel(f , engine='openpyxl')
                st.session_state.expense_full = pd.concat([st.session_state.expense_full, new_data], ignore_index=True)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.success("Expense data loaded successfully.")

def filtering_expense():
    initialise()
    st.markdown("## Expenses by Month")
    month = st.selectbox("Select Month",['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December'])
    x = pd.to_datetime(st.session_state.expense_full["Date"])
    st.session_state.filtered_expense = st.session_state.expense_full[x.dt.strftime("%B") == month]
    st.dataframe(st.session_state.filtered_expense ,width=1200)
    st.subheader(f"Total Expense in {month}: {st.session_state.filtered_expense['Amount'].sum() if not st.session_state.filtered_expense.empty else 0.0}")

def show_expense():
    if st.button("Delete all Expense"):
        del st.session_state.expense_full
        initialise()
    st.dataframe(st.session_state.expense_full , width=1200)
    st.subheader(f"Total Expense : {st.session_state.expense_full["Amount"].sum() if not st.session_state.expense_full.empty else 0.0}")

def Add_Income(d ,a , c, de):
    new_inc = pd.DataFrame({
        "Date":[d],
        "Amount":[a],
        "Category":[c],
        "Description":[de]
    })
    st.session_state.income = pd.concat([st.session_state.income, new_inc], ignore_index=True)
    st.session_state.income_latest = pd.concat([st.session_state.income_latest, new_inc], ignore_index=True)

def load_income():
    initialise()
    fi = st.file_uploader("Upload Income File", type=["csv", "xlsx" , "xlsm","xlm"])
    if fi is not None:
        if fi.name.endswith('.csv'):
            if st.session_state.income.empty:
                st.session_state.income = pd.read_csv(fi)
            else:
                new_data = pd.read_csv(fi)
                st.session_state.income = pd.concat([st.session_state.income, new_data], ignore_index=True)
        elif fi.name.endswith('.xlsx'):
            if st.session_state.income.empty:
                st.session_state.income = pd.read_excel(fi)
            else:
                new_data = pd.read_excel(fi)
                st.session_state.income = pd.concat([st.session_state.income, new_data], ignore_index=True)
        elif fi.name.endswith('.xlsm'):
            if st.session_state.income.empty:
                st.session_state.income = pd.read_excel(fi , engine='openpyxl')
            else:
                new_data = pd.read_excel(fi)
                st.session_state.income = pd.concat([st.session_state.income, new_data], ignore_index=True)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.success("Income data loaded successfully.")
def filtering_income():
    initialise()
    st.markdown("## Income by Month")
    month = st.selectbox("Select Month",['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December'])
    x = pd.to_datetime(st.session_state.income["Date"])
    st.session_state.filtered_income = st.session_state.income[x.dt.strftime("%B") == month]
    st.dataframe(st.session_state.filtered_income ,width=1200)
    st.subheader(f"Total Income in {month}: {st.session_state.filtered_income['Amount'].sum() if not st.session_state.filtered_income.empty else 0.0}")

def show_income():
    if st.button("Delete all Income"):
        del st.session_state.income
        initialise()
    st.dataframe(st.session_state.income , width=1200)
    st.subheader(f"Total Income : {st.session_state.income['Amount'].sum() if not st.session_state.income.empty else 0.0}")
        

def balance():
    total_expense = st.session_state.expense_full["Amount"].sum() if not st.session_state.expense_full.empty else 0.0
    total_income = st.session_state.income['Amount'].sum() if not st.session_state.income.empty else 0.0
    total_balance = total_income - total_expense
    st.subheader(f"Total Balance : {total_balance}")
    if total_balance == 0:
        st.error("Your balance is zero. Please check your income and expenses.")
    elif total_balance<1000:
        st.warning("Low balance alert!⚠️ Your balance has dropped⬇ under ₹1000⬇")
    else:
        st.success("Your balance is healthy! Keep it up! 👍")

        
