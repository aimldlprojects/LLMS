import json

def read_ndjson(file_path):
    """
    Read NDJSON file.
    
    Args:
        file_path (str): Path to the NDJSON file.
        
    Returns:
        list: List of dictionaries containing data from the NDJSON file.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Example usage
ndjson_file = 'data.ndjson'
data = read_ndjson(ndjson_file)
print(data)
