import streamlit as st
from streamlit_oauth import OAuth2Component

# Configure OAuth credentials
oauth_component = OAuth2Component(
    name="my_oauth", 
    key="your_client_id", 
    secret="your_client_secret", 
    authorize_url="https://<your_provider>/authorize", 
    token_url="https://<your_provider>/token", 
    scope="read:user",  # Adjust scope as needed
    state=None,  # Optional, for CSRF protection
    use_cookies=True 
)

if oauth_component.authorized:
    # Access user data (e.g., user ID, email)
    user_data = oauth_component.get_user_info() 
    st.write(f"Hello, {user_data['name']}!")
    # ... Rest of your app logic ...

else:
    st.write(f"Please log in: {oauth_component.login()}")
