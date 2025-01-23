from authlib.integrations.requests_client import OAuth2Session
import streamlit as st
from streamlit_oauth import OAuth2Component

minerva_oauth_keys = {
    'client_id': 'minerva_dev01_clinent',
    'validate_id': 'minerva_dev01_clinent',
    'client_secret': 'Kresgt87yhnly9',
    'validate_secret': 'Kresgt87yhnly9',
    'grant_type': 'Authorization Code',
    'OAuthEndpoint': 'https://devfederate.pfizer.com/as/authorization.oauth2',
    'OAuthTokenEndpoint': 'https://devfederate.pfizer.com/as/token.oauth2',
    'redirect_uri': 'https://minerva-dev01.pfizer.com/auth-redirect'  # Corrected redirect URI
}

# Configure Streamlit OAuth component
oauth_component = OAuth2Component(
    client_id=minerva_oauth_keys["client_id"],
    client_secret=minerva_oauth_keys["client_secret"],
    authorization_endpoint=minerva_oauth_keys["OAuthEndpoint"],
    token_url=minerva_oauth_keys["OAuthTokenEndpoint"],
    redirect_uri=minerva_oauth_keys["redirect_uri"],
    scopes=["edit"]  # Optional scopes (if required)
)

st.title("Minerva OAuth")

# Use Streamlit OAuth for login
if not st.session_state.get('authenticated'):
    login_info = oauth_component.login()
    if login_info:
        # User has logged in
        st.session_state['authenticated'] = True
        st.success("Successfully logged in!")

# Handle code and authentication after login
if st.session_state.get('authenticated'):
    if 'code' in st.experimental_get_query_params():
        code = st.experimental_get_query_params()['code'][0]
        token, response = validate_access_token(client_id, client_secret, redirect_uri,
                                                 authorization_base_url, token_url, code)
        if token:
            # Access token retrieved, handle user data and display authenticated content
            # ... (Your code to process user data and display content) ...
        else:
            st.write("Authentication Not Successful")
    else:
        st.write("Waiting for authorization...")

# ... (Rest of your Streamlit app logic) ...
