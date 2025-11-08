"""
Main application file for Binance Testnet Wallet Management.
Demonstrates usage of environment-based configuration.
"""
from config import config


def main():
    """Main application entry point."""
    print("Binance Testnet Wallet Management")
    print()
    
    # Display current configuration
    config.display()
    
    # Validate configuration
    try:
        config.validate()
        print("\n✓ Configuration is valid!")
        print("\nReady to manage Binance testnet wallet.")
        print("This application can be used for:")
        print("  - Transfer funds")
        print("  - Withdraw funds")
        print("  - Deposit funds")
        print("  - Check wallet balance")
    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nPlease ensure:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your Binance testnet API credentials")
        print("  3. Get testnet API keys from: https://testnet.binance.vision/")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
