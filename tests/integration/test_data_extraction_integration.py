import unittest
from src.data_extraction import fetch_stock_data
from config.config import get_alpha_vantage_api_key, get_verify_ssl

class TestFetchStockDataIntegration(unittest.TestCase):

    def test_fetch_stock_data_real_api(self):
        # Retrieve API key and SSL verification flag from config
        api_key = get_alpha_vantage_api_key()
        symbol = 'AAPL'
        verify_ssl = get_verify_ssl()
        
        # Ensure API key is retrieved
        self.assertIsNotNone(api_key, "API key must be set for integration tests.")
        
        # Call the function with SSL verification configured
        try:
            result = fetch_stock_data(symbol, api_key, verify_ssl=verify_ssl)
            # Assertions for expected structure and content
            self.assertIsInstance(result, dict)
            self.assertIn("Time Series (Daily)", result)
            self.assertGreater(len(result["Time Series (Daily)"]), 0)
        except Exception as e:
            self.fail(f"Integration test failed due to an unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
