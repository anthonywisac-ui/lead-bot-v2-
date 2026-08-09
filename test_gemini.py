#!/usr/bin/env python3
# Quick test to verify Gemini API is working

import os
import asyncio
from dotenv import load_dotenv

# Try different import paths
try:
    from google import genai
    print("✅ Using: from google import genai")
except ImportError:
    try:
        import genai
        print("✅ Using: import genai")
    except ImportError:
        print("❌ Neither import worked. Checking package...")
        import subprocess
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        if 'google-genai' in result.stdout:
            print("✅ google-genai is installed")
            try:
                from google.genai import Client
                genai = type('genai', (), {'Client': Client})()
                print("✅ Using: from google.genai import Client")
            except:
                pass
        print("\n📦 Installed packages containing 'google':")
        for line in result.stdout.split('\n'):
            if 'google' in line.lower():
                print(f"  {line}")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"🔍 API Key loaded: {GEMINI_API_KEY[:20]}...")

# Initialize client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Gemini client initialized")
except Exception as e:
    print(f"❌ Client init failed: {e}")
    exit(1)

# Test 1: Simple text generation
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("TEST 1: Simple Text Generation")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say 'Gemini is working' in exactly 4 words"
    )
    print(f"✅ Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Structured format (like order summary)
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("TEST 2: Order Summary Format")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

try:
    system_prompt = """You are a friendly restaurant chatbot.
Create a SHORT order summary.
- Keep it under 50 words
- Use emojis
- Be warm"""

    context = """
Order Details:
Items: 2x Biryani, 1x Raita
Delivery: Home delivery
Customer Location: Pakistan
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\n{context}"}
                ]
            }
        ]
    )
    print(f"✅ Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Async version (like in production)
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("TEST 3: Async Call (Production Style)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

async def test_async():
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash",
            contents=[{"role": "user", "parts": [{"text": "Say 'Async works' in 2 words"}]}]
        )
        print(f"✅ Async Response: {response.text}")
    except Exception as e:
        print(f"❌ Async Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_async())

# Test 4: JSON response (like intent classification)
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("TEST 4: JSON Response")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": 'Respond ONLY with JSON: {"status": "working", "test": true}'
                    }
                ]
            }
        ]
    )
    print(f"✅ JSON Response: {response.text}")

    # Try parsing
    import json
    result = json.loads(response.text)
    print(f"✅ Parsed: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("✅ ALL TESTS COMPLETED")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
