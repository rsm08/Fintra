import os 
import pandas as pd 
import streamlit as st
import base64

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

user_file = "users.csv"

# If file does not exist, create empty DataFrame
if not os.path.exists(user_file):
    users = pd.DataFrame(columns=["Name", "Username", "Password"])
    users.to_csv(user_file, index=False)
else:
    users = pd.read_csv(user_file)

# Sign-up function
def sign_up(name, username, password):
    global users
    if username in users["Username"].values:
        st.info("⚠️ Username already exists!")
        return
    new_user = pd.DataFrame([[name, username, password]], 
                            columns=["Name", "Username", "Password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(user_file, index=False)
    st.success("✅ Account Created Successfully!")

# Login function
def log_in(username, password):
    global users
    # Check username
    user_row = users[users["Username"] == username]
    if user_row.empty:
        st.error("❌ Username does not exist!")
    else:
        # Check password for that username
        if user_row.iloc[0]["Password"] != password:
            st.error("❌ Incorrect Password!")
        else:
            st.success(f"✅ Welcome {user_row.iloc[0]['Name']}!")

# Streamlit UI
st.title("🔐 Login / Signup")

menu = st.selectbox("Manage Account", ["Sign Up", "Login"])

if menu == "Sign Up":
    st.subheader("Create an Account")
    name = st.text_input("Full Name", placeholder="Enter your Full Name", key="signup_name")
    username = st.text_input("Username", placeholder="Create a Username", key="signup_username")
    password = st.text_input("Password", type="password", placeholder="Enter Password", key="signup_password")
    if st.button("Sign Up"):
        if name and username and password:
            sign_up(name, username, password)
        else:
            st.warning("⚠️ Please fill all fields!")

elif menu == "Login":
    st.subheader("Log In")
    username = st.text_input("Username", placeholder="Enter your Username", key="login_username")
    password = st.text_input("Password", type="password", placeholder="Enter Password", key="login_password")
    if st.button("Login"):
        if username and password:
            log_in(username, password)
        else:
            st.warning("⚠️ Please enter both Username and Password!")
