import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()

# For Gemini
# =================
# gemini_key=os.getenv('gemini_api_key')
# client = genai.Client(api_key=gemini_key)

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     input="Hi there! I am Anirban. Explain how AI works in a few words"
# )
# print(interaction.output_text)
# --------------------------------------------------------------------------------

# For Openai
# =============
gemini_key=os.getenv('gemini_api_key')
client = OpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        { "role": "system", "content": "You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that." },
        { "role": "user", "content": "Hey, can you help me solve the a + b whole square"}
    ]
)

print(response.choices[0].message.content)