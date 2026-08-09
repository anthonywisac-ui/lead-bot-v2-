import os
import json
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# Configuration
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your-verify-token")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
BUSINESS_ACCOUNT_ID = os.getenv("BUSINESS_ACCOUNT_ID")

app = FastAPI()

# ==================== WEBHOOK SETUP ====================
@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook endpoint"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"✅ Webhook verified!")
        return PlainTextResponse(challenge)
    else:
        return PlainTextResponse("Forbidden", status_code=403)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming messages from WhatsApp"""
    try:
        data = await request.json()

        if data.get("object") != "whatsapp_business_account":
            return {"status": "ok"}

        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        for message in messages:
            sender = message.get("from")
            msg_type = message.get("type")

            print(f"\n📨 Incoming Message")
            print(f"   From: {sender}")
            print(f"   Type: {msg_type}")

            if msg_type == "text":
                text = message.get("text", {}).get("body", "")
                print(f"   Text: {text}")

                # Process message
                await process_message(sender, text)

            elif msg_type == "interactive":
                interactive = message.get("interactive", {})
                button_reply = interactive.get("button_reply", {})
                list_reply = interactive.get("list_reply", {})

                reply_id = button_reply.get("id") or list_reply.get("id")
                print(f"   Reply ID: {reply_id}")

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}


# ==================== MESSAGE PROCESSING ====================
async def process_message(sender: str, text: str):
    """Process incoming message"""
    text = text.strip().lower()

    print(f"   ✓ Processing: {text}")

    if text in ["hi", "hello", "assalam", "assalamualaikum", "salam"]:
        await send_message(sender, "👋 Hello! Welcome to Lead Bot.\n\nWhat can I help you with today?")

    elif text == "menu":
        await send_interactive_menu(sender)

    else:
        await send_message(sender, f"✓ Received: {text}\n\nReply with 'menu' to see options.")


async def send_message(phone_number: str, message: str):
    """Send text message via WhatsApp Business API"""
    try:
        url = f"https://graph.instagram.com/v18.0/{WHATSAPP_PHONE_ID}/messages"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message,
            },
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            msg_id = response.json().get("messages", [{}])[0].get("id")
            print(f"   ✅ Message sent to {phone_number} (ID: {msg_id})")
            return True
        else:
            print(f"   ❌ Failed to send: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Error sending message: {e}")
        return False


async def send_interactive_menu(phone_number: str):
    """Send interactive menu with buttons"""
    try:
        url = f"https://graph.instagram.com/v18.0/{WHATSAPP_PHONE_ID}/messages"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "What would you like to do?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "option_1",
                                "title": "Option 1"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "option_2",
                                "title": "Option 2"
                            }
                        },
                    ]
                }
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"   ✅ Interactive menu sent to {phone_number}")
            return True
        else:
            print(f"   ❌ Failed to send menu: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Error sending menu: {e}")
        return False


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "lead-bot",
        "whatsapp_configured": bool(WHATSAPP_TOKEN and WHATSAPP_PHONE_ID)
    }


# ==================== RUN ====================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"\n🚀 Lead Bot starting on port {port}...")
    print(f"   Phone ID: {WHATSAPP_PHONE_ID}")
    print(f"   Business Account: {BUSINESS_ACCOUNT_ID}\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
