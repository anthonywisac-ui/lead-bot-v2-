# COMPLETE FLOW - Auto-detect country, full menu, deals, upselling, checkout
import asyncio
import random
import time
from menus_multi import (
    get_country_from_phone, get_menu, get_category_list,
    get_category_items, format_price, get_currency_symbol
)
from country_selector import COUNTRIES
from whatsapp_interactive import (
    send_interactive_buttons, send_interactive_list,
    send_text_message
)
from db import customer_sessions, customer_profiles, save_profile, save_to_sheet

# Category emojis
CATEGORY_EMOJIS = {
    "deals": "🔥", "biryani": "🍚", "karahi": "🍛", "bbq": "🍖",
    "fish": "🐟", "sides": "🍟", "drinks": "🥤", "desserts": "🍰",
    "mains": "🍚", "grills": "🍖", "shawarma": "🌯", "starters": "🥗",
    "burgers": "🍔", "chicken": "🍗", "pizza": "🍕", "wraps": "🌯",
    "bread": "🍞", "chinese": "🥢", "poutine": "🍟"
}

ITEM_EMOJIS = {
    "biryani": "🍚", "karahi": "🍛", "kebab": "🍖", "chicken": "🍗",
    "burger": "🍔", "pizza": "🍕", "fish": "🐟", "shake": "🥤",
    "lassi": "🥛", "naan": "🍞", "salad": "🥗", "fries": "🍟",
    "cake": "🍰", "dessert": "🍰"
}

def get_item_emoji(item_name):
    """Get emoji for item based on name"""
    name_lower = item_name.lower()
    for keyword, emoji in ITEM_EMOJIS.items():
        if keyword in name_lower:
            return emoji
    return "🍲"  # Default emoji

async def show_country_shortcodes(sender):
    """Show country selection with shortcodes"""
    msg = """🌍 SELECT YOUR COUNTRY:

1️⃣ 🇵🇰 Pakistan (PKR)
2️⃣ 🇦🇪 UAE (AED)
3️⃣ 🇸🇦 Saudi Arabia (SAR)
4️⃣ 🇶🇦 Qatar (QAR)
5️⃣ 🇰🇼 Kuwait (KWD)
6️⃣ 🇧🇭 Bahrain (BHD)
7️⃣ 🇴🇲 Oman (OMR)
8️⃣ 🇺🇸 USA (USD)
9️⃣ 🇬🇧 UK (GBP)
🔟 🇨🇦 Canada (CAD)

📌 Reply with number (1-10) to select"""

    await send_text_message(sender, msg)

def get_country_from_shortcode(code):
    """Get country from shortcode"""
    codes = {
        "1": "PK", "2": "AE", "3": "SA", "4": "QA", "5": "KW",
        "6": "BH", "7": "OM", "8": "US", "9": "GB", "10": "CA"
    }
    return codes.get(code)

async def show_main_menu(sender, country_code):
    """Show category menu with LIST (not buttons)"""
    menu = get_menu(country_code)
    categories = list(menu["categories"].items())

    # Show welcome message
    country_info = COUNTRIES[country_code]
    msg = f"""👋 Welcome to Wild Bites!

📍 {country_info['name']}
💱 Currency: {country_info['currency']}

Type 'owner' to change location

🍽️ Choose from menu below:"""

    await send_text_message(sender, msg)

    # Build ONE complete list with ALL categories
    rows = []
    for key, data in categories:
        emoji = CATEGORY_EMOJIS.get(key, "🍲")
        rows.append({
            "id": f"cat_{key}",
            "title": data["name"],
            "description": f"Browse {len(data['items'])} items"
        })

    sections = [{
        "title": "🍽️ CATEGORIES",
        "rows": rows
    }]

    await send_interactive_list(
        sender,
        header_text="📍 MENU CATEGORIES",
        body_text="Tap a category to see items",
        sections=sections
    )

async def show_category_items(sender, country_code, category_key):
    """Show items in category as ONE complete list"""
    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]
    category_name = category["name"]

    # Build list with proper emojis
    rows = []
    for item_id, item in items.items():
        emoji = get_item_emoji(item["name"])
        rows.append({
            "id": item_id,
            "title": f"{emoji} {item['name']}",
            "description": f"{format_price(country_code, item['price'])} • {item['desc'][:35]}"
        })

    sections = [{
        "title": category_name.upper(),
        "rows": rows
    }]

    # Send category message with image info
    msg = f"📸 Loading {category_name}...\n\n⬇️ Scroll and tap any item to add to cart"
    await send_text_message(sender, msg)

    # Send the list
    await send_interactive_list(
        sender,
        header_text=f"📍 {category_name}",
        body_text="Tap to add to cart 🛒",
        sections=sections
    )

async def show_cart(sender, country_code, cart, menu):
    """Show cart with checkout"""
    if not cart:
        await send_text_message(sender, "🛒 Your cart is empty!")
        await show_main_menu(sender, country_code)
        return

    currency = menu["symbol"]
    cart_text = "🛒 YOUR CART\n\n"
    total = 0

    for item_id, qty in cart.items():
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                subtotal = item["price"] * qty
                total += subtotal
                emoji = get_item_emoji(item["name"])
                cart_text += f"{emoji} {item['name']}\n   ×{qty} = {format_price(country_code, subtotal)}\n\n"
                break

    cart_text += f"{'='*40}\n"
    cart_text += f"💰 Total: {format_price(country_code, total)}\n"

    await send_text_message(sender, cart_text)

    # Action buttons
    buttons = [
        {"id": "cart_add_more", "title": "➕ Add More"},
        {"id": "cart_checkout", "title": "✅ Checkout"},
        {"id": "cart_clear", "title": "🗑️ Clear"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="🛒 CART OPTIONS",
        body_text="What's next?",
        buttons=buttons
    )

async def show_delivery_options(sender):
    """Delivery type selection"""
    buttons = [
        {"id": "delivery_home", "title": "🏠 Home Delivery"},
        {"id": "delivery_pickup", "title": "🏪 Pickup"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="📦 DELIVERY",
        body_text="How would you like to receive your order?",
        buttons=buttons
    )

async def show_payment_options(sender):
    """Payment method selection"""
    buttons = [
        {"id": "payment_card", "title": "💳 Card Payment"},
        {"id": "payment_cod", "title": "💵 Cash on Delivery"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="💰 PAYMENT",
        body_text="Choose payment method",
        buttons=buttons
    )

async def handle_complete_flow(sender, text_or_id, is_interactive=False):
    """Main flow handler"""

    # Get or create session
    if sender not in customer_sessions:
        customer_sessions[sender] = {
            "stage": "greeting",
            "country_code": None,
            "cart": {},
            "order": {}
        }

    session = customer_sessions[sender]

    # Handle "owner" command - show country shortcodes
    if text_or_id.lower() == "owner" and not is_interactive:
        await show_country_shortcodes(sender)
        return

    # Handle shortcode selection (1-10)
    if not is_interactive and text_or_id.strip() in ["1","2","3","4","5","6","7","8","9","10"]:
        country = get_country_from_shortcode(text_or_id.strip())
        if country:
            session["country_code"] = country
            session["stage"] = "browsing"
            customer_sessions[sender] = session

            country_info = COUNTRIES.get(country)
            await send_text_message(sender, f"✅ Selected: {country_info['name']} ({country_info['currency']})")
            await show_main_menu(sender, country)
            return

    # Auto-detect country if not set (NO PROMPT, just show menu)
    if not session.get("country_code"):
        detected = get_country_from_phone(sender)
        session["country_code"] = detected
        session["stage"] = "browsing"
        customer_sessions[sender] = session

        # Just show menu directly - no extra message
        await show_main_menu(sender, detected)
        return

    country_code = session["country_code"]
    menu = get_menu(country_code)

    # Handle interactive button/list selections
    if is_interactive:
        # Category selection
        if text_or_id.startswith("cat_"):
            category_key = text_or_id.replace("cat_", "")
            session["current_category"] = category_key
            customer_sessions[sender] = session
            await show_category_items(sender, country_code, category_key)
            return

        # Item selection from list
        # Check all categories for the item
        found = False
        for cat_key, cat_data in menu["categories"].items():
            if text_or_id in cat_data.get("items", {}):
                item = cat_data["items"][text_or_id]
                session["cart"][text_or_id] = session["cart"].get(text_or_id, 0) + 1
                customer_sessions[sender] = session

                # Show item added
                emoji = get_item_emoji(item["name"])
                await send_text_message(sender, f"✅ Added 1x {emoji} {item['name']} to cart!")

                # Show upsell
                await send_text_message(sender, "💡 How about adding:\n• Naan\n• Lassi\n• Dessert")

                # Show cart
                await show_cart(sender, country_code, session["cart"], menu)
                found = True
                break

        if found:
            return

        # Cart actions
        if text_or_id == "cart_add_more":
            await show_main_menu(sender, country_code)
            return

        if text_or_id == "cart_checkout":
            await show_delivery_options(sender)
            return

        if text_or_id == "cart_clear":
            session["cart"] = {}
            customer_sessions[sender] = session
            await send_text_message(sender, "🗑️ Cart cleared!")
            await show_main_menu(sender, country_code)
            return

        # Delivery options
        if text_or_id == "delivery_home":
            session["delivery_type"] = "delivery"
            customer_sessions[sender] = session
            await send_text_message(sender, "🏠 Home delivery selected")
            await show_payment_options(sender)
            return

        if text_or_id == "delivery_pickup":
            session["delivery_type"] = "pickup"
            customer_sessions[sender] = session
            await send_text_message(sender, "🏪 Pickup selected")
            await show_payment_options(sender)
            return

        # Payment options
        if text_or_id == "payment_card":
            session["payment"] = "card"
            customer_sessions[sender] = session
            cart_total = sum(menu["categories"][list(menu["categories"].keys())[0]]["items"].get(item_id, {}).get("price", 0) * qty
                           for item_id, qty in session["cart"].items()
                           for cat in menu["categories"].values() if item_id in cat["items"])

            msg = f"""
✅ ORDER CONFIRMED!

🏪 Wild Bites Restaurant
📍 {COUNTRIES[country_code]['name']}

🚗 Delivery: Home Delivery
💳 Payment: Card Payment

Thank you for your order! 🙏
"""
            await send_text_message(sender, msg)
            return

        if text_or_id == "payment_cod":
            session["payment"] = "cod"
            customer_sessions[sender] = session

            msg = f"""
✅ ORDER CONFIRMED!

🏪 Wild Bites Restaurant
📍 {COUNTRIES[country_code]['name']}

🚗 Delivery: Pickup
💵 Payment: Cash on Delivery

Thank you for your order! 🙏
"""
            await send_text_message(sender, msg)
            return
