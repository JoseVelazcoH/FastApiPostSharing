from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    DB_HOST: str
    DB_PORT: int
    API_SECRET: str
    IMAGEKIT_PRIVATE_KEY: str

    @property
    def base_url(self) -> str:
        return f"http://{self.DB_HOST}:{self.DB_PORT}"


settings = Settings()
