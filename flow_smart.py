# SMART FLOW - Gemini AI suggestions + proper message handling + complete cart
import asyncio
from menus_multi import get_country_from_phone, get_menu, format_price
from country_selector import COUNTRIES
from whatsapp_interactive import send_interactive_buttons, send_interactive_list, send_text_message
from gemini_ai import get_ai_response
from db import customer_sessions

CATEGORY_EMOJIS = {
    "deals": "🔥", "biryani": "🍚", "karahi": "🍛", "bbq": "🍖",
    "fish": "🐟", "sides": "🍟", "drinks": "🥤", "desserts": "🍰",
    "mains": "🍚", "grills": "🍖", "shawarma": "🌯", "starters": "🥗",
    "burgers": "🍔", "chicken": "🍗", "pizza": "🍕", "wraps": "🌯",
    "bread": "🍞", "chinese": "🥢", "poutine": "🍟"
}

def get_item_emoji(item_name):
    """Get emoji for item"""
    name_lower = item_name.lower()
    emoji_map = {
        "biryani": "🍚", "karahi": "🍛", "kebab": "🍖", "chicken": "🍗",
        "burger": "🍔", "pizza": "🍕", "fish": "🐟", "shake": "🥤",
        "lassi": "🥛", "naan": "🍞", "salad": "🥗", "fries": "🍟",
        "cake": "🍰", "dessert": "🍰"
    }
    for keyword, emoji in emoji_map.items():
        if keyword in name_lower:
            return emoji
    return "🍲"

async def show_welcome(sender, country_code):
    """Show welcome WITHOUT extra message"""
    country_info = COUNTRIES[country_code]
    menu = get_menu(country_code)
    categories = list(menu["categories"].items())

    # Build category list
    rows = [
        {
            "id": f"cat_{key}",
            "title": data["name"],
            "description": f"{len(data['items'])} items"
        }
        for key, data in categories
    ]

    sections = [{"title": "🍽️ SELECT CATEGORY", "rows": rows}]

    await send_interactive_list(
        sender,
        header_text="👋 Wild Bites Restaurant",
        body_text=f"📍 {country_info['name']} | {country_info['currency']}\n\nType 'owner' to change location",
        sections=sections
    )

async def get_gemini_suggestions(sender, user_input, country_code, menu):
    """Get AI suggestions for user input"""
    try:
        menu_summary = "\n".join([f"• {cat['name']}: {', '.join([item for item in cat['items'].keys()])}"
                                  for cat in menu["categories"].values()])

        ai_response = await get_ai_response(
            sender,
            user_input,
            restaurant="Wild Bites",
            lang="en",
            menu=menu_summary
        )

        if not ai_response.get("success"):
            return None

        return ai_response.get("message")
    except Exception as e:
        print(f"⚠️ Gemini error: {e}")
        return None

async def show_category_items(sender, country_code, category_key):
    """Show items in category"""
    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]

    rows = []
    for item_id, item in items.items():
        emoji = get_item_emoji(item["name"])
        rows.append({
            "id": item_id,
            "title": f"{emoji} {item['name']}",
            "description": f"{format_price(country_code, item['price'])} • {item['desc'][:35]}"
        })

    sections = [{"title": category["name"].upper(), "rows": rows}]

    await send_interactive_list(
        sender,
        header_text=f"📍 {category['name']}",
        body_text="Tap to add to cart",
        sections=sections
    )

async def show_cart_with_total(sender, country_code, cart, menu):
    """Show complete cart with total"""
    if not cart:
        await send_text_message(sender, "🛒 Your cart is empty!")
        return

    currency = menu["symbol"]
    cart_text = "🛒 YOUR CART\n\n"
    total = 0

    for item_id, qty in cart.items():
        found = False
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                subtotal = item["price"] * qty
                total += subtotal
                emoji = get_item_emoji(item["name"])
                cart_text += f"{emoji} {item['name']}\n   ×{qty} = {format_price(country_code, subtotal)}\n\n"
                found = True
                break
        if not found:
            cart_text += f"❓ {item_id} ×{qty}\n\n"

    cart_text += f"{'='*40}\n"
    cart_text += f"💰 TOTAL: {format_price(country_code, total)}\n"
    cart_text += f"{'='*40}"

    await send_text_message(sender, cart_text)

    # Action buttons
    buttons = [
        {"id": "cart_add_more", "title": "➕ Add More"},
        {"id": "cart_checkout", "title": "✅ Checkout"},
        {"id": "cart_clear", "title": "🗑️ Clear"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="🛒 WHAT'S NEXT?",
        body_text="Choose an action",
        buttons=buttons
    )

async def handle_smart_flow(sender, text_or_id, is_interactive=False):
    """Complete smart flow with Gemini"""

    if sender not in customer_sessions:
        customer_sessions[sender] = {
            "country_code": None,
            "cart": {},
            "current_category": None
        }

    session = customer_sessions[sender]

    # Handle "owner" command
    if text_or_id.lower() == "owner" and not is_interactive:
        msg = """🌍 SELECT COUNTRY:

1️⃣ 🇵🇰 Pakistan    2️⃣ 🇦🇪 UAE          3️⃣ 🇸🇦 Saudi Arabia
4️⃣ 🇶🇦 Qatar       5️⃣ 🇰🇼 Kuwait       6️⃣ 🇧🇭 Bahrain
7️⃣ 🇴🇲 Oman        8️⃣ 🇺🇸 USA          9️⃣ 🇬🇧 UK
🔟 🇨🇦 Canada

Reply with number (1-10)"""
        await send_text_message(sender, msg)
        return

    # Handle country shortcode
    if not is_interactive and text_or_id.strip() in ["1","2","3","4","5","6","7","8","9","10"]:
        codes = {"1": "PK", "2": "AE", "3": "SA", "4": "QA", "5": "KW", "6": "BH", "7": "OM", "8": "US", "9": "GB", "10": "CA"}
        country = codes.get(text_or_id.strip())
        if country:
            session["country_code"] = country
            customer_sessions[sender] = session
            country_info = COUNTRIES.get(country)
            await send_text_message(sender, f"✅ Selected: {country_info['name']}")
            await show_welcome(sender, country)
            return

    # Auto-detect country if not set
    if not session.get("country_code"):
        detected = get_country_from_phone(sender)
        session["country_code"] = detected
        customer_sessions[sender] = session
        await show_welcome(sender, detected)
        return

    country_code = session["country_code"]
    menu = get_menu(country_code)

    # Handle interactive selections
    if is_interactive:
        # Category selection
        if text_or_id.startswith("cat_"):
            category_key = text_or_id.replace("cat_", "")
            session["current_category"] = category_key
            customer_sessions[sender] = session
            await show_category_items(sender, country_code, category_key)
            return

        # Item selection from list
        found = False
        for cat_key, cat_data in menu["categories"].items():
            if text_or_id in cat_data.get("items", {}):
                item = cat_data["items"][text_or_id]
                session["cart"][text_or_id] = session["cart"].get(text_or_id, 0) + 1
                customer_sessions[sender] = session

                # Show added + upsell + cart (all in one go, no duplicate messages)
                emoji = get_item_emoji(item["name"])
                msg = f"✅ Added 1x {emoji} {item['name']} to cart!"
                msg += f"\n\n💡 Popular additions:\n• Naan\n• Lassi\n• Dessert"
                await send_text_message(sender, msg)

                await show_cart_with_total(sender, country_code, session["cart"], menu)
                found = True
                break

        if found:
            return

        # Cart actions
        if text_or_id == "cart_add_more":
            await show_welcome(sender, country_code)
            return

        if text_or_id == "cart_checkout":
            buttons = [
                {"id": "delivery_home", "title": "🏠 Home Delivery"},
                {"id": "delivery_pickup", "title": "🏪 Pickup"}
            ]
            await send_interactive_buttons(sender, "📦 DELIVERY", "Choose delivery type", buttons)
            return

        if text_or_id == "cart_clear":
            session["cart"] = {}
            customer_sessions[sender] = session
            await send_text_message(sender, "🗑️ Cart cleared!")
            await show_welcome(sender, country_code)
            return

        # Delivery
        if text_or_id == "delivery_home":
            session["delivery_type"] = "home"
            customer_sessions[sender] = session
            buttons = [
                {"id": "payment_card", "title": "💳 Card"},
                {"id": "payment_cod", "title": "💵 Cash"}
            ]
            await send_interactive_buttons(sender, "💰 PAYMENT", "Choose payment method", buttons)
            return

        if text_or_id == "delivery_pickup":
            session["delivery_type"] = "pickup"
            customer_sessions[sender] = session
            buttons = [
                {"id": "payment_card", "title": "💳 Card"},
                {"id": "payment_cod", "title": "💵 Cash"}
            ]
            await send_interactive_buttons(sender, "💰 PAYMENT", "Choose payment method", buttons)
            return

        # Payment
        if text_or_id in ["payment_card", "payment_cod"]:
            delivery = session.get("delivery_type", "home")
            payment = "Card" if text_or_id == "payment_card" else "Cash on Delivery"

            # Calculate total
            total = 0
            for item_id, qty in session["cart"].items():
                for cat in menu["categories"].values():
                    if item_id in cat["items"]:
                        total += cat["items"][item_id]["price"] * qty
                        break

            msg = f"""
✅ ORDER CONFIRMED!

🏪 Wild Bites Restaurant
📍 {COUNTRIES[country_code]['name']}

💰 Total: {format_price(country_code, total)}
🚗 Delivery: {'Home' if delivery == 'home' else 'Pickup'}
💳 Payment: {payment}

Thank you for your order! 🙏
"""
            await send_text_message(sender, msg)
            session["cart"] = {}
            customer_sessions[sender] = session
            return

    # Handle text input with Gemini suggestions
    if not is_interactive and text_or_id.strip():
        # Get AI suggestion
        ai_msg = await get_gemini_suggestions(sender, text_or_id, country_code, menu)

        if ai_msg:
            await send_text_message(sender, f"🤖 {ai_msg}")

            # Try to suggest based on keywords
            text_lower = text_or_id.lower()
            suggestions = []

            for cat_key, cat_data in menu["categories"].items():
                cat_name_lower = cat_data["name"].lower()
                if any(word in cat_name_lower for word in text_lower.split()):
                    suggestions.append((cat_key, cat_data["name"]))

            if suggestions:
                rows = [
                    {"id": f"cat_{key}", "title": name, "description": "Browse items"}
                    for key, name in suggestions
                ]
                sections = [{"title": "📍 SUGGESTIONS", "rows": rows}]

                await send_interactive_list(
                    sender,
                    header_text="💡 BASED ON YOUR REQUEST",
                    body_text="Tap to browse",
                    sections=sections
                )
            else:
                await show_welcome(sender, country_code)
        else:
            await send_text_message(sender, "Sorry, didn't understand. Here's the menu:")
            await show_welcome(sender, country_code)
