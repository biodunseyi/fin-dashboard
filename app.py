import streamlit as st
from supabase import create_client, Client
import bcrypt
import os

# Load from Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Set app layout
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
            st.warning("Passwords do not match.")
        elif username.strip() == "":
            st.warning("Username cannot be empty.")
        else:
            # Check if user exists
            res = supabase_client.table("users").select("*").eq("username", username).execute()
            if res.data:
                st.warning("Username already exists.")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                supabase_client.table("users").insert({"username": username, "password": hashed_pw}).execute()
                st.success("✅ Account created! Please go to Login.")

elif auth_action == "Login":
    st.subheader("🔐 Login to Your FinSight Account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login"):
        if username.strip() == "":
            st.warning("Enter a username.")
        else:
            res = supabase_client.table("users").select("*").eq("username", username).execute()
            user = res.data[0] if res.data else None

            if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
                st.success(f"Welcome, {username} 👋")
                st.sidebar.success(f"Logged in as {username}")
                st.session_state.logged_in = True

                # Add your dashboard logic here 👇
                st.markdown("### 📈 Dashboard goes here...")

            else:
                st.error("Incorrect username or password.")