import streamlit as st
import pandas as pd
import base64
from Expense_tracker import Add_Income , load_income ,load_expense , initialise ,Add_expense

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
base64_image = get_base64_image("images\BG.png")
# Apply the background image using CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}") !important;
        background-size: cover;
        background-attachment: fixed;
        /*background-color: #222224;  Fallback color */

        background-position: right top;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """<style>
    [data-testid = "stSidebar"]{
        /*background: linear-gradient(to bottom ,#1B1B21, rgb(38, 39, 48), rgb(38, 39, 48), rgb(38, 39, 48),rgb(38, 39, 48) ); */
        background-color: #324731 !important; 
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
        font-size: 20px !important;   
        font-weight: 400 !important; 
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

st.title("Transaction log")
st.write("Log your daily expenses here")

with st.expander("Add new expense"):
    Date = st.date_input("select date")
    Amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")
    Category = st.selectbox("Select Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    Description = st.text_input("Enter Description")
    if st.button("Save"):
        Add_expense(Date ,Amount ,Category ,Description )
        st.dataframe(st.session_state.expense_latest , width=1200)
        st.success("The Expense Added")
        if "expense_latest" in st.session_state:
            del st.session_state.expense_latest 

load_expense()

with st.expander("Add New Income"):
    date = st.date_input("Select Date")
    amount = st.number_input("enter amount", min_value = 0.00 , format = "%.2f")
    category = st.selectbox("Select Category", ["Salary" , "Investment" , "Family" , "Other"])
    descript = st.text_input("Enter description")
    if st.button("save"):
        Add_Income(date, amount ,category , descript )
        st.dataframe(st.session_state.income_latest , width=1200)
        st.success("The Income Added")
        st.balloons()
        if "income_latest" in st.session_state:
            del st.session_state.income_latest 

load_income()




