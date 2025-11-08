"""Test different Claude model names"""
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# List of model names to try
models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-latest",
    "claude-3-opus-latest",
]

print("Testing Claude Models...")
print("=" * 60)

for model in models_to_try:
    try:
        message = client.messages.create(
            model=model,
            max_tokens=5,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"SUCCESS: {model}")
        print(f"  Response: {message.content[0].text}")
        break  # Stop at first working model
    except Exception as e:
        error_msg = str(e)
        if "not_found" in error_msg.lower():
            print(f"NOT FOUND: {model}")
        else:
            print(f"ERROR: {model} - {error_msg[:50]}")

print("=" * 60)

