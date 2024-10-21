async def fetch_url(url):
    """
    Asynchronously fetches the content from the specified URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        The response object or None if an error occurs.
    """

    try:
        async with requests.get(url) as response:
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response
    except requests.exceptions.RequestException as e:   

        st.error(f"Error fetching URL: {e}")
        return None  # Indicate failure
