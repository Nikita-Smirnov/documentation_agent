from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION_NAME: str
    EMBEDDING_MODEL_NAME: str
    VECTOR_SIZE: int

    API_KEY: str
    OLLAMA_HOST: str
    OLLAMA_PORT: int
    OLLAMA_MODEL: str

    @property
    def qdrant_url(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @property
    def ollama_url(self):
        return f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"


settings = Settings()
