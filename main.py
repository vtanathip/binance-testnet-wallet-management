"""
Example usage of Binance Wallet Manager.
This script demonstrates the main features of the wallet manager.
"""

from binance_wallet_manager import BinanceWalletManager
from binance_wallet_manager.config import Config


def main():
    """Main function demonstrating wallet manager usage."""
    print("=== Binance Testnet Wallet Manager ===\n")
    
    try:
        # Initialize configuration
        config = Config()
        
        # Check if configuration is valid
        if not config.validate():
            print("⚠️  Configuration Error!")
            print("Please set up your .env file with API credentials.")
            print("Copy .env.example to .env and fill in your API keys.")
            print("\nGet your testnet API keys from: https://testnet.binance.vision/")
            return
        
        # Initialize wallet manager
        print("✓ Initializing Binance Wallet Manager...")
        manager = BinanceWalletManager(config)
        print("✓ Connected to Binance", "(Testnet)" if config.testnet else "(Live)")
        print()
        
        # Example 1: Get Balance
        print("--- Example 1: Get Balance ---")
        print("Fetching wallet balances...")
        try:
            balance = manager.get_balance()
            print(f"✓ Balance retrieved successfully")
            
            # Display balances with non-zero amounts
            print("\nNon-zero balances:")
            for coin, amount in balance['total'].items():
                if amount > 0:
                    print(f"  {coin}: {amount}")
        except Exception as e:
            print(f"✗ Error getting balance: {e}")
        print()
        
        # Example 2: Get Deposit Address
        print("--- Example 2: Get Deposit Address ---")
        print("Getting USDT deposit address (ERC20 network)...")
        try:
            deposit_info = manager.get_deposit_address(coin='USDT', network='ERC20')
            print(f"✓ Deposit address: {deposit_info['address']}")
            if deposit_info.get('tag'):
                print(f"  Tag/Memo: {deposit_info['tag']}")
        except Exception as e:
            print(f"✗ Error getting deposit address: {e}")
        print()
        
        # Example 3: Withdraw (commented out for safety)
        print("--- Example 3: Withdraw (Demo) ---")
        print("Withdraw function is available but commented out for safety.")
        print("Example usage:")
        print("""
        result = manager.withdraw(
            coin='USDT',
            amount=10.0,
            address='0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
            network='ERC20'
        )
        print(f"✓ Withdrawal successful! TX ID: {result['transaction_id']}")
        """)
        print()
        
        # Example 4: Get Deposit History
        print("--- Example 4: Get Deposit History ---")
        print("Fetching recent deposits...")
        try:
            deposits = manager.get_deposit_history(limit=5)
            print(f"✓ Found {len(deposits)} recent deposits")
            for i, deposit in enumerate(deposits[:3], 1):
                print(f"  {i}. {deposit.get('currency', 'N/A')} - "
                      f"Amount: {deposit.get('amount', 0)} - "
                      f"Status: {deposit.get('status', 'N/A')}")
        except Exception as e:
            print(f"✗ Error getting deposit history: {e}")
        print()
        
        # Example 5: Get Withdrawal History
        print("--- Example 5: Get Withdrawal History ---")
        print("Fetching recent withdrawals...")
        try:
            withdrawals = manager.get_withdrawal_history(limit=5)
            print(f"✓ Found {len(withdrawals)} recent withdrawals")
            for i, withdrawal in enumerate(withdrawals[:3], 1):
                print(f"  {i}. {withdrawal.get('currency', 'N/A')} - "
                      f"Amount: {withdrawal.get('amount', 0)} - "
                      f"Status: {withdrawal.get('status', 'N/A')}")
        except Exception as e:
            print(f"✗ Error getting withdrawal history: {e}")
        print()
        
        print("=== Demo Complete ===")
        
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
