from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:3000"
    
    storage_mode: str = "local"
    
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = ""
    aws_dynamodb_table: str = ""
    aws_lambda_function: str = ""
    
    # Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    
    # Legacy settings (kept for compatibility)
    sentiment_model: str = "gemini"  # Changed to indicate Gemini usage
    enable_ai_fallback: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
