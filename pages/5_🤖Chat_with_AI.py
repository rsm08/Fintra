import streamlit as st
import base64
from Expense_tracker import initialise
# from langchain_openai import ChatOpenAI
# from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv
import cohere
import os

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

st.markdown("<h1 style='text-align:center; color:#FFF;'>💬 Ask Finbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#DDD;'>Ask about your expenses, savings, or budgeting tips</p>", unsafe_allow_html=True)
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
load_dotenv()
api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

def get_budget_insights(user_query, transaction_text):
    prompt = f"""User query: {user_query}\n Transaction text: {transaction_text}\n You are a Finbot , a financial AI assistant developed by Ritika for the Fintra , A Finance tracker app and Respond to user, Your job is **ONLY** to assist users with their **financial queries** , including budgeting, expense tracking, and say "I can only assist with financial-related questions. Please ask me something about your finances." if user ask about making changes his expenses or income to delete or add , simply respond:""I can assist you with the process but I can not directly make changes"". if the user asks about **yourself** , simply respond: "I am Finbot , a financial assistant built by Ritika to help with budgeting and expense management . """
    response = co.chat(
        model="command-r-plus", 
        message=prompt
    )
    return response.text.strip()

with st.expander("💬 Chat with Finbot", expanded = True):
    st.markdown("<h3>Hi 👋 How can I help you today?</h3>", unsafe_allow_html=True)
    # ---------- Quick Preset Questions ----------
    st.markdown("**💡 Quick Questions:**")
    cols = st.columns(3)
    preset_questions = [
        "💰What is the Total Expense of this month?",
        "How much I spended on food🍔?",
        "How can I Improve my Savings💵?"
    ]
    triggered = False
    for i, q in enumerate(preset_questions):
        if cols[i].button(q):
            transactions_text = ""
            
            if "expense_full" in st.session_state and not st.session_state.expense_full.empty:
                expense_text = "\n".join(st.session_state.expense_full.apply(
                    lambda row: f"Expense -> {row['Date']} | {row['Category']} | {row['Amount']} | {row['Description']}", axis=1
                ))
                transactions_text += "Expenses:\n" + expense_text + "\n\n"

            if "income" in st.session_state and not st.session_state.income.empty:
                income_text = "\n".join(st.session_state.income.apply(
                    lambda row: f"Income -> {row['Date']} | {row['Category']} | {row['Amount']} | {row['Description']}", axis=1
                ))
                transactions_text += "Income:\n" + income_text + "\n\n"

            if transactions_text.strip():
                with st.spinner("🤖 Finbot is thinking..."):
                    budget_tip = get_budget_insights(q, transactions_text)
                    st.text_area("💬 Finbot says:", value=budget_tip, height=200)
                    triggered = True
            else:
                st.warning("⚠️No transaction data available yet!")
                transactions_text = ""

    if not triggered:
        st.info("Select a question above or ask your own below ✍️.")


    user_query = st.text_input("Enter your question: ")

    if st.button("Send▶"):
        if user_query.strip():
            transactions_text = ""
            
            if "expense_full" in st.session_state and not st.session_state.expense_full.empty:
                expense_text = "\n".join(st.session_state.expense_full.apply(
                    lambda row: f"Expense -> {row['Date']} | {row['Category']} | {row['Amount']} | {row['Description']}", axis=1
                ))
                transactions_text += "Expenses:\n" + expense_text + "\n\n"

            if "income" in st.session_state and not st.session_state.income.empty:
                income_text = "\n".join(st.session_state.income.apply(
                    lambda row: f"Income -> {row['Date']} | {row['Category']} | {row['Amount']} | {row['Description']}", axis=1
                ))
                transactions_text += "Income:\n" + income_text + "\n\n"

            if transactions_text.strip():
                with st.spinner("🤖 Finbot is thinking..."):
                    budget_tip = get_budget_insights(q, transactions_text)
                    st.text_area("💬 Finbot says:", value=budget_tip, height=200)
            else:
                st.warning("⚠️No transaction data available yet!")
                transactions_text = ""
        else:
            st.warning("Please Enter valid question.")
    st.markdown("---")
st.markdown("<p style='text-align:center; color:#AAA;'>Made with ❤️ by Ritika</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#AAA;'>© 2024 Fintra</p>", unsafe_allow_html=True)
    

