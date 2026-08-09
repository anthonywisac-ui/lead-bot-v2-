# Complete flow with interactive buttons and lists (NO NUMBERS)
import asyncio
from menus_multi import (
    get_country_from_phone, get_menu, get_category_list,
    get_category_items, format_price, get_currency_symbol
)
from country_selector import COUNTRIES, get_country_list_message
from whatsapp_interactive import (
    send_interactive_buttons, send_interactive_list,
    send_text_message, send_image_with_caption
)
from db import customer_sessions, customer_profiles

# Image URLs (replace with actual hosted URLs)
IMAGES = {
    "welcome": "https://via.placeholder.com/1080x1080?text=Welcome+to+Wild+Bites",
    "deals": "https://via.placeholder.com/1080x1080?text=Smokin+Hot+Deals",
    "karhai": "https://via.placeholder.com/1080x1080?text=Sizzling+Karhai",
    "biryani": "https://via.placeholder.com/1080x1080?text=Aromatic+Biryani",
    "grills": "https://via.placeholder.com/1080x1080?text=BBQ+Grills",
}

async def send_country_selection(sender):
    """Send country selection buttons"""
    buttons = [
        {"id": "country_pk", "title": "🇵🇰 Pakistan"},
        {"id": "country_ae", "title": "🇦🇪 UAE"},
        {"id": "country_sa", "title": "🇸🇦 Saudi Arabia"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="🌍 SELECT YOUR COUNTRY",
        body_text="Choose your location to see prices in local currency",
        buttons=buttons,
        footer_text="Swipe to see more countries"
    )

    # Show additional countries as text
    more_countries = """
🇶🇦 Qatar
🇰🇼 Kuwait
🇧🇭 Bahrain
🇴🇲 Oman
🇺🇸 USA
🇬🇧 UK
🇨🇦 Canada
"""
    await send_text_message(sender, more_countries)

async def send_category_menu(sender, country_code):
    """Send category selection as buttons"""
    menu = get_menu(country_code)
    categories = list(menu["categories"].items())

    # Convert to buttons (max 3 per message)
    buttons_batch_1 = [
        {"id": f"cat_{key}", "title": name.split()[0] + " " + " ".join(name.split()[1:3])}
        for key, data in categories[:3]
        for name in [data["name"]]
    ]

    await send_interactive_buttons(
        sender,
        header_text="🍽️ WHAT DO YOU WANT?",
        body_text="Select a category to explore our menu",
        buttons=buttons_batch_1
    )

    # Show remaining categories
    if len(categories) > 3:
        remaining = "\n".join([f"{data['name']}" for key, data in categories[3:]])
        await send_text_message(sender, f"More options:\n\n{remaining}")

async def send_category_items(sender, country_code, category_key):
    """Send items in a category as interactive list"""
    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]
    category_name = category["name"]

    # Send category image if available
    if "karhai" in category_key.lower():
        await send_image_with_caption(sender, IMAGES["karhai"], f"{category_name}\n\nScroll down to select an item...")
    elif "biryani" in category_key.lower():
        await send_image_with_caption(sender, IMAGES["biryani"], f"{category_name}\n\nScroll down to select an item...")
    elif "grill" in category_key.lower():
        await send_image_with_caption(sender, IMAGES["grills"], f"{category_name}\n\nScroll down to select an item...")
    elif "deal" in category_key.lower():
        await send_image_with_caption(sender, IMAGES["deals"], f"{category_name}\n\nScroll down to select an item...")

    # Build sections for list
    sections = [
        {
            "title": category_name.upper(),
            "rows": [
                {
                    "id": item_id,
                    "title": item["name"],
                    "description": f"{format_price(country_code, item['price'])} • {item['desc']}"
                }
                for item_id, item in items.items()
            ]
        }
    ]

    await send_interactive_list(
        sender,
        header_text=f"📍 {category_name}",
        body_text="Tap an item to add to your cart",
        sections=sections,
        footer_text="Select any item"
    )

async def send_quantity_selector(sender, item_name, price, country_code):
    """Send quantity buttons"""
    currency = format_price(country_code, price)

    buttons = [
        {"id": f"qty_1", "title": "1x " + currency},
        {"id": f"qty_2", "title": "2x " + currency},
        {"id": f"qty_3", "title": "3x " + currency}
    ]

    await send_interactive_buttons(
        sender,
        header_text=f"🛒 {item_name}",
        body_text="How many would you like?",
        buttons=buttons,
        footer_text="Select quantity"
    )

async def send_cart_view(sender, cart_items, country_code):
    """Show cart with action buttons"""
    menu = get_menu(country_code)
    currency = menu["symbol"]

    cart_text = "🛒 YOUR CART\n\n"
    total = 0

    for item_id, qty in cart_items.items():
        # Find item in menu
        found = False
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                subtotal = item["price"] * qty
                total += subtotal
                cart_text += f"✅ {item['name']} x{qty}\n   {format_price(country_code, subtotal)}\n\n"
                found = True
                break

        if not found:
            cart_text += f"❓ {item_id} x{qty}\n\n"

    cart_text += f"\n💰 Total: {format_price(country_code, total)}"

    buttons = [
        {"id": "btn_add_more", "title": "Add More Items"},
        {"id": "btn_checkout", "title": "Proceed to Checkout"},
        {"id": "btn_clear", "title": "Clear Cart"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="🛒 Your Cart",
        body_text=cart_text,
        buttons=buttons
    )

async def send_delivery_options(sender):
    """Send delivery type selection"""
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

async def send_payment_options(sender):
    """Send payment method selection"""
    buttons = [
        {"id": "pay_card", "title": "💳 Card Payment"},
        {"id": "pay_cod", "title": "💵 Cash on Delivery"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="💰 PAYMENT",
        body_text="Choose your payment method",
        buttons=buttons
    )

async def handle_button_press(sender, button_id):
    """Handle button press from user"""
    session = customer_sessions.get(sender, {})

    # Country selection
    if button_id.startswith("country_"):
        country_code = button_id.replace("country_", "").upper()
        session["country_code"] = country_code
        customer_sessions[sender] = session

        country_info = COUNTRIES.get(country_code)
        await send_text_message(sender, f"✅ Selected: {country_info['name']}")
        await send_category_menu(sender, country_code)
        return

    # Category selection
    if button_id.startswith("cat_"):
        category_key = button_id.replace("cat_", "")
        country_code = session.get("country_code", "PK")
        session["current_category"] = category_key
        customer_sessions[sender] = session

        await send_category_items(sender, country_code, category_key)
        return

    # Quantity selection
    if button_id.startswith("qty_"):
        qty = int(button_id.replace("qty_", ""))
        await send_text_message(sender, f"✅ Added {qty}x to cart!")
        return

    # Cart actions
    if button_id == "btn_add_more":
        country_code = session.get("country_code", "PK")
        await send_category_menu(sender, country_code)
        return

    if button_id == "btn_checkout":
        await send_delivery_options(sender)
        return

    if button_id == "btn_clear":
        session["cart"] = {}
        customer_sessions[sender] = session
        await send_text_message(sender, "🗑️ Cart cleared!")
        return

    # Delivery options
    if button_id == "delivery_home":
        session["delivery"] = "home"
        customer_sessions[sender] = session
        await send_text_message(sender, "🏠 Home delivery selected")
        await send_payment_options(sender)
        return

    if button_id == "delivery_pickup":
        session["delivery"] = "pickup"
        customer_sessions[sender] = session
        await send_text_message(sender, "🏪 Pickup selected")
        await send_payment_options(sender)
        return

    # Payment options
    if button_id == "pay_card":
        session["payment"] = "card"
        customer_sessions[sender] = session
        await send_text_message(sender, "💳 Redirecting to payment...")
        return

    if button_id == "pay_cod":
        session["payment"] = "cod"
        customer_sessions[sender] = session
        await send_text_message(sender, "✅ Order confirmed! Cash on Delivery selected")
        return

async def handle_list_item_selection(sender, item_id):
    """Handle item selection from list"""
    session = customer_sessions.get(sender, {})
    country_code = session.get("country_code", "PK")
    menu = get_menu(country_code)

    # Find the item
    item_data = None
    for cat in menu["categories"].values():
        if item_id in cat["items"]:
            item_data = cat["items"][item_id]
            break

    if not item_data:
        await send_text_message(sender, "❌ Item not found")
        return

    # Initialize cart if needed
    if "cart" not in session:
        session["cart"] = {}

    # Send quantity selector
    await send_quantity_selector(sender, item_data["name"], item_data["price"], country_code)

    # For now, add 1x to cart by default (user can change)
    session["cart"][item_id] = session["cart"].get(item_id, 0) + 1
    customer_sessions[sender] = session
