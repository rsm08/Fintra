import streamlit as st
import pandas as pd 
import plotly.express as px
from Expense_tracker import initialise, balance , Add_expense , Add_Income, filtering_expense, show_expense, show_income
import base64
import plotly.graph_objects as go

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
st.title("Report")
st.write("Visual representation of your income and expenses")

col1 , col2 = st.columns(2)
with col1:
    if not st.session_state.expense_full.empty:
        d = pd.to_datetime(st.session_state.expense_full["Date"])
        c = d.dt.strftime("%B").unique()
        y = st.session_state.expense_full.groupby(d.dt.strftime("%B"))["Amount"].sum().reset_index()
        fig_category_bar = px.bar(y, x='Date', y='Amount', title='Total Expense by Month', color='Amount', color_continuous_scale=px.colors.sequential.RdBu , barmode = "group" , labels = {"Date" : "Month" , "Amount" : "Total Amount"})
        st.plotly_chart(fig_category_bar)
    else:
        st.write("No expense data available to show the chart.")

with col2 :
    if not st.session_state.expense_full.empty:
        y = st.session_state.expense_full.groupby("Category")["Amount"].sum().reset_index()
        fig_expense_pie = px.pie(y, values='Amount', names='Category', title='Total Expense by Category', color_discrete_sequence=px.colors.sequential.RdBu, hole=0.4)
        st.plotly_chart(fig_expense_pie)
    else:
        st.write("No expense data available to show the chart.")

c1 , c2 = st.columns(2)

with c1 :
    if not st.session_state.expense_full.empty and not st.session_state.income.empty:
        d1 = pd.to_datetime(st.session_state.expense_full["Date"])
        d2 = pd.to_datetime(st.session_state.income["Date"])
        stacked_data = pd.concat([
            st.session_state.expense_full.groupby(d1.dt.strftime("%B"))["Amount"].sum().reset_index().assign(Type='Expense'),
            st.session_state.income.groupby(d2.dt.strftime("%B"))["Amount"].sum().reset_index().assign(Type='Income')      
        ])
        fig_stacked_bar = px.bar(stacked_data, x='Date', y='Amount', color='Type', title='Stacked Monthly Income vs Expense', barmode='stack', color_discrete_map={'Income': 'green', 'Expense': 'red'}, labels={"Date": "Month", "Amount": "Total Amount"})
        st.plotly_chart(fig_stacked_bar)
    else:
        st.write("Insufficient data to show the chart.")
with c2:
        if not st.session_state.expense_full.empty and not st.session_state.income.empty:
            d1 = pd.to_datetime(st.session_state.expense_full["Date"])
            d2 = pd.to_datetime(st.session_state.income["Date"])
            stacked_data = pd.concat([
                st.session_state.expense_full.groupby(d1.dt.strftime("%B"))["Amount"].sum().reset_index().assign(Type='Expense'),
                st.session_state.income.groupby(d2.dt.strftime("%B"))["Amount"].sum().reset_index().assign(Type='Income')      
            ])
            fig = px.area(stacked_data, x='Date', y='Amount', color='Type', title='Monthly Expense vs Income Trend', line_group = "Type", markers =True , labels={"Date": "Month", "Amount": "Total Amount"})
            st.plotly_chart(fig)
        else:
            st.write("Insufficient data to show the chart.")

column1 , column2 = st.columns(2)
with column1:
    if not st.session_state.income.empty:
        y = st.session_state.income.groupby("Category")["Amount"].sum().reset_index()
        figure = px.pie(y , values='Amount',names='Category', title='Total Income by Category', color_discrete_sequence=px.colors.sequential.RdBu )
        st.plotly_chart(figure)
    else:
        st.write("Insufficient data to show the chart.")

with column2:
    if not st.session_state.income.empty:
        d = pd.to_datetime(st.session_state.income["Date"])
        y = st.session_state.income.groupby(d.dt.strftime("%Y"))["Amount"].sum().reset_index()
        fig = px.line( y , x = "Date" , y = "Amount" , title = "Yearly Income Incrementation" , labels = {"Date" : "Year" , "Amount" : "Total Amount" })
        st.plotly_chart(fig)
    else:
        st.write("Insufficient data to show the chart.")


fig = go.Figure([go.Scatter(x=st.session_state.expense_full['Date'], y=st.session_state.expense_full.groupby("Category")['Amount'].sum(), mode='lines+markers', name='Cumulative Expense' , marker=dict(size=10, color='Red') , line=dict(width=2, color='DarkSlateGrey'))])
st.plotly_chart(fig)
