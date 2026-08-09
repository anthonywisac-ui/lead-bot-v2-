# Example: How to integrate Gemini catalog suggestions into your webhook

# In your main.py or webhook handler, update the message processing like this:

from fastapi import FastAPI, Request
from whatsapp_interactive import send_text_message
from catalog_gemini_integration import handle_catalog_message, suggest_based_on_cart
from menus_multi import get_country_from_phone
from db import customer_sessions

app = FastAPI()

# Your existing webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # Extract message details
    sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    message_text = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

    # Get or create session
    if sender not in customer_sessions:
        customer_sessions[sender] = {
            "stage": "greeting",
            "cart": {},
            "country_code": get_country_from_phone(sender)
        }

    session = customer_sessions[sender]
    country_code = session["country_code"]

    # ============================================
    # GEMINI CATALOG INTEGRATION STARTS HERE
    # ============================================

    # If customer is in catalog browsing stage, try Gemini first
    if session.get("stage") == "browsing":
        print(f"🤖 Trying Gemini for catalog question: {message_text}")

        # Gemini analyzes the message and suggests items
        handled = await handle_catalog_message(
            sender,
            message_text,
            country_code,
            session
        )

        if handled:
            print(f"✅ Gemini handled the catalog question")
            return {"status": "ok"}

    # ============================================
    # GEMINI CATALOG INTEGRATION ENDS HERE
    # ============================================

    # If Gemini didn't handle it, continue with regular flow
    await handle_regular_flow(sender, message_text, country_code, session)

    return {"status": "ok"}


# After customer adds items to cart, suggest complementary items
async def handle_add_to_cart(sender, item_id, qty, country_code, session):
    """When customer adds item, suggest complements"""

    # Add item to cart
    if "cart" not in session:
        session["cart"] = {}
    session["cart"][item_id] = qty

    # Send confirmation
    await send_text_message(sender, f"✅ Added {qty}x item to cart!")

    # ============================================
    # GEMINI UPSELL INTEGRATION
    # ============================================

    # Get smart suggestions for what they bought
    await suggest_based_on_cart(
        sender,
        session["cart"],
        country_code,
        session
    )

    # ============================================
    # Integration complete!
    # ============================================


# Handle regular flow (non-catalog messages)
async def handle_regular_flow(sender, message, country_code, session):
    """Your existing message handling"""

    # Your existing flow logic here
    print(f"Processing regular message: {message}")

    # Call your existing handlers
    # await show_menu(sender, ...)
    # etc.


# ============================================
# ALTERNATIVE: Simple inline integration
# ============================================

# If you want even simpler integration, just add this to handle text messages:

async def process_text_message(sender, message_text, country_code, session):
    """Simple inline Gemini integration"""

    # Check if this looks like a catalog question
    catalog_keywords = ["kaunsi", "which", "veg", "cheap", "best", "sweet", "spicy"]
    is_catalog_question = any(word in message_text.lower() for word in catalog_keywords)

    # If it's a catalog question AND user is browsing, use Gemini
    if is_catalog_question and session.get("stage") == "browsing":
        print("🤖 Analyzing catalog question with Gemini...")
        handled = await handle_catalog_message(sender, message_text, country_code, session)

        if handled:
            return  # Gemini handled it, no need to continue

    # Otherwise, handle normally
    await handle_regular_flow(sender, message_text, country_code, session)
