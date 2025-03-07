import streamlit as st
import socket

def login_form():
    
    placeholder = st.empty()
    actual_email = "ndasilvaW10"
    actual_password = "1234"

    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")      

        # Get the hostname of the machine
        machine_name = socket.gethostname()

        st.write(f"Machine Name: {machine_name}")
        email = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and email == actual_email and password == actual_password:
        placeholder.empty()
        return True
    elif submit:
        st.error("Login failed")
    return False
