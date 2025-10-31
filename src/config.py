import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str
    DATABASE: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '../.env'),
        env_prefix='DB_',
        extra='allow'
    )


settings = Settings()
