# Complete Working Order Flow
# Hi → Categories → Items with qty → Delivery method → Address/Table → Order summary → Confirm

async def greeting_and_categories(sender, country_code):
    """Show welcome and categories for selection"""
    from whatsapp_interactive import send_text_message, send_interactive_list
    from menus_multi import get_menu
    from country_selector import COUNTRIES

    country_info = COUNTRIES[country_code]
    menu = get_menu(country_code)

    msg = f"""
🎉 **Welcome to Wild Bites!**

📍 {country_info['name']} | {country_info['currency']}

Select a category to browse items:
"""
    await send_text_message(sender, msg)

    # Show categories as list
    rows = [
        {
            "id": f"cat_{key}",
            "title": f"{data['name']} ({len(data['items'])} items)",
            "description": "Tap to browse"
        }
        for key, data in menu["categories"].items()
    ]

    sections = [{"title": "📦 MENU CATEGORIES", "rows": rows}]

    await send_interactive_list(
        sender,
        header_text="🍽️ SELECT CATEGORY",
        body_text="Browse items in this category",
        sections=sections
    )


async def show_category_items_with_buttons(sender, country_code, category_key, session):
    """Show items in category - tap to add to cart"""
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from menus_multi import get_menu, format_price
    import asyncio

    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]

    msg = f"📋 **{category['name']} Items**\n\nTap any item to add to cart:\n"
    await send_text_message(sender, msg)

    # Show each item with "Add" button
    for item_id, item in items.items():
        price = format_price(country_code, item["price"])

        buttons = [
            {"id": f"add_{item_id}_qty", "title": f"➕ Add • {price}"},
        ]

        await send_interactive_buttons(
            sender,
            header_text=f"{item['name']}",
            body_text=f"{price} • {item.get('desc', '')[:50]}",
            buttons=buttons
        )
        await asyncio.sleep(0.2)

    # Done browsing this category
    done_buttons = [
        {"id": f"done_category_{category_key}", "title": "✅ Done Browsing"},
    ]

    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="Done with this category?",
        buttons=done_buttons
    )


async def ask_quantity_for_item(sender, item_id, item_name, price_str):
    """Ask user how many of this item"""
    from whatsapp_interactive import send_interactive_buttons

    buttons = [
        {"id": f"qty_{item_id}_1", "title": "1x"},
        {"id": f"qty_{item_id}_2", "title": "2x"},
        {"id": f"qty_{item_id}_3", "title": "3x"},
        {"id": f"qty_{item_id}_5", "title": "5x"},
        {"id": f"qty_{item_id}_custom", "title": "✏️ Other"},
    ]

    await send_interactive_buttons(
        sender,
        header_text=f"HOW MANY {item_name.upper()}?",
        body_text=f"{price_str} each",
        buttons=buttons
    )


async def show_cart_summary(sender, country_code, session):
    """Show current cart with total"""
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from menus_multi import get_menu, format_price

    cart = session.get("cart", {})
    menu = get_menu(country_code)

    if not cart:
        await send_text_message(sender, "🛒 Your cart is empty!")
        return

    summary = "🛒 **YOUR CART**\n\n"
    total = 0

    for item_id, qty in cart.items():
        # Find item
        found = False
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                price = item["price"] * qty
                total += price
                summary += f"• {qty}x {item['name']}\n"
                summary += f"  {format_price(country_code, price)}\n\n"
                found = True
                break

    summary += f"{'='*40}\n"
    summary += f"💰 **SUBTOTAL: {format_price(country_code, total)}**\n"
    summary += f"{'='*40}\n"

    await send_text_message(sender, summary)

    # Action buttons
    buttons = [
        {"id": "cart_add_more", "title": "➕ Add More"},
        {"id": "cart_checkout", "title": "✅ Checkout"},
    ]

    await send_interactive_buttons(
        sender,
        header_text="CART OPTIONS",
        body_text="What next?",
        buttons=buttons
    )


async def ask_delivery_method_complete(sender):
    """Ask: Delivery / Pickup / Dine-in"""
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    msg = "✅ **How would you like to receive your order?**"
    await send_text_message(sender, msg)

    buttons = [
        {"id": "method_delivery", "title": "🏠 Delivery"},
        {"id": "method_pickup", "title": "🚗 Pickup"},
        {"id": "method_dinein", "title": "🍽️ Dine-in"},
    ]

    await send_interactive_buttons(
        sender,
        header_text="DELIVERY METHOD",
        body_text="Select one",
        buttons=buttons
    )


async def create_and_send_order(sender, country_code, session):
    """Create order, show summary, send to manager"""
    from whatsapp_interactive import send_text_message
    from menus_multi import get_menu, format_price
    from order_manager import MANAGER_NUMBER

    cart = session.get("cart", {})
    delivery_type = session.get("delivery_type", "home")
    address = session.get("address", "")
    table_number = session.get("table_number", "")
    menu = get_menu(country_code)

    if not cart:
        await send_text_message(sender, "❌ Cart is empty!")
        return False

    # Build complete summary
    summary = "📦 **ORDER SUMMARY**\n\n"
    total = 0
    items_list = []

    for item_id, qty in cart.items():
        found = False
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                price = item["price"] * qty
                total += price
                summary += f"• {qty}x {item['name']}\n"
                summary += f"  {format_price(country_code, price)}\n\n"
                items_list.append(item["name"])
                found = True
                break

    # Add delivery info
    delivery_charge = 0
    if delivery_type == "home":
        delivery_charge = 150 if country_code == "PK" else 5
        summary += f"📍 **Address**: {address}\n"
        summary += f"🚚 **Delivery**: {format_price(country_code, delivery_charge)}\n"
        total += delivery_charge
    elif delivery_type == "pickup":
        summary += "🚗 **Pickup Order** (Ready in 20 min)\n"
    else:  # dine_in
        summary += f"🍽️ **Table**: {table_number}\n"

    summary += f"\n{'='*40}\n"
    summary += f"💰 **TOTAL: {format_price(country_code, total)}**\n"
    summary += f"{'='*40}\n"

    # Send to customer
    await send_text_message(sender, summary)

    # Send to manager
    manager_msg = f"""
🔔 **NEW ORDER** #{sender[-8:]}

📋 Items:
{summary}

📞 Customer: {sender}
🚚 Type: {delivery_type.upper()}
{f"📍 Address: {address}" if delivery_type == "home" else f"🍽️ Table: {table_number}"}

⏱️ Ready in: 20-25 minutes
"""

    await send_text_message(MANAGER_NUMBER, manager_msg)

    # Confirm to customer
    confirm_msg = f"""
✅ **ORDER CONFIRMED!**

Order ID: #WILD{sender[-8:]}

{summary}

🍳 Preparing your order...
⏱️ Ready in: 20-25 minutes

Thank you! 🙏
"""

    await send_text_message(sender, confirm_msg)

    return True
