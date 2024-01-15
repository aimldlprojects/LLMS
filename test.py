
def search_key_value(json_data, target_key):
    def search_recursive(dictionary, key):
        for k, v in dictionary.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                result = search_recursive(v, key)
                if result is not None:
                    return result
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        result = search_recursive(item, key)
                        if result is not None:
                            return result
        return None

    return search_recursive(json_data, target_key)
