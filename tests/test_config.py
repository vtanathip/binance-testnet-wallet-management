"""
Basic tests for Binance Wallet Manager configuration.
"""

import os
import pytest
from binance_wallet_manager.config import Config


def test_config_initialization():
    """Test that Config can be initialized."""
    config = Config()
    assert config is not None
    assert isinstance(config.testnet, bool)
    assert isinstance(config.sandbox_mode, bool)


def test_config_validation_without_credentials():
    """Test that Config validation fails without credentials."""
    # Clear environment variables
    old_key = os.environ.pop('BINANCE_API_KEY', None)
    old_secret = os.environ.pop('BINANCE_API_SECRET', None)
    
    try:
        config = Config()
        assert not config.validate()
    finally:
        # Restore environment variables if they existed
        if old_key:
            os.environ['BINANCE_API_KEY'] = old_key
        if old_secret:
            os.environ['BINANCE_API_SECRET'] = old_secret


def test_config_validation_with_credentials():
    """Test that Config validation passes with credentials."""
    # Set test environment variables
    os.environ['BINANCE_API_KEY'] = 'test_key'
    os.environ['BINANCE_API_SECRET'] = 'test_secret'
    
    try:
        config = Config()
        assert config.validate()
        assert config.api_key == 'test_key'
        assert config.api_secret == 'test_secret'
    finally:
        # Clean up
        os.environ.pop('BINANCE_API_KEY', None)
        os.environ.pop('BINANCE_API_SECRET', None)


def test_config_get_api_credentials():
    """Test that get_api_credentials returns correct format."""
    os.environ['BINANCE_API_KEY'] = 'test_key'
    os.environ['BINANCE_API_SECRET'] = 'test_secret'
    
    try:
        config = Config()
        credentials = config.get_api_credentials()
        assert isinstance(credentials, dict)
        assert 'apiKey' in credentials
        assert 'secret' in credentials
        assert credentials['apiKey'] == 'test_key'
        assert credentials['secret'] == 'test_secret'
    finally:
        os.environ.pop('BINANCE_API_KEY', None)
        os.environ.pop('BINANCE_API_SECRET', None)


def test_config_testnet_flag():
    """Test that testnet flag is properly read."""
    os.environ['BINANCE_TESTNET'] = 'true'
    config = Config()
    assert config.testnet is True
    
    os.environ['BINANCE_TESTNET'] = 'false'
    config = Config()
    assert config.testnet is False
    
    os.environ.pop('BINANCE_TESTNET', None)
