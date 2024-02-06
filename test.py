def get_value_by_key(nested_dict, key):
    """
    Recursively search for a key in a nested dictionary and return its value.
    
    Args:
    nested_dict (dict): The nested dictionary to search in.
    key (str): The key to search for.
    
    Returns:
    str: The value corresponding to the key, or None if the key is not found.
    """
    # Loop through the items in the dictionary
    for k, v in nested_dict.items():
        # If the current item's key matches the desired key, return its value
        if k == key:
            return v
        # If the current item's value is another dictionary, recursively search within it
        elif isinstance(v, dict):
            result = get_value_by_key(v, key)
            # If the key is found in the nested dictionary, return its value
            if result is not None:
                return result
    # If the key is not found in the dictionary or any nested dictionaries, return None
    return None

# Example nested dictionary
nested_dict = {
    'name': 'John',
    'age': 30,
    'address': {
        'city': 'New York',
        'country': 'USA'
    }
}

# Example key to search for
key_to_search = 'city'

# Get the value corresponding to the key
value = get_value_by_key(nested_dict, key_to_search)

# Print the result
print(value)
