import streamlit as st
from lamma2 import  *

# Hardcoded credentials (replace these with your actual credentials)
valid_username = "user123"
valid_password = "password123"

# Set page configuration
st.set_page_config(page_title="Multi-Page App with Login")

# Streamlit app layout
def main():
    st.title("Multi-Page App with Login")

    # Check if the user is authenticated
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # If not authenticated, show the login page
    if not st.session_state.authenticated:
        login()
    else:
        # If authenticated, show the content for authenticated users
        chatbot_app1()

# Login form
def login():
    st.subheader("Login")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            # Navigate to the next screen (chatbot_app)
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# Authentication function
def authenticate(username, password):
    return username == valid_username and password == valid_password

# Content for authenticated users
def chatbot_app1():
    chatbot_app()
if __name__ == "__main__":
    main()