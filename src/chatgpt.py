from openai import OpenAI
from pydantic import BaseModel

from src.config import QuestionAnswering


class Answer(BaseModel):
    index: int
    question: str
    answer: str

class Answers(BaseModel):
    answers: list[Answer]


def get_questions_answers(transcript: str, api_key: str, questions: list[QuestionAnswering]) -> Answers:
    client = OpenAI(api_key=api_key)
    formatted_questions = [
        f"#{i} {q.text}. Формат відповіді: {q.answer_format}" for i, q in enumerate(questions)
    ]

    response = client.responses.parse(
        model="o4-mini",
        input=[
            {
                "role": "system",
                "content": f"В тебе є текст який витягнуто з телефонної розмови між менеджером автосервісу БМВ і клієнтом, твоє завдання відповісти на ці питання по тексту:\n{transcript}",
            },
            {"role": "user", "content": ";".join(formatted_questions)},
        ],
        text_format=Answers
    )

    return response.output_parsed
