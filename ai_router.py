import os
import requests
from typing import Optional

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "inclusionai/ling-3.0-tiny:free"
OPENROUTER_API_URL = "https://openrouter.io/api/v1/chat/completions"

class ConversationManager:
    def __init__(self):
        self.conversations = {}  # Store per phone number

    def get_conversation(self, phone_number: str):
        if phone_number not in self.conversations:
            self.conversations[phone_number] = []
        return self.conversations[phone_number]

    def add_message(self, phone_number: str, role: str, content: str):
        self.conversations[phone_number].append({
            "role": role,
            "content": content
        })

    def clear_conversation(self, phone_number: str):
        if phone_number in self.conversations:
            self.conversations[phone_number] = []


conversation_manager = ConversationManager()


async def chat_with_ai(phone_number: str, user_message: str) -> dict:
    """
    Chat with AI model and get response
    Returns: {"type": "chat|routing", "message": str, "options": list, "selected": str}
    """
    try:
        conv = conversation_manager.get_conversation(phone_number)
        conversation_manager.add_message(phone_number, "user", user_message)

        system_prompt = """You are a helpful AI assistant for lead routing.
Your job is to:
1. Greet users warmly
2. Understand their needs
3. When appropriate, offer them options to choose a service

Available services:
1) Restaurant Lead Bot - For restaurant inquiries and orders
2) Aesthetic & Dental Lead Bot - For beauty and dental services
3) Real Estate Lead Bot - For property inquiries

If user is interested in any service, extract their choice and respond with the service number.

Format your response naturally. If you detect their interest in a specific service,
end with: [SERVICE_ID:1] or [SERVICE_ID:2] or [SERVICE_ID:3]

If they seem undecided, offer the options clearly."""

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                *conv
            ],
            "temperature": 0.7,
            "max_tokens": 256,
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Lead Bot Pipeline",
        }

        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"❌ OpenRouter error: {response.text}")
            return {
                "type": "chat",
                "message": "Sorry, I'm having trouble understanding. Please try again.",
                "error": response.text
            }

        result = response.json()
        ai_message = result["choices"][0]["message"]["content"]

        conversation_manager.add_message(phone_number, "assistant", ai_message)

        # Check if AI detected a service selection
        service_id = None
        if "[SERVICE_ID:1]" in ai_message:
            service_id = 1
            ai_message = ai_message.replace("[SERVICE_ID:1]", "").strip()
        elif "[SERVICE_ID:2]" in ai_message:
            service_id = 2
            ai_message = ai_message.replace("[SERVICE_ID:2]", "").strip()
        elif "[SERVICE_ID:3]" in ai_message:
            service_id = 3
            ai_message = ai_message.replace("[SERVICE_ID:3]", "").strip()

        # Check if we should offer options
        show_options = user_message.lower() in ["hi", "hello", "hey", "start", "help"] or \
                      "option" in ai_message.lower() or \
                      "service" in ai_message.lower()

        return {
            "type": "routing" if service_id else "chat",
            "message": ai_message,
            "service_id": service_id,
            "show_options": show_options,
            "options": [
                "🍔 Restaurant Lead Bot",
                "💅 Aesthetic & Dental Lead Bot",
                "🏠 Real Estate Lead Bot"
            ] if show_options else None
        }

    except Exception as e:
        print(f"❌ AI error: {e}")
        return {
            "type": "chat",
            "message": "Sorry, I'm having trouble. Please try again.",
            "error": str(e)
        }
