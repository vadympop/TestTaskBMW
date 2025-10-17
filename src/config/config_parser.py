from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, BaseModel


class EnvConfig(BaseSettings):
    hf_token: SecretStr
    openai_token: SecretStr
    low_performance_mode: bool = False

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class QuestionAnswering(BaseModel):
    text: str
    answer_format: str
    save_to_column: int


class QuestionAnsweringConfig(BaseModel):
    questions: list[QuestionAnswering]

    @classmethod
    def load_config(cls, filename: str) -> "QuestionAnsweringConfig":
        with open(filename, "r", encoding="utf-8") as f:
            return cls.model_validate_json(f)


class Config(BaseModel):
    env: EnvConfig
    questions_config: QuestionAnsweringConfig

    @classmethod
    def load_config(cls, filename: str = "questions.json") -> "Config":
        return cls(
            env=EnvConfig(),
            questions_config=QuestionAnsweringConfig.load_config(filename)
        )
