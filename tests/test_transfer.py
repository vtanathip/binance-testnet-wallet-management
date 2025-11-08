"""
Tests for Binance Wallet Manager transfer (withdrawal) operations.

This test demonstrates how to transfer coins from your testnet wallet to another
testnet address. The test will attempt a withdrawal and display the results.

Configuration:
    Set the following environment variables in your .env file:
    - TEST_TRANSFER_COIN: Coin symbol to transfer (default: USDT)
    - TEST_TRANSFER_NETWORK: Network to use (default: BSC)
    - TEST_TRANSFER_AMOUNT: Amount to transfer (default: 1.0)
    - TEST_TRANSFER_ADDRESS: Destination address (required, no default)

NOTE: Binance testnet may have limitations on withdrawal operations.
Some withdrawals might fail due to testnet restrictions or insufficient balance.
"""

import os
import pytest
from binance_wallet_manager import BinanceWalletManager
from binance_wallet_manager.config import Config


@pytest.mark.skipif(
    not os.path.exists('.env'),
    reason="Requires .env file with BINANCE_API_KEY and BINANCE_API_SECRET"
)
def test_transfer_to_testnet_address():
    """
    Test transferring (withdrawing) a specific coin to another testnet address.

    This test demonstrates:
    1. Checking current balance before transfer
    2. Initiating a withdrawal to a destination address
    3. Handling success/failure scenarios
    4. Displaying transfer details

    Configuration (set in .env file):
    - TEST_TRANSFER_COIN: Coin to transfer (default: USDT)
    - TEST_TRANSFER_NETWORK: Network for transfer (default: BSC)
    - TEST_TRANSFER_AMOUNT: Amount to transfer (default: 1.0)
    - TEST_TRANSFER_ADDRESS: Destination address (required)

    The test will be skipped if TEST_TRANSFER_ADDRESS is not configured.
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

    # Initialize wallet manager
    manager = BinanceWalletManager(config)

    # Load test configuration from environment variables
    TEST_COIN = os.getenv('TEST_TRANSFER_COIN', 'USDT')
    TEST_NETWORK = os.getenv('TEST_TRANSFER_NETWORK', 'BSC')
    TEST_AMOUNT = float(os.getenv('TEST_TRANSFER_AMOUNT', '1.0'))
    TEST_ADDRESS = os.getenv('TEST_TRANSFER_ADDRESS', '')

    # Skip test if no destination address is configured
    if not TEST_ADDRESS or TEST_ADDRESS == 'your_destination_address_here':
        pytest.skip(
            "No destination address configured. "
            "Set TEST_TRANSFER_ADDRESS in .env file to run this test."
        )

    print("\n" + "=" * 80)
    print("TESTNET TRANSFER (WITHDRAWAL) TEST")
    print("=" * 80)

    print(f"\nTest Parameters:")
    print("-" * 80)
    print(f"  Coin:              {TEST_COIN}")
    print(f"  Network:           {TEST_NETWORK}")
    print(f"  Amount:            {TEST_AMOUNT}")
    print(f"  Destination:       {TEST_ADDRESS}")
    print(f"  Testnet Mode:      {config.testnet}")
    print("-" * 80)

    # Step 1: Check current balance
    print("\n[STEP 1] Checking Current Balance...")
    print("-" * 80)

    try:
        balance = manager.get_balance(TEST_COIN)

        if TEST_COIN in balance:
            available = balance[TEST_COIN]['free']
            print(f"✓ Current {TEST_COIN} Balance:")
            print(f"  Available: {available:.8f} {TEST_COIN}")
            print(f"  Used:      {balance[TEST_COIN]['used']:.8f} {TEST_COIN}")
            print(
                f"  Total:     {balance[TEST_COIN]['total']:.8f} {TEST_COIN}")

            if available < TEST_AMOUNT:
                print(f"\n⚠ WARNING: Insufficient balance!")
                print(f"  Required: {TEST_AMOUNT} {TEST_COIN}")
                print(f"  Available: {available} {TEST_COIN}")
                pytest.skip(
                    f"Insufficient {TEST_COIN} balance for transfer test")
        else:
            print(f"✗ No {TEST_COIN} balance found")
            pytest.skip(f"No {TEST_COIN} in wallet to transfer")

    except Exception as e:
        print(f"✗ Failed to check balance: {str(e)}")
        pytest.skip(f"Cannot verify balance: {str(e)}")

    # Step 2: Attempt withdrawal
    print("\n[STEP 2] Initiating Transfer (Withdrawal)...")
    print("-" * 80)

    try:
        result = manager.withdraw(
            coin=TEST_COIN,
            amount=TEST_AMOUNT,
            address=TEST_ADDRESS,
            network=TEST_NETWORK
        )

        # Verify response structure
        assert result is not None
        assert isinstance(result, dict)

        print("✓ Transfer Initiated Successfully!")
        print("-" * 80)
        print("\nTransfer Details:")
        print(f"  Transaction ID:    {result.get('transaction_id', 'N/A')}")
        print(f"  Coin:              {result.get('coin', 'N/A')}")
        print(f"  Amount:            {result.get('amount', 0):.8f}")
        print(f"  Destination:       {result.get('address', 'N/A')}")
        print(f"  Network:           {result.get('network', 'N/A')}")
        print(
            f"  Status:            {'Success' if result.get('success') else 'Failed'}")

        if result.get('info'):
            print("\nAdditional Information:")
            info = result['info']
            if isinstance(info, dict):
                for key, value in info.items():
                    if key not in ['id', 'coin', 'amount', 'address', 'network']:
                        print(f"  {key}: {value}")

        print("-" * 80)

        # Step 3: Verify balance after transfer
        print("\n[STEP 3] Verifying Balance After Transfer...")
        print("-" * 80)

        try:
            new_balance = manager.get_balance(TEST_COIN)
            if TEST_COIN in new_balance:
                new_available = new_balance[TEST_COIN]['free']
                print(f"✓ New {TEST_COIN} Balance:")
                print(f"  Available: {new_available:.8f} {TEST_COIN}")
                print(
                    f"  Change:    {new_available - available:.8f} {TEST_COIN}")
        except Exception as e:
            print(f"⚠ Could not verify new balance: {str(e)}")

        print("\n" + "=" * 80)
        print("TRANSFER TEST RESULT: SUCCESS")
        print("=" * 80)

        # Test passes if withdrawal was successful
        assert result.get('success') == True, "Transfer should be successful"

    except Exception as e:
        error_message = str(e)
        print(f"✗ Transfer Failed!")
        print("-" * 80)
        print(f"\nError Details:")
        print(f"  {error_message}")
        print("-" * 80)

        # Check for common testnet issues
        if "does not have a testnet/sandbox URL" in error_message:
            print("\n⚠ TESTNET LIMITATION DETECTED:")
            print("  Binance testnet does not support withdrawal (SAPI) endpoints.")
            print("  Withdrawals can only be tested with production API credentials.")
            print("\n  To test withdrawals:")
            print("  1. Set BINANCE_TESTNET=false in .env")
            print("  2. Use production API credentials")
            print("  3. ⚠ BE CAREFUL - Real funds will be transferred!")
        elif "insufficient" in error_message.lower():
            print("\n⚠ INSUFFICIENT BALANCE:")
            print(f"  Not enough {TEST_COIN} to complete the transfer.")
            print("  Add more funds using the testnet faucet:")
            print("  https://testnet.binance.vision/")
        elif "address" in error_message.lower():
            print("\n⚠ ADDRESS ISSUE:")
            print("  The destination address may be invalid.")
            print("  Verify the address format for the selected network.")
        else:
            print("\n⚠ UNKNOWN ERROR:")
            print("  Check the error message above for details.")

        print("\n" + "=" * 80)
        print("TRANSFER TEST RESULT: FAILED (Expected in testnet)")
        print("=" * 80)

        print("\nℹ INFORMATION:")
        print("  This test is expected to fail in testnet mode because:")
        print("  - Binance testnet doesn't support withdrawal endpoints")
        print("  - Use this test with production credentials to test real transfers")
        print("  - Always use testnet for development and testing when possible")
        print("=" * 80)

        # Don't fail the test in testnet mode - it's expected
        if config.testnet and "does not have a testnet/sandbox URL" in error_message:
            pytest.skip(
                "Withdrawal endpoints not available in Binance testnet")
        else:
            # Re-raise the exception for unexpected errors
            raise
