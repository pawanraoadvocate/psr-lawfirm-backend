from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/psrlaw"
    SECRET_KEY: str = "change-this-to-a-long-random-string-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AWS_BUCKET_NAME: str = "psr-lawfirm-documents"
    AWS_REGION: str = "ap-south-1"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
