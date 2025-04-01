import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load config from Streamlit secrets if available, else from local file
if "config" in st.secrets:
    config = yaml.load(st.secrets["config"], Loader=SafeLoader)
else:
    try:
        with open("config.yaml") as file:
            config = yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        st.error("⚠️ No config.yaml file or secret found.")
        st.stop()

# Authenticate
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Show login/signup options
auth_option = st.sidebar.radio("Choose Action", ["Login", "Create Account"])

if auth_option == "Create Account":
    st.subheader("🔐 Create Your FinSight Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if new_password != confirm_password:
            st.warning("Passwords do not match.")
        elif new_username in config['credentials']['usernames']:
            st.warning("Username already exists.")
        else:
            hashed_pw = stauth.Hasher([new_password]).generate()[0]
            config['credentials']['usernames'][new_username] = {
                "name": new_username,
                "password": hashed_pw
            }

            # Save to local file (note: cloud version won't persist)
            with open("config.yaml", "w") as file:
                yaml.dump(config, file)

            st.success("✅ Account created! Please go to Login.")
            st.info("Note: This account won't persist on cloud unless connected to a real database.")

elif auth_option == "Login":
    st.subheader("🔐 Login to FinSight")
    name, auth_status, username = authenticator.login(location="sidebar")

    if auth_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.success(f"Welcome, {name} 👋")
        st.title("📊 FinSight Pro - Real-Time Investment Dashboard")
        st.subheader("Welcome to the future of portfolio intelligence.")
        st.markdown(
            "<div style='text-align: center; color: grey; font-size: 16px;'>Created by <b>ABIODUN ADEBAYO</b></div>",
            unsafe_allow_html=True
        )
        # 🔽 Add your main dashboard content here

    elif auth_status is False:
        st.error("Incorrect username or password.")
    elif auth_status is None:
        st.warning("Please enter your credentials.")
