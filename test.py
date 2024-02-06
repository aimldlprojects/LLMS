def get_key_value_pairs(nested_dict, prefix=''):
    """
    Recursively extract key-value pairs from a nested dictionary.
    
    Args:
    nested_dict (dict): The nested dictionary to extract key-value pairs from.
    prefix (str): Optional. Prefix to add to keys. Used for recursive calls.
    
    Returns:
    list: List of key-value pairs.
    """
    key_value_pairs = []
    
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            # If the value is a dictionary, recursively call the function with the nested dictionary
            key_value_pairs.extend(get_key_value_pairs(value, prefix + key + '_'))
        else:
            # If the value is not a dictionary, add the key-value pair to the list
            key_value_pairs.append((prefix + key, value))
    
    return key_value_pairs

# Example nested dictionary
nested_dict = {
    'name': 'John',
    'age': 30,
    'address': {
        'city': 'New York',
        'country': 'USA'
    }
}

# Get key-value pairs from the nested dictionary
key_value_pairs = get_key_value_pairs(nested_dict)

# Print key-value pairs
for key, value in key_value_pairs:
    print(f'{key}: {value}')
