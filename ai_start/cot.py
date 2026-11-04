import os
from typing import Literal
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

# Initialize the official Gemini Client
# It automatically picks up GEMINI_API_KEY from your environment variables
client = genai.Client()

# Define your exact structure using Pydantic
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

# Use Gemini's standard Content type to keep up with chat history
chats: list[types.Content] = [
    types.Content(role="user", parts=[types.Part.from_text(text=SYSTEM_PROMPT)]),
    types.Content(role="model", parts=[types.Part.from_text(text="Understood. I will strictly follow the execution loop step-by-step.")])
]

user_query = input("👉🏻 ")
chats.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))

while True:
    # Generate content using the proper config object
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Use the stable, up-to-date Flash model
        contents=chats,
        config=types.GenerateContentConfig(
            # This completely replaces the open-ended text instructions!
            response_mime_type="application/json",
            response_schema=CoTResponse,
            temperature=0.2,
        ),
    )

    # The SDK guarantees response.text matches your structure perfectly
    raw_result = response.text
    
    # Track history cleanly
    chats.append(types.Content(role="model", parts=[types.Part.from_text(text=raw_result)]))

    # Safely parse your schema directly into Python attributes
    parsed_result = CoTResponse.model_validate_json(raw_result)

    if parsed_result.step == "START":
        print("🔥", parsed_result.content)
        continue

    elif parsed_result.step == "PLAN":
        print("🧠", parsed_result.content)
        continue

    elif parsed_result.step == "OUTPUT":
        print("🤖", parsed_result.content)
        break

print("\n\n\n")
