import streamlit as st
import requests

# Streamlit app title and header
st.title("OpenAI Playground")

# Input controls
prompt = st.text_area("Enter your prompt:", "Which drugs are used for red eye")

max_new_tokens = st.slider("Max New Tokens", min_value=1, max_value=1000, value=512)
top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.8, step=0.1)

# Button to generate text
if st.button("Generate Text"):
    # API endpoint and parameters
    api_endpoint = "YOUR_API_ENDPOINT"  # Replace with your actual API endpoint
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Payload
    payload = {
        "inputs": [
            [{"role": "user", "content": prompt}]
        ],
        "parameters": {"max_new_tokens": max_new_tokens, "top_p": top_p, "temperature": temperature},
    }

    # Make API request
    response = requests.post(api_endpoint, headers=headers, json=payload)

    # Display generated text
    if response.status_code == 200:
        generated_text = response.json()[0]["generation"]["content"]
        st.subheader("Generated Text:")
        st.write(generated_text)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
