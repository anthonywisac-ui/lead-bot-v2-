# Gemini AI Integration for conversational ordering
import aiohttp
import json
import traceback
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class GeminiChat:
    def __init__(self):
        self.conversations = {}  # Store per phone number

    def get_conversation(self, phone_number):
        """Get conversation history for a phone number"""
        if phone_number not in self.conversations:
            self.conversations[phone_number] = []
        return self.conversations[phone_number]

    def add_message(self, phone_number, role, content):
        """Add message to conversation"""
        conv = self.get_conversation(phone_number)
        conv.append({"role": role, "content": content})
        # Keep only last 10 messages to save tokens
        if len(conv) > 20:
            self.conversations[phone_number] = conv[-20:]

    def clear_conversation(self, phone_number):
        """Clear conversation history"""
        if phone_number in self.conversations:
            self.conversations[phone_number] = []

async def chat_with_gemini(
    phone_number,
    user_message,
    restaurant_name="Wild Bites Restaurant",
    lang="en",
    menu_summary=""
):
    """
    Chat with Gemini AI

    Returns:
    {
        "success": True/False,
        "message": str,
        "suggestion": str (optional),
        "error": str (optional)
    }
    """
    gemini = GeminiChat()

    try:
        # Get conversation history
        conv_history = gemini.get_conversation(phone_number)
        gemini.add_message(phone_number, "user", user_message)

        # System prompt
        system_prompt = f"""You are a friendly and helpful customer service representative for {restaurant_name}.

Your responsibilities:
1. Assist customers with menu inquiries
2. Help with ordering process
3. Provide recommendations based on customer preferences
4. Answer questions about food, delivery, and prices
5. Be warm, casual, and natural in conversation
6. Keep responses short (2-3 sentences max)
7. Use appropriate emojis naturally

Restaurant Info:
- Name: {restaurant_name}
- Language: {lang}
- Menu: {menu_summary}

Guidelines:
- Always be helpful and patient
- If customer seems interested in ordering, guide them smoothly
- If they ask about something not on the menu, politely explain
- Suggest popular items when appropriate
- Handle complaints professionally and offer solutions

Respond naturally in {lang}."""

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": system_prompt}]
                },
                {
                    "role": "model",
                    "parts": [{"text": "I understand. I will act as a helpful customer service representative for this restaurant, keeping responses short and friendly."}]
                }
            ] + [
                {
                    "role": msg["role"],
                    "parts": [{"text": msg["content"]}]
                }
                for msg in conv_history[-6:]  # Last 6 messages for context
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 150,
            }
        }

        # Call Gemini API
        async with aiohttp.ClientSession() as session:
            url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    print(f"❌ Gemini error: {resp.status} - {error_text}")
                    return {
                        "success": False,
                        "message": "Sorry, I'm having trouble understanding. Please try again.",
                        "error": f"API Error: {resp.status}"
                    }

                result = await resp.json()

                # Extract response
                if "candidates" not in result or not result["candidates"]:
                    return {
                        "success": False,
                        "message": "Sorry, I couldn't generate a response. Please try again.",
                        "error": "No candidates in response"
                    }

                ai_message = result["candidates"][0]["content"]["parts"][0]["text"]
                gemini.add_message(phone_number, "model", ai_message)

                return {
                    "success": True,
                    "message": ai_message,
                }

    except Exception as e:
        print(f"❌ Gemini exception: {e}")
        print(traceback.format_exc())
        return {
            "success": False,
            "message": "Sorry, I'm having trouble. Please try again.",
            "error": str(e)
        }

# Global instance
gemini_chat = GeminiChat()

async def get_ai_response(phone, message, restaurant="Wild Bites", lang="en", menu=""):
    """Wrapper function for easy use"""
    return await chat_with_gemini(phone, message, restaurant, lang, menu)
