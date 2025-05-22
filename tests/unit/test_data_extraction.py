import unittest
from unittest.mock import patch, MagicMock
import requests
from src.data_extraction import fetch_stock_data

class TestFetchStockData(unittest.TestCase):

    @patch('src.data_extraction.requests.get')
    def test_fetch_stock_data_success(self, mock_get):
        # Set up the mock response object
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                "2023-10-10": {
                    "1. open": "150.00",
                    "2. high": "155.00",
                    "3. low": "148.00",
                    "4. close": "154.00",
                    "5. volume": "1000000"
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function with verify_ssl=False
        api_key = 'test_api_key'
        symbol = 'AAPL'
        result = fetch_stock_data(symbol, api_key, verify_ssl=False)

        # Assertions
        mock_get.assert_called_once_with(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}", 
            verify=False
        )
        self.assertIsInstance(result, dict)
        self.assertIn("Time Series (Daily)", result)

    @patch('src.data_extraction.requests.get')
    def test_fetch_stock_data_symbol_not_found(self, mock_get):
        # Simulate symbol not found
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"Error Message": "Invalid API call. Please retry or visit the documentation."}
        mock_get.return_value = mock_response

        # Call the function with verify_ssl=True
        api_key = 'test_api_key'
        symbol = 'INVALID'
        
        # Assertions
        with self.assertRaises(ValueError) as context:
            fetch_stock_data(symbol, api_key, verify_ssl=True)
        self.assertEqual(str(context.exception), f"Symbol '{symbol}' not found.")

    @patch('src.data_extraction.requests.get')
    def test_fetch_stock_data_http_error(self, mock_get):
        # Simulate an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.return_value = mock_response

        # Call the function with verify_ssl=True
        api_key = 'test_api_key'
        symbol = 'AAPL'
        
        # Assertions
        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_stock_data(symbol, api_key, verify_ssl=True)

    @patch('src.data_extraction.requests.get')
    def test_fetch_stock_data_general_exception(self, mock_get):
        # Simulate a general exception
        mock_get.side_effect = Exception("General Error")

        # Call the function with verify_ssl=True
        api_key = 'test_api_key'
        symbol = 'AAPL'
        
        # Assertions
        with self.assertRaises(Exception) as context:
            fetch_stock_data(symbol, api_key, verify_ssl=True)
        self.assertEqual(str(context.exception), "General Error")

if __name__ == '__main__':
    unittest.main()