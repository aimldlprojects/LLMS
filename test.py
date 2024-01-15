import xml.etree.ElementTree as ET

# Sample XML string (replace this with your XML content)
xml_string = '''
<root>
    <person>
        <name>John</name>
        <details>
            <age>30</age>
            <city>New York</city>
        </details>
    </person>
</root>
'''

# Parse the XML string
root = ET.fromstring(xml_string)

# Define the nested structure of the key (e.g., 'person/details/age')
nested_keys = ['person', 'details', 'age']

# Extract nested key-value pair
nested_value = root
for key in nested_keys:
    nested_value = nested_value.find(key)
    if nested_value is None:
        break

# Print the result
if nested_value is not None:
    key = '/'.join(nested_keys)
    value = nested_value.text
    print(f"{key}: {value}")
else:
    print("Key not found")
