from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, BaseModel

from src.models import QuestionInstruction


class EnvConfig(BaseSettings):
    hf_token: SecretStr
    openai_token: SecretStr
    low_performance_mode: bool = False

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class QuestionInstructionsConfig(BaseModel):
    questions: list[QuestionInstruction]

    @classmethod
    def load_config(cls, filename: str) -> "QuestionInstructionsConfig":
        with open(filename, "r", encoding="utf-8") as f:
            return cls.model_validate_json(f.read())


class Config(BaseModel):
    env: EnvConfig
    questions_config: QuestionInstructionsConfig

    @classmethod
    def load_config(cls, filename: str = "src/config/questions.json") -> "Config":
        return cls(
            env=EnvConfig(),
            questions_config=QuestionInstructionsConfig.load_config(filename)
        )
