from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Campus Parking System"
    # Password dihapus, tersisa root:
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/smart_parking_db"
    
    # Secret keys for JWT
    SECRET_KEY: str = "super_secret_jwt_key_here"  # In production, use env variables
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours

    class Config:
        env_file = ".env"

settings = Settings()