from authlib.integrations.requests_client import OAuth2Session
import streamlit as st

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

client_id = minerva_oauth_keys["client_id"]
client_secret = minerva_oauth_keys["client_secret"]
token_url = minerva_oauth_keys["OAuthTokenEndpoint"]
authorization_base_url = minerva_oauth_keys["OAuthEndpoint"]

validate_id = minerva_oauth_keys["validate_id"]
validate_secret = minerva_oauth_keys["validate_secret"]
grant_type = minerva_oauth_keys["grant_type"]

redirect_uri = minerva_oauth_keys["redirect_uri"]
oidc_config_uri = "https://minerva-dev01.pfizer.com/.well-known/openid-configuration"
userinfo_url = "https://minerva-dev01.pfizer.com/idp/userinfo.openid"
end_session_endpoint = "https://minerva-dev01.pfizer.com/idp/startSLO.ping"
Base_UR1 = "https://minerva-dev01.pfizer.com"  # outh2 session


def get_oauth_session(client_id, client_secret, redirect_uri, authorization_base_url, token_url):
    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
    session.authorization_url = authorization_base_url
    session.token_url = token_url
    return session


# Get authorization code (**No need to call in this function anymore**)
def get_authorization_code(client_id, client_secret, redirect_uri, authorization_base_url, token_url):
    # This function was previously used to generate the authorization URL.
    # However, we can leverage Streamlit's query parameters to handle the code.
    pass


# Validate access token using authorization code
def validate_access_token(client_id, client_secret, redirect_uri, authorization_base_url, token_url, code):
    oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
    token_response = oauth.fetch_token(token_url, grant_type="authorization_code", redirect_uri=redirect_uri, code=code)
    token = token_response['access_token']

    # Validate token
    if token:
        response = oauth.post(token_url,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'},
                              data={
                                  'client_id': validate_id,
                                  'client_secret': validate_secret,
                                  'grant_type': 'urn:pingidentity.com:oauth2:grant_type:validate_bearer',
                                  'token': token
                              })
        if response.json()['access_token']['NTID']:
            return token, response
        else:
            st.write("Authentication Not Successful")
            return None, None  # Indicate failed authentication
    else:
        st.write("Failed to retrieve access token")
        return None, None  # Indicate failed authentication


st.title("Minerva OAuth")

query_params = st.experimental_get_query_params()

# Check if 'code' is present in query parameters (indicating successful authorization)
if 'code' in query_params:
    code = query_params['code'][0]
    token, response = validate_access_token(client_id, client_secret, redirect_uri,
