# Order management system - tracking, approvals, status updates
import time
from datetime import datetime
from whatsapp_interactive import send_interactive_buttons, send_text_message
from menus_multi import format_price

# Order storage
orders = {}  # {order_id: {customer, cart, menu, total, timestamp, status, manager_response, ...}}
customer_last_order = {}  # {customer_phone: {order_id, timestamp, items, location, ...}}

MANAGER_NUMBER = "923351021321"

PREP_TIME = 300  # 5 minutes in seconds
DELIVERY_TIME = 120  # 2 minutes in seconds
TOTAL_TIME = PREP_TIME + DELIVERY_TIME  # 7 minutes

def create_order(customer_phone, country_code, cart, menu, address, delivery_type, payment_type):
    """Create new order"""
    order_id = f"ORD_{int(time.time())}_{customer_phone[-4:]}"

    # Calculate totals
    subtotal = sum(
        menu["categories"][cat_key]["items"].get(item_id, {}).get("price", 0) * qty
        for item_id, qty in cart.items()
        for cat_key in menu["categories"].keys()
        if item_id in menu["categories"][cat_key].get("items", {})
    )

    def get_delivery_charge(country_code, total):
        """Calculate delivery charge"""
        delivery_settings = {
            "PK": {"free_above": 2000, "fee": 150},
            "AE": {"free_above": 75, "fee": 8},
            "SA": {"free_above": 80, "fee": 10},
            "QA": {"free_above": 100, "fee": 12},
            "KW": {"free_above": 10, "fee": 1},
            "BH": {"free_above": 12, "fee": 1.2},
            "OM": {"free_above": 9, "fee": 0.9},
            "US": {"free_above": 50, "fee": 4.99},
            "GB": {"free_above": 40, "fee": 3.99},
            "CA": {"free_above": 60, "fee": 5.99},
        }
        settings = delivery_settings.get(country_code, delivery_settings["PK"])
        if total >= settings["free_above"]:
            return 0
        return settings["fee"]

    delivery_fee = get_delivery_charge(country_code, subtotal) if delivery_type == "home" else 0
    total = subtotal + delivery_fee

    orders[order_id] = {
        "customer": customer_phone,
        "country": country_code,
        "cart": cart,
        "menu": menu,
        "address": address,
        "delivery_type": delivery_type,
        "payment_type": payment_type,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "timestamp": time.time(),
        "status": "pending_approval",  # pending_approval → approved → preparing → delivering → delivered
        "manager_response": None,
    }

    # Store as customer's last order
    customer_last_order[customer_phone] = {
        "order_id": order_id,
        "timestamp": time.time(),
        "country": country_code,
        "address": address,
    }

    return order_id, total

def get_order(order_id):
    """Get order by ID"""
    return orders.get(order_id)

def get_customer_last_order(customer_phone):
    """Get customer's last order info"""
    return customer_last_order.get(customer_phone)

def update_order_status(order_id, status):
    """Update order status"""
    if order_id in orders:
        orders[order_id]["status"] = status
        return True
    return False

async def handle_manager_approval(manager_phone, action, customer_phone):
    """Handle manager approve/reject"""
    if action == "approve":
        # Find latest order for this customer
        for order_id, order in orders.items():
            if order["customer"] == customer_phone and order["status"] == "pending_approval":
                order["status"] = "approved"
                order["manager_response"] = "approved"

                msg = f"""✅ ORDER APPROVED!

Your order is now being prepared.

⏱️ Prep Time: 5 minutes
🚚 Delivery: 2 minutes
📋 Total Time: 7 minutes

We'll notify you when it's ready!"""
                await send_text_message(customer_phone, msg)
                return

    elif action == "reject":
        for order_id, order in orders.items():
            if order["customer"] == customer_phone and order["status"] == "pending_approval":
                order["status"] = "rejected"
                order["manager_response"] = "rejected"

                manager_num = "+92" + "335" + "1021321"  # Format manager number
                msg = f"""❌ ORDER REJECTED

Please contact restaurant:
📞 {manager_num}

Our team will assist you!"""
                await send_text_message(customer_phone, msg)
                return

def get_time_elapsed(order_id):
    """Get seconds elapsed since order creation"""
    if order_id not in orders:
        return 0
    return int(time.time() - orders[order_id]["timestamp"])

def get_order_status_message(order_id):
    """Get status message based on elapsed time"""
    elapsed = get_time_elapsed(order_id)
    order = orders[order_id]

    if order["status"] != "approved":
        return None

    if elapsed < PREP_TIME:  # Before 5 min
        remaining = PREP_TIME - elapsed
        return f"🍳 Your order is being prepared\n⏱️ Time passed: {elapsed // 60} min {elapsed % 60} sec\n✨ Still {remaining // 60}+ min remaining"

    elif elapsed < TOTAL_TIME:  # 5-7 min, ready to deliver
        delivery_remaining = TOTAL_TIME - elapsed
        return f"📦 Order ready! Out for delivery\n🚚 Will arrive in ~{delivery_remaining // 60}+ min"

    else:  # After 7 min
        return f"⏰ Order should have arrived by now. If you have any issue, please contact us!"

async def get_manager_status_options(order_id, manager_phone):
    """Send manager order status update options"""
    order = orders.get(order_id)
    if not order:
        return

    msg = f"""📋 ORDER STATUS UPDATE

Customer: {order["customer"]}
Order ID: {order_id}

Current Status: {order["status"]}"""

    await send_text_message(manager_phone, msg)

    buttons = [
        {"id": f"status_prep_{order_id}", "title": "🍳 Preparing"},
        {"id": f"status_deliv10_{order_id}", "title": "🚚 10 min away"},
        {"id": f"status_deliv20_{order_id}", "title": "🚚 20 min away"},
        {"id": f"status_delivered_{order_id}", "title": "✅ Delivered"}
    ]

    await send_interactive_buttons(
        manager_phone,
        header_text="MANAGER: Update Order Status",
        body_text="Select current status",
        buttons=buttons
    )

def get_order_by_customer_time(customer_phone):
    """Get customer's recent orders within last 30 minutes"""
    recent = []
    for order_id, order in orders.items():
        if order["customer"] == customer_phone:
            elapsed = int(time.time() - order["timestamp"])
            if elapsed < 1800:  # 30 minutes
                recent.append((order_id, order, elapsed))
    return sorted(recent, key=lambda x: x[2])  # Sort by time
