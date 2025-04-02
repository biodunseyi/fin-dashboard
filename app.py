from supabase import create_client, Client
import streamlit as st
import bcrypt
import os

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set Streamlit page config
st.set_page_config(page_title="FinSight Pro", layout="wide")
st.title("📊 FinSight Pro - Real-Time Investment Dashboard")
st.subheader("Welcome to the future of portfolio intelligence.")
st.markdown("<div style='text-align: center; color: grey; font-size: 16px;'>Created by <b>ABIODUN ADEBAYO</b></div>", unsafe_allow_html=True)

# Auth logic
auth_action = st.sidebar.radio("Choose Action", ["Login", "Create Account"])

if auth_action == "Create Account":
    st.subheader("🔐 Create Your FinSight Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if password != confirm:
            st.warning("❌ Passwords do not match.")
        elif username.strip() == "":
            st.warning("❌ Username cannot be empty.")
        else:
            # Check if user already exists
            res = supabase.table("users").select("*").eq("username", username).execute()
            if res.data:
                st.warning("❌ Username already exists.")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                supabase.table("users").insert({"username": username, "password": hashed_pw}).execute()
                st.success("✅ Account created! Please go to Login to access your dashboard.")

elif auth_action == "Login":
    st.subheader("🔐 Login to Your FinSight Account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login"):
        if username.strip() == "":
            st.warning("❌ Please enter a username.")
        else:
            res = supabase.table("users").select("*").eq("username", username).execute()
            user = res.data[0] if res.data else None

            if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
                st.success(f"Welcome, {username} 👋")
                st.sidebar.success(f"Logged in as {username}")
                st.session_state.logged_in = True

                # Add your dashboard logic here 👇
                st.markdown("### 📈 Dashboard goes here...")

            else:
                st.error("❌ Incorrect username or password.")
