import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def chat(message, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    return response["choices"][0]["message"]["content"]
