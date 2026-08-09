# Catalog Flow Handler
# Handle catalog selections aur continue the order flow

async def handle_catalog_order(sender, message_data, country_code, session):
    """
    When customer selects from catalog aur bhejta hai order.
    WhatsApp sends selected items in message.

    Continue flow: Ask delivery method → Address → Confirm
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from menus_multi import get_menu, format_price
    from flow_smart import get_item_emoji

    try:
        # Parse the message - might contain product IDs
        message = message_data.get("text", "").strip() if isinstance(message_data, dict) else str(message_data)

        menu = get_menu(country_code)

        # Initialize cart if needed
        if "cart" not in session:
            session["cart"] = {}

        # Try to extract item info from message
        # WhatsApp might send order info in the message

        # For now, if message is empty or just contains cart info,
        # assume they selected items and now proceed to delivery method

        if message.lower() in ["", "checkout", "confirm", "done"]:
            # They confirmed catalog selection, now ask delivery method
            await ask_delivery_method(sender, session, country_code)
            return

        print(f"📦 Catalog message from {sender}: {message}")

    except Exception as e:
        print(f"❌ Error handling catalog order: {e}")
        from whatsapp_interactive import send_text_message
        await send_text_message(sender, "Let me know when you're ready! 😊")


async def ask_delivery_method(sender, session, country_code):
    """
    After customer selects items from catalog,
    Ask them: Delivery / Pickup / Dine-in?
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    msg = """
✅ **Great Choice!**

How would you like to receive your order?
"""

    await send_text_message(sender, msg)

    buttons = [
        {"id": "delivery_home", "title": "🏠 Delivery"},
        {"id": "delivery_pickup", "title": "🚗 Pickup"},
        {"id": "delivery_dine_in", "title": "🍽️ Dine-in"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="DELIVERY METHOD",
        body_text="Choose how you want your order:",
        buttons=buttons
    )

    session["stage"] = "delivery_selection"


async def handle_delivery_method(sender, delivery_type, session, country_code):
    """
    Handle delivery/pickup/dine-in selection
    Continue flow: Ask for address or table number
    """
    from whatsapp_interactive import send_text_message

    session["delivery_type"] = delivery_type

    if delivery_type == "delivery_home":
        msg = """
🏠 **Home Delivery**

Please share your delivery address:

📍 Format: House/Flat number, Street Name, Area, Nearest Landmark

Example: House B-32, Block 4, Gulshan-e-Iqbal, near Mosque
"""
        await send_text_message(sender, msg)
        session["stage"] = "collecting_address"

    elif delivery_type == "delivery_pickup":
        msg = """
🚗 **Pickup Order**

We'll have your order ready in 15-20 minutes!

Please confirm your name and phone number:
"""
        await send_text_message(sender, msg)
        session["stage"] = "confirming_pickup"

    elif delivery_type == "delivery_dine_in":
        msg = """
🍽️ **Dine-in Order**

Which table are you at? (e.g., Table 5, Corner Table, etc.)
"""
        await send_text_message(sender, msg)
        session["stage"] = "waiting_table_number"


async def handle_address_input(sender, address, session, country_code):
    """
    Customer provided delivery address
    Validate and confirm order
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from menus_multi import get_menu, format_price
    from flow_smart import get_item_emoji

    session["address"] = address

    # Validate address format
    if len(address) < 10:
        await send_text_message(sender, "❌ Address too short. Please provide complete address with area and landmark.")
        return

    # Show order summary
    menu = get_menu(country_code)
    cart = session.get("cart", {})

    if not cart:
        await send_text_message(sender, "❌ No items in cart! Please select items from catalog.")
        return

    summary = "📦 **ORDER SUMMARY**\n\n"
    total = 0

    for item_id, qty in cart.items():
        # Find item
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                price = item["price"] * qty
                total += price
                emoji = get_item_emoji(item["name"])

                summary += f"{emoji} {qty}x {item['name']}\n"
                summary += f"   {format_price(country_code, price)}\n\n"
                break

    # Add delivery charge
    delivery_charge = 0
    if session.get("delivery_type") == "delivery_home":
        delivery_charge = 150 if country_code == "PK" else 5

    summary += f"📍 Address: {address}\n"
    summary += f"🚚 Delivery Charge: {format_price(country_code, delivery_charge)}\n"
    summary += f"{'='*40}\n"
    summary += f"💰 **TOTAL: {format_price(country_code, total + delivery_charge)}**\n"
    summary += f"{'='*40}"

    await send_text_message(sender, summary)

    # Confirm button
    buttons = [
        {"id": "confirm_order", "title": "✅ Confirm"},
        {"id": "cancel_order", "title": "❌ Cancel"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="CONFIRM ORDER",
        body_text="Ready to place your order?",
        buttons=buttons
    )

    session["stage"] = "confirming_order"


async def handle_table_number(sender, table_number, session, country_code):
    """
    Customer provided table number for dine-in
    Confirm order
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from menus_multi import get_menu, format_price
    from flow_smart import get_item_emoji

    session["table_number"] = table_number

    # Show order summary
    menu = get_menu(country_code)
    cart = session.get("cart", {})

    summary = "📦 **DINE-IN ORDER**\n\n"
    total = 0

    for item_id, qty in cart.items():
        # Find item
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                price = item["price"] * qty
                total += price
                emoji = get_item_emoji(item["name"])

                summary += f"{emoji} {qty}x {item['name']}\n"
                summary += f"   {format_price(country_code, price)}\n\n"
                break

    summary += f"🍽️ Table: {table_number}\n"
    summary += f"{'='*40}\n"
    summary += f"💰 **TOTAL: {format_price(country_code, total)}**\n"
    summary += f"{'='*40}"

    await send_text_message(sender, summary)

    # Confirm button
    buttons = [
        {"id": "confirm_order", "title": "✅ Confirm"},
        {"id": "cancel_order", "title": "❌ Cancel"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="CONFIRM ORDER",
        body_text="Ready to place your order?",
        buttons=buttons
    )

    session["stage"] = "confirming_order"


async def confirm_order(sender, session, country_code):
    """
    Final order confirmation
    Send to manager + show customer confirmation
    """
    from whatsapp_interactive import send_text_message
    from order_manager import create_order

    cart = session.get("cart", {})
    delivery_type = session.get("delivery_type", "delivery_home")
    address = session.get("address", "Not provided")
    table_number = session.get("table_number", "")

    if not cart:
        await send_text_message(sender, "❌ Cart is empty!")
        return

    # Create order
    try:
        order_id = create_order(
            sender,
            country_code,
            cart,
            delivery_type,
            address if delivery_type == "delivery_home" else table_number,
            delivery_type
        )

        msg = f"""
✅ **ORDER CONFIRMED!**

Order ID: #{order_id}

🍳 Preparing your order...

⏱️ Ready in: 20-25 minutes
📍 Location: Wild Bites Restaurant

Thank you for ordering! 🙏
"""

        await send_text_message(sender, msg)
        session["stage"] = "order_confirmed"

    except Exception as e:
        print(f"❌ Error creating order: {e}")
        await send_text_message(sender, "❌ Error creating order. Please try again!")
