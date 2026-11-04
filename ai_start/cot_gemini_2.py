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
    You need to first PLAN what needs to be done.
    Once you think enough PLAN has been done, give an OUTPUT.
"""

# 1. Pass the System Prompt and JSON config directly into the session configuration
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT, # No more faking chat history!
    response_mime_type="application/json",
    response_schema=CoTResponse,
    temperature=0.2,
)

# 2. Initialize the automated chat session
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=config
)

print("\n\n\n")
user_query = input("👉🏻 ")

# 3. Use send_message(). The SDK builds the Content and Part objects automatically.
response = chat.send_message(user_query)

while True:
    raw_result = response.text
    parsed_result = CoTResponse.model_validate_json(raw_result)

    if parsed_result.step == "START":
        print("🔥", parsed_result.content)
        # Just pass standard strings. The SDK handles the rest and appends it to history.
        response = chat.send_message("Acknowledge start and move to planning.")
        continue

    elif parsed_result.step == "PLAN":
        print("🧠", parsed_result.content)
        response = chat.send_message("Proceed with the next step of your chain of thought.")
        continue

    elif parsed_result.step == "OUTPUT":
        print("🤖", parsed_result.content)
        break

print("\n\n\n")