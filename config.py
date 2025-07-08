from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Credentials
    oxylabs_username: str
    oxylabs_password: str
    openai_api_key: str

    # Application Settings
    log_level: str = "INFO"
    debug: bool = False

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Cache Settings
    cache_expiry_days: int = 1
    max_cache_size: int = 1000

    # OpenAI Settings
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7

    # Logging Settings
    log_file: str = "app.log"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields in .env to be ignored


settings = Settings()
