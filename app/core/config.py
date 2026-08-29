from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    SQLALCHEMY_DATABASE_URL : str
    JWT_SECRET_KEY : str = "test_secret_key"
    JWT_ALGORITHM : str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")
    
setting = Setting()