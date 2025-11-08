"""
Configuration module for Binance Wallet Manager.
Handles environment variables and API credentials.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Binance API credentials and settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.api_key: Optional[str] = os.getenv('BINANCE_API_KEY')
        self.api_secret: Optional[str] = os.getenv('BINANCE_API_SECRET')
        self.testnet: bool = os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        self.sandbox_mode: bool = os.getenv('BINANCE_SANDBOX', 'true').lower() == 'true'
    
    def validate(self) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        if not self.api_key or not self.api_secret:
            return False
        return True
    
    def get_api_credentials(self) -> dict:
        """
        Get API credentials as a dictionary.
        
        Returns:
            dict: Dictionary containing API key and secret.
        """
        return {
            'apiKey': self.api_key,
            'secret': self.api_secret,
        }
