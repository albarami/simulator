"""Find the latest Claude models available"""
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Try latest model naming patterns
latest_models = [
    "claude-sonnet-4-20250514",
    "claude-4-sonnet-latest",
    "claude-4-opus-latest", 
    "claude-sonnet-4.0-20250514",
    "claude-opus-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
    "claude-sonnet-3-5-20241022",
    "anthropic.claude-sonnet-4-v1",
]

print("Finding Latest Claude Models...")
print("=" * 60)

working_models = []

for model in latest_models:
    try:
        message = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        result = message.content[0].text
        print(f"WORKS: {model}")
        print(f"  --> {result}")
        working_models.append(model)
    except Exception as e:
        error_str = str(e).lower()
        if "not_found" in error_str or "invalid" in error_str:
            print(f"Not available: {model}")
        else:
            print(f"ERROR {model}: {str(e)[:60]}")

print("\n" + "=" * 60)
if working_models:
    print(f"WORKING MODELS FOUND: {len(working_models)}")
    for m in working_models:
        print(f"  - {m}")
    print(f"\nBest to use: {working_models[0]}")
else:
    print("No working models found!")
    print("Using OpenRouter or OpenAI instead")
print("=" * 60)

