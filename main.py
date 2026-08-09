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

# Load menu from menu.json
def load_menu():
    try:
        with open("menu.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading menu.json: {e}")
        return {}

menu_data = load_menu()

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
                msg = "🍔 Welcome to Restaurant!\n\n👇 Select a category:\n\n"
                for idx, (cat_id, cat_info) in enumerate(menu_data.items(), 1):
                    msg += f"{idx}️⃣ {cat_info['name']}\n"
                msg += f"\nReply with number (1-{len(menu_data)})"
                await send_message(phone_number, msg)

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
    """Handle restaurant ordering flow with full menu"""

    user_input = user_input.strip().lower()
    categories = list(menu_data.keys())

    # Show category menu
    if user_input in ["menu", "start"]:
        msg = "🍽️ *SELECT CATEGORY*\n\n"
        for idx, (cat_id, cat_info) in enumerate(menu_data.items(), 1):
            msg += f"{idx}️⃣ {cat_info['name']}\n"
        msg += f"\nReply with number (1-{len(categories)})"
        await send_message(phone_number, msg)

    # Category selection (1-8)
    elif user_input.isdigit():
        cat_idx = int(user_input) - 1
        if 0 <= cat_idx < len(categories):
            category = categories[cat_idx]
            cat_info = menu_data[category]
            items = list(cat_info['items'].items())

            msg = f"{cat_info['name']}\n\n"
            for idx, (item_id, item_data) in enumerate(items, 1):
                msg += f"{idx}️⃣ {item_data['emoji']} {item_data['name']} - ${item_data['price']}\n"
            msg += f"\nReply with number to add to cart"

            await send_message(phone_number, msg)
            session["current_category"] = category
            session["current_items"] = items

        elif user_input == "0":  # View cart shortcut
            await show_cart(phone_number, session)
        else:
            await send_message(phone_number, f"Invalid choice. Please reply 1-{len(categories)}")

    # Add item to cart
    elif user_input.isdigit() and session.get("current_items"):
        item_idx = int(user_input) - 1
        current_items = session.get("current_items", [])

        if 0 <= item_idx < len(current_items):
            item_id, item_data = current_items[item_idx]
            item_to_add = {
                "id": item_id,
                "name": item_data['name'],
                "price": item_data['price'],
                "emoji": item_data['emoji']
            }
            session["cart"].append(item_to_add)
            await send_message(phone_number,
                f"✅ Added {item_data['emoji']} {item_data['name']} to cart!\n\n1️⃣ Add more items\n2️⃣ View cart\n3️⃣ Checkout")

    # View cart
    elif user_input == "2":
        await show_cart(phone_number, session)

    # Checkout
    elif user_input == "3":
        if session["cart"]:
            total = sum(item['price'] for item in session["cart"])
            session["total"] = total
            session["stage"] = "checkout"
            await send_message(phone_number,
                f"📦 *ORDER SUMMARY*\n\nTotal: ${total:.2f}\n\n1️⃣ Cash on Delivery\n2️⃣ Card Payment\n3️⃣ Cancel Order")
        else:
            await send_message(phone_number, "Your cart is empty! Add items first.")

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

        # Notify manager
        manager_msg = f"📦 NEW ORDER #{order_id}\n\n👤 Customer: {phone_number}\n💰 Total: ${session.get('total', 0):.2f}\n\n📋 Items:\n"
        for item in session["cart"]:
            manager_msg += f"• {item['emoji']} {item['name']} - ${item['price']:.2f}\n"

        await send_message(MANAGER_NUMBER, manager_msg)
        await send_message(phone_number,
            f"✅ Order confirmed!\n\n🎟️ Order ID: #{order_id}\n💰 Total: ${session.get('total', 0):.2f}\n\nThank you! 🙏")

        session["cart"] = []
        session["stage"] = "complete"

    # Card payment
    elif user_input == "2" and session.get("stage") == "checkout":
        await send_message(phone_number, "💳 Card payment coming soon!\n\nFor now, please use Cash on Delivery.")

    # Cancel
    elif user_input == "3" and session.get("stage") == "checkout":
        session["cart"] = []
        session["stage"] = "restaurant_greeting"
        await send_message(phone_number, "❌ Order cancelled.\n\n1️⃣ View menu\n2️⃣ Exit")

    else:
        await send_message(phone_number, "Please reply with a number from the menu.")


async def show_cart(phone_number: str, session: dict):
    """Show current cart"""
    if session["cart"]:
        msg = "🛒 *YOUR CART*\n\n"
        total = 0
        for idx, item in enumerate(session["cart"], 1):
            msg += f"{idx}. {item['emoji']} {item['name']} - ${item['price']:.2f}\n"
            total += item['price']
        session["total"] = total
        msg += f"\n*Total: ${total:.2f}*\n\n1️⃣ Add more items\n2️⃣ Clear cart\n3️⃣ Checkout"
        await send_message(phone_number, msg)
    else:
        await send_message(phone_number, "Your cart is empty! 📪\n\nType 'menu' to start ordering.")


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
