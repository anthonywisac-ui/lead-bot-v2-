# ========================================
# Gemini-Powered Conversation Handler
# ========================================
# Uses Gemini to understand customer intent and generate contextual responses

import os
import asyncio
import google.generativeai as genai
from menus_multi import get_menu, get_country_from_phone
from whatsapp_interactive import send_text_message

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"

# ========================================
# INTENT CLASSIFICATION
# ========================================

async def classify_customer_intent(
    message: str,
    country_code: str
) -> dict:
    """
    Use Gemini to classify customer message intent.

    Returns: {
        "intent": "greeting" | "menu_question" | "order_status" | "complaint" | "order_related" | "other",
        "confidence": 0.0-1.0,
        "extracted_info": {...}
    }
    """
    try:
        prompt = f"""
Analyze this customer message and classify their intent.

Message: "{message}"
Country: {country_code}

Classify as ONE of:
- greeting: "Hi", "Hello", start new order
- menu_question: Asking about items, prices, menu
- order_status: "Where's my order?", "When ready?"
- complaint: "Wrong item", "Late", negative feedback
- order_related: Already in ordering flow
- other: Doesn't fit above

Respond ONLY with JSON:
{{
    "intent": "<one of above>",
    "confidence": 0.95,
    "extracted_info": {{
        "keyword": "<main keyword if any>"
    }}
}}
"""

        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        import json
        try:
            result = json.loads(response.text)
            return result
        except:
            # Fallback parsing
            return {
                "intent": "other",
                "confidence": 0.5,
                "extracted_info": {"keyword": message[:20]}
            }

    except Exception as e:
        print(f"⚠️ Intent classification failed: {e}")
        return {"intent": "other", "confidence": 0.3, "extracted_info": {}}


# ========================================
# SMART RESPONSE GENERATION
# ========================================

async def generate_contextual_response(
    sender: str,
    message: str,
    country_code: str,
    order_history: dict = None
) -> str:
    """
    Generate contextual response based on customer message.

    Handles:
    - Menu questions
    - Order status inquiries
    - Complaints/feedback
    - General conversation
    """
    try:
        menu = get_menu(country_code)

        # Build menu reference
        menu_summary = "Available Categories: "
        menu_summary += ", ".join([f"{cat['name']}" for cat in menu["categories"].values()])

        # Build order context if exists
        order_context = ""
        if order_history:
            order_context = f"""
Recent Order: {order_history.get('status', 'pending')}
Last Order Items: {', '.join(order_history.get('items', []))}
"""

        prompt = f"""
You are a friendly Pakistani restaurant customer service AI.

Customer Location: {country_code}
Customer Message: "{message}"

{menu_summary}

{order_context if order_context else "No recent order history"}

Generate a HELPFUL, FRIENDLY response:
- Answer questions accurately
- Be warm and professional
- Keep it under 2 sentences
- Use relevant emojis
- If they ask about ordering, guide them to menu

Response:
"""

        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        return response.text.strip()

    except Exception as e:
        print(f"⚠️ Contextual response failed: {e}")
        return "Thanks for reaching out! 😊 How can we help you today?"


# ========================================
# MENU SEARCH WITH GEMINI
# ========================================

async def search_menu_with_gemini(
    query: str,
    country_code: str
) -> list:
    """
    Use Gemini to intelligently search menu for customer query.

    E.g., "something spicy" → [KR1, KR2, CH3, ...]
    """
    try:
        menu = get_menu(country_code)

        # Build menu items list
        all_items = []
        for category_name, category_data in menu["categories"].items():
            for item_id, item_data in category_data["items"].items():
                all_items.append({
                    "id": item_id,
                    "name": item_data["name"],
                    "desc": item_data.get("desc", ""),
                    "price": item_data.get("price", 0)
                })

        items_text = "\n".join([f"{item['id']}: {item['name']} - {item['desc']}" for item in all_items])

        prompt = f"""
Customer is searching for menu items.
Query: "{query}"

Available menu items:
{items_text}

Return the TOP 3 item IDs that match the customer's request.
Format: ID1, ID2, ID3

Only return item IDs, nothing else.
"""

        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        # Parse response
        item_ids = [id.strip() for id in response.text.strip().split(",")]
        return item_ids[:3]  # Return top 3

    except Exception as e:
        print(f"⚠️ Menu search failed: {e}")
        return []


# ========================================
# HANDLE CUSTOMER INQUIRY
# ========================================

async def handle_customer_inquiry(sender: str, message: str) -> bool:
    """
    Handle customer question/inquiry using Gemini.

    Returns True if handled (customer got a response).
    Returns False if should route to regular flow.
    """
    try:
        country_code = get_country_from_phone(sender)

        # Classify intent
        intent_result = await classify_customer_intent(message, country_code)
        intent = intent_result.get("intent", "other")

        print(f"🤖 Intent: {intent} (confidence: {intent_result.get('confidence')})")

        # Route based on intent
        if intent == "greeting":
            # Let regular flow handle
            return False

        elif intent == "menu_question":
            # Search menu and provide recommendation
            item_ids = await search_menu_with_gemini(message, country_code)

            if item_ids:
                response = f"""Great question! 😊 Here are some items that match:

"""
                menu = get_menu(country_code)
                for item_id in item_ids:
                    for category in menu["categories"].values():
                        if item_id in category["items"]:
                            item = category["items"][item_id]
                            price = format_price(country_code, item["price"])
                            response += f"• {item['name']} - {price}\n"
                            break

                response += "\nSay \"Hi\" to start ordering! 📝"
            else:
                response = "We have a great variety! Say \"Hi\" to browse our full menu. 🍽️"

            await send_text_message(sender, response)
            return True

        elif intent == "order_status":
            # Would query order history (implement later)
            response = await generate_contextual_response(sender, message, country_code)
            await send_text_message(sender, response)
            return True

        elif intent == "complaint":
            # Acknowledge and offer help
            response = "😞 We're sorry to hear that! Please let us know the details and we'll make it right. Contact us anytime! 🙏"
            await send_text_message(sender, response)
            return True

        else:
            # General response
            response = await generate_contextual_response(sender, message, country_code)
            await send_text_message(sender, response)
            return True

    except Exception as e:
        print(f"❌ Customer inquiry handler failed: {e}")
        return False


# ========================================
# FORMAT PRICE HELPER
# ========================================

def format_price(country_code: str, amount: float) -> str:
    """Format price for display"""
    from menus_multi import format_price as mp_format_price
    return mp_format_price(country_code, amount)
