# binance-testnet-wallet-management

A repository for managing Binance testnet wallet to transfer, withdraw and deposit for testing.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Binance testnet API credentials:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET_URL=https://testnet.binance.vision/api
LOG_LEVEL=INFO
ENABLE_TESTNET=true
```

**Note:** Get your testnet API keys from [https://testnet.binance.vision/](https://testnet.binance.vision/)

### 3. Run the Application

```bash
python main.py
```

## Configuration

The application uses environment variables for configuration, loaded from a `.env` file. Available configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Your Binance testnet API key (required) | - |
| `BINANCE_API_SECRET` | Your Binance testnet API secret (required) | - |
| `BINANCE_TESTNET_URL` | Binance testnet API base URL | `https://testnet.binance.vision/api` |
| `LOG_LEVEL` | Application log level | `INFO` |
| `ENABLE_TESTNET` | Enable testnet mode | `true` |

## Features

- Transfer funds
- Withdraw funds
- Deposit funds
- Check wallet balance

## Security

⚠️ **Important:** Never commit your `.env` file to version control. It contains sensitive API credentials. The `.env` file is already included in `.gitignore`.
