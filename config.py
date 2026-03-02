"""
Configuration management for the Fractal Trading Engine.
Centralized config prevents hardcoded values and enables easy environment switching.
"""
import os
from dataclasses import dataclass
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key_env: str
    api_secret_env: str
    rate_limit: int = 10  # requests per second
    supported_markets: List[str] = None
    
    def get_credentials(self) -> Dict:
        """Safely retrieve API credentials from environment"""
        api_key = os.getenv(self.api_key_env)
        api_secret = os.getenv(self.api_secret_env)
        
        if not api_key or not api_secret:
            raise ValueError(
                f"Missing credentials for {self.name}. "
                f"Set {self.api_key_env} and {self.api_secret_env} in .env"
            )
        
        return {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        }

class TradingConfig:
    """Main configuration class with validation"""
    
    # Exchange configurations
    EXCHANGES = {
        'binance': ExchangeConfig(
            name='binance',
            api_key_env='BINANCE_API_KEY',
            api_secret_env='BINANCE_API_SECRET',
            supported_markets=['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
        ),
        'coinbase': ExchangeConfig(
            name='coinbase',
            api_key_env='COINBASE_API_KEY',
            api_secret_env='COINBASE_API_SECRET',
            rate_limit=5
        )
    }
    
    # Trading parameters
    DEFAULT_TIMEFRAME = '1h'
    MAX_POSITION_SIZE = 0.1  # 10% of portfolio per trade
    MIN_CONFIDENCE_THRESHOLD = 0.65
    
    # Fractal analysis
    FRACTAL_WINDOW_SIZE = 20
    MIN_FRACTAL_POINTS = 5
    PATTERN_TYPES = ['bullish', 'bearish', 'consolidation']
    
    # Risk management
    STOP_LOSS_PERCENT = 0.02  # 2%
    TAKE_PROFIT_RATIO = 2.0   # 2:1 reward:risk
    
    # Firebase configuration
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
    FIRESTORE_COLLECTIONS = {
        'market_data': 'market_data',
        'fractal_patterns': 'fractal_patterns',
        'trading_signals': 'trading_signals',
        'executed_trades': 'executed_trades',
        'system_metrics': 'system_metrics'
    }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate all configuration parameters"""
        validations = []
        
        # Check required environment variables
        required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
        for var in required_vars:
            if not os.getenv(var):
                validations.append(f"Missing required environment variable: {var}")
        
        # Validate Firebase credentials exist
        if not os.path.exists(cls.FIREBASE_CREDENTIALS_PATH):
            validations.append(f"Firebase credentials not found at: {cls.FIREBASE_CREDENTIALS_PATH}")
        
        if validations:
            raise ConfigurationError("\n".join(validations))
        
        return True

class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass

# Global config instance
config = TradingConfig()