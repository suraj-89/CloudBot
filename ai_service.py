from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(question: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":"You are CloudBot. Give short, simple answers in 3-5 lines suitable for beginners."
            },
            {
                "role":"user",
                "content":question
            }
        ]
    )

    return response.choices[0].message.content

   