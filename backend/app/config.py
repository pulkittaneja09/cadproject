from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    
    storage_mode: str = "local"
    
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = ""
    aws_dynamodb_table: str = ""
    aws_lambda_function: str = ""
    
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    enable_ai_fallback: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
