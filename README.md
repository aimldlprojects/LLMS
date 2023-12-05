Goodluck


r'"key1":\s*{"key2":\s*{"key3":\s*"([^"]+)"}}'

r'\{(?:[^{}]|[^{}]*\{[^{}]*\}[^{}]*)*\}'

def extract_json_from_string(input_string):
    # Define a regex pattern to match JSON content
    json_pattern = r'\{.*?\}'

    # Find all matches of the pattern in the input string
    matches = re.findall(json_pattern, input_string)

    # Process each match (assuming there is only one JSON object in each match)
    for match in matches:
        # Print the matched JSON string
        print("Matched JSON:", match)

        # Parse the JSON string
        try:
            json_object = json.loads(match)
            # Process the parsed JSON object as needed
            print("Parsed JSON:", json_object)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
