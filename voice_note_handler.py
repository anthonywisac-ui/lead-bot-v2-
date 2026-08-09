# ========================================
# WhatsApp Voice Note Handler with Gemini
# ========================================
# Process voice notes/audio messages using Gemini AI

import os
import requests
from google import genai
from google.genai import types
from whatsapp_interactive import send_text_message

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ========================================
# DOWNLOAD AUDIO FROM META SERVERS
# ========================================

def download_whatsapp_media(media_id: str) -> tuple[bytes, str]:
    """
    Download audio/voice note from WhatsApp Meta servers.

    Args:
        media_id: WhatsApp media ID (from message.audio.id)

    Returns:
        tuple: (audio_bytes, mime_type)
    """
    try:
        # Get Media URL
        url = f"https://graph.facebook.com/v25.0/{media_id}"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
        res = requests.get(url, headers=headers).json()

        if "error" in res:
            print(f"❌ Media fetch error: {res['error']}")
            return None, None

        media_url = res.get("url")
        mime_type = res.get("mime_type", "audio/ogg")

        print(f"📥 Downloading audio: {mime_type}")

        # Download raw media bytes
        media_res = requests.get(media_url, headers=headers)

        if media_res.status_code == 200:
            print(f"✅ Audio downloaded: {len(media_res.content)} bytes")
            return media_res.content, mime_type
        else:
            print(f"❌ Download failed: {media_res.status_code}")
            return None, None

    except Exception as e:
        print(f"❌ Media download error: {e}")
        return None, None


# ========================================
# PROCESS VOICE NOTE WITH GEMINI
# ========================================

async def process_voice_note(
    sender: str,
    media_id: str,
    country_code: str = "PK"
) -> str:
    """
    Process voice note with Gemini AI.

    Steps:
    1. Download audio from WhatsApp Meta servers
    2. Send to Gemini for transcription + understanding
    3. Generate smart response in Urdu/English
    4. Send back to customer

    Args:
        sender: Customer phone number
        media_id: WhatsApp media ID
        country_code: For localization

    Returns:
        Response text to send to customer
    """
    try:
        # Step 1: Download audio
        print(f"🎤 Processing voice note from {sender}")
        audio_bytes, mime_type = download_whatsapp_media(media_id)

        if not audio_bytes:
            return "❌ Could not process voice note. Please try again or send a text message."

        # Step 2: Send to Gemini
        print(f"🤖 Sending to Gemini (mime_type: {mime_type})")

        response = await _call_gemini_with_audio(audio_bytes, mime_type, country_code)

        if response:
            print(f"✅ Got response from Gemini: {response[:100]}...")
            return response
        else:
            return "❌ Could not understand the voice note. Please try again."

    except Exception as e:
        print(f"❌ Voice note processing error: {e}")
        return "❌ Error processing voice note. Please try again or send text."


async def _call_gemini_with_audio(audio_bytes: bytes, mime_type: str, country_code: str) -> str:
    """
    Call Gemini API with audio content.

    Gemini will:
    1. Transcribe the audio
    2. Understand the intent
    3. Generate helpful response
    """
    try:
        import asyncio

        # Prepare the prompt
        system_prompt = f"""You are a helpful restaurant customer service AI.
A customer from {country_code} sent you a voice note.

Your task:
1. Understand what they're asking (menu question, order status, etc.)
2. Provide a SHORT, helpful response in Urdu/English
3. Keep it under 100 words
4. Be warm and professional

If it's order-related, answer helpfully. If menu-related, suggest items.
If something else, answer appropriately.

IMPORTANT: Respond in the language they used (Urdu or English)."""

        # Call Gemini (this is synchronous, wrap in thread)
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type  # e.g., "audio/ogg", "audio/mp3"
                ),
                system_prompt
            ]
        )

        return response.text.strip()

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return None


# ========================================
# WEBHOOK INTEGRATION
# ========================================

async def handle_voice_message(sender: str, message_data: dict) -> bool:
    """
    Handle incoming voice note message.

    Called from main.py webhook when msg_type == "audio"

    Args:
        sender: Customer phone number
        message_data: Full message data from webhook

    Returns:
        True if handled successfully
    """
    try:
        # Extract audio info
        audio_data = message_data.get("audio", {})
        media_id = audio_data.get("id")

        if not media_id:
            await send_text_message(sender, "❌ Could not get voice note. Please try again.")
            return False

        # Process voice note
        response = await process_voice_note(sender, media_id)

        # Send response
        await send_text_message(sender, response)

        return True

    except Exception as e:
        print(f"❌ Voice message handler error: {e}")
        await send_text_message(sender, "❌ Error processing voice. Please send text instead.")
        return False


# ========================================
# USAGE IN main.py
# ========================================

"""
Add this to your webhook handler in main.py:

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = msg.get("from")
        msg_type = msg.get("type")

        # VOICE NOTE HANDLING
        if msg_type == "audio":
            from voice_note_handler import handle_voice_message
            await handle_voice_message(from_number, msg)
            return {"status": "ok"}

        # ... rest of message handlers
"""
