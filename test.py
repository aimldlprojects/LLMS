# Hardcoded credentials (replace these with your actual credentials)
valid_username = "user123"
valid_password = "password123"

# Streamlit app layout
def main():
    st.title("Login Page")

    # Sidebar for login
    with st.sidebar:
        login()

# Login form
def login():
    st.subheader("Login")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login Successful!")
            # Add redirection or other actions after successful login
        else:
            st.error("Invalid credentials. Please try again.")

# Authentication function
def authenticate(username, password):
    return username == valid_username and password == valid_password
