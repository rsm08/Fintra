import streamlit as st
import pandas as pd
import base64
from Expense_tracker import initialise
from Expense_tracker import show_income , filtering_income
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
st.title("View Income")

with st.expander("Delete Particular Income"):
    num = st.number_input("Select Income ID to delete", min_value=0)
    if st.button("Delete"):
        st.session_state.income.drop(num,axis = 0 , inplace = True)
        st.session_state.income.reset_index(drop = False , inplace = False)
show_income()
filtering_income()
