# SMART FLOW v2 - Complete order system with manager approval, timing, returning customers
import asyncio
import time
from datetime import datetime
from menus_multi import get_country_from_phone, get_menu, format_price
from country_selector import COUNTRIES
from whatsapp_interactive import send_interactive_buttons, send_interactive_list, send_text_message
from gemini_ai import get_ai_response
from db import customer_sessions
from order_manager import create_order, MANAGER_NUMBER

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

MANAGER_NUMBER = "923351021321"  # Update with actual manager number

ITEMS_NEED_QUANTITY = ["naan", "roti", "roll", "burger", "karahi", "curry", "pizza", "kebab"]

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

def needs_quantity_selection(item_name):
    """Check if item needs qty selection"""
    name_lower = item_name.lower()
    return any(keyword in name_lower for keyword in ITEMS_NEED_QUANTITY)

def get_item_emoji(item_name):
    """Get emoji for item"""
    name_lower = item_name.lower()
    emoji_map = {
        "biryani": "🍚", "karahi": "🍛", "kebab": "🍖", "chicken": "🍗",
        "burger": "🍔", "pizza": "🍕", "fish": "🐟", "shake": "🥤",
        "lassi": "🥛", "naan": "🍞", "salad": "🥗", "fries": "🍟",
        "cake": "🍰", "dessert": "🍰", "roll": "🌯", "roti": "🍞"
    }
    for keyword, emoji in emoji_map.items():
        if keyword in name_lower:
            return emoji
    return "🍲"

def get_smart_suggestions(item_name):
    """Get relevant suggestions based on item"""
    name_lower = item_name.lower()

    if "biryani" in name_lower or "rice" in name_lower:
        return [
            {"id": "upsell_raita", "title": "🥛 Raita"},
            {"id": "upsell_lassi", "title": "🥛 Lassi"},
            {"id": "upsell_pickle", "title": "🌶️ Pickle"}
        ]

    if "karahi" in name_lower or "curry" in name_lower or "handi" in name_lower or "nihari" in name_lower:
        return [
            {"id": "upsell_naan", "title": "🍞 Naan"},
            {"id": "upsell_raita", "title": "🥛 Raita"},
            {"id": "upsell_bread", "title": "🍞 Roti"}
        ]

    if "burger" in name_lower or "sandwich" in name_lower:
        return [
            {"id": "upsell_fries", "title": "🍟 Fries"},
            {"id": "upsell_drink", "title": "🥤 Drink"},
            {"id": "upsell_sauce", "title": "🌶️ Sauce"}
        ]

    if "pizza" in name_lower:
        return [
            {"id": "upsell_wings", "title": "🍗 Wings"},
            {"id": "upsell_drink", "title": "🥤 Drink"},
            {"id": "upsell_dessert", "title": "🍰 Dessert"}
        ]

    if "roll" in name_lower or "wrap" in name_lower or "shawarma" in name_lower:
        return [
            {"id": "upsell_fries", "title": "🍟 Fries"},
            {"id": "upsell_drink", "title": "🥤 Drink"},
            {"id": "upsell_sauce", "title": "🌶️ Sauce"}
        ]

    return None

async def show_welcome(sender, country_code):
    """Show welcome menu"""
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
        body_text="Tap to select",
        sections=sections
    )

async def show_quantity_and_proceed(sender, item_id, item_name):
    """Show Quantity and Proceed buttons"""
    buttons = [
        {"id": f"qty_btn_{item_id}", "title": "📊 Quantity"},
        {"id": "proceed_order", "title": "✅ Proceed"}
    ]
    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="Adjust quantity or proceed to cart",
        buttons=buttons
    )

async def show_quantity_list(sender, item_id):
    """Show quantity list: 2x, 3x, 4x, 5x, 6x"""
    buttons = [
        {"id": f"qty_set_2_{item_id}", "title": "2x"},
        {"id": f"qty_set_3_{item_id}", "title": "3x"},
        {"id": f"qty_set_4_{item_id}", "title": "4x"},
        {"id": f"qty_set_5_{item_id}", "title": "5x"},
        {"id": f"qty_set_6_{item_id}", "title": "6x"}
    ]
    await send_interactive_buttons(
        sender,
        header_text="📊 SELECT QUANTITY",
        body_text="How many would you like?",
        buttons=buttons
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
    cart_text += f"💰 SUBTOTAL: {format_price(country_code, total)}\n"
    cart_text += f"{'='*40}"

    await send_text_message(sender, cart_text)

    buttons = [
        {"id": "cart_add_more", "title": "➕ Add More"},
        {"id": "cart_checkout", "title": "✅ Checkout"},
        {"id": "cart_clear", "title": "🗑️ Clear"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="🛒 CART ACTIONS",
        body_text="What's next?",
        buttons=buttons
    )

async def send_to_manager(sender, country_code, cart, menu, address, delivery_type, payment_method):
    """Send order to manager for approval"""
    # Create order in order_manager
    order_id, total = create_order(sender, country_code, cart, menu, address, delivery_type, payment_method)

    # Build order bill
    subtotal = sum(
        menu["categories"][cat_key]["items"].get(item_id, {}).get("price", 0) * qty
        for item_id, qty in cart.items()
        for cat_key in menu["categories"].keys()
        if item_id in menu["categories"][cat_key].get("items", {})
    )

    delivery_charge = get_delivery_charge(country_code, subtotal) if delivery_type == "home" else 0

    bill_text = f"""🆕 NEW ORDER - {order_id}

📱 Customer: {sender}
📍 Country: {COUNTRIES[country_code]['name']}

📊 ITEMS:
"""
    for item_id, qty in cart.items():
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                bill_text += f"• {qty}x {item['name']} = {format_price(country_code, item['price'] * qty)}\n"
                break

    bill_text += f"""
💰 BREAKDOWN:
Subtotal: {format_price(country_code, subtotal)}
🚚 Delivery: {format_price(country_code, delivery_charge) if delivery_charge > 0 else 'FREE'}
───────────────────
💵 TOTAL: {format_price(country_code, total)}

📍 Address: {address if delivery_type == 'home' else 'Pickup from Restaurant'}
🚗 Type: {'Home Delivery' if delivery_type == 'home' else 'Pickup'}
💳 Payment: {payment_method}

⏱️ Prep Time: 5 min
🚚 Delivery: {'2 min' if delivery_type == 'home' else '0 min'}
📋 TOTAL TIME: {'7 min' if delivery_type == 'home' else '5 min'}
"""

    await send_text_message(MANAGER_NUMBER, bill_text)

    # Manager buttons
    buttons = [
        {"id": f"approve_{sender}", "title": "✅ Approve"},
        {"id": f"reject_{sender}", "title": "❌ Reject"}
    ]
    await send_interactive_buttons(
        MANAGER_NUMBER,
        header_text="MANAGER ACTION NEEDED",
        body_text=f"Customer: {sender}",
        buttons=buttons
    )

    return total

async def handle_smart_flow(sender, text_or_id, is_interactive=False):
    """Main flow handler"""

    if sender not in customer_sessions:
        customer_sessions[sender] = {
            "country_code": None,
            "cart": {},
            "current_category": None,
            "stage": "greeting",
            "last_order": None,
            "order_timestamp": None,
        }

    session = customer_sessions[sender]
    country_code = session.get("country_code")
    menu = get_menu(country_code) if country_code else None

    # ========== STAGE 1: PHONE NUMBER COLLECTION ==========
    if session.get("stage") == "greeting" and not is_interactive and not session.get("phone_collected"):
        session["phone_collected"] = True
        session["customer_phone"] = sender
        customer_sessions[sender] = session
        await send_text_message(sender, f"✅ Number registered: {sender}\n\n📍 Detecting location...")

        # Auto-detect country
        detected = get_country_from_phone(sender)
        session["country_code"] = detected
        session["stage"] = "browsing"
        customer_sessions[sender] = session
        await show_welcome(sender, detected)
        return

    # ========== STAGE 2: ADDRESS INPUT (PRIORITY) ==========
    if session.get("stage") == "address_input" and not is_interactive:
        address = text_or_id.strip()
        if len(address) < 10:
            await send_text_message(sender, "❌ Address too short. Please be more specific.\n\n(e.g., House/Flat 123, Street Name, Area, Nearest Place)")
            return

        session["address"] = address
        session["stage"] = "payment_selection"
        customer_sessions[sender] = session

        # Send to manager
        total = await send_to_manager(
            sender,
            country_code,
            session["cart"],
            menu,
            address,
            session.get("delivery_type", "home"),
            "Pending"
        )

        await send_text_message(sender, f"📤 Order sent to manager...\n⏱️ Expected time: 7 minutes\n\n💰 Total: {format_price(country_code, total)}")
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

        # Item selection from list
        found = False
        for cat_key, cat_data in menu["categories"].items():
            if text_or_id in cat_data.get("items", {}):
                item = cat_data["items"][text_or_id]

                # Add 1x to cart
                session["cart"][text_or_id] = session["cart"].get(text_or_id, 0) + 1
                customer_sessions[sender] = session

                emoji = get_item_emoji(item["name"])
                msg = f"✅ Added 1x {emoji} {item['name']} to cart!"
                await send_text_message(sender, msg)

                # Show smart suggestions
                suggestions = get_smart_suggestions(item["name"])
                if suggestions:
                    await send_interactive_buttons(
                        sender,
                        header_text="💡 ADD-ONS",
                        body_text="Pair with popular additions",
                        buttons=suggestions
                    )

                # If needs quantity, show Quantity+Proceed buttons
                if needs_quantity_selection(item["name"]):
                    await show_quantity_and_proceed(sender, text_or_id, item["name"])
                else:
                    # Show cart directly
                    await show_cart_with_total(sender, country_code, session["cart"], menu)

                found = True
                break

        if found:
            return

        # ===== QUANTITY BUTTONS =====
        if text_or_id.startswith("qty_btn_"):
            item_id = text_or_id.replace("qty_btn_", "")
            await show_quantity_list(sender, item_id)
            return

        # ===== QUANTITY SET (2x, 3x, 4x, 5x, 6x) =====
        if text_or_id.startswith("qty_set_"):
            parts = text_or_id.split("_")
            if len(parts) >= 3:
                new_qty = int(parts[2])
                item_id = "_".join(parts[3:]) if len(parts) > 3 else parts[2]

                # Update cart to new quantity
                session["cart"][item_id] = new_qty
                customer_sessions[sender] = session

                # Find and show item
                for cat_key, cat_data in menu["categories"].items():
                    if item_id in cat_data.get("items", {}):
                        item = cat_data["items"][item_id]
                        emoji = get_item_emoji(item["name"])
                        await send_text_message(sender, f"✅ Updated to {new_qty}x {emoji} {item['name']}")
                        await show_cart_with_total(sender, country_code, session["cart"], menu)
                        return

        # ===== PROCEED BUTTON =====
        if text_or_id == "proceed_order":
            await show_cart_with_total(sender, country_code, session["cart"], menu)
            return

        # ===== UPSELL BUTTONS =====
        if text_or_id.startswith("upsell_"):
            # Find the item to add based on upsell ID
            upsell_map = {
                "upsell_raita": ("DR2", "Raita"),
                "upsell_lassi": ("DR1", "Lassi"),
                "upsell_pickle": ("SD", "Pickle"),
                "upsell_naan": ("BD1", "Naan"),
                "upsell_bread": ("BD6", "Roti"),
                "upsell_fries": ("SD5", "Fries"),
                "upsell_drink": ("DR1", "Drink"),
                "upsell_sauce": ("SD", "Sauce"),
                "upsell_wings": ("SD4", "Wings"),
                "upsell_dessert": ("DS", "Dessert"),
            }

            if text_or_id in upsell_map:
                item_id, item_name = upsell_map[text_or_id]
                session["cart"][item_id] = session["cart"].get(item_id, 0) + 1
                customer_sessions[sender] = session
                emoji = get_item_emoji(item_name)
                await send_text_message(sender, f"✅ Added 1x {emoji} {item_name}")
                await show_cart_with_total(sender, country_code, session["cart"], menu)
            return

        # ===== CART ACTIONS =====
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

        # ===== DELIVERY SELECTION =====
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

            # Calculate total
            total = sum(
                menu["categories"][cat_key]["items"].get(item_id, {}).get("price", 0) * qty
                for item_id, qty in session["cart"].items()
                for cat_key in menu["categories"].keys()
                if item_id in menu["categories"][cat_key].get("items", {})
            )

            is_valid, min_amount = validate_minimum_order(country_code, total, "pickup")
            if not is_valid:
                msg = f"❌ Minimum pickup order: {format_price(country_code, min_amount)}\nYour cart: {format_price(country_code, total)}\n\nPlease add more items."
                await send_text_message(sender, msg)
                return

            # Send to manager
            await send_to_manager(sender, country_code, session["cart"], menu, "Pickup", "pickup", "Pending")

            await send_text_message(sender, f"📤 Order sent to manager...\n⏱️ Expected time: 5 minutes (pickup, no delivery)")
            return
