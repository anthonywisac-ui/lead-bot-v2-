# Gemini AI Integration with WhatsApp Catalog
# When customers browse catalog and send messages, Gemini analyzes & suggests items

import asyncio
import json
from gemini_ai import get_ai_response
from menus_multi import get_menu, format_price
from flow_smart import get_item_emoji

async def analyze_catalog_query(sender, message, country_code, session):
    """
    When customer sends message while browsing catalog,
    Gemini analyzes and suggests relevant items

    Examples:
    - "kaunsi cheez sust hai?" → Suggests cheapest items
    - "vegetarian options?" → Suggests veggie items
    - "2 logo ke liye?" → Suggests deals/combos
    - "spicy kya hai?" → Suggests spicy items
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    menu = get_menu(country_code)
    all_items = {}

    # Flatten all items
    for category in menu["categories"].values():
        all_items.update(category["items"])

    # Create catalog summary for Gemini
    catalog_context = _build_catalog_summary(all_items, country_code)

    # Ask Gemini to analyze the customer's request
    prompt = f"""
    Customer is browsing our restaurant menu catalog on WhatsApp.
    They asked: "{message}"

    Here's our menu:
    {catalog_context}

    Based on their question, suggest the BEST 3-5 items from the menu.
    Return as JSON with this format:
    {{
        "understanding": "brief understanding of what they want",
        "suggestions": [
            {{"item_id": "DL1", "name": "...", "reason": "why this is good for them"}},
            ...
        ]
    }}

    Be helpful, personalized, and suggest items that match their needs.
    """

    try:
        response = await get_ai_response(prompt)
        suggestions = json.loads(response)

        # Build recommendation message
        msg = f"✨ **Gemini's Suggestions for You**:\n\n"
        msg += f"💭 *Understanding:* {suggestions['understanding']}\n\n"

        await send_text_message(sender, msg)

        # Send suggested items with add buttons
        for i, item_data in enumerate(suggestions['suggestions'], 1):
            item_id = item_data['item_id']
            item_name = item_data['name']
            reason = item_data['reason']

            # Find the actual item to get price
            item = all_items.get(item_id)
            if item:
                emoji = get_item_emoji(item['name'])
                price = format_price(country_code, item['price'])

                msg = f"{i}. {emoji} **{item_name}**\n"
                msg += f"   💵 {price}\n"
                msg += f"   💡 *{reason}*"

                await send_text_message(sender, msg)
                await asyncio.sleep(0.3)

        # Add action buttons
        buttons = [
            {"id": "catalog_browse", "title": "📦 Browse More"},
            {"id": "view_cart", "title": "🛒 View Cart"},
            {"id": "checkout", "title": "✅ Checkout"}
        ]

        await send_interactive_buttons(
            sender,
            header_text="What Next?",
            body_text="Found what you need?",
            buttons=buttons
        )

    except Exception as e:
        print(f"Gemini catalog analysis error: {e}")
        await send_text_message(sender, "Sorry, couldn't analyze that. Browse our full catalog with the 📦 button!")


def _build_catalog_summary(items, country_code):
    """Build a compact catalog summary for Gemini"""
    summary = ""

    for item_id, item in list(items.items())[:15]:  # Top 15 items
        price = format_price(country_code, item["price"])
        summary += f"- {item['name']}: {price} ({item.get('desc', 'Delicious')})\n"

    return summary


async def handle_catalog_message(sender, message, country_code, session):
    """
    Main handler for messages while browsing catalog.
    Decides whether to use Gemini or regular flow.
    """

    # If message seems like a catalog-related question, use Gemini
    catalog_keywords = [
        "kaunsi", "konsa", "which", "cheapest", "sust", "expensive", "mehnge",
        "vegetarian", "veg", "spicy", "mild", "sweet", "kids", "family",
        "best", "popular", "recommend", "suggest", "2 log", "1 log",
        "healthy", "light", "heavy", "filling", "quick"
    ]

    message_lower = message.lower()

    # Check if this looks like a catalog query
    is_catalog_query = any(keyword in message_lower for keyword in catalog_keywords)

    if is_catalog_query and len(message) > 5:
        # Use Gemini to analyze
        await analyze_catalog_query(sender, message, country_code, session)
        return True

    return False


async def suggest_based_on_cart(sender, cart_items, country_code, session):
    """
    When customer adds items to cart, Gemini suggests complementary items.

    Example:
    - Added biryani → Suggest raita, lassi, pickle
    - Added burger → Suggest fries, drink, sauce
    """
    from whatsapp_interactive import send_text_message
    from menus_multi import get_menu

    if not cart_items:
        return

    menu = get_menu(country_code)

    # Get what they ordered
    items_summary = ""
    for item_id, qty in list(cart_items.items())[:3]:
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                items_summary += f"- {qty}x {item['name']}\n"
                break

    prompt = f"""
    Customer ordered these items:
    {items_summary}

    Suggest 2-3 complementary side dishes, drinks, or desserts that go well.
    Keep suggestions brief and appetizing.
    Return as a simple bullet list.
    """

    try:
        response = await get_ai_response(prompt)

        msg = "✨ **Perfect with your order:**\n\n"
        msg += response + "\n\n"
        msg += "Want to add any? Tap 📦 Browse"

        await send_text_message(sender, msg)
    except:
        pass  # Silent fail, don't interrupt checkout
