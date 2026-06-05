import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    # LLM
    LLM_API_KEY = os.getenv('LLM_API_KEY', '')
    LLM_API_BASE = os.getenv('LLM_API_BASE', 'https://api.openai.com')
    LLM_DEFAULT_MODEL = os.getenv('LLM_DEFAULT_MODEL', 'gpt-4o-mini')
    LLM_CACHE_TTL = int(os.getenv('LLM_CACHE_TTL', '86400'))  # 24 hours

    # Rate limiting
    RATE_LIMIT_AI_GENERATE = int(os.getenv('RATE_LIMIT_AI_GENERATE', '20'))  # per minute

class DevelopmentConfig(Config):
    DEBUG = True
    # Default to SQLite for zero-dependency local development
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db'))
    REDIS_URL = os.getenv('DEV_REDIS_URL', '')  # Empty = Redis disabled (OK for dev)

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDIS_URL = os.getenv('REDIS_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_URL = 'redis://localhost:6379/1'

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
