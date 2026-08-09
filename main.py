import os
import json
import requests
import stripe
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv
from ai_router import chat_with_ai, conversation_manager

load_dotenv()

# Configuration
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "lead_bot_verify_token_12345")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
BUSINESS_ACCOUNT_ID = os.getenv("BUSINESS_ACCOUNT_ID")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
MANAGER_NUMBER = os.getenv("MANAGER_NUMBER", "923351021321")

stripe.api_key = STRIPE_SECRET_KEY

app = FastAPI()

# ==================== DATA STORES ====================
user_sessions = {}  # Store user state: {phone: {service_id, stage, order, ...}}
saved_orders = {}   # Store completed orders
menu_data = {
    "pizza": [
        {"name": "Margherita", "price": 500, "desc": "Classic cheese pizza"},
        {"name": "Pepperoni", "price": 600, "desc": "Loaded with pepperoni"},
        {"name": "Veggie", "price": 550, "desc": "Fresh vegetables"},
    ],
    "burger": [
        {"name": "Burger Classic", "price": 400, "desc": "Beef burger"},
        {"name": "Chicken Burger", "price": 350, "desc": "Crispy chicken"},
    ]
}

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

            if msg_type == "text":
                text = message.get("text", {}).get("body", "").strip()
                print(f"   Text: {text}")
                await process_user_message(sender, text)

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}


# ==================== MESSAGE PROCESSING ====================
async def process_user_message(phone_number: str, text: str):
    """Process user message through AI or direct command"""

    # Get or create user session
    if phone_number not in user_sessions:
        user_sessions[phone_number] = {"service_id": None, "stage": "greeting", "cart": []}

    session = user_sessions[phone_number]

    # If no service selected yet, use AI routing
    if session["service_id"] is None:
        ai_response = await chat_with_ai(phone_number, text)

        # Send AI message
        await send_message(phone_number, ai_response["message"])

        # If service selected, set it and show menu
        if ai_response.get("service_id"):
            session["service_id"] = ai_response["service_id"]

            if ai_response["service_id"] == 1:
                session["stage"] = "restaurant_greeting"
                await send_message(phone_number,
                    "🍔 Welcome to Restaurant!\n\nWhat would you like?\n\n1️⃣ View Pizza Menu\n2️⃣ View Burger Menu\n3️⃣ View Cart\n4️⃣ Checkout")

        # Show options if needed
        elif ai_response.get("show_options"):
            options_msg = "Choose a service:\n\n1️⃣ 🍔 Restaurant Lead Bot\n2️⃣ 💅 Aesthetic & Dental Lead Bot\n3️⃣ 🏠 Real Estate Lead Bot\n\nReply with number (1-3)"
            await send_message(phone_number, options_msg)

    # If service is restaurant, process order flow
    elif session["service_id"] == 1:
        await handle_restaurant_flow(phone_number, text, session)

    # Other services - show coming soon
    else:
        await send_message(phone_number, "🔄 This service is coming soon! Please check back later.")


# ==================== RESTAURANT FLOW ====================
async def handle_restaurant_flow(phone_number: str, user_input: str, session: dict):
    """Handle restaurant ordering flow"""

    stage = session.get("stage", "greeting")
    user_input = user_input.strip().lower()

    # Menu selection
    if user_input == "1":
        msg = "🍕 *PIZZA MENU*\n\n"
        for idx, item in enumerate(menu_data["pizza"], 1):
            msg += f"{idx}️⃣ {item['name']} - Rs{item['price']}\n   {item['desc']}\n\n"
        msg += "Reply with number (1-3) to add to cart"
        await send_message(phone_number, msg)
        session["menu_type"] = "pizza"

    elif user_input == "2":
        msg = "🍔 *BURGER MENU*\n\n"
        for idx, item in enumerate(menu_data["burger"], 1):
            msg += f"{idx}️⃣ {item['name']} - Rs{item['price']}\n   {item['desc']}\n\n"
        msg += "Reply with number (1-2) to add to cart"
        await send_message(phone_number, msg)
        session["menu_type"] = "burger"

    # Add to cart
    elif user_input in ["1", "2", "3"]:
        menu_type = session.get("menu_type")
        if menu_type and menu_type in menu_data:
            idx = int(user_input) - 1
            if idx < len(menu_data[menu_type]):
                item = menu_data[menu_type][idx]
                session["cart"].append(item)
                await send_message(phone_number,
                    f"✅ Added {item['name']} to cart!\n\n1️⃣ Add more\n2️⃣ View cart\n3️⃣ Checkout")

    # View cart
    elif user_input == "3":
        if session["cart"]:
            msg = "🛒 *YOUR CART*\n\n"
            total = 0
            for idx, item in enumerate(session["cart"], 1):
                msg += f"{idx}. {item['name']} - Rs{item['price']}\n"
                total += item['price']
            msg += f"\n*Total: Rs{total}*\n\n1️⃣ Add more\n2️⃣ Checkout\n3️⃣ Clear cart"
            session["total"] = total
            await send_message(phone_number, msg)
        else:
            await send_message(phone_number, "Your cart is empty!\n\n1️⃣ View Pizza Menu\n2️⃣ View Burger Menu")

    # Checkout
    elif user_input == "4" or user_input == "2":
        if session["cart"]:
            total = session.get("total", sum(item['price'] for item in session["cart"]))
            session["stage"] = "checkout"
            await send_message(phone_number,
                f"📦 *ORDER SUMMARY*\n\nTotal: Rs{total}\n\n1️⃣ Cash on Delivery\n2️⃣ Card Payment\n3️⃣ Cancel Order")
        else:
            await send_message(phone_number, "Your cart is empty!")

    # Clear cart
    elif user_input == "3" and stage == "checkout":
        session["cart"] = []
        await send_message(phone_number, "Cart cleared!\n\n1️⃣ View Pizza Menu\n2️⃣ View Burger Menu")

    # COD
    elif user_input == "1" and session.get("stage") == "checkout":
        order_id = len(saved_orders) + 1000
        saved_orders[order_id] = {
            "phone": phone_number,
            "items": session["cart"],
            "total": session.get("total", 0),
            "payment": "cod",
            "status": "pending"
        }
        session["cart"] = []
        session["stage"] = "complete"

        # Notify manager
        manager_msg = f"📦 NEW ORDER #{order_id}\n\nCustomer: {phone_number}\nTotal: Rs{session.get('total', 0)}\n\nItems:\n"
        for item in saved_orders[order_id]["items"]:
            manager_msg += f"• {item['name']} - Rs{item['price']}\n"

        await send_message(MANAGER_NUMBER, manager_msg)
        await send_message(phone_number,
            f"✅ Order confirmed!\n\nOrder ID: #{order_id}\nTotal: Rs{session.get('total', 0)}\n\nThank you! 🙏")

    # Card payment
    elif user_input == "2" and session.get("stage") == "checkout":
        await send_message(phone_number, "💳 Card payment coming soon!\n\nFor now, please use Cash on Delivery.")

    # Cancel
    elif user_input == "3" and session.get("stage") == "checkout":
        session["cart"] = []
        session["stage"] = "greeting"
        await send_message(phone_number, "Order cancelled.\n\n1️⃣ View Pizza Menu\n2️⃣ View Burger Menu\n3️⃣ Exit")

    else:
        await send_message(phone_number, "I didn't understand. Please try again or reply with a number.")


# ==================== SEND MESSAGE ====================
async def send_message(phone_number: str, message: str):
    """Send text message via WhatsApp Business API"""
    try:
        url = f"https://graph.facebook.com/v25.0/{WHATSAPP_PHONE_ID}/messages"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message
            }
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


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "lead-bot-pipeline",
        "whatsapp_configured": bool(WHATSAPP_TOKEN and WHATSAPP_PHONE_ID),
        "ai_configured": bool(os.getenv("OPENROUTER_API_KEY"))
    }


# ==================== RUN ====================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"\n🚀 Lead Bot Pipeline starting on port {port}...")
    print(f"   WhatsApp: {WHATSAPP_PHONE_ID}")
    print(f"   AI Router: Ready\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
