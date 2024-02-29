import xml.etree.ElementTree as ET

def replace_xml_value(xml_file, tag, new_value):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the element with the specified tag
    for elem in root.iter(tag):
        elem.text = new_value

    # Write the modified XML back to file
    tree.write(xml_file)

# Example usage:
xml_file_path = "example.xml"
tag_to_replace = "value"
new_value = "new_value"

replace_xml_value(xml_file_path, tag_to_replace, new_value)
