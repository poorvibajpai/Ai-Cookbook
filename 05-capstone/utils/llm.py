import os
from openai import OpenAI
from utils.prompts import build_support_prompt

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_support_reply(user_message: str, retrieved_context: str, sentiment: str, escalate: bool) -> str:
    prompt = build_support_prompt(
        user_message=user_message,
        retrieved_context=retrieved_context,
        sentiment=sentiment,
        escalate=escalate,
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text