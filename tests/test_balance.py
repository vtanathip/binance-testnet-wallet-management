"""
Tests for Binance Wallet Manager balance operations.
"""

import os
import pytest
from binance_wallet_manager import BinanceWalletManager
from binance_wallet_manager.config import Config


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_get_real_balance_from_env():
    """Test fetching real balance from Binance testnet using .env credentials."""
    from dotenv import load_dotenv

    # Load config from .env file
    load_dotenv()

    # Check if credentials are loaded
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret or api_key == 'your_api_key_here':
        pytest.skip("Valid API credentials not found in .env file")

    # Load config from environment variables
    config = Config()

    # Ensure we're in testnet mode
    assert config.testnet is True, "Test should run in testnet mode"

    # Initialize wallet manager
    manager = BinanceWalletManager(config)

    # Fetch balance for all coins
    balance = manager.get_balance()

    # Verify response structure
    assert balance is not None
    assert isinstance(balance, dict)
    assert 'free' in balance
    assert 'used' in balance
    assert 'total' in balance

    # Print structured balance output
    print("\n" + "=" * 80)
    print("BINANCE TESTNET BALANCE REPORT")
    print("=" * 80)

    # Get coins with non-zero balances
    coins_with_balance = {
        coin: {
            'free': balance['free'].get(coin, 0),
            'used': balance['used'].get(coin, 0),
            'total': balance['total'].get(coin, 0)
        }
        for coin in balance['total']
        if balance['total'].get(coin, 0) > 0
    }

    print(f"\nTotal Coins with Balance: {len(coins_with_balance)}")
    print("\n" + "-" * 80)
    print(f"{'COIN':<15} {'FREE':<20} {'USED':<20} {'TOTAL':<20}")
    print("-" * 80)

    # Sort by total balance descending
    sorted_coins = sorted(
        coins_with_balance.items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )

    # Display top 20 coins by balance
    for coin, amounts in sorted_coins[:20]:
        print(
            f"{coin:<15} {amounts['free']:<20.8f} {amounts['used']:<20.8f} {amounts['total']:<20.8f}")

    if len(sorted_coins) > 20:
        print(f"\n... and {len(sorted_coins) - 20} more coins with balance")

    print("-" * 80)

    # Test fetching balance for a specific coin (e.g., BNB)
    bnb_balance = manager.get_balance('BNB')
    assert bnb_balance is not None
    assert isinstance(bnb_balance, dict)
    assert 'BNB' in bnb_balance
    assert 'free' in bnb_balance['BNB']
    assert 'used' in bnb_balance['BNB']
    assert 'total' in bnb_balance['BNB']

    print("\n" + "=" * 80)
    print("SPECIFIC COIN QUERY TEST (BNB)")
    print("=" * 80)
    print(f"\nCoin: BNB")
    print(f"  Free:  {bnb_balance['BNB']['free']:.8f}")
    print(f"  Used:  {bnb_balance['BNB']['used']:.8f}")
    print(f"  Total: {bnb_balance['BNB']['total']:.8f}")
    print("\n" + "=" * 80)
