# SMART FLOW - Gemini AI suggestions + proper message handling + complete cart + address + delivery
import asyncio
from menus_multi import get_country_from_phone, get_menu, format_price
from country_selector import COUNTRIES
from whatsapp_interactive import send_interactive_buttons, send_interactive_list, send_text_message
from gemini_ai import get_ai_response
from db import customer_sessions

# Delivery settings per country
DELIVERY_SETTINGS = {
    "PK": {"min_delivery": 500, "min_pickup": 200, "delivery_fee": 150, "free_above": 2000},
    "AE": {"min_delivery": 25, "min_pickup": 10, "delivery_fee": 8, "free_above": 75},
    "SA": {"min_delivery": 30, "min_pickup": 15, "delivery_fee": 10, "free_above": 80},
    "QA": {"min_delivery": 40, "min_pickup": 20, "delivery_fee": 12, "free_above": 100},
    "KW": {"min_delivery": 3.5, "min_pickup": 1.5, "delivery_fee": 1, "free_above": 10},
    "BH": {"min_delivery": 4, "min_pickup": 2, "delivery_fee": 1.2, "free_above": 12},
    "OM": {"min_delivery": 3, "min_pickup": 1.5, "delivery_fee": 0.9, "free_above": 9},
    "US": {"min_delivery": 15, "min_pickup": 5, "delivery_fee": 4.99, "free_above": 50},
    "GB": {"min_delivery": 12, "min_pickup": 5, "delivery_fee": 3.99, "free_above": 40},
    "CA": {"min_delivery": 18, "min_pickup": 7, "delivery_fee": 5.99, "free_above": 60},
}

def get_delivery_charge(country_code, total):
    """Calculate delivery charge based on country and total"""
    settings = DELIVERY_SETTINGS.get(country_code, DELIVERY_SETTINGS["PK"])
    if total >= settings["free_above"]:
        return 0
    return settings["delivery_fee"]

def validate_minimum_order(country_code, total, delivery_type):
    """Check if order meets minimum"""
    settings = DELIVERY_SETTINGS.get(country_code, DELIVERY_SETTINGS["PK"])
    min_amount = settings["min_delivery"] if delivery_type == "home" else settings["min_pickup"]
    return total >= min_amount, min_amount

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

def get_smart_suggestions(item_name):
    """Get relevant suggestions based on item"""
    name_lower = item_name.lower()

    # Biryani suggestions
    if "biryani" in name_lower or "rice" in name_lower:
        return [
            {"id": "upsell_raita", "title": "🥛 Raita"},
            {"id": "upsell_lassi", "title": "🥛 Lassi"},
            {"id": "upsell_pickle", "title": "🌶️ Pickle"}
        ]

    # Karahi suggestions
    if "karahi" in name_lower or "curry" in name_lower:
        return [
            {"id": "upsell_naan", "title": "🍞 Naan"},
            {"id": "upsell_raita", "title": "🥛 Raita"},
            {"id": "upsell_bread", "title": "🍞 Roti"}
        ]

    # Burger suggestions
    if "burger" in name_lower or "sandwich" in name_lower:
        return [
            {"id": "upsell_fries", "title": "🍟 Fries"},
            {"id": "upsell_drink", "title": "🥤 Cold Drink"},
            {"id": "upsell_sauce", "title": "🌶️ Sauce"}
        ]

    # Pizza suggestions
    if "pizza" in name_lower:
        return [
            {"id": "upsell_wings", "title": "🍗 Wings"},
            {"id": "upsell_drink", "title": "🥤 Drink"},
            {"id": "upsell_dessert", "title": "🍰 Dessert"}
        ]

    # Default suggestions (don't overuse)
    return None

async def show_welcome(sender, country_code):
    """Show welcome without extra message"""
    country_info = COUNTRIES[country_code]
    menu = get_menu(country_code)
    categories = list(menu["categories"].items())

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
            "current_category": None,
            "stage": "greeting"
        }

    session = customer_sessions[sender]
    country_code = session.get("country_code")
    menu = get_menu(country_code) if country_code else None

    # ========== STAGE 1: ADDRESS INPUT (PRIORITY) ==========
    if session.get("stage") == "address_input" and not is_interactive:
        address = text_or_id.strip()
        if len(address) < 10:
            await send_text_message(sender, "❌ Address too short. Please be more specific.\n\n(e.g., House/Flat 123, Street Name, Area, Nearest Place)")
            return

        session["address"] = address
        session["stage"] = "payment_selection"
        customer_sessions[sender] = session

        # Check minimum order
        total = sum(menu["categories"][list(menu["categories"].keys())[0]]["items"].get(item_id, {}).get("price", 0) * qty
                   for item_id, qty in session["cart"].items()
                   for cat in menu["categories"].values() if item_id in cat["items"])

        is_valid, min_amount = validate_minimum_order(country_code, total, "home")
        if not is_valid:
            msg = f"❌ Minimum delivery order: {format_price(country_code, min_amount)}\nYour cart: {format_price(country_code, total)}\n\nPlease add more items."
            await send_text_message(sender, msg)
            return

        buttons = [
            {"id": "payment_card", "title": "💳 Card"},
            {"id": "payment_cod", "title": "💵 Cash"}
        ]
        await send_interactive_buttons(sender, "💰 PAYMENT", "Choose payment method", buttons)
        return

    # ========== COMMANDS ==========
    if text_or_id.lower() == "owner" and not is_interactive:
        msg = """🌍 SELECT COUNTRY:

1️⃣ 🇵🇰 Pakistan    2️⃣ 🇦🇪 UAE          3️⃣ 🇸🇦 Saudi Arabia
4️⃣ 🇶🇦 Qatar       5️⃣ 🇰🇼 Kuwait       6️⃣ 🇧🇭 Bahrain
7️⃣ 🇴🇲 Oman        8️⃣ 🇺🇸 USA          9️⃣ 🇬🇧 UK
🔟 🇨🇦 Canada

Reply with number (1-10)"""
        await send_text_message(sender, msg)
        return

    # ========== COUNTRY SHORTCODE ==========
    if not is_interactive and text_or_id.strip() in ["1","2","3","4","5","6","7","8","9","10"]:
        codes = {"1": "PK", "2": "AE", "3": "SA", "4": "QA", "5": "KW", "6": "BH", "7": "OM", "8": "US", "9": "GB", "10": "CA"}
        country = codes.get(text_or_id.strip())
        if country:
            session["country_code"] = country
            session["stage"] = "browsing"
            customer_sessions[sender] = session
            country_info = COUNTRIES.get(country)
            await send_text_message(sender, f"✅ Selected: {country_info['name']}")
            await show_welcome(sender, country)
            return

    # ========== AUTO-DETECT COUNTRY ==========
    if not country_code:
        detected = get_country_from_phone(sender)
        session["country_code"] = detected
        session["stage"] = "browsing"
        customer_sessions[sender] = session
        menu = get_menu(detected)
        await show_welcome(sender, detected)
        return

    # ========== INTERACTIVE SELECTIONS ==========
    if is_interactive:
        # Category selection
        if text_or_id.startswith("cat_"):
            category_key = text_or_id.replace("cat_", "")
            session["current_category"] = category_key
            customer_sessions[sender] = session
            await show_category_items(sender, country_code, category_key)
            return

        # Item selection
        found = False
        for cat_key, cat_data in menu["categories"].items():
            if text_or_id in cat_data.get("items", {}):
                item = cat_data["items"][text_or_id]
                session["cart"][text_or_id] = session["cart"].get(text_or_id, 0) + 1
                customer_sessions[sender] = session

                emoji = get_item_emoji(item["name"])
                msg = f"✅ Added 1x {emoji} {item['name']} to cart!"
                await send_text_message(sender, msg)

                # Show smart suggestions if available
                suggestions = get_smart_suggestions(item["name"])
                if suggestions:
                    await send_interactive_buttons(
                        sender,
                        header_text="💡 ADD-ONS",
                        body_text="Pair with popular additions",
                        buttons=suggestions
                    )

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

        # Delivery selection
        if text_or_id == "delivery_home":
            session["delivery_type"] = "home"
            session["stage"] = "address_input"
            customer_sessions[sender] = session
            msg = """📍 Please provide your delivery address:

(e.g., House/Flat 123, Street Name, Area, Nearest Place)

Example:
House B-32, Block 4, Gulshan-e-Iqbal, near Mosque"""
            await send_text_message(sender, msg)
            return

        if text_or_id == "delivery_pickup":
            session["delivery_type"] = "pickup"
            customer_sessions[sender] = session

            total = sum(menu["categories"][list(menu["categories"].keys())[0]]["items"].get(item_id, {}).get("price", 0) * qty
                       for item_id, qty in session["cart"].items()
                       for cat in menu["categories"].values() if item_id in cat["items"])

            is_valid, min_amount = validate_minimum_order(country_code, total, "pickup")
            if not is_valid:
                msg = f"❌ Minimum pickup order: {format_price(country_code, min_amount)}\nYour cart: {format_price(country_code, total)}\n\nPlease add more items."
                await send_text_message(sender, msg)
                return

            buttons = [
                {"id": "payment_card", "title": "💳 Card"},
                {"id": "payment_cod", "title": "💵 Cash"}
            ]
            await send_interactive_buttons(sender, "💰 PAYMENT", "Choose payment method", buttons)
            return

        # Payment selection
        if text_or_id in ["payment_card", "payment_cod"]:
            delivery = session.get("delivery_type", "home")
            payment = "Card" if text_or_id == "payment_card" else "Cash on Delivery"

            subtotal = 0
            for item_id, qty in session["cart"].items():
                for cat in menu["categories"].values():
                    if item_id in cat["items"]:
                        subtotal += cat["items"][item_id]["price"] * qty
                        break

            delivery_charge = get_delivery_charge(country_code, subtotal) if delivery == "home" else 0
            final_total = subtotal + delivery_charge

            address_line = f"📍 {session.get('address', 'Pickup')}" if delivery == "home" else "🏪 Restaurant Pickup"

            msg = f"""
✅ ORDER CONFIRMED!

🏪 Wild Bites Restaurant
📍 {COUNTRIES[country_code]['name']}

📊 BREAKDOWN:
Subtotal: {format_price(country_code, subtotal)}
🚚 Delivery: {format_price(country_code, delivery_charge) if delivery_charge > 0 else 'FREE'}
{'─' * 35}
💰 TOTAL: {format_price(country_code, final_total)}

{address_line}
🚗 {'Home Delivery' if delivery == 'home' else 'Pickup'}
💳 {payment}

Thank you for your order! 🙏
"""
            await send_text_message(sender, msg)
            session["cart"] = {}
            session["stage"] = "completed"
            customer_sessions[sender] = session
            return

    # ========== TEXT INPUT WITH GEMINI SUGGESTIONS ==========
    if not is_interactive and text_or_id.strip():
        ai_msg = await get_ai_response(
            sender,
            text_or_id,
            restaurant="Wild Bites",
            lang="en",
            menu="\n".join([f"• {cat['name']}" for cat in menu["categories"].values()])
        )

        if ai_msg and ai_msg.get("success"):
            await send_text_message(sender, f"🤖 {ai_msg['message']}")

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
                sections = [{"title": "💡 SUGGESTIONS", "rows": rows}]

                await send_interactive_list(
                    sender,
                    header_text="📍 BASED ON YOUR REQUEST",
                    body_text="Tap to browse",
                    sections=sections
                )
            else:
                await show_welcome(sender, country_code)
        else:
            await send_text_message(sender, "Sorry, didn't understand. Here's the menu:")
            await show_welcome(sender, country_code)
