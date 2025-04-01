import streamlit as st

st.set_page_config(
    page_title="FinSight Pro",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main {background-color: #f5f5f5;}
        .css-18e3th9 {padding: 2rem;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 FinSight Pro - Real-Time Investment Dashboard")
st.subheader("Welcome to the future of portfolio intelligence.")
st.markdown("<div style='text-align: center; color: grey; font-size: 16px;'>Created by <b>ABIODUN ADEBAYO</b></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Use the sidebar to navigate between tools.")
