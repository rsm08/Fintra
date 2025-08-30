import streamlit as st
from Expense_tracker import balance , initialise , filtering_expense
import base64
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Fintra",
    page_icon="images/Fintra (1).png",
    layout="wide",
)

# Function to encode the image in Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the background image
base64_image1 = get_base64_image("images\BG.png")
base64_image2 = get_base64_image("images\LOGO_2.png")
# Apply the background image using CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image1}");
        background-size: cover;
        background-attachment: fixed;
        background-color: #222224; /* Fallback color */

        background-position: right top;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)
# Custom CSS for the title
st.markdown(
    """
    <style>
    h1{
        font-size: 80px !important; 
        padding-top: 0;
        margin-top:0
        margin-bottom: 0;
        font-family: "Tiro Telugu", serif;
        font-weight: 400;
        font-style: normal;
        color:rgb(250, 244, 203) !important;
    }
    .centered-title {
        text-align: center; 
        font-weight: bold;
    }
    </style>
    <h1 class="centered-title">Fintra</h1>
    <h3 class="centered-title">Your Personal Finance Tracker</h3>
    """,
    unsafe_allow_html=True
)
# Custom CSS to position the image in the top-right corner
st.markdown(
    f"""
    <style>
    .top-right-image{{
        position: fixed;
        margin-top:50px;
        margin-left: 300px;
        top: 10px;
        left: 10px;
        z-index: 9999; 
    }}
    </style>
    <img src="data:image/png;base64,{base64_image2}" class="top-right-image" width="100">
    """,
    unsafe_allow_html=True
)
st.markdown(
    """<style>
    [data-testid = "stSidebar"]{
        /*background: linear-gradient(to bottom ,#1B1B21, rgb(38, 39, 48), rgb(38, 39, 48), rgb(38, 39, 48),rgb(38, 39, 48) ); */
        background-color: #324731; /* Fallback color */
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Custom CSS to increase sidebar height
st.markdown("""
    <style>
    /* Sidebar nav items (page names) */
    div[data-testid="stSidebarNav"] li a {
        font-size: 25px !important;   
        font-weight: 600 !important; 
        padding: 5px 5px !important;
    }

    /* Hover effect */
    div[data-testid="stSidebarNav"] li a:hover {
        background-color: #3a3a3a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)


initialise()
balance()

col1 , col2 = st.columns(2)
with col1:
    st.subheader("Average Expense")
    x= pd.to_datetime(st.session_state.expense_full["Date"])
    if not st.session_state.expense_full.empty:
        monthly_avg_expense = st.session_state.expense_full.groupby(x.dt.strftime("%B"))['Amount'].sum()
        av_exp = monthly_avg_expense.mean()
        st.markdown(av_exp)
    else:
        st.write("No expense data available.")
with col2:
    st.subheader("Average Income")
    if not st.session_state.income.empty:
        monthly_avg_income = st.session_state.income.groupby(pd.to_datetime(st.session_state.income["Date"]).dt.strftime("%B"))['Amount'].sum()
        av_inc = monthly_avg_income.mean()
        st.markdown(av_inc)
    else:
        st.write("No income data available.")        


current_datetime = datetime.now()
current_month_name = current_datetime.strftime("%B")
st.subheader(f"Budget Status for {current_month_name}")

budget = st.number_input("Enter Your budget for this month")
    
if budget>st.session_state.expense_full[pd.to_datetime(st.session_state.expense_full["Date"]).dt.strftime("%B") == current_month_name]["Amount"].sum():
    st.success("You are within your budget!")
else:
    st.error("⚠️You have exceeded your budget!")
    
    
    # .stApp {
    #     background: linear-gradient(to bottom, rgb(14, 17, 23),rgb(14, 17, 23),rgb(14, 17, 23),#033015);
    # }


