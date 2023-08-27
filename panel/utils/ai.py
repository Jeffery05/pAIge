import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def chat(prompt,oldMsg):
    msg = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt +" "+ oldMsg}
        ]
    )
    return msg['choices'][0]['message']['content']
