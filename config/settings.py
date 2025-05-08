from pydantic import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Load .env before Pydantic reads it
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DISCORD_TOKEN: str
    BOT_PREFIX: str = "!"
    MODEL_PATH: str = "models/vosk-model-en-us-0.22-lgraph"

    class Config:
        env_file = str(env_path)
        env_file_encoding = "utf-8"

settings = Settings()
