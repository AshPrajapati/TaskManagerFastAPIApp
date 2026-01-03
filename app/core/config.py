from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_TEST_DB: str
    TEST_POSTGRES_PORT: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRES: float

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def DATABASE_URL(self):
        return (f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@localhost:{self.TEST_POSTGRES_PORT}/{self.POSTGRES_TEST_DB}")


settings = Settings()
