from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
# Base_dir nechta papka ichida bolsa shuncha parent yoziladi
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_DIR = BASE_DIR / ".env"

assert ENV_DIR.exists(), f"{ENV_DIR} not found."


class AppSettings(BaseSettings):
    # DATABASE uchun 
    DB_HOST: str |None = None
    DB_USER: str |None = None
    DB_PORT: str |None = None
    DB_NAME: str |None = None
    DB_PASSWORD: str |None = None
    SQLITE_URL: str |None = None
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    DEFAULT_TOKEN_EXPIRE_MINUTE: int
    
    
    HOST: str
    # bot
    BOT_TOKEN: str
    
    model_config =  SettingsConfigDict(
        env_file=ENV_DIR,
        env_file_encoding='utf-8',
        extra='ignore'
    )
    @property
    def DB_URL(self):
        if self.SQLITE_URL is None:
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return self.SQLITE_URL
    
        
settings = AppSettings()