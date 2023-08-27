import openai

openai.api_key = "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"


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
