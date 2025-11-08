"""
Test script to verify OpenAI and Anthropic API keys.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("API KEY VERIFICATION TEST")
print("=" * 60)

# Check if keys exist
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

print("\n1. CHECKING API KEY PRESENCE:")
print("-" * 60)
print(f"[OK] OPENAI_API_KEY: {'Found' if openai_key else '[X] NOT FOUND'}")
if openai_key:
    print(f"  Preview: {openai_key[:20]}...{openai_key[-4:]}")

print(f"[OK] ANTHROPIC_API_KEY: {'Found' if anthropic_key else '[X] NOT FOUND'}")
if anthropic_key:
    print(f"  Preview: {anthropic_key[:20]}...{anthropic_key[-4:]}")

print(f"[OK] OPENROUTER_API_KEY: {'Found' if openrouter_key else '[X] NOT FOUND'}")
if openrouter_key:
    print(f"  Preview: {openrouter_key[:20]}...{openrouter_key[-4:]}")

# Test OpenAI
print("\n2. TESTING OPENAI API:")
print("-" * 60)
if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        print("Sending test request to GPT-4...")
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": "Say 'API working' if you receive this"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"✅ SUCCESS!")
        print(f"   Model: gpt-4-turbo-preview")
        print(f"   Response: {result}")
        print(f"   Tokens used: {tokens}")
        print(f"   Estimated cost: ${(tokens / 1000) * 0.01:.4f}")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
else:
    print("❌ Skipped - No API key found")

# Test Anthropic
print("\n3. TESTING ANTHROPIC API:")
print("-" * 60)
if anthropic_key:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_key)
        
        print("Sending test request to Claude...")
        
        # Try the latest model first
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Say 'API working' if you receive this"}
                ]
            )
            model_used = "claude-3-5-sonnet-20241022"
        except Exception as e1:
            print(f"   First attempt failed: {str(e1)[:50]}")
            print("   Trying alternative model...")
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Say 'API working' if you receive this"}
                ]
            )
            model_used = "claude-3-5-sonnet-20240620"
        
        result = message.content[0].text
        tokens_in = message.usage.input_tokens
        tokens_out = message.usage.output_tokens
        
        print(f"✅ SUCCESS!")
        print(f"   Model: {model_used}")
        print(f"   Response: {result}")
        print(f"   Tokens used: {tokens_in + tokens_out} (in: {tokens_in}, out: {tokens_out})")
        print(f"   Estimated cost: ${((tokens_in / 1000) * 0.003 + (tokens_out / 1000) * 0.015):.4f}")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check for common issues
        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
            print("   Issue: Authentication failed - check API key validity")
        elif "not_found" in str(e).lower():
            print("   Issue: Model not found - may need different model name")
        elif "rate_limit" in str(e).lower():
            print("   Issue: Rate limit exceeded - wait and try again")
        elif "insufficient" in str(e).lower():
            print("   Issue: Insufficient credits/quota")
else:
    print("❌ Skipped - No API key found")

# Test OpenRouter
print("\n4. TESTING OPENROUTER API:")
print("-" * 60)
if openrouter_key:
    try:
        import requests
        
        print("Sending test request to OpenRouter...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {"role": "user", "content": "Say 'API working' if you receive this"}
                ],
                "max_tokens": 10
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data['choices'][0]['message']['content']
            print(f"✅ SUCCESS!")
            print(f"   Model: anthropic/claude-3.5-sonnet")
            print(f"   Response: {result}")
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
else:
    print("❌ Skipped - No API key found")

# Summary
print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)

working_count = 0
total_count = 3

if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        working_count += 1
        print("✅ OpenAI: WORKING")
    except:
        print("❌ OpenAI: FAILED")
else:
    print("⚠️  OpenAI: NO KEY")

if anthropic_key:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_key)
        client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=5,
            messages=[{"role": "user", "content": "test"}]
        )
        working_count += 1
        print("✅ Anthropic: WORKING")
    except:
        print("❌ Anthropic: FAILED")
else:
    print("⚠️  Anthropic: NO KEY")

if openrouter_key:
    try:
        import requests
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {openrouter_key}"},
            json={"model": "anthropic/claude-3.5-sonnet", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5}
        )
        if r.status_code == 200:
            working_count += 1
            print("✅ OpenRouter: WORKING")
        else:
            print("❌ OpenRouter: FAILED")
    except:
        print("❌ OpenRouter: FAILED")
else:
    print("⚠️  OpenRouter: NO KEY")

print(f"\n{working_count}/{total_count} APIs working correctly")

if working_count == 0:
    print("\n⚠️  WARNING: No APIs are working! Check your .env file.")
elif working_count < total_count:
    print(f"\n⚠️  {total_count - working_count} API(s) have issues - check details above")
else:
    print("\n🎉 All APIs working perfectly!")

print("=" * 60)

