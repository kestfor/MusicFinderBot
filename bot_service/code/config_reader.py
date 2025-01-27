from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    bot_token: SecretStr
    spotify_username: SecretStr
    spotify_client_id: SecretStr
    spotify_client_secret: SecretStr
    data_path: SecretStr

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


config = Settings()
