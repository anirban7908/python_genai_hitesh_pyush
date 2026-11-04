import os
from typing import Literal
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

client = genai.Client()


class CoTResponse(BaseModel):
    step: Literal["START", "PLAN", "OUTPUT"]
    content: str


SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT.
"""

print("\n\n\n")

chats: list[types.Content] = [
    types.Content(role="user", parts=[types.Part.from_text(text=SYSTEM_PROMPT)]),
    types.Content(
        role="model",
        parts=[
            types.Part.from_text(
                text="Understood. I will strictly follow the execution loop step-by-step."
            )
        ],
    ),
]

user_query = input("👉🏻 ")
chats.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))

while True:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", 
        contents=chats,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CoTResponse,
            temperature=0.2,
        ),
    )

    raw_result = response.text

    # 1. Append the model's response to the history
    chats.append(
        types.Content(role="model", parts=[types.Part.from_text(text=raw_result)])
    )

    parsed_result = CoTResponse.model_validate_json(raw_result)

    if parsed_result.step == "START":
        print("🔥", parsed_result.content)
        # 2. FIX: Append a user prompt so the next loop run ends with a user turn
        chats.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Acknowledge start and move to planning.")
                ],
            )
        )
        continue

    elif parsed_result.step == "PLAN":
        print("🧠", parsed_result.content)
        # 2. FIX: Append a user prompt so the next loop run ends with a user turn
        chats.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="Proceed with the next step of your chain of thought."
                    )
                ],
            )
        )
        continue

    elif parsed_result.step == "OUTPUT":
        print("🤖", parsed_result.content)
        break

print("\n\n\n")
