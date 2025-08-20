"""Configuration settings for the FURIA chatbot application."""
import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'furia-chatbot-secret-key-dev'
    DEBUG = False
    TESTING = False
    
    # API settings
    HLTV_DOMAIN = 'https://www.hltv.org/'
    REQUEST_TIMEOUT = 30
    
    # NLP settings
    DEFAULT_CONFIDENCE_THRESHOLD = 65
    MAX_MESSAGE_LENGTH = 500
    
    # Chatbot settings
    MAX_RESPONSE_LENGTH = 2000
    ENABLE_LOGGING = True
    
    @staticmethod
    def init_app(app):
        """Initialize application with config."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENABLE_LOGGING = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    DEFAULT_CONFIDENCE_THRESHOLD = 50  # Lower threshold for testing


config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}