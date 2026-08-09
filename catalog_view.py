# Catalog View - Multi-select items at once
# Customers can select multiple items from a category in one go

async def show_catalog(sender, country_code, category_key):
    """
    Show catalog view of all items in a category
    Customer can select multiple items with quantities
    Format: DL1:2, DL2:1, BR1:3 (item_id:quantity)
    """
    from whatsapp_interactive import send_text_message, send_image_with_caption
    from flow_smart import GITHUB_IMAGES, get_item_emoji
    from menus_multi import get_menu, format_price

    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        await send_text_message(sender, "❌ Category not found")
        return

    category = menu["categories"][category_key]
    items = category["items"]

    # Send category image
    image_url = GITHUB_IMAGES.get(category_key, "")
    if image_url:
        await send_image_with_caption(sender, image_url, "")

    # Build catalog list
    catalog_msg = f"""📋 {category['name'].upper()} - CATALOG

Select multiple items at once!

Format: item_id:quantity, item_id:quantity
Example: DL1:2, DL2:1, BR1:3

─────────────────────────────────
"""

    # Add all items with IDs and prices
    for item_id, item in items.items():
        emoji = get_item_emoji(item["name"])
        price = format_price(country_code, item["price"])
        desc = item["desc"][:30]
        catalog_msg += f"\n{emoji} {item_id:4} | {item['name'][:20]:20} | {price:8} | {desc}"

    catalog_msg += f"""
─────────────────────────────────

💡 How to order:
1. Find the item ID (left column)
2. Decide quantity
3. Type: DL1:2, DL2:3, KH1:1
4. Send! ✅

📝 Multiple items from different categories?
Send items from same category, then:
- Tap "Add More" to select from another category
- Or type: cat_karahi (to switch category)
"""

    await send_text_message(sender, catalog_msg)

    # Send help message
    help_msg = """
🎯 QUICK TIPS:
• Use commas to separate items
• Space after commas is optional
• Zero quantity (DL1:0) skips item
• Don't order from multiple categories at once

✨ Examples:
  DL1:2, DL2:1
  BR1:3, BR2:2, BR3:1
  KH1:5
  BD1:2, DR1:1, SD1:1

Ready? Send your items! 🛒
"""

    await send_text_message(sender, help_msg)

async def parse_catalog_input(sender, text_input, country_code, category_key):
    """
    Parse customer's catalog input
    Format: DL1:2, DL2:1, BR1:3

    Returns: dict with item_id as key, quantity as value
    Example: {"DL1": 2, "DL2": 1, "BR1": 3}
    """
    from menus_multi import get_menu

    menu = get_menu(country_code)

    if category_key not in menu["categories"]:
        return None

    category = menu["categories"][category_key]
    items = category["items"]

    # Parse input
    parsed_items = {}

    try:
        # Split by comma
        pairs = text_input.split(",")

        for pair in pairs:
            pair = pair.strip()

            if not pair:
                continue

            # Split by colon
            if ":" not in pair:
                return None  # Invalid format

            parts = pair.split(":")
            item_id = parts[0].strip().upper()
            qty_str = parts[1].strip()

            # Validate
            if item_id not in items:
                return None  # Item not found

            qty = int(qty_str)

            if qty < 0:
                return None  # Invalid quantity

            if qty == 0:
                continue  # Skip zero quantities

            parsed_items[item_id] = qty

        if not parsed_items:
            return None  # No valid items selected

        return parsed_items

    except:
        return None  # Parse error


async def add_catalog_items_to_cart(sender, parsed_items, session, country_code):
    """
    Add all parsed catalog items to cart at once
    Return success message with cart summary
    """
    from whatsapp_interactive import send_text_message
    from flow_smart import get_item_emoji
    from menus_multi import get_menu, format_price

    menu = get_menu(country_code)

    # Add all items to cart
    for item_id, qty in parsed_items.items():
        session["cart"][item_id] = qty

    # Build confirmation message
    confirm_msg = "🛒 ITEMS ADDED TO CART!\n\n"

    total = 0
    for item_id, qty in parsed_items.items():
        # Find item
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                emoji = get_item_emoji(item["name"])
                subtotal = item["price"] * qty
                total += subtotal
                confirm_msg += f"{emoji} {qty}x {item['name']}\n"
                confirm_msg += f"   {format_price(country_code, subtotal)}\n"
                break

    confirm_msg += f"\n{'='*40}\n"
    confirm_msg += f"💰 SUBTOTAL: {format_price(country_code, total)}\n"
    confirm_msg += f"{'='*40}\n\n"
    confirm_msg += "Options:\n"
    confirm_msg += "  ➕ Add More items\n"
    confirm_msg += "  ✅ Proceed to Checkout\n"
    confirm_msg += "  🗑️ Clear Cart\n"
    confirm_msg += "  📱 Change Category\n"

    await send_text_message(sender, confirm_msg)

    return True

# ==================== EXAMPLES ====================
"""
CATALOG FLOW:

1. Customer selects category
   Customer: "Deals" (cat_deals)

2. Bot shows CATALOG with all items
   Output:
   📋 DEALS - CATALOG

   DL1 | Chicken Biryani Deal | Rs 850 | Aromatic basmati
   DL2 | Beef Biryani Deal    | Rs 950 | Tender beef
   DL3 | Combo Deal           | Rs 1200| Biryani + Naan

   Format: item_id:quantity, item_id:quantity
   Example: DL1:2, DL2:1, BR1:3

3. Customer sends multiple items at once
   Customer: "DL1:2, DL2:1, BR1:3"

4. Bot parses and adds all to cart
   Bot: "🛒 ITEMS ADDED!
        ✅ 2x Chicken Biryani Deal
        ✅ 1x Beef Biryani Deal
        ✅ 3x Naan

        Subtotal: Rs 3200

        ➕ Add More  ✅ Checkout  🗑️ Clear"

5. Customer can continue
   - "Add More" → show another category catalog
   - "Checkout" → proceed to delivery/pickup/dine-in
   - "Clear" → empty cart and restart

ADVANTAGES:
✅ Customer selects multiple items at once
✅ No back-and-forth for each item
✅ Faster ordering process
✅ See all options before deciding
✅ Easy to add more from other categories
"""
