from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    token_expire_minutes: int

    database_name_test: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Config()

