"""Check for Claude 4.1 and newest models"""
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Check for Claude 4.1 and latest
newest_models = [
    "claude-4.1-sonnet",
    "claude-sonnet-4.1",
    "claude-4.1-opus",
    "claude-opus-4.1",
    "claude-sonnet-4.1-20250514",
    "claude-opus-4.1-20250514",
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
]

print("Checking for Claude 4.1 and latest models...")
print("=" * 60)

best_model = None

for model in newest_models:
    try:
        message = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"FOUND: {model}")
        if not best_model:
            best_model = model
    except Exception as e:
        if "not_found" in str(e).lower():
            print(f"Not available: {model}")
        else:
            print(f"Error: {model} - {str(e)[:50]}")

print("\n" + "=" * 60)
if best_model:
    print(f"BEST MODEL TO USE: {best_model}")
else:
    print("No 4.1 found, using Claude 4 Opus")
print("=" * 60)

