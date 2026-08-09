import os
import json
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from config import VERIFY_TOKEN
from flow_smart import handle_smart_flow
from order_manager import handle_manager_approval

app = FastAPI()

# ==================== WEBHOOK SETUP ====================
@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook endpoint"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"✅ Webhook verified!")
        return PlainTextResponse(challenge)
    else:
        return PlainTextResponse("Forbidden", status_code=403)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming messages from WhatsApp"""
    try:
        data = await request.json()

        if data.get("object") != "whatsapp_business_account":
            return {"status": "ok"}

        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        for message in messages:
            sender = message.get("from")
            msg_type = message.get("type")

            print(f"\n📨 Message from {sender}")

            # Text messages
            if msg_type == "text":
                text = message.get("text", {}).get("body", "").strip()
                print(f"   Text: {text}")
                await handle_smart_flow(sender, text, is_interactive=False)

            # ORDER MESSAGE - Customer selected items from WhatsApp catalog
            elif msg_type == "order":
                print(f"   Order received from catalog!")
                order_data = message.get("order", {})

                # Extract selected items
                product_items = order_data.get("product_items", [])

                if product_items:
                    print(f"   Selected {len(product_items)} items from catalog")

                    # Import here to avoid circular imports
                    from db import customer_sessions
                    from menus_multi import get_country_from_phone
                    from whatsapp_interactive import send_text_message
                    from complete_order_flow import ask_delivery_method_complete, show_cart_summary

                    # Initialize or get session
                    if sender not in customer_sessions:
                        customer_sessions[sender] = {
                            "country_code": get_country_from_phone(sender),
                            "cart": {},
                            "stage": "delivery_method",
                        }

                    session = customer_sessions[sender]

                    # Populate cart from order items
                    cart_items_text = "🛒 **Order Items Received!**\n\n"

                    for item in product_items:
                        sku = item.get("product_retailer_id")  # This is the item_id
                        qty = item.get("quantity")

                        if sku and qty:
                            # Add to cart
                            session["cart"][sku] = session["cart"].get(sku, 0) + int(qty)
                            cart_items_text += f"• {qty}x {sku}\n"

                    customer_sessions[sender] = session

                    # Show cart summary
                    await show_cart_summary(sender, session["country_code"], session)

                    # Ask for delivery method
                    await ask_delivery_method_complete(sender)

            # Interactive messages (buttons/lists)
            elif msg_type == "interactive":
                interactive = message.get("interactive", {})
                button_reply = interactive.get("button_reply", {})
                list_reply = interactive.get("list_reply", {})

                if button_reply:
                    button_id = button_reply.get("id")
                    print(f"   Button: {button_id}")
                    if button_id:
                        # Handle manager actions
                        if button_id.startswith("approve_"):
                            customer = button_id.replace("approve_", "")
                            await handle_manager_approval(sender, "approve", customer)
                        elif button_id.startswith("reject_"):
                            customer = button_id.replace("reject_", "")
                            await handle_manager_approval(sender, "reject", customer)
                        elif button_id.startswith("status_"):
                            # Manager status update - pass to flow_smart
                            await handle_smart_flow(sender, button_id, is_interactive=True)
                        else:
                            # Regular customer flow
                            await handle_smart_flow(sender, button_id, is_interactive=True)

                elif list_reply:
                    item_id = list_reply.get("id")
                    print(f"   List Item: {item_id}")
                    if item_id:
                        await handle_smart_flow(sender, item_id, is_interactive=True)

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Error: {e}")
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}


# ==================== TABLE ORDERS ====================
@app.get("/table/{table_id}")
async def table_order(table_id: str):
    """Handle table QR code scan"""
    return {
        "status": "ok",
        "message": "Scan successful",
        "table_id": table_id,
        "info": "Send your WhatsApp number to start ordering from this table"
    }


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "wild-bites-restaurant-bot",
        "whatsapp_configured": bool(os.getenv("WHATSAPP_TOKEN"))
    }


# ==================== RUN ====================
if __name__ == "__main__":
    import sys
    # Fix encoding for Windows
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    port = int(os.getenv("PORT", "8000"))
    print(f"\n[STARTING] Wild Bites Restaurant Bot on port {port}...")
    print(f"[OK] Multi-country system ready")
    print(f"[OK] Button-based menu ready")
    print(f"[OK] Shortcode system active\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
