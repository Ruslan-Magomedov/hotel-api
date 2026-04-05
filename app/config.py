from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path



class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    DB_PASS: str

    def connection_path(self):
        return f"{self.DB_HOST}/{self.DB_PORT}/{self.DB_NAME}/{self.DB_PASS}"

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env")



settings = Settings()
