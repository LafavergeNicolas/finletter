import os
from dotenv import load_dotenv

# Load environment variables from .env located in the config directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def get_alpha_vantage_api_key() -> str:
    """Retrieve the ALPHA_VANTAGE_API_KEY environment variable."""
    return os.getenv('ALPHA_VANTAGE_API_KEY')

def get_verify_ssl() -> bool:
    """Retrieve the VERIFY_SSL environment variable as a boolean."""
    return os.getenv('VERIFY_SSL', 'true').strip().lower() == 'true'
