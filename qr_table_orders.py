# QR Code Table Ordering System
# Customers scan QR code at table to order from specific restaurant

import qrcode
import uuid
from io import BytesIO
from datetime import datetime

# Table sessions: {table_id: {order_id, phone, items, timestamp}}
table_sessions = {}
qr_codes = {}  # {table_id: qr_image_path}

RESTAURANT_NAME = "Wild Bites Restaurant"
RESTAURANT_PHONE = "923351021321"

async def generate_table_qr(table_number, restaurant_code="WB"):
    """Generate QR code for table"""
    table_id = f"{restaurant_code}_TABLE_{table_number}"

    # Create QR code data
    qr_data = f"https://bot.wildbi.com/table/{table_id}"

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code
    qr_path = f"qr_codes/{table_id}.png"
    img.save(qr_path)

    qr_codes[table_id] = qr_path
    return table_id, qr_path

def get_table_qr(table_id):
    """Get QR code for existing table"""
    return qr_codes.get(table_id)

async def create_table_session(table_id, customer_phone):
    """Create new order session for table"""
    order_id = f"TBL_{table_id}_{uuid.uuid4().hex[:6].upper()}"

    table_sessions[table_id] = {
        "order_id": order_id,
        "customer_phone": customer_phone,
        "items": {},
        "timestamp": datetime.now().isoformat(),
        "status": "active"  # active, completed, cancelled
    }

    return order_id

def add_item_to_table_order(table_id, item_id, qty):
    """Add item to table order"""
    if table_id not in table_sessions:
        return False

    session = table_sessions[table_id]
    session["items"][item_id] = session["items"].get(item_id, 0) + qty
    return True

def get_table_order(table_id):
    """Get current table order"""
    return table_sessions.get(table_id)

def complete_table_order(table_id):
    """Mark table order as complete"""
    if table_id in table_sessions:
        table_sessions[table_id]["status"] = "completed"
        return True
    return False

async def send_table_order_to_manager(table_id, manager_number, menu):
    """Send completed table order to manager"""
    from whatsapp_interactive import send_text_message, send_interactive_buttons

    session = table_sessions.get(table_id)
    if not session:
        return False

    # Build order summary
    order_text = f"""📋 TABLE ORDER - {session['order_id']}

📍 {RESTAURANT_NAME}
🪑 Table: {table_id.split('_')[-1]}
📱 Customer: {session['customer_phone']}
⏰ Time: {session['timestamp']}

🛒 ITEMS:
"""

    total = 0
    for item_id, qty in session["items"].items():
        # Find item in menu
        for cat in menu["categories"].values():
            if item_id in cat["items"]:
                item = cat["items"][item_id]
                subtotal = item["price"] * qty
                total += subtotal
                from menus_multi import format_price
                price_fmt = format_price(menu["code"], subtotal)
                order_text += f"• {qty}x {item['name']} = {price_fmt}\n"
                break

    order_text += f"""
💰 TOTAL: {subtotal}

[✅ Ready] [❌ Cancel]
"""

    await send_text_message(manager_number, order_text)
    return True

# QR Code Scanner Endpoint would be added to main.py
# GET /table/<table_id> - Opens bot for that table
