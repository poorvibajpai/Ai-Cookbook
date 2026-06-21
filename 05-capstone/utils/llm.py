import os
from openai import OpenAI, RateLimitError, APIError
from utils.prompts import build_support_prompt

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)


def generate_support_reply(user_message: str, retrieved_context: str, sentiment: str, escalate: bool) -> str:
    prompt = build_support_prompt(
        user_message=user_message,
        retrieved_context=retrieved_context,
        sentiment=sentiment,
        escalate=escalate,
    )

    try:
        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt,
        )
        return response.output_text

    except RateLimitError:
        return (
            "The support assistant is temporarily unavailable because the API quota is exhausted. "
            "Please try again later."
        )

    except APIError:
        return (
            "The support assistant ran into an API error. Please try again in a moment."
        )

    except Exception as e:
        return f"Something went wrong while generating the support reply: {str(e)}"