from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM
    llm_api_key: str = "sk-PNoBeaZqoztJmvS36pMfyXQhe5dSToluyV4ffkOTkqCg4Thx"
    llm_base_url: str = "http://localhost:3000/v1"
    llm_model: str = "qwen-flash"

    # Database
    database_url: str = "postgresql://postgres:.520Zxy1314.@localhost:5432/research_copilot"

    # App
    app_name: str = "Research Copilot"
    log_level: str = "INFO"


settings = Settings()
