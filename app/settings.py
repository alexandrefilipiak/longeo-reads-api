from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the app. Pydantic will read all environment variables
    from .env and transform them from UPPER_SNAKE_CASE to snake_case.
    """
    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file='.env.local',
        extra='allow',
        env_file_encoding='utf-8'
    )

    # General
    app_title: str = 'The Flutterflow Starter Kit'
    environment: str = 'development'
    app_description: str = 'Set the title and description in settings.py'
    log_level: str = 'DEBUG'
    slack_webhook_url: str | None = None
    require_verified_email: bool = False
    frontend_origin: str = ''
    support_email: str = ''

    # Supabase
    supabase_url: str = 'https://test123.supabase.co'
    supabase_secret_key: str = 'test123'
    supabase_anon_key: str = 'test123'
    supabase_jwt_secret: str = 'test123'
    users_table: str = 'users'

    # Firebase Auth
    firebase_config: dict = {}
    firebase_web_api_key: str = 'test123'

    # Cloudinary
    cloudinary_cloud_name: str = 'test123'
    cloudinary_api_key: str = 'test234'
    cloudinary_api_secret: str = 'test456'
    cloudinary_folder: str = ''
    avatar_placeholder_url: str = ''

    # Resend Emailer
    resend_api_key: str = 'sk_test_test123'
    disable_email: bool = True
    from_email: str = ''
    from_name: str = 'FFSK Admin'


@lru_cache()
def get_settings():
    return Settings()
