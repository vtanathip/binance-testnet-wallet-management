"""
Configuration module for Binance Testnet Wallet Management.
Loads configuration from environment variables using .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage all application settings."""
    
    # Binance API Configuration
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    # Testnet Configuration
    BINANCE_TESTNET_URL = os.getenv('BINANCE_TESTNET_URL', 'https://testnet.binance.vision/api')
    
    # Application Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_TESTNET = os.getenv('ENABLE_TESTNET', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if not cls.BINANCE_API_KEY:
            errors.append("BINANCE_API_KEY is not set")
        
        if not cls.BINANCE_API_SECRET:
            errors.append("BINANCE_API_SECRET is not set")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (hiding sensitive data)."""
        print("=" * 50)
        print("Current Configuration")
        print("=" * 50)
        print(f"Binance API Key: {'*' * 10 if cls.BINANCE_API_KEY else 'NOT SET'}")
        print(f"Binance API Secret: {'*' * 10 if cls.BINANCE_API_SECRET else 'NOT SET'}")
        print(f"Testnet URL: {cls.BINANCE_TESTNET_URL}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Testnet Enabled: {cls.ENABLE_TESTNET}")
        print("=" * 50)


# Create a singleton instance
config = Config()
