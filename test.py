import streamlit as st
import boto3
import json

# Set page layout
st.set_page_config(layout="wide")

# Streamlit app title and header
st.title("OpenAI Playground")

# Define columns for layout
col1, col2 = st.beta_columns([3, 1])  # Adjust the ratio as needed

# Input controls in the left column
with col1:
    prompt = st.text_area("Enter your prompt:", "Which drugs are used for red eye")

    max_new_tokens = st.slider("Max New Tokens", min_value=1, max_value=1000, value=512)
    top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.8, step=0.1)

# Output panel in the top right
with col2:
    st.subheader("Generated Text:")
    generated_text_placeholder = st.empty()  # Placeholder for generated text

# Button to generate text
if st.button("Generate Text"):
    # SageMaker endpoint details
    endpoint_name = "meta-textgeneration-llama-2-7b-f-2023-11-09-14-39-45-878"  # Replace with your actual endpoint name
    region_name = "us-east-2"  # Replace with your actual region

    # SageMaker client
    client = boto3.client("sagemaker-runtime", region_name=region_name)

    # Payload
    payload = {
        "inputs": [
            [{"role": "user", "content": prompt}]
        ],
        "parameters": {"max_new_tokens": max_new_tokens, "top_p": top_p, "temperature": temperature},
    }

    # Encode payload to JSON
    encoded_json = json.dumps(payload).encode("utf-8")

    # Make API request
    try:
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=encoded_json,
            CustomAttributes='accept_eula=true',
        )

        # Display generated text
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            result = json.loads(response["Body"].read())
            generated_text = result[0]["generation"]["content"]
            generated_text_placeholder.write(generated_text)
        else:
            st.error(f"Error: {response['ResponseMetadata']['HTTPStatusCode']} - {response['Body'].read()}")
    except Exception as e:
        st.error(f"Error: {e}")

# Chat box at the bottom
chat_box = st.text_area("Chat Box:")
