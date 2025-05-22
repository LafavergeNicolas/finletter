import requests

def fetch_stock_data(symbol: str, api_key: str, verify_ssl: bool = True) -> dict:
    """
    Fetches daily stock data for a given symbol from the Alpha Vantage API.

    Args:
        symbol (str): The stock symbol to retrieve data for (e.g., 'AAPL').
        api_key (str): Your Alpha Vantage API key.
        verify_ssl (bool): Whether to verify SSL certificates.

    Returns:
        dict: A dictionary containing the stock data returned by the API.

    Raises:
        ValueError: If the symbol is not found or is invalid.
        requests.exceptions.HTTPError: If an HTTP error occurs.
        Exception: For other exceptions that may occur during the request.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url, verify=verify_ssl)
        response.raise_for_status()

        data = response.json()

        # Check if the symbol is found
        if "Error Message" in data:
            raise ValueError(f"Symbol '{symbol}' not found.")

        return data

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        raise  # Re-raise the exception
    except Exception as err:
        print(f"An error occurred: {err}")
        raise  # Re-raise the exception
