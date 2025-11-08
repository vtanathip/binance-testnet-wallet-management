"""
Binance Wallet Manager - Main module for wallet operations.
Provides withdraw and deposit functionality for Binance testnet.
"""

import ccxt
from typing import Dict, Optional, Any
from .config import Config


class BinanceWalletManager:
    """
    Manages Binance testnet wallet operations including withdrawals and deposits.
    Uses CCXT library for exchange interactions.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the Binance Wallet Manager.
        
        Args:
            config: Optional Config object. If not provided, creates a new Config.
        
        Raises:
            ValueError: If configuration is invalid.
        """
        self.config = config or Config()
        
        if not self.config.validate():
            raise ValueError(
                "Invalid configuration. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET environment variables."
            )
        
        # Initialize CCXT Binance exchange
        self.exchange = ccxt.binance({
            'apiKey': self.config.api_key,
            'secret': self.config.api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',  # spot, margin, future, delivery
            }
        })
        
        # Set testnet mode if configured
        if self.config.testnet:
            self.exchange.set_sandbox_mode(True)
    
    def get_balance(self, coin: Optional[str] = None) -> Dict[str, Any]:
        """
        Get wallet balance for a specific coin or all coins.
        
        Args:
            coin: Optional coin symbol (e.g., 'BTC', 'USDT'). If None, returns all balances.
        
        Returns:
            Dictionary containing balance information.
        
        Raises:
            Exception: If balance retrieval fails.
        """
        try:
            balance = self.exchange.fetch_balance()
            
            if coin:
                if coin in balance['total']:
                    return {
                        coin: {
                            'free': balance['free'].get(coin, 0),
                            'used': balance['used'].get(coin, 0),
                            'total': balance['total'].get(coin, 0),
                        }
                    }
                else:
                    return {coin: {'free': 0, 'used': 0, 'total': 0}}
            
            return balance
        except Exception as e:
            raise Exception(f"Failed to fetch balance: {str(e)}")
    
    def withdraw(
        self,
        coin: str,
        amount: float,
        address: str,
        network: Optional[str] = None,
        tag: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Withdraw cryptocurrency to a specific address and network.
        
        Args:
            coin: Coin symbol to withdraw (e.g., 'BTC', 'USDT', 'ETH').
            amount: Amount to withdraw.
            address: Destination wallet address.
            network: Optional network specification (e.g., 'ERC20', 'TRC20', 'BEP20').
            tag: Optional address tag/memo for certain coins (e.g., XRP, XLM).
            **kwargs: Additional parameters to pass to the exchange.
        
        Returns:
            Dictionary containing withdrawal information including transaction ID.
        
        Raises:
            Exception: If withdrawal fails.
        
        Example:
            >>> manager = BinanceWalletManager()
            >>> result = manager.withdraw(
            ...     coin='USDT',
            ...     amount=10.0,
            ...     address='0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
            ...     network='ERC20'
            ... )
        """
        try:
            params = {}
            
            # Add network parameter if specified
            if network:
                params['network'] = network
            
            # Add tag/memo if specified
            if tag:
                params['tag'] = tag
            
            # Merge additional kwargs
            params.update(kwargs)
            
            # Perform withdrawal
            result = self.exchange.withdraw(
                code=coin,
                amount=amount,
                address=address,
                tag=tag,
                params=params
            )
            
            return {
                'success': True,
                'transaction_id': result.get('id'),
                'coin': coin,
                'amount': amount,
                'address': address,
                'network': network,
                'info': result
            }
        except Exception as e:
            raise Exception(f"Withdrawal failed: {str(e)}")
    
    def get_deposit_address(
        self,
        coin: str,
        network: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get deposit address for a specific coin and network.
        
        Args:
            coin: Coin symbol (e.g., 'BTC', 'USDT', 'ETH').
            network: Optional network specification (e.g., 'ERC20', 'TRC20', 'BEP20').
            **kwargs: Additional parameters to pass to the exchange.
        
        Returns:
            Dictionary containing deposit address information.
        
        Raises:
            Exception: If fetching deposit address fails.
        
        Example:
            >>> manager = BinanceWalletManager()
            >>> result = manager.get_deposit_address(coin='USDT', network='ERC20')
            >>> print(result['address'])
        """
        try:
            params = {}
            
            # Add network parameter if specified
            if network:
                params['network'] = network
            
            # Merge additional kwargs
            params.update(kwargs)
            
            # Fetch deposit address
            result = self.exchange.fetch_deposit_address(
                code=coin,
                params=params
            )
            
            return {
                'success': True,
                'coin': coin,
                'address': result.get('address'),
                'tag': result.get('tag'),
                'network': network,
                'info': result
            }
        except Exception as e:
            raise Exception(f"Failed to fetch deposit address: {str(e)}")
    
    def get_deposit_history(
        self,
        coin: Optional[str] = None,
        since: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs
    ) -> list:
        """
        Get deposit history for specific coin or all deposits.
        
        Args:
            coin: Optional coin symbol. If None, returns all deposits.
            since: Optional timestamp to fetch deposits since (in milliseconds).
            limit: Optional limit on number of results.
            **kwargs: Additional parameters to pass to the exchange.
        
        Returns:
            List of deposit transactions.
        
        Raises:
            Exception: If fetching deposit history fails.
        
        Example:
            >>> manager = BinanceWalletManager()
            >>> deposits = manager.get_deposit_history(coin='USDT', limit=10)
        """
        try:
            params = kwargs
            
            deposits = self.exchange.fetch_deposits(
                code=coin,
                since=since,
                limit=limit,
                params=params
            )
            
            return deposits
        except Exception as e:
            raise Exception(f"Failed to fetch deposit history: {str(e)}")
    
    def get_withdrawal_history(
        self,
        coin: Optional[str] = None,
        since: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs
    ) -> list:
        """
        Get withdrawal history for specific coin or all withdrawals.
        
        Args:
            coin: Optional coin symbol. If None, returns all withdrawals.
            since: Optional timestamp to fetch withdrawals since (in milliseconds).
            limit: Optional limit on number of results.
            **kwargs: Additional parameters to pass to the exchange.
        
        Returns:
            List of withdrawal transactions.
        
        Raises:
            Exception: If fetching withdrawal history fails.
        
        Example:
            >>> manager = BinanceWalletManager()
            >>> withdrawals = manager.get_withdrawal_history(coin='BTC', limit=5)
        """
        try:
            params = kwargs
            
            withdrawals = self.exchange.fetch_withdrawals(
                code=coin,
                since=since,
                limit=limit,
                params=params
            )
            
            return withdrawals
        except Exception as e:
            raise Exception(f"Failed to fetch withdrawal history: {str(e)}")
