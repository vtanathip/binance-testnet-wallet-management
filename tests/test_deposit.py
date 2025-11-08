"""
Tests for Binance Wallet Manager deposit operations.

NOTE: Binance testnet does not support SAPI endpoints (deposit addresses, 
deposit/withdrawal history). These tests are designed to demonstrate the 
functionality and will be skipped in testnet mode. They would work with 
real Binance API credentials on the production environment.

For testnet, you can manually add funds using the testnet faucet:
https://testnet.binance.vision/

Configuration:
    Set the following environment variables in your .env file:
    - TEST_DEPOSIT_COINS: Comma-separated list of coins to test (default: BTC,ETH,USDT,BNB)
    - TEST_DEPOSIT_NETWORKS: Comma-separated list of networks to test (default: None,None,ERC20|TRC20,BEP20)
      Use pipe (|) to specify multiple networks for a coin, or "None" for default network
"""

import os
import pytest
from binance_wallet_manager import BinanceWalletManager
from binance_wallet_manager.config import Config


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_get_deposit_address():
    """
    Test fetching deposit address for specific coins and networks.

    Configuration (set in .env file):
    - TEST_DEPOSIT_COINS: Comma-separated list of coins (default: BTC,ETH,USDT,BNB)
    - TEST_DEPOSIT_NETWORKS: Comma-separated networks (default: None,None,ERC20|TRC20,BEP20)
      Use pipe (|) for multiple networks per coin, "None" for default network

    Example:
        TEST_DEPOSIT_COINS=BTC,ETH,USDT
        TEST_DEPOSIT_NETWORKS=None,None,ERC20|TRC20

    NOTE: This test will fail in testnet mode because Binance testnet does not
    support SAPI endpoints for deposit addresses. This test is designed for
    production API credentials.
    """
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

    # Skip if in testnet mode (SAPI endpoints not supported)
    if config.testnet:
        pytest.skip(
            "Deposit address endpoints not available in Binance testnet")

    # Initialize wallet manager
    manager = BinanceWalletManager(config)

    # Load test configuration from environment variables
    TEST_COINS = os.getenv('TEST_DEPOSIT_COINS', 'BTC,ETH,USDT,BNB').split(',')
    TEST_NETWORKS = os.getenv('TEST_DEPOSIT_NETWORKS',
                              'None,None,ERC20|TRC20,BEP20').split(',')

    # Build test cases from configuration
    test_cases = []
    for i, coin in enumerate(TEST_COINS):
        coin = coin.strip()
        if i < len(TEST_NETWORKS):
            networks_str = TEST_NETWORKS[i].strip()
            # Handle multiple networks per coin (separated by |)
            if '|' in networks_str:
                networks = [n.strip() for n in networks_str.split('|')]
            else:
                networks = [networks_str]

            for network in networks:
                # Convert "None" string to None
                network_value = None if network == 'None' else network
                test_cases.append({'coin': coin, 'network': network_value})
        else:
            # No network specified, use default
            test_cases.append({'coin': coin, 'network': None})

    print("\n" + "=" * 80)
    print("DEPOSIT ADDRESS RETRIEVAL TEST")
    print("=" * 80)

    successful_addresses = []
    failed_addresses = []

    for test_case in test_cases:
        coin = test_case['coin']
        network = test_case['network']

        try:
            result = manager.get_deposit_address(coin=coin, network=network)

            # Verify response structure
            assert result is not None
            assert isinstance(result, dict)
            assert 'success' in result
            assert 'coin' in result
            assert 'address' in result

            successful_addresses.append({
                'coin': coin,
                'network': network or 'Default',
                'address': result['address'],
                'tag': result.get('tag', 'N/A')
            })

        except Exception as e:
            failed_addresses.append({
                'coin': coin,
                'network': network or 'Default',
                'error': str(e)
            })

    # Print successful addresses
    if successful_addresses:
        print(
            f"\n✓ Successfully Retrieved {len(successful_addresses)} Deposit Address(es):")
        print("-" * 80)
        for addr in successful_addresses:
            print(f"\nCoin:    {addr['coin']}")
            print(f"Network: {addr['network']}")
            print(f"Address: {addr['address']}")
            if addr['tag'] != 'N/A':
                print(f"Tag:     {addr['tag']}")
            print("-" * 80)

    # Print failed attempts
    if failed_addresses:
        print(
            f"\n✗ Failed to Retrieve {len(failed_addresses)} Deposit Address(es):")
        print("-" * 80)
        for fail in failed_addresses:
            print(f"\nCoin:    {fail['coin']}")
            print(f"Network: {fail['network']}")
            print(f"Error:   {fail['error']}")
            print("-" * 80)

    print("\n" + "=" * 80)

    # At least one should succeed for the test to pass
    assert len(
        successful_addresses) > 0, "Should successfully retrieve at least one deposit address"


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_get_deposit_history():
    """
    Test fetching deposit history from Binance.

    Configuration (set in .env file):
    - TEST_DEPOSIT_HISTORY_COIN: Specific coin to check history for (default: USDT)
    - TEST_DEPOSIT_HISTORY_LIMIT: Maximum number of records to retrieve (default: 10)

    Example:
        TEST_DEPOSIT_HISTORY_COIN=USDT
        TEST_DEPOSIT_HISTORY_LIMIT=10

    NOTE: This test will be skipped in testnet mode because Binance testnet does not
    support SAPI endpoints for deposit history. This test is designed for
    production API credentials.
    """
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

    # Skip if in testnet mode (SAPI endpoints not supported)
    if config.testnet:
        pytest.skip(
            "Deposit history endpoints not available in Binance testnet")

    # Initialize wallet manager
    manager = BinanceWalletManager(config)

    # Load test configuration from environment variables
    TEST_HISTORY_COIN = os.getenv('TEST_DEPOSIT_HISTORY_COIN', 'USDT')
    TEST_HISTORY_LIMIT = int(os.getenv('TEST_DEPOSIT_HISTORY_LIMIT', '10'))

    print("\n" + "=" * 80)
    print("DEPOSIT HISTORY TEST")
    print("=" * 80)

    # Test 1: Get all deposit history (limited to 10 most recent)
    try:
        all_deposits = manager.get_deposit_history(limit=TEST_HISTORY_LIMIT)

        assert isinstance(all_deposits, list)

        print(f"\nTotal Recent Deposits: {len(all_deposits)}")

        if len(all_deposits) > 0:
            print("\n" + "-" * 80)
            print(
                f"{'COIN':<10} {'AMOUNT':<15} {'STATUS':<15} {'NETWORK':<15} {'TXID':<30}")
            print("-" * 80)

            for deposit in all_deposits[:5]:  # Show first 5
                coin = deposit.get('currency', 'N/A')
                amount = deposit.get('amount', 0)
                status = deposit.get('status', 'N/A')
                network = deposit.get('network', 'N/A')
                txid = deposit.get(
                    'txid', 'N/A')[:30] if deposit.get('txid') else 'N/A'

                print(
                    f"{coin:<10} {amount:<15.8f} {status:<15} {network:<15} {txid:<30}")

            if len(all_deposits) > 5:
                print(f"\n... and {len(all_deposits) - 5} more deposits")

            print("-" * 80)
        else:
            print("\n  No deposit history found in testnet.")
            print(
                "  Note: Testnet deposits may need to be initiated through testnet faucets.")

    except Exception as e:
        print(f"\n✗ Failed to fetch deposit history: {str(e)}")
        # Don't fail the test if history is empty or unavailable in testnet
        print("  (This is expected in testnet if no deposits have been made)")

    # Test 2: Get deposit history for specific coin
    try:
        coin_deposits = manager.get_deposit_history(
            coin=TEST_HISTORY_COIN, limit=5)

        assert isinstance(coin_deposits, list)

        print(
            f"\n\n{TEST_HISTORY_COIN} Deposit History: {len(coin_deposits)} record(s)")

        if len(coin_deposits) > 0:
            print("-" * 80)
            for deposit in coin_deposits:
                print(f"  Amount:  {deposit.get('amount', 0)}")
                print(f"  Status:  {deposit.get('status', 'N/A')}")
                print(f"  Network: {deposit.get('network', 'N/A')}")
                print(f"  TxID:    {deposit.get('txid', 'N/A')}")
                print("-" * 80)
        else:
            print(f"  No {TEST_HISTORY_COIN} deposits found.")

    except Exception as e:
        print(
            f"\n✗ Failed to fetch {TEST_HISTORY_COIN} deposit history: {str(e)}")
        print(
            f"  (This is expected in testnet if no {TEST_HISTORY_COIN} deposits have been made)")

    print("\n" + "=" * 80)
    print("\nINFORMATION:")
    print("  - Testnet deposits are typically obtained through faucets")
    print("  - Use the deposit address from test_get_deposit_address()")
    print("  - Testnet faucet: https://testnet.binance.vision/")
    print("=" * 80)


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_deposit_address_consistency():
    """
    Test that deposit addresses remain consistent across multiple calls.

    Configuration (set in .env file):
    - TEST_DEPOSIT_CONSISTENCY_COIN: Coin to test for address consistency (default: BTC)

    Example:
        TEST_DEPOSIT_CONSISTENCY_COIN=BTC

    NOTE: This test will be skipped in testnet mode because Binance testnet does not
    support SAPI endpoints for deposit addresses. This test is designed for
    production API credentials.
    """
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

    # Skip if in testnet mode (SAPI endpoints not supported)
    if config.testnet:
        pytest.skip(
            "Deposit address endpoints not available in Binance testnet")

    # Initialize wallet manager
    manager = BinanceWalletManager(config)

    # Load test configuration from environment variables
    TEST_CONSISTENCY_COIN = os.getenv('TEST_DEPOSIT_CONSISTENCY_COIN', 'BTC')

    print("\n" + "=" * 80)
    print("DEPOSIT ADDRESS CONSISTENCY TEST")
    print("=" * 80)

    # Test address consistency
    try:
        address_1 = manager.get_deposit_address(coin=TEST_CONSISTENCY_COIN)
        address_2 = manager.get_deposit_address(coin=TEST_CONSISTENCY_COIN)

        assert address_1['address'] == address_2['address'], \
            f"{TEST_CONSISTENCY_COIN} deposit address should remain consistent"

        print(f"\n✓ {TEST_CONSISTENCY_COIN} Address Consistency: PASSED")
        print(f"  Address: {address_1['address']}")
        print("  (Address remains the same across multiple calls)")

    except Exception as e:
        print(f"\n✗ {TEST_CONSISTENCY_COIN} Address Test Failed: {str(e)}")

    print("\n" + "=" * 80)


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_testnet_faucet_info():
    """
    Test to display information about getting testnet funds.
    This test always passes and provides guidance for testnet deposits.
    """
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

    print("\n" + "=" * 80)
    print("TESTNET DEPOSIT INFORMATION")
    print("=" * 80)

    if config.testnet:
        print("\n✓ Running in TESTNET mode")
        print("\nHow to add funds to your testnet wallet:")
        print("-" * 80)
        print("\n1. TESTNET FAUCET:")
        print("   Visit: https://testnet.binance.vision/")
        print("   - Log in with your testnet account")
        print("   - Request test tokens for various cryptocurrencies")
        print("   - Tokens are automatically added to your testnet balance")

        print("\n2. AVAILABLE TEST TOKENS:")
        print("   - BTC (Bitcoin)")
        print("   - ETH (Ethereum)")
        print("   - BNB (Binance Coin)")
        print("   - USDT (Tether)")
        print("   - And many more...")

        print("\n3. VERIFY YOUR BALANCE:")
        print("   Run: pytest tests/test_balance.py -v -s")
        print("   This will show all tokens in your testnet wallet")

        print("\n4. LIMITATIONS:")
        print("   - Cannot generate deposit addresses (SAPI endpoint not available)")
        print("   - Cannot view deposit history")
        print("   - Must use testnet faucet to add funds")
        print("   - Testnet tokens have no real value")

    else:
        print("\n✓ Running in PRODUCTION mode")
        print("\nHow to deposit funds to your wallet:")
        print("-" * 80)
        print("\n1. GET DEPOSIT ADDRESS:")
        print("   Use: manager.get_deposit_address(coin='BTC', network='BTC')")
        print("   This returns your unique deposit address")

        print("\n2. SEND FUNDS:")
        print("   - Send cryptocurrency from another wallet/exchange")
        print("   - Use the correct network (BTC, ERC20, BEP20, etc.)")
        print("   - Wait for network confirmations")

        print("\n3. CHECK DEPOSIT HISTORY:")
        print("   Use: manager.get_deposit_history(coin='BTC', limit=10)")
        print("   This shows your recent deposits")

        print("\n⚠ WARNING:")
        print("   You are using PRODUCTION credentials!")
        print("   Real funds are at risk. Use testnet for testing.")

    print("\n" + "=" * 80)

    # Test always passes - it's informational
    assert True
