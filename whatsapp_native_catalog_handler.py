# WhatsApp Native Catalog Handler
# Skip the text/button catalog - use WhatsApp's native catalog UI instead!

async def show_whatsapp_native_catalog(sender):
    """
    Send link to WhatsApp's native catalog
    Customer will see beautiful catalog UI in WhatsApp
    They select items directly
    """
    from whatsapp_interactive import send_text_message

    msg = """
📦 **BROWSE OUR MENU**

Tap the link below to see our full catalog with all items, prices, and images!

You can select multiple items at once! 🛒
    """

    await send_text_message(sender, msg)

    # Send catalog link button (WhatsApp handles this)
    # The catalog is already linked to your WhatsApp number in Meta
    # Just send a simple message with catalog reference


async def handle_catalog_selection(sender, message, session):
    """
    When customer sends order from catalog.

    WhatsApp passes the selected product IDs.
    Example message: "DL1,BR2,KR1" (multiple items)
    Or single item: "DL1"
    """
    from menus_multi import get_menu, get_country_from_phone, format_price
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from flow_smart import get_item_emoji

    sender_country = get_country_from_phone(sender)
    menu = get_menu(sender_country)

    # Parse catalog selection
    # WhatsApp sends product IDs
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

    # Show what they ordered
    msg = "✅ **ORDER SUMMARY**\n\n"
    for item in cart_items:
        msg += f"{item}\n"
    msg += f"\n💰 **Subtotal**: {format_price(sender_country, total)}\n\n"
    msg += "How would you like to receive your order?"

    await send_text_message(sender, msg)

    # Ask for delivery method
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


async def handle_delivery_selection(sender, delivery_type, session, country_code):
    """Handle delivery/pickup/dine-in selection"""
    from whatsapp_interactive import send_text_message

    session["delivery_type"] = delivery_type

    if delivery_type == "dine_in":
        # Ask for table number
        msg = "🍽️ **Dine-in Order**\n\nWhich table are you at?"
        await send_text_message(sender, msg)
        session["stage"] = "waiting_table_number"

    elif delivery_type == "pickup":
        # Ask for address confirmation
        msg = "🚗 **Pickup Order**\n\nWe'll have it ready in 15-20 minutes!\n\nConfirm your phone number to proceed."
        await send_text_message(sender, msg)
        session["stage"] = "confirming_pickup"

    else:  # delivery_home
        # Ask for address
        msg = "🏠 **Home Delivery**\n\nPlease share your delivery address:\n\n📍 Format: House/Flat number, Street, Area, Nearest landmark"
        await send_text_message(sender, msg)
        session["stage"] = "collecting_address"


# ============================================
# SIMPLE FLOW: Remove custom catalog, use native
# ============================================

async def greeting_flow(sender, country_code, session):
    """
    Simple greeting that points to WhatsApp catalog
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    msg = """
🎉 **Welcome to Wild Bites!**

📦 **Browse Full Menu** - Tap the catalog icon above to see all our items with beautiful photos and prices!

Select multiple items at once, then tap the button below when you're ready!
    """

    await send_text_message(sender, msg)

    # Add button to continue to checkout
    buttons = [
        {"id": "ready_to_order", "title": "✅ Ready to Order"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="When you've selected your items:",
        buttons=buttons
    )
