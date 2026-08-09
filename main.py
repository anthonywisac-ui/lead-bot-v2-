import os
import json
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from config import VERIFY_TOKEN
from flow_buttons import (
    handle_button_press, handle_list_item_selection,
    send_country_selection, send_text_message
)
from db import customer_sessions

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

            print(f"\n📨 Incoming Message from {sender}")
            print(f"   Type: {msg_type}")

            # Handle text messages
            if msg_type == "text":
                text = message.get("text", {}).get("body", "").strip()
                print(f"   Text: {text}")

                # Check if user is asking for country selection
                if text.lower() in ["owner", "countries", "select", "change"]:
                    await send_country_selection(sender)
                else:
                    # For other text, just acknowledge
                    await send_text_message(sender, "👍 Got it! Use buttons to navigate the menu")

            # Handle button clicks (category, quantity, delivery, payment)
            elif msg_type == "interactive":
                interactive = message.get("interactive", {})
                button_reply = interactive.get("button_reply", {})
                list_reply = interactive.get("list_reply", {})

                if button_reply:
                    button_id = button_reply.get("id")
                    print(f"   Button: {button_id}")
                    if button_id:
                        await handle_button_press(sender, button_id)

                elif list_reply:
                    item_id = list_reply.get("id")
                    print(f"   List Selection: {item_id}")
                    if item_id:
                        await handle_list_item_selection(sender, item_id)

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "restaurant-bot-pipeline",
        "whatsapp_configured": bool(os.getenv("WHATSAPP_TOKEN") and os.getenv("WHATSAPP_PHONE_NUMBER_ID"))
    }


# ==================== RUN ====================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"\n🚀 Restaurant Bot Pipeline starting on port {port}...")
    print(f"   Phone ID: {os.getenv('WHATSAPP_PHONE_NUMBER_ID')}")
    print(f"   Manager: {os.getenv('MANAGER_NUMBER')}\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
