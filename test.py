[4:38 PM] Suresh Kamakshigari
def update_json_values(json1, json2):     # Iterate through each item in json2    for item in json2:         # Check if the detected language is not English        if item['detected_language'] != 'English':             # Extract the tag, original text, and translated text            tag = item['tag']             original_text = item['original_text']             translated_text = item['translated_text']             # Define a function to recursively search and replace values in json1            def update_recursive(d, key, old_value, new_value):                 if isinstance(d, dict):                     for k, v in d.items():                         if isinstance(v, (dict, list)):                             update_recursive(v, key, old_value, new_value)                         elif k == key and v == old_value:                             d[k] = new_value                 elif isinstance(d, list):                     for item in d:                         if isinstance(item, (dict, list)):                             update_recursive(item, key, old_value, new_value)             # Update json1 with the new value            update_recursive(json1, tag, original_text, translated_text)     return json1
 
 
[4:40 PM] Suresh Kamakshigari
def update_json_values(json1, json2):

    # Iterate through each item in json2

    for item in json2:

        # Check if the detected language is not English

        if item['detected_language'] != 'English':

            # Extract the tag, original text, and translated text

            tag = item['tag']

            original_text = item['original_text']

            translated_text = item['translated_text']
 
            # Define a function to recursively search and replace values in json1

            def update_recursive(d, key, old_value, new_value):

                if isinstance(d, dict):

                    for k, v in d.items():

                        if isinstance(v, (dict, list)):

                            update_recursive(v, key, old_value, new_value)

                        elif k == key and v == old_value:

                            d[k] = new_value
 
                elif isinstance(d, list):

                    for item in d:

                        if isinstance(item, (dict, list)):

                            update_recursive(item, key, old_value, new_value)
 
            # Update json1 with the new value

            update_recursive(json1, tag, original_text, translated_text)
 
    return json1
