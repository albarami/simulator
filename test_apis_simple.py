"""Simple API test without Unicode characters"""
import os
import sys
from dotenv import load_dotenv

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

print("=" * 60)
print("API VERIFICATION TEST")
print("=" * 60)

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

print("\n1. KEYS FOUND:")
print("-" * 60)
print(f"OpenAI: {openai_key[:15]}..." if openai_key else "OpenAI: MISSING")
print(f"Anthropic: {anthropic_key[:15]}..." if anthropic_key else "Anthropic: MISSING")
print(f"OpenRouter: {openrouter_key[:15]}..." if openrouter_key else "OpenRouter: MISSING")

print("\n2. TESTING OPENAI:")
print("-" * 60)
if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": "Reply with: Working"}],
            max_tokens=5
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
        print(f"Tokens: {response.usage.total_tokens}")
    except Exception as e:
        print(f"FAILED: {str(e)[:100]}")
else:
    print("SKIPPED")

print("\n3. TESTING ANTHROPIC:")
print("-" * 60)
if anthropic_key:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=5,
            messages=[{"role": "user", "content": "Reply with: Working"}]
        )
        print(f"SUCCESS: {message.content[0].text}")
        print(f"Tokens: {message.usage.input_tokens + message.usage.output_tokens}")
    except Exception as e:
        print(f"FAILED: {str(e)[:100]}")
        print(f"Error type: {type(e).__name__}")
else:
    print("SKIPPED")

print("\n4. TESTING OPENROUTER:")
print("-" * 60)
if openrouter_key:
    try:
        import requests
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {openrouter_key}"},
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [{"role": "user", "content": "Reply with: Working"}],
                "max_tokens": 5
            },
            timeout=10
        )
        if r.status_code == 200:
            print(f"SUCCESS: {r.json()['choices'][0]['message']['content']}")
        else:
            print(f"FAILED: HTTP {r.status_code}")
            print(f"Response: {r.text[:100]}")
    except Exception as e:
        print(f"FAILED: {str(e)[:100]}")
else:
    print("SKIPPED")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

