# Simple Button-Based Catalog
# Customers just tap buttons - no text format, no confusion!

async def show_catalog_simple(sender, country_code, category_key, session):
    """
    Show catalog with quantity buttons for each item
    Customer taps [1x] [2x] [3x] etc to select quantity
    Then taps "ADD ALL TO CART"

    No text format, pure buttons!
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons, send_image_with_caption
    from flow_smart import GITHUB_IMAGES, get_item_emoji
    from menus_multi import get_menu, format_price

    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]

    # Initialize catalog selections in session
    if "catalog_selections" not in session:
        session["catalog_selections"] = {}

    # Send category image
    image_url = GITHUB_IMAGES.get(category_key, "")
    if image_url:
        await send_image_with_caption(sender, image_url, "")

    # Send catalog with instructions
    catalog_msg = f"""📋 {category['name'].upper()} - CATALOG

Tap [1x] [2x] [3x] to add items!

Items available:"""

    await send_text_message(sender, catalog_msg)

    # Show each item with quantity buttons
    for idx, (item_id, item) in enumerate(items.items(), 1):
        emoji = get_item_emoji(item["name"])
        price = format_price(country_code, item["price"])

        # Create buttons for this item
        buttons = [
            {"id": f"qty_catalog_{item_id}_1", "title": "1x"},
            {"id": f"qty_catalog_{item_id}_2", "title": "2x"},
            {"id": f"qty_catalog_{item_id}_3", "title": "3x"},
            {"id": f"qty_catalog_{item_id}_4", "title": "4x"},
            {"id": f"qty_catalog_{item_id}_5", "title": "5x"},
            {"id": f"qty_catalog_{item_id}_skip", "title": "Skip"},
        ]

        # Send item with buttons
        item_msg = f"{idx}. {emoji} {item['name']} - {price}"

        await send_interactive_buttons(
            sender,
            header_text=f"{item['name']}",
            body_text=f"{price} • {item['desc']}\n\nHow many?",
            buttons=buttons
        )

        await asyncio.sleep(0.5)  # Small delay between items

    # Final action buttons
    final_buttons = [
        {"id": f"catalog_add_all_{category_key}", "title": "✅ ADD ALL"},
        {"id": "cart_add_more", "title": "📱 MORE"},
        {"id": "cart_clear", "title": "🗑️ CLEAR"},
    ]

    final_msg = f"""
Done selecting?
✅ ADD ALL - Add all to cart
📱 MORE - Add from another category
🗑️ CLEAR - Start over"""

    await send_text_message(sender, final_msg)
    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="What next?",
        buttons=final_buttons
    )

async def handle_catalog_qty_selection(sender, item_id, qty, session, country_code):
    """
    Handle when customer selects quantity for an item
    Just update session, show updated selections
    """
    from whatsapp_interactive import send_text_message

    if "catalog_selections" not in session:
        session["catalog_selections"] = {}

    if qty == 0 or qty == "skip":
        # Remove from selections
        if item_id in session["catalog_selections"]:
            del session["catalog_selections"][item_id]
        msg = f"❌ Removed from cart"
    else:
        # Add to selections
        session["catalog_selections"][item_id] = int(qty)
        msg = f"✅ Selected {qty}x"

    await send_text_message(sender, msg)

async def add_catalog_to_cart(sender, category_key, session, country_code):
    """
    Add all catalog selections to cart at once
    """
    from whatsapp_interactive import send_text_message, send_interactive_buttons
    from flow_smart import get_item_emoji
    from menus_multi import get_menu, format_price

    if "catalog_selections" not in session or not session["catalog_selections"]:
        await send_text_message(sender, "❌ No items selected! Please select items first.")
        return

    menu = get_menu(country_code)
    selections = session["catalog_selections"]

    # Add all to cart
    total = 0
    confirm_msg = f"🛒 ADDED TO CART!\n\n"

    for item_id, qty in selections.items():
        # Find item
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                emoji = get_item_emoji(item["name"])
                subtotal = item["price"] * qty
                total += subtotal

                # Add to cart
                session["cart"][item_id] = qty

                confirm_msg += f"{emoji} {qty}x {item['name']}\n"
                confirm_msg += f"   {format_price(country_code, subtotal)}\n\n"
                break

    confirm_msg += f"{'='*40}\n"
    confirm_msg += f"💰 SUBTOTAL: {format_price(country_code, total)}\n"
    confirm_msg += f"{'='*40}"

    await send_text_message(sender, confirm_msg)

    # Clear catalog selections for next time
    session["catalog_selections"] = {}

    # Show next steps
    buttons = [
        {"id": "cart_add_more", "title": "➕ Add More"},
        {"id": "cart_checkout", "title": "✅ Checkout"},
        {"id": "cart_clear", "title": "🗑️ Clear"},
    ]

    await send_interactive_buttons(
        sender,
        header_text="NEXT STEP",
        body_text="What would you like to do?",
        buttons=buttons
    )
