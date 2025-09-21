from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    gemini_api_key: str
    serp_api_key: str
    port: int
    mcp_port: int

    class Config:
        env_file = ".env"


settings = Settings()
