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

# Image URLs
IMAGE_URLS = {
    "welcome": "file:///D:/WILD-AUTOMATIONS/lead-bot/images/Welcome-image.png",
    "deals": "file:///D:/WILD-AUTOMATIONS/lead-bot/images/deals-image.png",
    "karhai": "file:///D:/WILD-AUTOMATIONS/lead-bot/images/karhai-image.png",
}

# Deal rules (from old flow)
DEAL_RULES = {
    "DL1": {"trigger": "burger", "msg": "Add fries + soda for just {price}!"},
    "DL2": {"trigger": "pizza", "msg": "Get wings free with this pizza!"},
    "DL3": {"trigger": "main", "msg": "Complete this meal with naan + drink!"},
}

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
    """Show category menu with buttons"""
    menu = get_menu(country_code)
    categories = list(menu["categories"].items())

    # Show welcome image
    msg = f"👋 Welcome to Wild Bites!\n🌍 {COUNTRIES[country_code]['name']}\n\n"
    msg += "🍽️ What would you like to order?"
    await send_text_message(sender, msg)

    # First 3 categories as buttons
    buttons = []
    for key, data in categories[:3]:
        cat_name = data["name"].split()[1] if len(data["name"].split()) > 1 else data["name"]
        buttons.append({
            "id": f"cat_{key}",
            "title": data["name"][:20]  # Limit title length
        })

    if buttons:
        await send_interactive_buttons(
            sender,
            header_text="🍽️ SELECT CATEGORY",
            body_text="Choose what you'd like to eat",
            buttons=buttons
        )

    # Show remaining categories as text
    if len(categories) > 3:
        remaining = "\n".join([f"{i+4}️⃣ {data['name']}" for i, (key, data) in enumerate(categories[3:])])
        await send_text_message(sender, f"More options:\n\n{remaining}")

async def show_category_items(sender, country_code, category_key, page=0):
    """Show items in category as list"""
    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]
    category_name = category["name"]

    # Send category image
    image_key = "deals" if "deal" in category_key.lower() else "karhai" if "karahi" in category_key.lower() else "welcome"
    if image_key in IMAGE_URLS:
        await send_text_message(sender, f"🖼️ Fetching {category_name}...")

    # Build list
    rows = []
    for item_id, item in items.items():
        rows.append({
            "id": item_id,
            "title": f"{item['emoji']} {item['name']}",
            "description": f"{format_price(country_code, item['price'])} • {item['desc'][:30]}..."
        })

    if rows:
        sections = [{
            "title": category_name.upper(),
            "rows": rows
        }]

        await send_interactive_list(
            sender,
            header_text=f"📍 {category_name}",
            body_text="Tap to add to cart 🛒",
            sections=sections
        )

async def show_item_detail(sender, item_id, country_code, menu):
    """Show item with quantity selector"""
    # Find item
    item_data = None
    for cat in menu["categories"].values():
        if item_id in cat["items"]:
            item_data = cat["items"][item_id]
            break

    if not item_data:
        return

    msg = f"""
{item_data['emoji']} {item_data['name']}

{item_data['desc']}

💰 {format_price(country_code, item_data['price'])}

✅ Added to cart!
"""
    await send_text_message(sender, msg)

    # Quantity buttons
    price = item_data['price']
    buttons = [
        {"id": f"add_{item_id}_1", "title": f"1x {format_price(country_code, price)}"},
        {"id": f"add_{item_id}_2", "title": f"2x {format_price(country_code, price*2)}"},
        {"id": f"add_{item_id}_3", "title": f"3x {format_price(country_code, price*3)}"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="📦 How Many?",
        body_text=f"{item_data['name']}",
        buttons=buttons
    )

async def show_cart(sender, country_code, cart):
    """Show cart with checkout"""
    if not cart:
        await send_text_message(sender, "🛒 Your cart is empty!")
        await show_main_menu(sender, country_code)
        return

    menu = get_menu(country_code)
    currency = menu["symbol"]

    cart_text = "🛒 YOUR CART\n\n"
    total = 0

    for item_id, qty in cart.items():
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                subtotal = item["price"] * qty
                total += subtotal
                cart_text += f"✅ {item['name']}\n   ×{qty} = {format_price(country_code, subtotal)}\n\n"
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

    # Auto-detect country if not set (ONLY on first greeting, no prompt)
    if not session.get("country_code"):
        detected = get_country_from_phone(sender)
        session["country_code"] = detected
        session["stage"] = "browsing"
        customer_sessions[sender] = session

        country_info = COUNTRIES.get(detected)
        msg = f"📍 Detected: {country_info['name']}\n\n"
        msg += "Type 'owner' to change country\n\n"
        msg += "🍽️ What would you like to order?"
        await send_text_message(sender, msg)
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
        if text_or_id in menu["categories"].get(session.get("current_category", ""), {}).get("items", {}):
            item_id = text_or_id
            qty = 1
            session["cart"][item_id] = session["cart"].get(item_id, 0) + qty
            customer_sessions[sender] = session

            # Show item detail
            item = menu["categories"][session["current_category"]]["items"][item_id]
            await send_text_message(sender, f"✅ Added {qty}x {item['name']} to cart!")

            # Upsell
            upsell_msg = f"💡 How about adding:\n"
            upsell_msg += f"• Naan (Rs 180)\n"
            upsell_msg += f"• Lassi (Rs 350)\n"
            upsell_msg += f"• Dessert (Rs 250)"
            await send_text_message(sender, upsell_msg)

            # Show cart
            await show_cart(sender, country_code, session["cart"])
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
            msg = f"""
✅ ORDER CONFIRMED!

🏪 Wild Bites Restaurant
📍 {COUNTRIES[country_code]['name']}

💰 Total: {format_price(country_code, sum(menu['categories'][session.get('current_category','')]['items'][item_id]['price'] * qty for item_id, qty in session['cart'].items()))}

🚗 Delivery: {session.get('delivery_type','home')}
💳 Payment: Card

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

💰 Total: {format_price(country_code, sum(menu['categories'][session.get('current_category','')]['items'][item_id]['price'] * qty for item_id, qty in session['cart'].items()))}

🚗 Delivery: {session.get('delivery_type','home')}
💵 Payment: Cash on Delivery

Thank you for your order! 🙏
"""
            await send_text_message(sender, msg)
            return
