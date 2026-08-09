# ========================================
# Gemini AI Integration for Order Processing
# ========================================
# Handles all AI-powered responses: summaries, confirmations, upsells, manager alerts

import os
import json
import asyncio
from typing import Dict, List, Optional
from google import genai
from menus_multi import get_menu, format_price
from country_selector import COUNTRIES

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"  # Fast model for quick responses (gemini-2.5-flash deprecated)

# ========================================
# GEMINI CONFIGURATION
# ========================================

SYSTEM_PROMPTS = {
    "order_summary": """You are a friendly Pakistani restaurant chatbot assistant.
Your job is to create SHORT, warm, engaging order summaries for customers.
- Keep it under 150 words
- Use relevant food emojis (🍚 biryani, 🍛 karahi, 🍖 bbq, etc.)
- Be enthusiastic but concise
- Mention estimated time warmly
- Use customer's location naturally in one sentence
- Suggest adding something only if it makes sense (NO pushy sales)
Format: Greeting + items recap + add-on suggestion (optional) + delivery info + thank you
Do NOT include prices in the response (already shown separately)
Do NOT use markdown - plain text with emojis only""",

    "manager_alert": """You are a restaurant manager's AI assistant.
Create a brief, actionable priority alert for kitchen staff.
- Identify order complexity (simple/medium/complex based on items)
- Flag any special requests or timing constraints
- Suggest prep strategy if needed (e.g., "Start biryani first")
- Keep it under 100 words
- Use urgency indicators: 🔴 URGENT, 🟡 BUSY, 🟢 NORMAL
- Include prep time estimate
Format: Priority + complexity + key items + action item
Be direct and operational, not flowery""",

    "upsell": """You are a friendly restaurant suggestions AI.
Given an order, suggest ONE complementary item that would genuinely enhance it.
- Only suggest if it makes sense (don't suggest drinks if they ordered tea)
- Be natural and helpful, not pushy
- Keep suggestion to ONE sentence max
- Use format: "Would [item name] complete your meal nicely?"
- If no good upsell exists for this order, respond with empty string ""
Return ONLY the suggestion or empty string, nothing else""",

    "customer_response": """You are a helpful restaurant customer service AI.
Respond to customer messages naturally and helpfully.
- Answer questions about menu items, delivery, timing
- Be warm and professional
- Keep responses under 100 words
- Use relevant emojis
- If they ask about menu, reference available items
- Never make up information about items not in menu
- Always be helpful and friendly"""
}

# ========================================
# ORDER SUMMARY GENERATION
# ========================================

async def generate_order_summary(
    sender: str,
    country_code: str,
    cart: Dict[str, int],
    delivery_type: str,
    address_or_table: str,
    menu: Dict
) -> str:
    """
    Generate AI-powered order summary for customer.

    Uses Gemini to create warm, personalized confirmation message.
    Falls back to basic summary if Gemini fails.
    """
    try:
        # Build context for Gemini
        items_list = []
        for item_id, qty in cart.items():
            # Find item in menu
            for category in menu["categories"].values():
                if item_id in category["items"]:
                    item = category["items"][item_id]
                    items_list.append(f"{qty}x {item['name']}")
                    break

        delivery_info = {
            "home": f"delivery to {address_or_table}",
            "pickup": "pickup from restaurant in 20 minutes",
            "dinein": f"dine-in at table {address_or_table}"
        }

        context = f"""
Order Details:
Items: {', '.join(items_list)}
Delivery: {delivery_info.get(delivery_type, 'TBD')}
Customer Location: {COUNTRIES[country_code]['name']}
Estimated prep time: 20-25 minutes
"""

        # Call Gemini
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=f"{SYSTEM_PROMPTS['order_summary']}\n\n{context}"
        )

        summary = response.text.strip()
        return summary if summary else _get_fallback_summary(items_list, delivery_type)

    except Exception as e:
        print(f"⚠️ Gemini order summary failed: {e}")
        items_list = []
        for item_id, qty in cart.items():
            for category in menu["categories"].values():
                if item_id in category["items"]:
                    item = category["items"][item_id]
                    items_list.append(f"{qty}x {item['name']}")
                    break
        return _get_fallback_summary(items_list, delivery_type)


def _get_fallback_summary(items: List[str], delivery_type: str) -> str:
    """Fallback summary if Gemini fails"""
    items_text = ", ".join(items)
    delivery_text = {
        "home": "delivery",
        "pickup": "pickup",
        "dinein": "dine-in"
    }.get(delivery_type, "order")

    return f"""✅ Order Confirmed!

Your {delivery_text} order:
{chr(10).join(f"• {item}" for item in items)}

Thank you! Your food will be ready soon. 🙏"""


# ========================================
# MANAGER ALERT GENERATION
# ========================================

async def generate_manager_alert(
    order_id: str,
    customer: str,
    country_code: str,
    cart: Dict[str, int],
    delivery_type: str,
    address_or_table: str,
    menu: Dict,
    total: float
) -> str:
    """
    Generate AI-powered manager alert for kitchen/delivery coordination.

    Analyzes order complexity and suggests optimal prep strategy.
    """
    try:
        # Build order context
        items_list = []
        for item_id, qty in cart.items():
            for category in menu["categories"].values():
                if item_id in category["items"]:
                    item = category["items"][item_id]
                    items_list.append(f"{qty}x {item['name']}")
                    break

        context = f"""
Order ID: {order_id}
Customer: {customer}
Items: {', '.join(items_list)}
Total: {format_price(country_code, total)}
Delivery Type: {delivery_type}
Location: {address_or_table if delivery_type == 'home' else address_or_table}
Item Count: {sum(cart.values())}
Country: {COUNTRIES[country_code]['name']}
"""

        # Call Gemini
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            f"{SYSTEM_PROMPTS['manager_alert']}\n\n{context}"
        )

        alert = response.text.strip()
        return alert if alert else _get_fallback_manager_alert(items_list, total)

    except Exception as e:
        print(f"⚠️ Gemini manager alert failed: {e}")
        return _get_fallback_manager_alert(items_list, total)


def _get_fallback_manager_alert(items: List[str], total: float) -> str:
    """Fallback alert if Gemini fails"""
    return f"""🟡 NEW ORDER

Items: {', '.join(items)}
Total: {total} PKR

Status: Awaiting prep approval"""


# ========================================
# UPSELL SUGGESTION
# ========================================

async def generate_upsell_suggestion(
    cart: Dict[str, int],
    menu: Dict,
    country_code: str
) -> Optional[str]:
    """
    Generate ONE smart upsell suggestion based on order.

    Returns None if no good upsell exists.
    """
    try:
        # Build order context
        items_text = []
        for item_id in cart.keys():
            for category in menu["categories"].values():
                if item_id in category["items"]:
                    item = category["items"][item_id]
                    items_text.append(f"{item['name']} ({item_id})")
                    break

        # Available add-ons (drinks, bread, sides, desserts)
        addons = []
        for category_key in ["bread", "sides", "drinks", "desserts"]:
            if category_key in menu["categories"]:
                for item_id, item in menu["categories"][category_key]["items"].items():
                    if item_id not in cart:  # Don't suggest if already ordered
                        addons.append(f"{item['name']} ({item_id})")

        context = f"""
Current order items: {', '.join(items_text)}
Available add-ons: {', '.join(addons[:8])}

Suggest ONE complementary item from the add-ons list that would enhance this order.
"""

        # Call Gemini
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            f"{SYSTEM_PROMPTS['upsell']}\n\n{context}"
        )

        suggestion = response.text.strip()

        # Return None if Gemini says no good upsell
        if not suggestion or suggestion.lower() in ["", "none", "no", "no suggestion"]:
            return None

        return suggestion

    except Exception as e:
        print(f"⚠️ Gemini upsell failed: {e}")
        return None


# ========================================
# CUSTOMER QUERY RESPONSE
# ========================================

async def generate_customer_response(
    user_message: str,
    country_code: str,
    menu: Dict,
    context: Optional[str] = None
) -> str:
    """
    Generate contextual response to customer message.

    Handles menu questions, delivery inquiries, etc.
    """
    try:
        # Build menu reference for Gemini
        menu_items = []
        for category_name, category_data in menu["categories"].items():
            items = [f"{name} ({id})" for id, name_data in category_data["items"].items()
                    for name in [name_data.get("name", "")]]
            menu_items.append(f"{category_data['name']}: {', '.join(items)}")

        context_prompt = f"""
You are helping a customer in {COUNTRIES[country_code]['name']}.
Available menu: {chr(10).join(menu_items[:5])}  {('...' if len(menu_items) > 5 else '')}

Customer message: {user_message}
{f'Context: {context}' if context else ''}
"""

        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            f"{SYSTEM_PROMPTS['customer_response']}\n\n{context_prompt}"
        )

        return response.text.strip()

    except Exception as e:
        print(f"⚠️ Gemini customer response failed: {e}")
        return "Thanks for reaching out! How can we help you? 😊"


# ========================================
# ORDER CONFIRMATION WITH ALL DETAILS
# ========================================

async def generate_full_order_confirmation(
    sender: str,
    order_id: str,
    country_code: str,
    cart: Dict[str, int],
    delivery_type: str,
    address_or_table: str,
    total: float,
    menu: Dict
) -> str:
    """
    Generate complete AI-powered order confirmation.

    Includes summary, timing, and warm closing.
    """
    try:
        items_list = []
        for item_id, qty in cart.items():
            for category in menu["categories"].values():
                if item_id in category["items"]:
                    item = category["items"][item_id]
                    items_list.append(f"{qty}x {item['name']}")
                    break

        context = f"""
Order Confirmation Details:
Order ID: {order_id}
Items: {', '.join(items_list)}
Total: {format_price(country_code, total)}
Delivery: {delivery_type}
{f'Address: {address_or_table}' if delivery_type == 'home' else f'Location: {address_or_table}'}
Ready in: 20-25 minutes
"""

        prompt = f"""Create a warm, professional order confirmation message.
Include:
1. Greeting and order ID
2. What they ordered (just list items, no prices)
3. Delivery details and timing
4. Thank you message
Keep it under 100 words. Use emojis appropriately.

{context}"""

        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        return response.text.strip()

    except Exception as e:
        print(f"⚠️ Gemini confirmation failed: {e}")
        return f"""✅ ORDER CONFIRMED!
Order ID: {order_id}
Total: {format_price(country_code, total)}
Ready in: 20-25 minutes
Thank you! 🙏"""


# ========================================
# BATCH GENERATION (for efficiency)
# ========================================

async def generate_order_package(
    order_id: str,
    sender: str,
    country_code: str,
    cart: Dict[str, int],
    delivery_type: str,
    address_or_table: str,
    total: float,
    menu: Dict
) -> Dict[str, str]:
    """
    Generate all order messages in parallel for efficiency.

    Returns dict with:
    - customer_summary: For customer confirmation
    - manager_alert: For kitchen/manager
    - upsell: Optional upsell suggestion
    """
    try:
        # Run all Gemini calls in parallel
        tasks = [
            generate_order_summary(sender, country_code, cart, delivery_type, address_or_table, menu),
            generate_manager_alert(order_id, sender, country_code, cart, delivery_type, address_or_table, menu, total),
            generate_upsell_suggestion(cart, menu, country_code)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            "customer_summary": results[0] if not isinstance(results[0], Exception) else _get_fallback_summary([], delivery_type),
            "manager_alert": results[1] if not isinstance(results[1], Exception) else _get_fallback_manager_alert([], total),
            "upsell": results[2] if not isinstance(results[2], Exception) else None
        }

    except Exception as e:
        print(f"❌ Order package generation failed: {e}")
        return {
            "customer_summary": "✅ Order confirmed! Thank you! 🙏",
            "manager_alert": "🟡 NEW ORDER - Processing",
            "upsell": None
        }
