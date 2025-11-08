"""
Basic tests for Binance Wallet Manager.
"""

import os
import pytest
from binance_wallet_manager import BinanceWalletManager
from binance_wallet_manager.config import Config


def test_wallet_manager_initialization_without_config():
    """Test that WalletManager raises error without valid config."""
    # Clear environment variables
    old_key = os.environ.pop('BINANCE_API_KEY', None)
    old_secret = os.environ.pop('BINANCE_API_SECRET', None)
    
    try:
        with pytest.raises(ValueError, match="Invalid configuration"):
            manager = BinanceWalletManager()
    finally:
        # Restore environment variables if they existed
        if old_key:
            os.environ['BINANCE_API_KEY'] = old_key
        if old_secret:
            os.environ['BINANCE_API_SECRET'] = old_secret


def test_wallet_manager_initialization_with_config():
    """Test that WalletManager initializes with valid config."""
    # Set test environment variables
    os.environ['BINANCE_API_KEY'] = 'test_key'
    os.environ['BINANCE_API_SECRET'] = 'test_secret'
    
    try:
        config = Config()
        manager = BinanceWalletManager(config)
        assert manager is not None
        assert manager.exchange is not None
        assert manager.config == config
    finally:
        # Clean up
        os.environ.pop('BINANCE_API_KEY', None)
        os.environ.pop('BINANCE_API_SECRET', None)


def test_wallet_manager_methods_exist():
    """Test that all expected methods exist on WalletManager."""
    os.environ['BINANCE_API_KEY'] = 'test_key'
    os.environ['BINANCE_API_SECRET'] = 'test_secret'
    
    try:
        config = Config()
        manager = BinanceWalletManager(config)
        
        # Check that all expected methods exist
        assert hasattr(manager, 'get_balance')
        assert hasattr(manager, 'withdraw')
        assert hasattr(manager, 'get_deposit_address')
        assert hasattr(manager, 'get_deposit_history')
        assert hasattr(manager, 'get_withdrawal_history')
        
        # Check that methods are callable
        assert callable(manager.get_balance)
        assert callable(manager.withdraw)
        assert callable(manager.get_deposit_address)
        assert callable(manager.get_deposit_history)
        assert callable(manager.get_withdrawal_history)
    finally:
        os.environ.pop('BINANCE_API_KEY', None)
        os.environ.pop('BINANCE_API_SECRET', None)
