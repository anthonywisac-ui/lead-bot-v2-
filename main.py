import os
import json
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from config import VERIFY_TOKEN
from flow_complete import handle_complete_flow

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

            print(f"\n📨 Message from {sender}")

            # Text messages
            if msg_type == "text":
                text = message.get("text", {}).get("body", "").strip()
                print(f"   Text: {text}")
                await handle_complete_flow(sender, text, is_interactive=False)

            # Interactive messages (buttons/lists)
            elif msg_type == "interactive":
                interactive = message.get("interactive", {})
                button_reply = interactive.get("button_reply", {})
                list_reply = interactive.get("list_reply", {})

                if button_reply:
                    button_id = button_reply.get("id")
                    print(f"   Button: {button_id}")
                    if button_id:
                        await handle_complete_flow(sender, button_id, is_interactive=True)

                elif list_reply:
                    item_id = list_reply.get("id")
                    print(f"   List Item: {item_id}")
                    if item_id:
                        await handle_complete_flow(sender, item_id, is_interactive=True)

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Error: {e}")
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "wild-bites-restaurant-bot",
        "whatsapp_configured": bool(os.getenv("WHATSAPP_TOKEN"))
    }


# ==================== RUN ====================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"\n🚀 Wild Bites Restaurant Bot starting on port {port}...")
    print(f"✅ Multi-country system ready")
    print(f"✅ Button-based menu ready")
    print(f"✅ Images integrated\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
