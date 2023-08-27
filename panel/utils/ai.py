import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def chat(prompt):
    msg = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return msg["choices"][0]["message"]["content"]
