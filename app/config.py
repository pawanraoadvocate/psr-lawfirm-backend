from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./psrlaw.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AWS_BUCKET_NAME: str = "psr-lawfirm-documents"
    AWS_REGION: str = "ap-south-1"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
