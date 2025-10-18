import logging

from openai import OpenAI

from src.models import AIAnswersOutput, QuestionInstruction


logger = logging.getLogger(__name__)

def get_questions_answers(transcript: str, api_key: str, questions: list[QuestionInstruction]) -> AIAnswersOutput:
    """
    Use openai API(chatgpt) to get answers for specified questions from transcribed text.

    :param transcript: str
    :param api_key: str
    :param questions: list[QuestionInstruction]
    :return: AiAnswersOutput
    """
    logger.info("Using AI to answer questions from transcribed text")

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
        text_format=AIAnswersOutput
    )

    return response.output_parsed
