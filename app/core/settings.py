from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = "mysql+pymysql://root:root@localhost/stock"
    jwt_secret: str = "secret"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
