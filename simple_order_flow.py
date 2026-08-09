# Simple Complete Order Flow
# Hi → Menu → Select Items → Delivery/Pickup/Dine-in → Address/Table → Order Summary → Create Order

async def show_simple_menu(sender, country_code):
    """Show simple menu with categories - user can select"""
    from whatsapp_interactive import send_interactive_list
    from menus_multi import get_menu
    from country_selector import COUNTRIES

    menu = get_menu(country_code)
    country_info = COUNTRIES[country_code]

    rows = [
        {
            "id": f"cat_{key}",
            "title": data["name"],
            "description": f"{len(data['items'])} items • Browse & select"
        }
        for key, data in list(menu["categories"].items())
    ]

    sections = [{"title": "🍽️ SELECT CATEGORY", "rows": rows}]

    body_text = f"📍 {country_info['name']} | {country_info['currency']}"

    await send_interactive_list(
        sender,
        header_text="📦 BROWSE MENU",
        body_text=body_text,
        sections=sections
    )


async def show_category_items(sender, country_code, category_key, session):
    """Show items in category - user selects what they want"""
    from whatsapp_interactive import send_interactive_buttons
    from menus_multi import get_menu, format_price
    from flow_smart import get_item_emoji
    import asyncio

    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        from whatsapp_interactive import send_text_message
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]

    # Show each item with quantity buttons
    msg = f"📋 **{category['name'].upper()}**\n\nSelect items and quantities:\n"
    await send_text_message(sender, msg)

    # Show items
    for item_id, item in list(items.items())[:5]:  # Show first 5
        emoji = get_item_emoji(item["name"])
        price = format_price(country_code, item["price"])

        buttons = [
            {"id": f"add_{item_id}_1", "title": "1x"},
            {"id": f"add_{item_id}_2", "title": "2x"},
            {"id": f"add_{item_id}_3", "title": "3x"},
            {"id": f"add_{item_id}_skip", "title": "Skip"},
        ]

        await send_interactive_buttons(
            sender,
            header_text=f"{emoji} {item['name']}",
            body_text=f"{price} • {item['desc'][:40]}",
            buttons=buttons
        )
        await asyncio.sleep(0.3)

    # Done button
    done_buttons = [
        {"id": f"done_category_{category_key}", "title": "✅ Done with this"},
    ]

    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="Done selecting from this category?",
        buttons=done_buttons
    )


async def show_delivery_options(sender):
    """Ask customer: Delivery / Pickup / Dine-in?"""
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    msg = "✅ **Great!** How would you like to receive your order?"
    await send_text_message(sender, msg)

    buttons = [
        {"id": "delivery_home", "title": "🏠 Delivery"},
        {"id": "delivery_pickup", "title": "🚗 Pickup"},
        {"id": "delivery_dine_in", "title": "🍽️ Dine-in"}
    ]

    await send_interactive_buttons(
        sender,
        header_text="DELIVERY METHOD",
        body_text="Choose one:",
        buttons=buttons
    )


async def show_order_summary_and_create(sender, session, country_code):
    """Show complete order summary and create the order"""
    from whatsapp_interactive import send_text_message
    from menus_multi import get_menu, format_price
    from flow_smart import get_item_emoji, send_to_manager, MANAGER_NUMBER
    from order_manager import create_order

    menu = get_menu(country_code)
    cart = session.get("cart", {})
    delivery_type = session.get("delivery_type", "home")
    address = session.get("address", "")
    table_number = session.get("table_number", "")

    if not cart:
        await send_text_message(sender, "❌ No items in cart!")
        return

    # Build summary
    summary = "📦 **ORDER SUMMARY**\n\n"
    total = 0
    items_list = []

    for item_id, qty in cart.items():
        # Find item in all categories
        found = False
        for category in menu["categories"].values():
            if item_id in category["items"]:
                item = category["items"][item_id]
                price = item["price"] * qty
                total += price
                emoji = get_item_emoji(item["name"])

                summary += f"{emoji} {qty}x {item['name']}\n"
                summary += f"   {format_price(country_code, price)}\n\n"
                items_list.append(item["name"])
                found = True
                break

        if not found:
            print(f"⚠️ Item not found: {item_id}")

    # Add delivery details
    if delivery_type == "home":
        summary += f"📍 Address: {address}\n"
        delivery_charge = 150 if country_code == "PK" else 5
        summary += f"🚚 Delivery: {format_price(country_code, delivery_charge)}\n"
        total += delivery_charge
    elif delivery_type == "pickup":
        summary += "🚗 **Pickup Order**\n"
        summary += "Ready in 20 minutes\n"
    else:  # dine_in
        summary += f"🍽️ Table: {table_number}\n"

    summary += f"\n{'='*40}\n"
    summary += f"💰 **TOTAL: {format_price(country_code, total)}**\n"
    summary += f"{'='*40}\n"

    await send_text_message(sender, summary)

    # Create actual order in database
    try:
        order_data = {
            "customer": sender,
            "items": [(item_id, qty) for item_id, qty in cart.items()],
            "delivery_type": delivery_type,
            "address": address if delivery_type == "home" else table_number,
            "total": total,
            "country_code": country_code
        }

        # Send to manager with detailed info
        msg_to_manager = f"""
🔔 **NEW ORDER** #{sender[-10:]}

📋 Items:
{summary}

📞 Customer: {sender}
🚚 Type: {delivery_type.upper()}
{"📍 Address: " + address if delivery_type == "home" else "🍽️ Table: " + table_number}

⏱️ Ready in: 20-25 minutes
"""

        await send_text_message(MANAGER_NUMBER, msg_to_manager)

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

    except Exception as e:
        print(f"❌ Error creating order: {e}")
        await send_text_message(sender, "❌ Error creating order. Please try again!")
        return False
