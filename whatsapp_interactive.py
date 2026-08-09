# WhatsApp Interactive Messages - Lists & Buttons (v25.0 API)
import aiohttp
from config import WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID

GRAPH_API_URL = f"https://graph.facebook.com/v25.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

async def send_interactive_buttons(phone, header_text, body_text, buttons, footer_text=""):
    """
    Send interactive buttons
    buttons = [
        {"id": "btn1", "title": "Option 1"},
        {"id": "btn2", "title": "Option 2"}
    ]

    WhatsApp Limits:
    - Button title: max 20 characters
    - Header text: max 60 characters
    - Body text: max 1024 characters
    """
    # Enforce WhatsApp character limits
    safe_header = header_text[:60]
    safe_body = body_text[:1024]

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": safe_header
            },
            "body": {
                "text": safe_body
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": btn["id"],
                            "title": btn["title"][:20]  # Max 20 chars per WhatsApp
                        }
                    }
                    for btn in buttons[:3]  # Max 3 buttons
                ]
            }
        }
    }

    if footer_text:
        payload["interactive"]["footer"] = {"text": footer_text}

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPH_API_URL, json=payload, headers=headers) as resp:
                result = await resp.json()
                if resp.status == 200:
                    print(f"✅ Buttons sent to {phone}")
                    return True
                else:
                    print(f"❌ Error: {result}")
                    return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def send_interactive_list(phone, header_text, body_text, sections, footer_text=""):
    """
    Send interactive list with sections
    sections = [
        {
            "title": "BIRYANI",
            "rows": [
                {"id": "BR1", "title": "Chicken Biryani", "description": "Rs 650"},
                {"id": "BR2", "title": "Beef Biryani", "description": "Rs 750"}
            ]
        }
    ]

    WhatsApp Limits:
    - Row title: max 24 characters
    - Row description: max 72 characters
    - Section title: max 24 characters
    - Header text: max 60 characters
    - Body text: max 1024 characters
    """
    # Enforce WhatsApp character limits
    safe_header = header_text[:60]
    safe_body = body_text[:1024]

    # Trim section and row titles/descriptions
    safe_sections = []
    for section in sections:
        safe_section = {
            "title": section.get("title", "")[:24],  # Max 24 chars
            "rows": [
                {
                    "id": row["id"],
                    "title": row.get("title", "")[:24],  # Max 24 chars - CRITICAL FIX
                    "description": row.get("description", "")[:72]  # Max 72 chars
                }
                for row in section.get("rows", [])
            ]
        }
        safe_sections.append(safe_section)

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": safe_header
            },
            "body": {
                "text": safe_body
            },
            "action": {
                "button": "SELECT ITEM",
                "sections": safe_sections
            }
        }
    }

    if footer_text:
        payload["interactive"]["footer"] = {"text": footer_text}

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPH_API_URL, json=payload, headers=headers) as resp:
                result = await resp.json()
                if resp.status == 200:
                    print(f"✅ List sent to {phone}")
                    return True
                else:
                    print(f"❌ Error: {result}")
                    return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def send_image_with_caption(phone, image_url, caption):
    """Send image with caption"""
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "image",
        "image": {
            "link": image_url
        }
    }

    if caption:
        # Send caption as separate text message
        await send_text_message(phone, caption)

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPH_API_URL, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    print(f"✅ Image sent to {phone}")
                    return True
                else:
                    print(f"❌ Error sending image")
                    return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def send_text_message(phone, text):
    """Send simple text message"""
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPH_API_URL, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    return True
                return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
