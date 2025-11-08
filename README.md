# Binance Testnet Wallet Management

A Python package for managing Binance testnet wallet operations including withdraw and deposit functionality. Built with [CCXT](https://github.com/ccxt/ccxt) library and managed with [uv](https://github.com/astral-sh/uv) package manager.

## Features

- 💸 **Withdraw**: Transfer cryptocurrency to specific addresses with network selection (ERC20, TRC20, BEP20, etc.)
- 💰 **Deposit**: Get deposit addresses and track deposit history for specific coins
- 📊 **Balance**: Check wallet balances for all or specific cryptocurrencies
- 📜 **Transaction History**: View withdrawal and deposit transaction history
- 🔒 **Testnet Support**: Safe testing environment using Binance testnet
- 🚀 **Modern Tools**: Built with uv package manager and CCXT library

## Prerequisites

- Python 3.12 or higher
- Binance testnet API keys (get them from [https://testnet.binance.vision/](https://testnet.binance.vision/))

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/vtanathip/binance-testnet-wallet-management.git
cd binance-testnet-wallet-management

# Install dependencies with uv
uv sync
```

### Manual installation

```bash
# Install dependencies
pip install ccxt python-dotenv
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Binance testnet API credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true
BINANCE_SANDBOX=true
```

3. **(Optional)** Configure deposit test settings in `.env`:
```env
# Deposit Test Configuration (Optional)
# NOTE: Deposit endpoints are not available in testnet (SAPI limitation)
TEST_DEPOSIT_COINS=BTC,ETH,USDT,BNB               # Coins to test
TEST_DEPOSIT_NETWORKS=None,None,ERC20|TRC20,BEP20 # Networks (use | for multiple)
TEST_DEPOSIT_HISTORY_COIN=USDT                    # Coin for history check
TEST_DEPOSIT_HISTORY_LIMIT=10                     # Max history records
TEST_DEPOSIT_CONSISTENCY_COIN=BTC                 # Coin for consistency test
```
   **Note:** Deposit tests will be skipped in testnet mode due to SAPI endpoint limitations.

4. **(Optional)** Configure transfer test settings in `.env`:
```env
# Transfer Test Configuration (Optional)
TEST_TRANSFER_COIN=USDT              # Coin to transfer
TEST_TRANSFER_NETWORK=BSC            # Network (BSC, ERC20, TRC20, etc.)
TEST_TRANSFER_AMOUNT=1.0             # Amount to transfer
TEST_TRANSFER_ADDRESS=0xYourAddress  # Destination address
```
   **Note:** The transfer test will be skipped if `TEST_TRANSFER_ADDRESS` is not configured.

5. Get your API keys from [Binance Testnet](https://testnet.binance.vision/)

## Usage

### Quick Start

Run the example script to see the wallet manager in action:

```bash
# Using uv
uv run main.py

# Or with Python directly
python main.py
```

### Basic Examples

#### Initialize Wallet Manager

```python
from binance_wallet_manager import BinanceWalletManager

# Initialize with default config (reads from .env)
manager = BinanceWalletManager()
```

#### Check Balance

```python
# Get all balances
balance = manager.get_balance()
print(balance)

# Get balance for specific coin
usdt_balance = manager.get_balance(coin='USDT')
print(f"USDT Balance: {usdt_balance['USDT']['total']}")
```

#### Get Deposit Address

```python
# Get deposit address for USDT on ERC20 network
deposit_info = manager.get_deposit_address(coin='USDT', network='ERC20')
print(f"Deposit Address: {deposit_info['address']}")
print(f"Network: {deposit_info['network']}")
```

#### Withdraw Cryptocurrency

```python
# Withdraw USDT to an address via ERC20 network
result = manager.withdraw(
    coin='USDT',
    amount=10.0,
    address='0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    network='ERC20'
)
print(f"Withdrawal successful! TX ID: {result['transaction_id']}")
```

#### Withdraw with Tag/Memo (for coins like XRP, XLM)

```python
# Withdraw XRP with destination tag
result = manager.withdraw(
    coin='XRP',
    amount=100,
    address='rDsbeomae4FXwgQTJp9Rs64Qg9vDiTCdBv',
    tag='123456789'
)
```

#### View Transaction History

```python
# Get recent deposits
deposits = manager.get_deposit_history(coin='USDT', limit=10)
for deposit in deposits:
    print(f"Amount: {deposit['amount']} - Status: {deposit['status']}")

# Get recent withdrawals
withdrawals = manager.get_withdrawal_history(coin='BTC', limit=5)
for withdrawal in withdrawals:
    print(f"Amount: {withdrawal['amount']} - Status: {withdrawal['status']}")
```

## API Reference

### BinanceWalletManager

#### `__init__(config: Optional[Config] = None)`
Initialize the wallet manager with optional configuration.

#### `get_balance(coin: Optional[str] = None) -> Dict[str, Any]`
Get wallet balance for a specific coin or all coins.

#### `withdraw(coin: str, amount: float, address: str, network: Optional[str] = None, tag: Optional[str] = None, **kwargs) -> Dict[str, Any]`
Withdraw cryptocurrency to a specific address and network.

**Parameters:**
- `coin`: Coin symbol (e.g., 'BTC', 'USDT', 'ETH')
- `amount`: Amount to withdraw
- `address`: Destination wallet address
- `network`: Network specification (e.g., 'ERC20', 'TRC20', 'BEP20')
- `tag`: Address tag/memo for certain coins (e.g., XRP, XLM)

#### `get_deposit_address(coin: str, network: Optional[str] = None, **kwargs) -> Dict[str, Any]`
Get deposit address for a specific coin and network.

#### `get_deposit_history(coin: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, **kwargs) -> list`
Get deposit history for specific coin or all deposits.

#### `get_withdrawal_history(coin: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, **kwargs) -> list`
Get withdrawal history for specific coin or all withdrawals.

## Development

### Project Structure

```
binance-testnet-wallet-management/
├── binance_wallet_manager/       # Main package
│   ├── __init__.py               # Package initialization
│   ├── config.py                 # Configuration management
│   └── wallet_manager.py         # Main wallet operations
├── main.py                       # Example usage script
├── pyproject.toml                # Project configuration (uv)
├── .env.example                  # Example environment file
└── README.md                     # This file
```

### Running Tests

```bash
# Install test dependencies (if any are added)
uv add --dev pytest

# Run tests
uv run pytest
```

## Supported Networks

Common networks supported by Binance:
- **ERC20**: Ethereum network
- **TRC20**: Tron network
- **BEP20**: Binance Smart Chain
- **BEP2**: Binance Chain
- **BTC**: Bitcoin network
- **And many more...**

Check the [CCXT documentation](https://docs.ccxt.com/) for more details on supported networks and coins.

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit your `.env` file** - Keep your API keys secure
2. **Use testnet for development** - Always test with testnet before using real funds
3. **Restrict API permissions** - Only enable necessary permissions on your API keys
4. **Monitor withdrawals** - Always verify withdrawal addresses and amounts
5. **Enable 2FA** - Use two-factor authentication on your Binance account

## Technologies Used

- **[CCXT](https://github.com/ccxt/ccxt)**: A cryptocurrency trading library with support for 100+ exchanges
- **[uv](https://github.com/astral-sh/uv)**: An extremely fast Python package installer and resolver
- **Python 3.12+**: Modern Python with type hints and async support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational and testing purposes only. Use at your own risk. The authors are not responsible for any losses incurred through the use of this software.

## Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/vtanathip/binance-testnet-wallet-management/issues).
