"""
Flask application configuration settings.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # API configuration
    API_TITLE = 'Flask API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Ensure SECRET_KEY is set in production
    if not os.getenv('SECRET_KEY'):
        raise ValueError("SECRET_KEY environment variable must be set in production")


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}