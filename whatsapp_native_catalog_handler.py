# WhatsApp Native Catalog Handler - PRIMARY ORDER FLOW
# Use WhatsApp's native catalog as main interface
# Button-based menu is BACKUP ONLY (when catalog fails)

async def show_view_catalog_button(sender, country_code):
    """
    Show greeting + "View Catalog" button as PRIMARY flow.

    This is THE main interface - customers tap to open native catalog.
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from country_selector import COUNTRIES

    country_info = COUNTRIES[country_code]

    msg = f"""
🎉 **Welcome to Wild Bites!**

📍 {country_info['name']} | {country_info['currency']}

Tap below to browse our full menu with beautiful photos and prices!
Select multiple items at once, then checkout.
    """

    await send_text_message(sender, msg)

    # PRIMARY: View Catalog button
    buttons = [
        {"id": "view_catalog", "title": "📦 View Catalog"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="WILD BITES MENU",
        body_text="Start here 👇",
        buttons=buttons
    )


async def handle_catalog_selection(sender, message, session):
    """
    Process catalog selection from native WhatsApp UI.

    WhatsApp passes selected product IDs when customer checks out from catalog.
    Example: "DL1,BR2,KR1" (multiple items) or "DL1" (single)
    """
    from menus_multi import get_menu, get_country_from_phone, format_price
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from flow_smart import get_item_emoji
    from customer_profile import save_customer_profile

    sender_country = get_country_from_phone(sender)
    menu = get_menu(sender_country)

    # Parse catalog selection from WhatsApp
    selected_ids = message.strip().split(",")

    # Initialize cart
    if "cart" not in session:
        session["cart"] = {}

    cart_items = []
    total = 0

    # Find items and add to cart
    for item_id in selected_ids:
        item_id = item_id.strip()

        # Find item in menu
        found = False
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                qty = 1  # Default quantity

                session["cart"][item_id] = qty
                emoji = get_item_emoji(item["name"])
                price = item["price"]
                total += price

                cart_items.append(f"{emoji} {item['name']} - {format_price(sender_country, price)}")
                found = True
                break

        if not found:
            print(f"⚠️ Item not found: {item_id}")

    if not cart_items:
        await send_text_message(sender, "❌ No valid items selected. Please try again!")
        return

    # Show cart summary
    msg = "✅ **CART SUMMARY**\n\n"
    for item in cart_items:
        msg += f"{item}\n"
    msg += f"\n💰 **Subtotal**: {format_price(sender_country, total)}\n"
    msg += "\n**How would you like to receive your order?**"

    await send_text_message(sender, msg)

    # Ask for delivery method
    buttons = [
        {"id": "delivery_home", "title": "🏠 Delivery"},
        {"id": "delivery_pickup", "title": "🚗 Pickup"},
        {"id": "delivery_dinein", "title": "🍽️ Dine-in"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="DELIVERY METHOD",
        body_text="Select one:",
        buttons=buttons
    )

    session["stage"] = "delivery_selection"
    session["country_code"] = sender_country


async def handle_delivery_selection(sender, delivery_type, session, country_code):
    """Handle delivery/pickup/dine-in selection"""
    from whatsapp_interactive import send_text_message

    session["delivery_type"] = delivery_type

    if delivery_type == "delivery_dine_in":
        # Ask for table number
        msg = "🍽️ **Dine-in Order**\n\nWhich table are you at? (e.g., Table 5)"
        await send_text_message(sender, msg)
        session["stage"] = "waiting_table_number"

    elif delivery_type == "delivery_pickup":
        # Pickup confirmation
        msg = "🚗 **Pickup Order**\n\nWe'll have it ready in 15-20 minutes!\n\nCome pick it up from Wild Bites! 🎉"
        await send_text_message(sender, msg)
        session["stage"] = "confirming_pickup"

    else:  # delivery_home
        # Ask for address
        msg = "🏠 **Home Delivery**\n\nPlease share your delivery address:\n\n📍 Format: House/Flat #, Street, Area, Landmark"
        await send_text_message(sender, msg)
        session["stage"] = "collecting_address"


# ========================================
# NEW: SMART GREETING WITH RETURNING CUSTOMER LOGIC
# ========================================

async def smart_greeting(sender, country_code, session):
    """
    Smart greeting that:
    1. Detects returning customers (within 10 min)
    2. Greets by name if known
    3. Shows last order shortcut
    4. Shows "View Catalog" button for new order
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from customer_profile import is_returning_customer, get_customer_name, format_last_order
    from country_selector import COUNTRIES

    country_info = COUNTRIES[country_code]

    # Check if returning customer
    is_returning, profile = is_returning_customer(sender, within_minutes=10)

    if is_returning and profile:
        # RETURNING CUSTOMER FLOW
        name = profile.get("name", "Friend")
        msg = f"""
👋 **Welcome back, {name}!**

📍 {country_info['name']} | {country_info['currency']}

Ready for your next order?
        """

        await send_text_message(sender, msg)

        # Show last order if available
        last_order = format_last_order(profile)
        if last_order:
            await send_text_message(sender, last_order)

        # Offer quick options
        buttons = [
            {"id": "repeat_last_order", "title": "🔄 Repeat Order"},
            {"id": "view_catalog", "title": "📦 New Order"}
        ]

        await send_interactive_buttons(
            sender,
            header_text="QUICK OPTIONS",
            body_text="What would you like?",
            buttons=buttons
        )

        session["stage"] = "greeting"

    else:
        # NEW CUSTOMER OR 10+ MINUTES HAVE PASSED
        msg = f"""
🎉 **Welcome to Wild Bites!**

📍 {country_info['name']} | {country_info['currency']}

Let's get you started! Tap below to browse our menu.
        """

        await send_text_message(sender, msg)

        # PRIMARY: View Catalog button
        buttons = [
            {"id": "view_catalog", "title": "📦 View Catalog"}
        ]

        await send_interactive_buttons(
            sender,
            header_text="WILD BITES MENU",
            body_text="Start here 👇",
            buttons=buttons
        )

    session["stage"] = "greeting"
