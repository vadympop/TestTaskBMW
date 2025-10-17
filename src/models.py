from pydantic import BaseModel


class QuestionInstruction(BaseModel):
    text: str
    answer_format: str
    save_to_column: int


class AIAnswerItem(BaseModel):
    index: int
    question: str
    answer: str


class AIAnswersOutput(BaseModel):
    answers: list[AIAnswerItem]


class AnswerResult(BaseModel):
    answer: str
    save_to_column: int
