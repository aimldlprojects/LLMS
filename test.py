import pandas as pd

def csv_to_ndjson(csv_file, ndjson_file):
    """
    Convert CSV file to NDJSON format.
    
    Args:
        csv_file (str): Path to the CSV file.
        ndjson_file (str): Path to the NDJSON file to save.
    """
    # Read CSV into pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Write each row as a JSON object to NDJSON file
    with open(ndjson_file, 'w') as f:
        for _, row in df.iterrows():
            json.dump(row.to_dict(), f)
            f.write('\n')

# Example usage
csv_to_ndjson('data.csv', 'data.ndjson')
