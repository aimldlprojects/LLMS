import requests
import json

# Replace 'YOUR_GATEWAY_URL' with the actual URL of your AWS Gateway endpoint
gateway_url = 'YOUR_GATEWAY_URL'

# Example payload (if needed)
payload = {
    "key": "value"
}

try:
    # Make a POST request to the AWS Gateway endpoint
    response = requests.post(gateway_url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response from the endpoint
        print(response.json())
    else:
        # Print an error message if the request was not successful
        print("Error:", response.text)
except Exception as e:
    # Print any exceptions that occur during the request
    print("Exception:", e)
