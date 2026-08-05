import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("GROQ_API_KEY")

# Create the Groq client
client = Groq(api_key=api_key)

# Send a simple message
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hello! Can you introduce yourself in one sentence?"}
    ]
)

# Print the reply
print(response.choices[0].message.content)