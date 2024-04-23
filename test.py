import json

def replace_nan_with_null(ndjson_file, output_file):
    with open(ndjson_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            record = json.loads(line)
            # Replace NaN with null
            for key, value in record.items():
                if value != value:  # Check for NaN
                    record[key] = None
            # Write the updated record to the output file
            json.dump(record, outfile)
            outfile.write('\n')

# Example usage
replace_nan_with_null('data.ndjson', 'data_with_null.ndjson')
